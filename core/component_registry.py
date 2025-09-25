"""
Component registry for automatic registration of all components.
"""
from core.factories.parser_factory import ParserFactory
from core.factories.chunker_factory import ChunkerFactory
from core.factories.vector_store_factory import VectorStoreFactory
from core.factories.agent_factory import AgentFactory

from parsers.docling_parser import DoclingParser
from chunkers.semantic_chunker import SemanticChunker
from chunkers.hierarchical_chunker import HierarchicalChunker
from vector_stores.qdrant_store import QdrantStore
from agents.manager_agent import ManagerAgent
from agents.assistant_agent import AssistantAgent


def register_all_components():
    """Register all available components with their factories."""
    
    ParserFactory.register_parser("DoclingParser", DoclingParser)
    
    ChunkerFactory.register_chunker("SemanticChunker", SemanticChunker)
    ChunkerFactory.register_chunker("HierarchicalChunker", HierarchicalChunker)
    
    VectorStoreFactory.register_vector_store("QdrantStore", QdrantStore)
    
    AgentFactory.register_agent("ManagerAgent", ManagerAgent)
    AgentFactory.register_agent("AssistantAgent", AssistantAgent)


register_all_components()
