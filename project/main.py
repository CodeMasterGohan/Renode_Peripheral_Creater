#!/usr/bin/env python3
"""
Main application entry point for the Renode Peripheral Model Generator.

This module provides a comprehensive CLI interface for generating, validating,
and managing Renode peripheral models using RAG-based documentation retrieval
and LLM-powered code generation.
"""

import os
import sys
import json
import yaml
import argparse
import logging
import traceback
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
import shutil
import zipfile
import time

from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeRemainingColumn
from rich.table import Table
from rich.panel import Panel
from rich.syntax import Syntax
from rich.markdown import Markdown
from rich.tree import Tree
from rich import print as rprint
from dotenv import load_dotenv

# Import all components
from milvus_rag_handler import MilvusRAGHandler
from model_manager import ModelManager
from validation_engine import ValidationEngine
from generation_pipeline import GenerationPipeline
from todo_processor import TodoProcessor
from renode_templates import RenodeTemplates


class RenodeModelGenerator:
    """Main application class for Renode model generation."""
    
    def __init__(self, config_path: str = "config.yaml"):
        """Initialize the application with all components."""
        self.console = Console()
        self.config_path = config_path
        self.config = self._load_config()
        self.session_data = {}
        self.current_session_id = None
        
        # Initialize logging
        self._setup_logging()
        
        # Initialize components (lazy loading)
        self._milvus_handler = None
        self._model_manager = None
        self._validation_engine = None
        self._generation_pipeline = None
        self._todo_processor = None
        self._renode_templates = None
        
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        try:
            with open(self.config_path, 'r') as f:
                config = yaml.safe_load(f)
            
            # Load environment variables
            load_dotenv()
            
            # Override with environment variables if present
            if os.getenv('MILVUS_HOST'):
                config['milvus']['host'] = os.getenv('MILVUS_HOST')
            if os.getenv('MILVUS_PORT'):
                config['milvus']['port'] = int(os.getenv('MILVUS_PORT'))
            if os.getenv('OPENAI_API_KEY'):
                config['llm']['openai_api_key'] = os.getenv('OPENAI_API_KEY')
            if os.getenv('ANTHROPIC_API_KEY'):
                config['llm']['anthropic_api_key'] = os.getenv('ANTHROPIC_API_KEY')
                
            return config
            
        except Exception as e:
            self.console.print(f"[red]Error loading configuration: {e}[/red]")
            sys.exit(1)
            
    def _setup_logging(self):
        """Setup logging configuration."""
        print("Setting up logging...")  # Debug statement
        try:
            log_dir = Path(self.config.get('output', {}).get('log_directory', 'logs'))
            log_dir.mkdir(exist_ok=True)
            
            log_file = log_dir / f"renode_generator_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
            print(f"Log file: {log_file}")  # Debug statement
            
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                handlers=[
                    logging.FileHandler(log_file),
                    logging.StreamHandler(sys.stdout)
                ]
            )
            
            self.logger = logging.getLogger(__name__)
            print("Logging setup complete")  # Debug statement
        except Exception as e:
            print(f"Error setting up logging: {e}")  # Debug statement
            # Fallback to basic logging
            logging.basicConfig(level=logging.INFO, stream=sys.stdout)
            self.logger = logging.getLogger(__name__)
        
    @property
    def milvus_handler(self) -> MilvusRAGHandler:
        """Lazy load Milvus handler."""
        if self._milvus_handler is None:
            # Pass the config path to the handler instead of individual parameters
            self._milvus_handler = MilvusRAGHandler(self.config_path)
        return self._milvus_handler
        
    @property
    def model_manager(self) -> ModelManager:
        """Lazy load model manager."""
        if self._model_manager is None:
            self._model_manager = ModelManager(self.config_path)
        return self._model_manager
        
    @property
    def validation_engine(self) -> ValidationEngine:
        """Lazy load validation engine."""
        if self._validation_engine is None:
            self._validation_engine = ValidationEngine(self.config)
        return self._validation_engine
        
    @property
    def generation_pipeline(self) -> GenerationPipeline:
        """Lazy load generation pipeline."""
        if self._generation_pipeline is None:
            # Initialize with only config path
            self._generation_pipeline = GenerationPipeline(self.config_path)
            
            # Set required components from Application instance
            self._generation_pipeline.milvus_handler = self.milvus_handler
            self._generation_pipeline.model_manager = self.model_manager
            self._generation_pipeline.validation_engine = self.validation_engine
            
        return self._generation_pipeline
        
    @property
    def todo_processor(self) -> TodoProcessor:
        """Lazy load TODO processor."""
        if self._todo_processor is None:
            self._todo_processor = TodoProcessor(self.model_manager)
        return self._todo_processor
        
    @property
    def renode_templates(self) -> RenodeTemplates:
        """Lazy load Renode templates."""
        if self._renode_templates is None:
            self._renode_templates = RenodeTemplates()
        return self._renode_templates
        
    def run(self):
        """Main entry point for the application."""
        parser = self._create_parser()
        args = parser.parse_args()
        
        try:
            # Display welcome banner
            self._display_welcome()
            
            # Execute command
            if hasattr(args, 'func'):
                args.func(args)
            else:
                parser.print_help()
                
        except KeyboardInterrupt:
            self.console.print("\n[yellow]Operation cancelled by user.[/yellow]")
            sys.exit(0)
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}", exc_info=True)
            self.console.print(f"[red]Unexpected error: {e}[/red]")
            sys.exit(1)
            
    def _create_parser(self) -> argparse.ArgumentParser:
        """Create command-line argument parser."""
        parser = argparse.ArgumentParser(
            description="Renode Peripheral Model Generator",
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        
        subparsers = parser.add_subparsers(dest='command', help='Available commands')
        
        # Generate command
        generate_parser = subparsers.add_parser(
            'generate',
            help='Generate a Renode peripheral model from a query'
        )
        generate_parser.add_argument(
            'query',
            nargs='?',
            help='Natural language query describing the peripheral'
        )
        generate_parser.add_argument(
            '--interactive', '-i',
            action='store_true',
            help='Interactive mode with step-by-step confirmation'
        )
        generate_parser.add_argument(
            '--output', '-o',
            help='Output directory for generated files'
        )
        generate_parser.set_defaults(func=self.cmd_generate)
        
        # Validate command
        validate_parser = subparsers.add_parser(
            'validate',
            help='Validate an existing peripheral model'
        )
        validate_parser.add_argument(
            'file',
            help='Path to the C# file to validate'
        )
        validate_parser.add_argument(
            '--fix',
            action='store_true',
            help='Attempt to fix validation issues'
        )
        validate_parser.set_defaults(func=self.cmd_validate)
        
        # List models command
        list_models_parser = subparsers.add_parser(
            'list-models',
            help='List available LLM models'
        )
        list_models_parser.set_defaults(func=self.cmd_list_models)
        
        # Test connection command
        test_parser = subparsers.add_parser(
            'test-connection',
            help='Test Milvus and LLM connections'
        )
        test_parser.set_defaults(func=self.cmd_test_connection)
        
        # Export templates command
        export_parser = subparsers.add_parser(
            'export-templates',
            help='Export peripheral templates'
        )
        export_parser.add_argument(
            '--output', '-o',
            default='templates',
            help='Output directory for templates'
        )
        export_parser.set_defaults(func=self.cmd_export_templates)
        
        # Resume command
        resume_parser = subparsers.add_parser(
            'resume',
            help='Resume a previous generation session'
        )
        resume_parser.add_argument(
            'session_id',
            nargs='?',
            help='Session ID to resume (shows list if not provided)'
        )
        resume_parser.set_defaults(func=self.cmd_resume)
        
        # Configure command
        configure_parser = subparsers.add_parser(
            'configure',
            help='Interactive configuration setup'
        )
        configure_parser.set_defaults(func=self.cmd_configure)
        
        return parser
        
    def _display_welcome(self):
        """Display welcome banner."""
        banner = """
╔═══════════════════════════════════════════════════════════════╗
║           Renode Peripheral Model Generator v1.0              ║
║                                                               ║
║  Generate high-quality Renode peripheral models using         ║
║  RAG-based documentation retrieval and LLM code generation    ║
╚═══════════════════════════════════════════════════════════════╝
        """
        self.console.print(Panel(banner, style="bold blue"))
        
    def cmd_generate(self, args):
        """Generate a Renode peripheral model."""
        # Get query interactively if not provided
        if not args.query:
            self.console.print("[bold]Generate Renode Peripheral Model[/bold]\n")
            args.query = Prompt.ask(
                "Enter your query",
                default="Create a Renode model for the eDMA controller"
            )
            
        # Set output directory
        output_dir = args.output or self.config['output']['directory']
        output_path = Path(output_dir) / f"generation_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Create session
        self.current_session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.session_data = {
            'id': self.current_session_id,
            'query': args.query,
            'output_path': str(output_path),
            'interactive': args.interactive,
            'start_time': datetime.now().isoformat(),
            'status': 'in_progress'
        }
        
        # Save session data
        self._save_session()
        
        try:
            # Display query analysis
            self.console.print(f"\n[bold]Query:[/bold] {args.query}")
            self.console.print(f"[bold]Output:[/bold] {output_path}")
            
            if args.interactive:
                if not Confirm.ask("\nProceed with generation?"):
                    self.console.print("[yellow]Generation cancelled.[/yellow]")
                    return
                    
            # Execute generation pipeline
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TimeRemainingColumn(),
                console=self.console
            ) as progress:
                
                # Step 1: Retrieve documentation
                task = progress.add_task("Retrieving relevant documentation...", total=100)
                # Retrieve documentation using Milvus
                docs = self.milvus_handler.perform_similarity_search(
                    query=args.query,
                    peripheral_name=args.query.split()[-1],  # Extract peripheral name from query
                    top_k=5
                )
                progress.update(task, completed=100)
                
                # Step 2: Generate model
                task = progress.add_task("Generating peripheral model...", total=6)
                
                # Run the generation pipeline
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(
                    self.generation_pipeline.run_pipeline(
                        peripheral_name=args.query.split()[-1],
                        documentation_path="",
                        resume_from=None,
                        pipeline_id=self.current_session_id
                    )
                )
                
                progress.update(task, completed=6)
                
            # Save results
            self._save_generation_results(result, output_path)
            
            # Display summary
            self._display_generation_summary(result, output_path)
            
            # Update session status
            self.session_data['status'] = 'completed'
            self.session_data['end_time'] = datetime.now().isoformat()
            self._save_session()
            
        except Exception as e:
            self.logger.error(f"Generation failed: {e}", exc_info=True)
            self.console.print(f"[red]Generation failed: {e}[/red]")
            
            # Update session status
            self.session_data['status'] = 'failed'
            self.session_data['error'] = str(e)
            self._save_session()
            
            # Offer recovery options
            self._offer_recovery_options(e)
            
    def cmd_validate(self, args):
        """Validate a peripheral model."""
        file_path = Path(args.file)
        
        if not file_path.exists():
            self.console.print(f"[red]File not found: {file_path}[/red]")
            return
            
        self.console.print(f"\n[bold]Validating:[/bold] {file_path}")
        
        try:
            with open(file_path, 'r') as f:
                code = f.read()
                
            # Run validation
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=self.console
            ) as progress:
                task = progress.add_task("Running validation checks...", total=None)
                
                results = self.validation_engine.validate_peripheral_model(code)
                
                progress.update(task, completed=100)
                
            # Display results
            self._display_validation_results(results)
            
            # Offer to fix issues if requested
            if args.fix and not results['is_valid']:
                if Confirm.ask("\nAttempt to fix validation issues?"):
                    self._fix_validation_issues(file_path, code, results)
                    
        except Exception as e:
            self.logger.error(f"Validation failed: {e}", exc_info=True)
            self.console.print(f"[red]Validation failed: {e}[/red]")
            
    def cmd_list_models(self, args):
        """List available LLM models."""
        self.console.print("\n[bold]Available LLM Models[/bold]\n")
        
        try:
            models = self.model_manager.list_available_models()
            
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Provider", style="cyan")
            table.add_column("Model", style="green")
            table.add_column("Status", style="yellow")
            
            for provider, model_list in models.items():
                for model in model_list:
                    status = "✓ Available" if model.get('available', True) else "✗ Unavailable"
                    table.add_row(provider, model['name'], status)
                    
            self.console.print(table)
            
            # Show current model
            current = self.model_manager.get_current_model()
            self.console.print(f"\n[bold]Current model:[/bold] {current}")
            
        except Exception as e:
            self.logger.error(f"Failed to list models: {e}", exc_info=True)
            self.console.print(f"[red]Failed to list models: {e}[/red]")
            
    def cmd_test_connection(self, args):
        """Test connections to Milvus and LLM services."""
        self.console.print("\n[bold]Testing Connections[/bold]\n")
        
        # Test Milvus
        self.console.print("Testing Milvus connection...")
        try:
            # Handler initialization already connects to Milvus
            handler = self.milvus_handler
            try:
                self.logger.debug("Getting collection stats")
                stats = handler.get_collection_stats()
                self.console.print(f"[green]✓ Milvus connected[/green]")
                
                # Print document collection stats
                doc_stats = stats["document_collection"]
                self.console.print(f"  Document Collection: {doc_stats['name']}")
                self.console.print(f"  Documents: {doc_stats['num_entities']}")
                
                # Print example collection stats
                example_stats = stats["example_collection"]
                self.console.print(f"  Example Collection: {example_stats['name']}")
                self.console.print(f"  Examples: {example_stats['num_entities']}")
                
            except Exception as e:
                self.logger.error(f"Failed to get collection stats: {e}", exc_info=True)
                self.console.print(f"[red]✗ Failed to get collection stats: {e}[/red]")
        except Exception as e:
            self.logger.error(f"Milvus error: {e}", exc_info=True)
            self.console.print(f"[red]✗ Milvus error: {e}[/red]")
        
        # Test LLM
        self.console.print("\nTesting LLM connection...")
        try:
            # Use a simple method to test LLM connection
            models = self.model_manager.list_available_models()
            if models:
                self.console.print(f"[green]✓ LLM connected[/green]")
                self.console.print(f"  Models available: {len(models)}")
            else:
                self.console.print("[red]✗ LLM connection failed[/red]")
        except Exception as e:
            self.console.print(f"[red]✗ LLM error: {e}[/red]")
            
    def cmd_export_templates(self, args):
        """Export peripheral templates."""
        output_dir = Path(args.output)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        self.console.print(f"\n[bold]Exporting Templates to:[/bold] {output_dir}")
        
        try:
            templates = self.renode_templates.get_all_templates()
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                console=self.console
            ) as progress:
                task = progress.add_task("Exporting templates...", total=len(templates))
                
                for name, template in templates.items():
                    file_path = output_dir / f"{name}.cs"
                    with open(file_path, 'w') as f:
                        f.write(template['code'])
                    progress.update(task, advance=1)
                    
            # Create README
            readme_path = output_dir / "README.md"
            with open(readme_path, 'w') as f:
                f.write(self._generate_template_readme(templates))
                
            self.console.print(f"[green]✓ Exported {len(templates)} templates[/green]")
            
        except Exception as e:
            self.logger.error(f"Export failed: {e}", exc_info=True)
            self.console.print(f"[red]Export failed: {e}[/red]")
            
    def cmd_resume(self, args):
        """Resume a previous generation session."""
        sessions = self._list_sessions()
        
        if not sessions:
            self.console.print("[yellow]No previous sessions found.[/yellow]")
            return
            
        # Show session list if ID not provided
        if not args.session_id:
            self._display_session_list(sessions)
            session_id = Prompt.ask("Enter session ID to resume")
        else:
            session_id = args.session_id
            
        # Load session
        session = self._load_session(session_id)
        if not session:
            self.console.print(f"[red]Session not found: {session_id}[/red]")
            return
            
        self.console.print(f"\n[bold]Resuming session:[/bold] {session_id}")
        self.console.print(f"Query: {session['query']}")
        self.console.print(f"Status: {session['status']}")
        
        # Resume based on status
        if session['status'] == 'completed':
            self.console.print("[green]Session already completed.[/green]")
            self._display_session_results(session)
        elif session['status'] == 'failed':
            if Confirm.ask("\nRetry failed generation?"):
                # Retry with same query
                self.cmd_generate(argparse.Namespace(
                    query=session['query'],
                    interactive=session.get('interactive', False),
                    output=session.get('output_path')
                ))
        else:
            self.console.print("[yellow]Session resumption not implemented yet.[/yellow]")
            
    def cmd_configure(self, args):
        """Interactive configuration setup."""
        self.console.print("\n[bold]Configuration Setup[/bold]\n")
        
        # Load current config
        config = self.config.copy()
        
        # Milvus configuration
        self.console.print("[bold cyan]Milvus Configuration[/bold cyan]")
        config['milvus']['host'] = Prompt.ask(
            "Milvus host",
            default=config['milvus']['host']
        )
        config['milvus']['port'] = int(Prompt.ask(
            "Milvus port",
            default=str(config['milvus']['port'])
        ))
        
        # LLM configuration
        self.console.print("\n[bold cyan]LLM Configuration[/bold cyan]")
        
        provider = Prompt.ask(
            "Default LLM provider",
            choices=['openai', 'anthropic'],
            default=config['llm']['default_provider']
        )
        config['llm']['default_provider'] = provider
        
        if provider == 'openai':
            api_key = Prompt.ask(
                "OpenAI API key",
                password=True,
                default=config['llm'].get('openai_api_key', '')
            )
            if api_key:
                config['llm']['openai_api_key'] = api_key
        else:
            api_key = Prompt.ask(
                "Anthropic API key",
                password=True,
                default=config['llm'].get('anthropic_api_key', '')
            )
            if api_key:
                config['llm']['anthropic_api_key'] = api_key
                
        # Output configuration
        self.console.print("\n[bold cyan]Output Configuration[/bold cyan]")
        config['output']['base_directory'] = Prompt.ask(
            "Output directory",
            default=config['output']['base_directory']
        )
        
        # Save configuration
        if Confirm.ask("\nSave configuration?"):
            with open(self.config_path, 'w') as f:
                yaml.dump(config, f, default_flow_style=False)
            self.console.print("[green]✓ Configuration saved[/green]")
            
            # Update .env file
            self._update_env_file(config)
            
    def _retrieve_documentation(self, query: str) -> List[Dict[str, Any]]:
        """Retrieve relevant documentation for the query."""
        try:
            results = self.milvus_handler.search(query, limit=10)
            
            # Group by source
            docs_by_source = {}
            for result in results:
                source = result.get('source', 'unknown')
                if source not in docs_by_source:
                    docs_by_source[source] = []
                docs_by_source[source].append(result)
                
            self.console.print(f"\n[green]Retrieved {len(results)} relevant documents from {len(docs_by_source)} sources[/green]")
            
            return results
            
        except Exception as e:
            self.logger.error(f"Documentation retrieval failed: {e}")
            return []
            
    def _save_generation_results(self, result: Dict[str, Any], output_path: Path):
        """Save generation results to files."""
        # Save generated code
        code_file = output_path / f"{result['peripheral_name']}.cs"
        with open(code_file, 'w') as f:
            f.write(result['code'])
            
        # Save validation report
        validation_file = output_path / "validation_report.json"
        with open(validation_file, 'w') as f:
            json.dump(result['validation_results'], f, indent=2)
            
        # Generate README
        readme_file = output_path / "README.md"
        with open(readme_file, 'w') as f:
            f.write(self._generate_readme(result))
            
        # Save integration instructions
        integration_file = output_path / "integration_instructions.md"
        with open(integration_file, 'w') as f:
            f.write(self._generate_integration_instructions(result))
            
        # Create archive
        archive_path = output_path / f"{result['peripheral_name']}_package.zip"
        with zipfile.ZipFile(archive_path, 'w') as zf:
            for file in output_path.glob('*'):
                if file.suffix != '.zip':
                    zf.write(file, file.name)
                    
        self.logger.info(f"Results saved to {output_path}")
        
    def _display_generation_summary(self, result: Dict[str, Any], output_path: Path):
        """Display generation summary."""
        self.console.print("\n[bold green]Generation Complete![/bold green]\n")
        
        # Create summary tree
        tree = Tree("[bold]Generation Summary[/bold]")
        
        # Add peripheral info
        info = tree.add("[cyan]Peripheral Information[/cyan]")
        info.add(f"Name: {result['peripheral_name']}")
        info.add(f"Type: {result.get('peripheral_type', 'Unknown')}")
        info.add(f"Base Address: {result.get('base_address', 'Not specified')}")
        
        # Add validation results
        validation = tree.add("[yellow]Validation Results[/yellow]")
        val_results = result['validation_results']
        validation.add(f"Status: {'✓ Valid' if val_results['is_valid'] else '✗ Invalid'}")
        validation.add(f"Score: {val_results['overall_score']:.1f}/100")
        
        if val_results['errors']:
            errors = validation.add("[red]Errors[/red]")
            for error in val_results['errors'][:3]:
                errors.add(error['message'])
                
        # Add output files
        files = tree.add("[green]Output Files[/green]")
        for file in output_path.glob('*'):
            files.add(file.name)
            
        self.console.print(tree)
        
        # Show next steps
        self.console.print("\n[bold]Next Steps:[/bold]")
        self.console.print("1. Review the generated code in:", style="dim")
        self.console.print(f"   {output_path / f'{result['peripheral_name']}.cs'}")
        self.console.print("2. Check the validation report for any issues", style="dim")
        self.console.print("3. Follow the integration instructions to add to your Renode platform", style="dim")
        
    def _display_validation_results(self, results: Dict[str, Any]):
        """Display validation results in a formatted way."""
        # Overall status
        status = "[green]✓ VALID[/green]" if results['is_valid'] else "[red]✗ INVALID[/red]"
        self.console.print(f"\n[bold]Validation Status:[/bold] {status}")
        self.console.print(f"[bold]Overall Score:[/bold] {results['overall_score']:.1f}/100")
        
        # Create results table
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Check", style="cyan")
        table.add_column("Status", style="green")
        table.add_column("Score", style="yellow")
        table.add_column("Details")
        
        # Add check results
        for check_name, check_result in results['checks'].items():
            status = "✓" if check_result['passed'] else "✗"
            score = f"{check_result['score']:.0f}"
            details = check_result.get('message', '')
            table.add_row(check_name, status, score, details)
            
        self.console.print("\n", table)
        
        # Show errors if any
        if results['errors']:
            self.console.print("\n[bold red]Errors:[/bold red]")
            for i, error in enumerate(results['errors'], 1):
                self.console.print(f"{i}. {error['type']}: {error['message']}")
                if 'line' in error:
                    self.console.print(f"   Line {error['line']}: {error.get('context', '')}", style="dim")
                    
        # Show warnings if any
        if results['warnings']:
            self.console.print("\n[bold yellow]Warnings:[/bold yellow]")
            for i, warning in enumerate(results['warnings'], 1):
                self.console.print(f"{i}. {warning['type']}: {warning['message']}", style="yellow")
                
    def _fix_validation_issues(self, file_path: Path, code: str, results: Dict[str, Any]):
        """Attempt to fix validation issues."""
        self.console.print("\n[bold]Attempting to fix validation issues...[/bold]")
        
        try:
            # Process TODOs if present
            if any('TODO' in error.get('message', '') for error in results['errors']):
                self.console.print("Processing TODO items...")
                fixed_code = self.todo_processor.process_todos_in_code(code)
            else:
                fixed_code = code
                
            # Re-validate
            new_results = self.validation_engine.validate_peripheral_model(fixed_code)
            
            if new_results['is_valid']:
                # Save fixed code
                backup_path = file_path.with_suffix('.bak')
                shutil.copy(file_path, backup_path)
                
                with open(file_path, 'w') as f:
                    f.write(fixed_code)
                    
                self.console.print("[green]✓ Issues fixed and file updated[/green]")
                self.console.print(f"Original backed up to: {backup_path}")
                
                # Show new validation results
                self._display_validation_results(new_results)
            else:
                self.console.print("[yellow]Some issues could not be automatically fixed[/yellow]")
                self._display_validation_results(new_results)
                
        except Exception as e:
            self.logger.error(f"Failed to fix issues: {e}")
            self.console.print(f"[red]Failed to fix issues: {e}[/red]")
            
    def _offer_recovery_options(self, error: Exception):
        """Offer recovery options after a failure."""
        self.console.print("\n[bold yellow]Recovery Options:[/bold yellow]")
        
        error_type = type(error).__name__
        
        if "Milvus" in str(error) or "connection" in str(error).lower():
            self.console.print("1. Check Milvus connection settings")
            self.console.print("2. Ensure Milvus server is running")
            self.console.print("3. Run 'test-connection' command to diagnose")
            
        elif "API" in str(error) or "model" in str(error).lower():
            self.console.print("1. Check API key configuration")
            self.console.print("2. Verify model availability")
            self.console.print("3. Try switching to a different model provider")
            
        elif "validation" in str(error).lower():
            self.console.print("1. Review the generated code manually")
            self.console.print("2. Check validation report for specific issues")
            self.console.print("3. Try regenerating with different parameters")
            
        else:
            self.console.print("1. Check the log file for detailed error information")
            self.console.print("2. Ensure all dependencies are installed")
            self.console.print("3. Try running with --interactive flag for step-by-step execution")
            
        self.console.print("\n[dim]For more help, check the documentation or submit an issue.[/dim]")
        
    def _save_session(self):
        """Save current session data."""
        session_dir = Path(self.config.get('output', {}).get('session_directory', 'sessions'))
        session_dir.mkdir(exist_ok=True)
        
        session_file = session_dir / f"{self.current_session_id}.json"
        with open(session_file, 'w') as f:
            json.dump(self.session_data, f, indent=2)
            
    def _list_sessions(self) -> List[Dict[str, Any]]:
        """List all saved sessions."""
        session_dir = Path(self.config.get('output', {}).get('session_directory', 'sessions'))
        if not session_dir.exists():
            return []
            
        sessions = []
        for session_file in session_dir.glob('*.json'):
            try:
                with open(session_file, 'r') as f:
                    session = json.load(f)
                    sessions.append(session)
            except Exception:
                continue
                
        # Sort by start time
        sessions.sort(key=lambda x: x.get('start_time', ''), reverse=True)
        return sessions
        
    def _load_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Load a specific session."""
        session_dir = Path(self.config.get('output', {}).get('session_directory', 'sessions'))
        session_file = session_dir / f"{session_id}.json"
        
        if not session_file.exists():
            return None
            
        try:
            with open(session_file, 'r') as f:
                return json.load(f)
        except Exception:
            return None
            
    def _display_session_list(self, sessions: List[Dict[str, Any]]):
        """Display list of sessions."""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Session ID", style="cyan")
        table.add_column("Query", style="green")
        table.add_column("Status", style="yellow")
        table.add_column("Start Time")
        
        for session in sessions[:10]:  # Show last 10 sessions
            status_color = {
                'completed': 'green',
                'failed': 'red',
                'in_progress': 'yellow'
            }.get(session.get('status', 'unknown'), 'white')
            
            table.add_row(
                session['id'],
                session['query'][:50] + '...' if len(session['query']) > 50 else session['query'],
                f"[{status_color}]{session.get('status', 'unknown')}[/{status_color}]",
                session.get('start_time', 'N/A')
            )
            
        self.console.print("\n[bold]Previous Sessions[/bold]\n")
        self.console.print(table)
        
    def _display_session_results(self, session: Dict[str, Any]):
        """Display results from a completed session."""
        output_path = Path(session.get('output_path', ''))
        
        if not output_path.exists():
            self.console.print("[yellow]Output directory no longer exists.[/yellow]")
            return
            
        self.console.print(f"\n[bold]Session Output:[/bold] {output_path}")
        
        # List generated files
        files = list(output_path.glob('*'))
        if files:
            self.console.print("\n[bold]Generated Files:[/bold]")
            for file in files:
                self.console.print(f"  - {file.name}")
                
    def _generate_readme(self, result: Dict[str, Any]) -> str:
        """Generate README content for the peripheral."""
        return f"""# {result['peripheral_name']} - Renode Peripheral Model

## Overview

This is a generated Renode peripheral model for {result['peripheral_name']}.

**Type:** {result.get('peripheral_type', 'Unknown')}
**Base Address:** {result.get('base_address', 'Not specified')}
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Validation Results

- **Status:** {'✓ Valid' if result['validation_results']['is_valid'] else '✗ Invalid'}
- **Score:** {result['validation_results']['overall_score']:.1f}/100

## Files

- `{result['peripheral_name']}.cs` - Main peripheral implementation
- `validation_report.json` - Detailed validation results
- `integration_instructions.md` - How to integrate this peripheral

## Usage

```csharp
// Add to your platform file
{result['peripheral_name'].lower()}: {result['peripheral_name']} @ sysbus {result.get('base_address', '<address>')}
```

## Features

{self._extract_features(result.get('code', ''))}

## Notes

This model was automatically generated based on the query: "{result.get('query', 'N/A')}"

For more information, see the integration instructions.
"""

    def _generate_integration_instructions(self, result: Dict[str, Any]) -> str:
        """Generate integration instructions for the peripheral."""
        return f"""# Integration Instructions for {result['peripheral_name']}

## Prerequisites

- Renode version 1.13.0 or higher
- Platform file for your target system

## Integration Steps

### 1. Copy the Peripheral File

Copy `{result['peripheral_name']}.cs` to your Renode peripherals directory:

```bash
cp {result['peripheral_name']}.cs /path/to/renode/peripherals/
```

### 2. Add to Platform File

Add the following line to your platform file (.repl):

```
{result['peripheral_name'].lower()}: {result['peripheral_name']} @ sysbus {result.get('base_address', '<address>')}
```

### 3. Configure Interrupts (if applicable)

If the peripheral uses interrupts, connect them to your interrupt controller:

```
{result['peripheral_name'].lower()}:
    -> interrupt_controller@<irq_number>
```

### 4. Set Register Values (optional)

You can set initial register values:

```
{result['peripheral_name'].lower()}:
    RegisterName: 0x1234
```

## Testing

### Basic Test

```python
# In Renode monitor
mach create
machine LoadPlatformDescription @path/to/your/platform.repl
showAnalyzer sysbus.{result['peripheral_name'].lower()}
start
```

### Register Access Test

```python
# Read register
sysbus.{result['peripheral_name'].lower()} ReadDoubleWord 0x0

# Write register
sysbus.{result['peripheral_name'].lower()} WriteDoubleWord 0x0 0x1234
```

## Troubleshooting

### Common Issues

1. **Peripheral not found**
   - Ensure the .cs file is in the correct directory
   - Check the class name matches the platform file

2. **Address conflicts**
   - Verify the base address doesn't overlap with other peripherals
   - Check the size of the peripheral's address space

3. **Missing features**
   - Review the validation report for any warnings
   - Check if all required registers are implemented

## Customization

You can extend this peripheral by:

1. Adding more registers
2. Implementing additional functionality
3. Connecting to other peripherals
4. Adding custom commands

For more information, see the Renode documentation.
"""

    def _generate_template_readme(self, templates: Dict[str, Any]) -> str:
        """Generate README for exported templates."""
        return f"""# Renode Peripheral Templates

This directory contains {len(templates)} peripheral templates that can be used as starting points for creating new Renode peripherals.

## Available Templates

{chr(10).join(f"- **{name}** - {template.get('description', 'No description')})" for name, template in templates.items())}

## Usage

1. Choose a template that matches your peripheral type
2. Copy the template file and rename it
3. Modify the class name and namespace
4. Implement the specific functionality for your peripheral
5. Add appropriate registers and logic

## Template Structure

Each template includes:
- Basic peripheral structure
- Common register implementations
- Interrupt handling (where applicable)
- Logging setup
- Documentation comments

## Customization Tips

- Replace TODO comments with actual implementation
- Add peripheral-specific registers
- Implement proper reset behavior
- Add validation for register values
- Include appropriate logging

## Contributing

To add new templates, ensure they follow the established patterns and include comprehensive documentation.
"""

    def _extract_features(self, code: str) -> str:
        """Extract features from generated code."""
        features = []
        
        if 'IDoubleWordPeripheral' in code:
            features.append("- 32-bit register access")
        if 'IWordPeripheral' in code:
            features.append("- 16-bit register access")
        if 'IBytePeripheral' in code:
            features.append("- 8-bit register access")
        if 'GPIO' in code:
            features.append("- GPIO functionality")
        if 'Timer' in code:
            features.append("- Timer/counter functionality")
        if 'Interrupt' in code or 'IRQ' in code:
            features.append("- Interrupt generation")
        if 'DMA' in code:
            features.append("- DMA support")
        if 'FIFO' in code:
            features.append("- FIFO buffers")
            
        return '\n'.join(features) if features else "- Basic register access"
        
    def _update_env_file(self, config: Dict[str, Any]):
        """Update .env file with configuration."""
        env_path = Path('.env')
        
        env_content = []
        env_content.append(f"# Renode Peripheral Model Generator Configuration")
        env_content.append(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        env_content.append("")
        
        # Milvus settings
        env_content.append("# Milvus Settings")
        env_content.append(f"MILVUS_HOST={config['milvus']['host']}")
        env_content.append(f"MILVUS_PORT={config['milvus']['port']}")
        env_content.append("")
        
        # LLM settings
        env_content.append("# LLM Settings")
        if config['llm'].get('openai_api_key'):
            env_content.append(f"OPENAI_API_KEY={config['llm']['openai_api_key']}")
        if config['llm'].get('anthropic_api_key'):
            env_content.append(f"ANTHROPIC_API_KEY={config['llm']['anthropic_api_key']}")
            
        with open(env_path, 'w') as f:
            f.write('\n'.join(env_content))
            
        self.console.print("[green]✓ .env file updated[/green]")


def main():
    """Main entry point."""
    app = RenodeModelGenerator()
    app.run()


if __name__ == "__main__":
    main()