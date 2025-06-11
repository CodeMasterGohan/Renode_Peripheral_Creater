"""
Milvus Vector Database Interface and Smart Document Retrieval

This module handles all interactions with the Milvus vector database for
Retrieval-Augmented Generation (RAG). It provides intelligent document
retrieval capabilities, semantic search, and context management for
peripheral documentation and Renode examples.

Key features:
- Vector similarity search for relevant documentation sections
- Smart document selection with metadata filtering
- Complete document retrieval with all chunks
- Context validation for completeness
- Proper chunk ordering by section type
- Comprehensive error handling

Author: Renode Model Generator Team
Version: 2.0.0
"""

import json
import logging
import yaml
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple, Set
from collections import defaultdict
from enum import Enum

import numpy as np
from pymilvus import (
    connections,
    Collection,
    CollectionSchema,
    FieldSchema,
    DataType,
    utility,
    MilvusException
)
from sentence_transformers import SentenceTransformer


class SectionType(Enum):
    """Enumeration of document section types in priority order."""
    MEMORY_MAP = "memory_map"
    REGISTERS = "registers"
    FUNCTIONAL_DESCRIPTION = "functional_description"
    INTERRUPTS = "interrupts"
    TIMING = "timing"
    EXAMPLES = "examples"
    OTHER = "other"


class MilvusConnectionError(Exception):
    """Raised when connection to Milvus fails."""
    pass


class DocumentRetrievalError(Exception):
    """Raised when document retrieval fails."""
    pass


class ContextValidationError(Exception):
    """Raised when retrieved context fails validation."""
    pass


class MilvusRAGHandler:
    """Handles vector database operations for RAG-based document retrieval."""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize Milvus connection and collections.
        
        Args:
            config_path: Path to configuration file. If None, uses default config.yaml
            
        Raises:
            MilvusConnectionError: If connection to Milvus fails
        """
        self.logger = logging.getLogger(__name__)
        
        # Load configuration
        if config_path:
            with open(config_path, 'r') as f:
                full_config = yaml.safe_load(f)
        else:
            with open('config.yaml', 'r') as f:
                full_config = yaml.safe_load(f)
        
        self.config = full_config.get('milvus', {})
        self.knowledge_config = full_config.get('knowledge_base', {})
        
        # Initialize embedding model from config
        self.embedding_model_name = self.config["embedding_model"]
        self.logger.info(f"Using embedding model: {self.embedding_model_name}")
        
        # We'll load the model when needed
        self.embedding_model = None
        
        # Connect to Milvus
        self._connect()
        
        # Initialize collections using names from config
        collections_config = self.config.get("collections", {})
        doc_collection_name = collections_config.get("peripheral_docs", "peripheral_docs")
        example_collection_name = collections_config.get("renode_examples", "renode_examples")
        
        self.doc_collection = self._init_collection(doc_collection_name)
        self.example_collection = self._init_collection(example_collection_name)
        
        # Section type priorities for ordering
        self.section_priorities = {
            SectionType.MEMORY_MAP: 1,
            SectionType.REGISTERS: 2,
            SectionType.FUNCTIONAL_DESCRIPTION: 3,
            SectionType.INTERRUPTS: 4,
            SectionType.TIMING: 5,
            SectionType.EXAMPLES: 6,
            SectionType.OTHER: 7
        }
    
    def _connect(self) -> None:
        """
        Establish connection to Milvus server.
        
        Raises:
            MilvusConnectionError: If connection fails
        """
        try:
            connections.connect(
                alias="default",
                host=self.config["host"],
                port=self.config["port"],
                timeout=30
            )
            self.logger.info(f"Connected to Milvus at {self.config['host']}:{self.config['port']}")
        except Exception as e:
            self.logger.error(f"Failed to connect to Milvus: {e}")
            raise MilvusConnectionError(f"Failed to connect to Milvus: {e}")
    
    def _init_collection(self, collection_name: str) -> Collection:
        """
        Initialize or load a Milvus collection.
        
        Args:
            collection_name: Name of the collection
            
        Returns:
            Collection instance
            
        Raises:
            MilvusConnectionError: If collection initialization fails
        """
        try:
            self.logger.info(f"Initializing collection: {collection_name}")
            if utility.has_collection(collection_name):
                self.logger.info(f"Collection exists: {collection_name}")
                collection = Collection(collection_name)
                self.logger.info(f"Collection object created: {collection_name}")
                collection.load()
                self.logger.info(f"Loaded existing collection: {collection_name}")
            else:
                self.logger.info(f"Collection does not exist, creating: {collection_name}")
                collection = self._create_collection(collection_name)
                self.logger.info(f"Created new collection: {collection_name}")
            
            # Verify collection properties
            self.logger.info(f"Collection properties: {collection.describe()}")
            self.logger.info(f"Collection entities: {collection.num_entities}")
            
            return collection
        except Exception as e:
            import traceback
            error_trace = traceback.format_exc()
            self.logger.error(f"Failed to initialize collection {collection_name}: {error_trace}")
            raise MilvusConnectionError(f"Failed to initialize collection: {e}")
    
    def _create_collection(self, collection_name: str) -> Collection:
        """
        Create a new Milvus collection with appropriate schema.
        
        Args:
            collection_name: Name of the collection to create
            
        Returns:
            Created collection instance
        """
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name="content", dtype=DataType.VARCHAR, max_length=65535),
            FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=self.config["embedding_dim"]),
            FieldSchema(name="metadata", dtype=DataType.JSON),
            FieldSchema(name="timestamp", dtype=DataType.INT64)
        ]
        
        schema = CollectionSchema(
            fields=fields,
            description=f"Collection for {collection_name}"
        )
        
        collection = Collection(
            name=collection_name,
            schema=schema
        )
        
        # Create index for vector field
        # NOTE: The index type is set to FLAT. This provides a brute-force, exact search
        # that guarantees 100% recall. For the specialized and relatively small-to-medium sized
        # knowledge base of this project, the performance is sufficient, and the guarantee of
        # finding the absolute best match is prioritized over the speed of an Approximate
        # Nearest Neighbor (ANN) index. If the dataset scales into the millions of vectors,
        # consider switching to an ANN index like HNSW or IVF_FLAT for better performance.
        index_params = self.config.get("index_params", {
            "metric_type": "L2",
            "index_type": "FLAT",
            "params": {} # FLAT index has no build parameters
        })
        
        collection.create_index(
            field_name="embedding",
            index_params=index_params
        )
        
        collection.load()
        
        return collection
    
    def perform_similarity_search(
        self,
        query: str,
        peripheral_name: Optional[str] = None,
        section_type: Optional[str] = None,
        top_k: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Perform vector similarity search with metadata filtering.
        
        Args:
            query: Search query text
            peripheral_name: Optional peripheral name filter
            section_type: Optional section type filter
            top_k: Number of results to return
            
        Returns:
            List of documents with similarity scores
            
        Raises:
            DocumentRetrievalError: If search fails
        """
        self.logger.info(f"[PSS_ENTRY] Entered perform_similarity_search for query: {query}, peripheral: {peripheral_name}")
        try:
            # Build metadata filters
            filters = {}
            if peripheral_name:
                filters["peripheral_name"] = peripheral_name
            if section_type:
                filters["section_type"] = section_type
            self.logger.info(f"[PSS_PRE_SEARCH_DOCS] Filters built: {filters}. Attempting to call search_documents.")
            
            results = self.search_documents(
                query=query,
                top_k=top_k,
                filters=filters,
                collection_name="peripheral_docs"
            )
            
            self.logger.info(f"[PSS_POST_SEARCH_DOCS] search_documents returned. Found {len(results)} documents for query: {query}")
            return results
            
        except Exception as e:
            self.logger.error(f"[PSS_EXCEPTION] Similarity search failed: {e}", exc_info=True)
            raise DocumentRetrievalError(f"Similarity search failed: {e}")
    
    def retrieve_all_chunks(
        self,
        document_ids: List[str],
        peripheral_name: str
    ) -> List[Dict[str, Any]]:
        """
        Retrieve all chunks from identified documents.
        
        Args:
            document_ids: List of document IDs to retrieve
            peripheral_name: Peripheral name to filter by
            
        Returns:
            List of all chunks from the documents
            
        Raises:
            DocumentRetrievalError: If retrieval fails
        """
        try:
            # Build filter expression for peripheral name
            expr = f'metadata["peripheral_name"] == "{peripheral_name}"'
            
            # Query all chunks for the peripheral
            results = self.doc_collection.query(
                expr=expr,
                output_fields=["id", "content", "metadata"],
                limit=1000  # Adjust based on expected document size
            )
            
            # Convert to standard format
            chunks = []
            for result in results:
                chunks.append({
                    "id": result.get("id"),
                    "content": result.get("content"),
                    "metadata": result.get("metadata", {})
                })
            
            self.logger.info(f"Retrieved {len(chunks)} chunks for peripheral: {peripheral_name}")
            return chunks
            
        except Exception as e:
            self.logger.error(f"Failed to retrieve chunks: {e}")
            raise DocumentRetrievalError(f"Failed to retrieve chunks: {e}")
    
    def assemble_comprehensive_context(
        self,
        chunks: List[Dict[str, Any]],
        max_tokens: int = 8000
    ) -> Tuple[str, Dict[str, List[Dict[str, Any]]]]:
        """
        Assemble chunks into comprehensive context with proper ordering.
        
        Args:
            chunks: List of document chunks
            max_tokens: Maximum context size in tokens
            
        Returns:
            Tuple of (assembled context string, chunks organized by section)
        """
        # Organize chunks by section type
        sections = defaultdict(list)
        for chunk in chunks:
            section_type = chunk.get("metadata", {}).get("section_type", "other")
            sections[section_type].append(chunk)
        
        # Sort chunks within each section by position if available
        for section_type, section_chunks in sections.items():
            sections[section_type] = sorted(
                section_chunks,
                key=lambda x: x.get("metadata", {}).get("position", 0)
            )
        
        # Assemble context in priority order
        context_parts = []
        current_tokens = 0
        
        # Define section order
        section_order = [
            SectionType.MEMORY_MAP.value,
            SectionType.REGISTERS.value,
            SectionType.FUNCTIONAL_DESCRIPTION.value,
            SectionType.INTERRUPTS.value,
            SectionType.TIMING.value,
            SectionType.EXAMPLES.value,
            SectionType.OTHER.value
        ]
        
        for section_type in section_order:
            if section_type in sections:
                context_parts.append(f"\n=== {section_type.upper()} ===\n")
                
                for chunk in sections[section_type]:
                    # Estimate tokens (rough approximation)
                    chunk_tokens = len(chunk["content"]) // 4
                    
                    if current_tokens + chunk_tokens <= max_tokens:
                        context_parts.append(chunk["content"])
                        context_parts.append("\n")
                        current_tokens += chunk_tokens
                    else:
                        self.logger.warning(f"Reached token limit, truncating context at {current_tokens} tokens")
                        break
        
        assembled_context = "\n".join(context_parts)
        return assembled_context, dict(sections)
        
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics for the current collections."""
        stats = {}
        try:
            # Get stats for document collection
            stats["document_collection"] = {
                "name": self.doc_collection.name,
                "num_entities": self.doc_collection.num_entities,
                "indexes": [index.to_dict() for index in self.doc_collection.indexes],
                "schema": self.doc_collection.schema.to_dict()
            }
            
            # Get stats for example collection
            stats["example_collection"] = {
                "name": self.example_collection.name,
                "num_entities": self.example_collection.num_entities,
                "indexes": [index.to_dict() for index in self.example_collection.indexes],
                "schema": self.example_collection.schema.to_dict()
            }
        except Exception as e:
            self.logger.error(f"Failed to get collection stats: {e}")
            raise DocumentRetrievalError(f"Failed to get collection stats: {e}")
            
        return stats
    
    def validate_context(
        self,
        context: str,
        sections: Dict[str, List[Dict[str, Any]]]
    ) -> Tuple[bool, List[str]]:
        """
        Validate retrieved context for completeness with early termination.
        
        Args:
            context: Assembled context string
            sections: Chunks organized by section type
            
        Returns:
            Tuple of (is_valid, list of missing sections)
        """
        missing_sections = []
        
        # Early termination for empty context
        if not context.strip():
            self.logger.warning("Context validation failed: empty_context")
            return False, ["empty_context"]
        
        # Define essential sections
        essential_sections = [
            SectionType.MEMORY_MAP.value,
            SectionType.REGISTERS.value,
            SectionType.FUNCTIONAL_DESCRIPTION.value
        ]
        
        # Check for missing essential sections
        for section in essential_sections:
            if not sections.get(section):
                missing_sections.append(section)
        
        # Check content length if no essential sections missing
        if not missing_sections and len(context) < 500:
            missing_sections.append("insufficient_content")
        
        is_valid = not missing_sections
        
        if is_valid:
            self.logger.info("Context validation passed")
        else:
            self.logger.warning(f"Context validation failed. Missing: {missing_sections}")
        
        return is_valid, missing_sections
    
    def get_smart_context(
        self,
        query: str,
        peripheral_name: str,
        max_tokens: int = 8000,
        validate: bool = True
    ) -> Dict[str, Any]:
        """
        Main method for smart document retrieval with all requested features.
        
        Args:
            query: User query for similarity search
            peripheral_name: Name of the peripheral
            max_tokens: Maximum context size
            validate: Whether to validate the context
            
        Returns:
            Dictionary containing:
                - context: Assembled context string
                - sections: Organized chunks by section
                - is_valid: Validation result
                - missing_sections: List of missing sections
                - metadata: Additional metadata
                
        Raises:
            DocumentRetrievalError: If retrieval fails
            ContextValidationError: If validation fails and validate=True
        """
        try:
            # Pre-check: Verify collection has documents
            if self.doc_collection.num_entities == 0:
                self.logger.error(f"Document collection '{self.doc_collection.name}' is empty! Cannot retrieve documents.")
                raise DocumentRetrievalError("Document collection is empty. Please run the 'update-knowledge' command first to populate the vector database.")
            
            # Log start of retrieval with parameters
            self.logger.info(f"Starting smart context retrieval for peripheral: {peripheral_name}, query: '{query}'")
            start_time = datetime.now()
            
            # Step 1: Perform similarity search
            self.logger.info(f"[RETRIEVAL] Searching documents for peripheral: {peripheral_name}")
            search_start = datetime.now()
            search_results = self.perform_similarity_search(
                query=query,
                peripheral_name=peripheral_name,
                top_k=5
            )
            search_duration = (datetime.now() - search_start).total_seconds()
            self.logger.info(f"[RETRIEVAL] Found {len(search_results)} documents in {search_duration:.2f}s")
            
            if not search_results:
                # Fallback: Try without peripheral filter
                self.logger.warning("[RETRIEVAL] No results with peripheral filter, trying without")
                fallback_start = datetime.now()
                search_results = self.perform_similarity_search(
                    query=query,
                    top_k=10
                )
                fallback_duration = (datetime.now() - fallback_start).total_seconds()
                self.logger.info(f"[RETRIEVAL] Fallback search found {len(search_results)} documents in {fallback_duration:.2f}s")
            
            if not search_results:
                raise DocumentRetrievalError("No documents found for query")
            
            # Step 2: Extract unique document IDs
            doc_ids = list(set(doc["id"] for doc in search_results))
            
            # Step 3: Retrieve all chunks for the peripheral
            all_chunks = self.retrieve_all_chunks(doc_ids, peripheral_name)
            
            if not all_chunks:
                raise DocumentRetrievalError(f"No chunks found for peripheral: {peripheral_name}")
            
            # Step 4: Assemble comprehensive context
            context, sections = self.assemble_comprehensive_context(
                chunks=all_chunks,
                max_tokens=max_tokens
            )
            
            # Step 5: Validate context
            is_valid, missing_sections = self.validate_context(context, sections)
            
            if validate and not is_valid:
                raise ContextValidationError(
                    f"Context validation failed. Missing sections: {missing_sections}"
                )
            
            # Prepare result
            result = {
                "context": context,
                "sections": sections,
                "is_valid": is_valid,
                "missing_sections": missing_sections,
                "metadata": {
                    "peripheral_name": peripheral_name,
                    "total_chunks": len(all_chunks),
                    "context_length": len(context),
                    "estimated_tokens": len(context) // 4,
                    "retrieval_timestamp": datetime.now().isoformat()
                }
            }
            
            self.logger.info(
                f"Successfully retrieved context: {result['metadata']['total_chunks']} chunks, "
                f"{result['metadata']['estimated_tokens']} tokens"
            )
            
            return result
            
        except Exception as e:
            self.logger.error(f"Smart context retrieval failed: {e}")
            raise
    
    def search_documents(
        self,
        query: str,
        top_k: int = 10,
        filters: Optional[Dict[str, Any]] = None,
        collection_name: str = "peripheral_docs"
    ) -> List[Dict[str, Any]]:
        """
        Search for relevant documents using vector similarity.
        
        Args:
            query: Search query text
            top_k: Number of results to return
            filters: Optional metadata filters
            collection_name: Collection to search in
            
        Returns:
            List of relevant documents with scores
        """
        collection = self.doc_collection if collection_name == "peripheral_docs" else self.example_collection
        
        # Generate query embedding
        self.logger.debug(f"Generating embedding for query: {query}")
        query_embedding = self._generate_embeddings([query])[0]
        self.logger.debug(f"Embedding generated for query: {query}")
        
        # Build search parameters
        search_params = {
            "metric_type": "L2",
            "params": {} # FLAT index has no search parameters
        }
        
        # Build filter expression if provided
        expr = self._build_filter_expression(filters) if filters else None
        
        # Perform search
        self.logger.debug(f"Searching collection {collection.name} with expr: {expr}")
        results = collection.search(
            data=[query_embedding],
            anns_field="embedding",
            param=search_params,
            limit=top_k,
            expr=expr,
            output_fields=["content", "metadata"],
            timeout=self.config.get("milvus_search_timeout", 30.0) # Added timeout for Milvus search
        )
        self.logger.debug(f"Search completed on {collection.name}. Found {len(results[0]) if results else 0} hits.")
        
        # Format results
        documents = []
        for hits in results:
            for hit in hits:
                documents.append({
                    "id": hit.id,
                    "content": hit.entity.get("content"),
                    "metadata": hit.entity.get("metadata"),
                    "score": hit.distance
                })
        
        return documents
    
    def insert_documents(
        self,
        documents: List[Dict[str, Any]],
        collection_name: str = "peripheral_docs"
    ) -> List[int]:
        """
        Insert documents into Milvus collection.
        
        Args:
            documents: List of documents with content and metadata
            collection_name: Target collection name
            
        Returns:
            List of inserted document IDs
            
        Raises:
            MilvusException: If insertion fails
        """
        try:
            collection = self.doc_collection if collection_name == "peripheral_docs" else self.example_collection
            
            # Prepare data for insertion
            contents = [doc["content"] for doc in documents]
            embeddings = self._generate_embeddings(contents)
            metadata = [doc.get("metadata", {}) for doc in documents]
            timestamps = [int(datetime.now().timestamp()) for _ in documents]
            
            # Insert data - create proper entity structure
            entities = []
            # Check that all lists have the same length
            if not (len(contents) == len(embeddings) == len(metadata) == len(timestamps)):
                self.logger.error(f"List lengths do not match: contents={len(contents)}, embeddings={len(embeddings)}, metadata={len(metadata)}, timestamps={len(timestamps)}")
                raise MilvusException("List lengths do not match, cannot insert documents")
            
            # Use zip to safely iterate through the lists
            for content, embedding, meta, ts in zip(contents, embeddings, metadata, timestamps):
                entity = {
                    "content": content,
                    "embedding": embedding,
                    "metadata": meta,
                    "timestamp": ts
                }
                entities.append(entity)
            
            insert_result = collection.insert(entities)
            collection.flush()
            
            self.logger.info(f"Inserted {len(entities)} documents into {collection_name}")
            return insert_result.primary_keys
            
        except Exception as e:
            self.logger.error(f"Failed to insert documents: {e}")
            raise MilvusException(f"Failed to insert documents: {e}")
    
    def _generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts.
        
        Args:
            texts: List of text strings
            
        Returns:
            List of embedding vectors
        """
        self.logger.info(f"[_generate_embeddings_ENTRY] Called for {len(texts)} texts. Service: {self.embedding_service}")
        if self.embedding_service == "ollama":
            # Use Ollama embedding endpoint with batch processing
            try:
                import requests
                self.logger.info(f"[_generate_embeddings_OLLAMA_TRY] Attempting Ollama embedding with batch processing.")
                
                # Process texts one by one since Ollama only supports single-prompt embedding
                embeddings = []
                ollama_request_timeout = self.config.get("ollama_request_timeout", 10.0)
                
                for text in texts:
                    try:
                        payload = {
                            "model": self.config.get("ollama_model", self.ollama_model),
                            "prompt": text  # Send single text per request
                        }
                        self.logger.info(f"[_generate_embeddings_OLLAMA_REQUEST] Processing text: {text[:50]}...")
                        
                        response = requests.post(
                            f"{self.config.get('ollama_endpoint', self.ollama_endpoint)}/api/embeddings",
                            json=payload,
                            timeout=ollama_request_timeout
                        )
                        response.raise_for_status()
                        
                        embedding_data = response.json()
                        if "embedding" in embedding_data:
                            embeddings.append(embedding_data["embedding"])
                        else:
                            self.logger.error(f"[_generate_embeddings_OLLAMA_MISSING] Embedding missing in response for text: {text[:50]}...")
                            embeddings.append([])  # Append empty list to maintain index alignment
                    except Exception as e:
                        self.logger.error(f"[_generate_embeddings_OLLAMA_ERROR] Failed to get embedding for text: {text[:50]}... Error: {e}")
                        embeddings.append([])  # Append empty list to maintain index alignment
                
                self.logger.info(f"[_generate_embeddings_OLLAMA_SUCCESS] Generated {len(embeddings)} embeddings")
                return embeddings
            except requests.exceptions.Timeout:
                self.logger.error(f"[_generate_embeddings_OLLAMA_TIMEOUT] Ollama batch request timed out after {ollama_request_timeout} seconds.", exc_info=True)
                raise
            except Exception as e:
                self.logger.error(f"[_generate_embeddings_OLLAMA_EXCEPTION] Ollama batch embedding failed: {e}", exc_info=True)
                raise
        else:
            self.logger.info(f"[_generate_embeddings_SENTENCE_TRANSFORMERS] Using SentenceTransformers.")
            embeddings = self.embedding_model.encode(texts)
            self.logger.info(f"[_generate_embeddings_SENTENCE_TRANSFORMERS_SUCCESS] SentenceTransformers embeddings generated.")
            return embeddings.tolist()
    
    def _build_filter_expression(self, filters: Dict[str, Any]) -> str:
        """
        Build Milvus filter expression from dictionary.
        
        Args:
            filters: Dictionary of field-value pairs
            
        Returns:
            Filter expression string
        """
        expressions = []
        for field, value in filters.items():
            if isinstance(value, str):
                expressions.append(f'metadata["{field}"] == "{value}"')
            elif isinstance(value, (int, float)):
                expressions.append(f'metadata["{field}"] == {value}')
            elif isinstance(value, list):
                values_str = ", ".join([f'"{v}"' if isinstance(v, str) else str(v) for v in value])
                expressions.append(f'metadata["{field}"] in [{values_str}]')
        
        return " and ".join(expressions)
    
    def update_knowledge_base(self, knowledge_dir: str) -> Dict[str, int]:
        """
        Update knowledge base from directory of documents.
        
        Args:
            knowledge_dir: Directory containing knowledge documents
            
        Returns:
            Statistics about updated documents
        """
        knowledge_path = Path(knowledge_dir)
        stats = {"processed": 0, "inserted": 0, "errors": 0, "code_examples": 0, "docs": 0}
        
        # Get chunking parameters from config
        chunk_size = self.knowledge_config.get("indexing", {}).get("chunk_size", 1000)
        chunk_overlap = self.knowledge_config.get("indexing", {}).get("chunk_overlap", 200)
        
        # Use ThreadPoolExecutor for parallel file processing
        from concurrent.futures import ThreadPoolExecutor
        import threading
        
        # Thread-safe data structures
        stats_lock = threading.Lock()
        documents_lock = threading.Lock()
        all_documents = {"peripheral_docs": [], "renode_examples": []}
        
        def process_file(file_path):
            nonlocal stats
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                file_documents = []
                collection_name = "peripheral_docs"
                file_stats = {"code_examples": 0, "docs": 0, "inserted": 0}
                
                if file_path.suffix.lower() == ".cs":
                    # Process C# code examples as single documents
                    metadata = {
                        "source": str(file_path),
                        "filename": file_path.name,
                        "title": file_path.stem,
                        "type": "code_example"
                    }
                    
                    file_documents.append({
                        "content": content,
                        "metadata": metadata
                    })
                    collection_name = "renode_examples"
                    file_stats["code_examples"] = 1
                    
                else:  # .md files
                    # Extract metadata from file
                    peripheral_name = self._extract_peripheral_name(file_path)
                    section_type = self._extract_section_type(content)
                    
                    # Chunk the document
                    chunks = self._chunk_document(content, chunk_size, chunk_overlap)
                    
                    for i, chunk in enumerate(chunks):
                        metadata = {
                            "source": str(file_path),
                            "filename": file_path.name,
                            "peripheral_name": peripheral_name,
                            "section_type": section_type,
                            "position": i,
                            "total_chunks": len(chunks)
                        }
                        
                        file_documents.append({
                            "content": chunk,
                            "metadata": metadata
                        })
                    file_stats["docs"] = 1
                
                # Add to global documents list
                with documents_lock:
                    if collection_name == "peripheral_docs":
                        all_documents["peripheral_docs"].extend(file_documents)
                    else:
                        all_documents["renode_examples"].extend(file_documents)
                
                # Update statistics
                file_stats["inserted"] = len(file_documents)
                return file_stats
                
            except Exception as e:
                self.logger.error(f"Error processing {file_path}: {e}")
                return {"errors": 1}
        
        # Process files in parallel
        file_paths = [fp for fp in knowledge_path.rglob("*.*")
                     if fp.suffix.lower() in [".md", ".cs"]]
        
        with ThreadPoolExecutor(max_workers=4) as executor:
            future_to_path = {executor.submit(process_file, fp): fp for fp in file_paths}
            for future in future_to_path:
                file_stats = future.result()
                with stats_lock:
                    for key in ["code_examples", "docs", "inserted", "errors"]:
                        if key in file_stats:
                            stats[key] += file_stats[key]
                    stats["processed"] += 1 if "errors" not in file_stats else 0
        
        # Bulk insert documents after parallel processing
        for collection_name, docs in all_documents.items():
            if docs:
                # Insert in chunks to avoid large batches
                chunk_size = 100  # Milvus recommended batch size
                for i in range(0, len(docs), chunk_size):
                    batch = docs[i:i+chunk_size]
                    self.insert_documents(batch, collection_name=collection_name)
        
        return stats
    
    def _chunk_document(self, content: str, chunk_size: int, overlap: int) -> List[str]:
        """
        Split document into overlapping chunks.
        
        Args:
            content: Document content
            chunk_size: Size of each chunk
            overlap: Overlap between chunks
            
        Returns:
            List of text chunks
        """
        chunks = []
        start = 0
        
        while start < len(content):
            end = start + chunk_size
            chunk = content[start:end]
            
            # Try to break at sentence boundary
            if end < len(content):
                last_period = chunk.rfind('.')
                if last_period > chunk_size * 0.8:  # If period is in last 20%
                    chunk = chunk[:last_period + 1]
                    end = start + last_period + 1
            
            chunks.append(chunk.strip())
            start = end - overlap
        
        return chunks
    
    from functools import lru_cache

    @lru_cache(maxsize=100)
    def _extract_peripheral_name(self, file_path: Path) -> str:
        """
        Extract peripheral name from file path or name.
        Uses LRU caching to avoid repeated processing of same filenames.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Extracted peripheral name
        """
        # Convert to string for caching since Path objects aren't hashable
        filename = file_path.stem.lower()
        
        # Remove common prefixes/suffixes
        for prefix in ["chapter", "chatper", "section"]:
            if filename.startswith(prefix):
                filename = filename[len(prefix):].strip("-_ ")
        
        # Extract peripheral type from content
        parts = filename.split("-")
        if len(parts) > 1:
            return parts[-1].strip()
        
        return filename
    
    def _extract_section_type(self, content: str) -> str:
        """
        Extract section type from document content.
        
        Args:
            content: Document content
            
        Returns:
            Detected section type
        """
        content_lower = content.lower()
        
        # Check for section indicators
        if "memory map" in content_lower or "register map" in content_lower:
            return SectionType.MEMORY_MAP.value
        elif "register" in content_lower and "description" in content_lower:
            return SectionType.REGISTERS.value
        elif "functional description" in content_lower or "operation" in content_lower:
            return SectionType.FUNCTIONAL_DESCRIPTION.value
        elif "interrupt" in content_lower:
            return SectionType.INTERRUPTS.value
        elif "timing" in content_lower or "clock" in content_lower:
            return SectionType.TIMING.value
        elif "example" in content_lower or "code" in content_lower:
            return SectionType.EXAMPLES.value
        else:
            return SectionType.OTHER.value
    
    def close(self) -> None:
        """Close Milvus connection."""
        try:
            connections.disconnect("default")
            self.logger.info("Disconnected from Milvus")
        except Exception as e:
            self.logger.error(f"Error closing Milvus connection: {e}")