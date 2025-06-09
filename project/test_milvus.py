import os
os.environ['CURL_CA_BUNDLE'] = ''
from milvus_rag_handler import MilvusRAGHandler
import logging

logging.basicConfig(level=logging.INFO)
handler = MilvusRAGHandler()
print("MilvusRAGHandler initialized successfully")