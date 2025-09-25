"""
Main RAG orchestrator for the Agentic RAG system.
"""
from typing import List, Dict, Any, Optional
from core.config.base_config import ConfigManager, RAGConfig
from core.factories.parser_factory import ParserFactory
from core.factories.chunker_factory import ChunkerFactory
from core.factories.vector_store_factory import VectorStoreFactory
from core.factories.agent_factory import AgentFactory
from core.interfaces.parser_interface import ParserInterface
from core.interfaces.chunker_interface import ChunkerInterface
from core.interfaces.vector_store_interface import VectorStoreInterface
from core.interfaces.agent_interface import AgentInterface
from llama_index.core.schema import Document, BaseNode, NodeWithScore


class RAGOrchestrator:
    """Main orchestrator for the RAG system."""
    
    def __init__(self, config_path: str = "config.json"):
        """
        Initialize RAG orchestrator.
        
        Args:
            config_path: Path to configuration file
        """
        self.config_manager = ConfigManager(config_path)
        self.config: Optional[RAGConfig] = None
        
        self.parser: Optional[ParserInterface] = None
        self.chunker: Optional[ChunkerInterface] = None
        self.vector_store: Optional[VectorStoreInterface] = None
        self.manager_agent: Optional[AgentInterface] = None
        self.assistant_agent: Optional[AgentInterface] = None
        
        self._initialize_components()
    
    def _initialize_components(self) -> None:
        """Initialize all components from configuration."""
        try:
            self.config = self.config_manager.load_config()
            
            self.parser = ParserFactory.create_from_config(self.config.parsers)
            
            self.chunker = ChunkerFactory.create_from_config(self.config.chunkers)
            
            self.vector_store = VectorStoreFactory.create_from_config(self.config.vector_stores)
            
            self.manager_agent = AgentFactory.create_from_config(self.config.agents, "manager")
            self.assistant_agent = AgentFactory.create_from_config(self.config.agents, "assistant")
            
            self._register_agent_tools()
            
        except Exception as e:
            raise RuntimeError(f"Failed to initialize RAG orchestrator: {str(e)}")
    
    def _register_agent_tools(self) -> None:
        """Register tools for agents."""
        if self.manager_agent and self.vector_store:
            if hasattr(self.manager_agent, 'register_context_tool'):
                self.manager_agent.register_context_tool(self.vector_store)
            if hasattr(self.manager_agent, 'register_assistant_agents'):
                self.manager_agent.register_assistant_agents(self.assistant_agent)
      
        if self.assistant_agent and self.vector_store:
            if hasattr(self.assistant_agent, 'register_context_tool'):
                self.assistant_agent.register_context_tool(self.vector_store)
      
    def process_document(self, file_path: {str, str}) -> List[str]:
        """
        Process a document through the entire pipeline.
        
        Args:
            file_path: Path to the document to process and name of the document
            
        Returns:
            List of node IDs that were added to the vector store
        """
        if not self.parser or not self.chunker or not self.vector_store:
            raise RuntimeError("Components not initialized")
        
        try:
            documents = self.parser.parse(file_path)
            
            nodes = self.chunker.chunk(documents)
            
            node_ids = self.vector_store.add(nodes)
            
            return node_ids
            
        except Exception as e:
            raise RuntimeError(f"Failed to process document {file_path}: {str(e)}")
    
    def query(self, question: str, use_manager: bool = True) -> str:
        """
        Process a user query.
        
        Args:
            question: User question
            use_manager: Whether to use manager agent (True) or assistant agent (False)
            
        Returns:
            Agent response
        """
        if not self.vector_store:
            raise RuntimeError("Vector store not initialized")
        
        try:
            # context = self.vector_store.search(question, top_k=5)
            
            agent = self.manager_agent if use_manager else self.assistant_agent
            
            if not agent:
                raise RuntimeError("Agent not initialized")
            
            response = agent.process_query(question)
            
            return response
            
        except Exception as e:
            raise RuntimeError(f"Failed to process query: {str(e)}")
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get system information."""
        return {
            "config": {
                "system": {
                    "name": self.config.system.name,
                    "version": self.config.system.version,
                    "debug": self.config.system.debug
                },
                "components": {
                    "parser": self.config.parsers.default,
                    "chunker": self.config.chunkers.default,
                    "vector_store": self.config.vector_stores.default
                }
            },
            "components": {
                "parser": self.parser.get_parser_name() if self.parser else None,
                "chunker": self.chunker.get_chunking_strategy() if self.chunker else None,
                "vector_store": self.vector_store.get_store_name() if self.vector_store else None,
                "manager_agent": self.manager_agent.get_agent_name() if self.manager_agent else None,
                "assistant_agent": self.assistant_agent.get_agent_name() if self.assistant_agent else None
            }
        }
    
    def reload_config(self) -> None:
        """Reload configuration and reinitialize components."""
        self.config_manager.load_config()
        self._initialize_components()
    
    def switch_parser(self, parser_name: str) -> None:
        """Switch to a different parser."""
        if parser_name not in self.config.parsers.available:
            raise ValueError(f"Parser '{parser_name}' not found in configuration")
        
        self.parser = ParserFactory.create_from_config(
            self.config.parsers, 
            parser_name
        )
    
    def switch_chunker(self, chunker_name: str) -> None:
        """Switch to a different chunker."""
        if chunker_name not in self.config.chunkers.available:
            raise ValueError(f"Chunker '{chunker_name}' not found in configuration")
        
        self.chunker = ChunkerFactory.create_from_config(
            self.config.chunkers, 
            chunker_name
        )
    
    def switch_vector_store(self, vector_store_name: str) -> None:
        """Switch to a different vector store."""
        if vector_store_name not in self.config.vector_stores.available:
            raise ValueError(f"Vector store '{vector_store_name}' not found in configuration")
        
        self.vector_store = VectorStoreFactory.create_from_config(
            self.config.vector_stores, 
            vector_store_name
        )
        
        self._register_agent_tools()
