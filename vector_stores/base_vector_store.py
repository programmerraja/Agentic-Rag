"""
Base vector store implementation.
"""
from typing import List, Dict, Any
from core.interfaces.vector_store_interface import VectorStoreInterface
from llama_index.core.schema import BaseNode, NodeWithScore


class BaseVectorStore(VectorStoreInterface):
    """Base vector store implementation with common functionality."""
    
    def __init__(self, **kwargs):
        """Initialize base vector store."""
        self.config = kwargs
        self._initialized = False
    
    def _ensure_initialized(self) -> None:
        """Ensure the vector store is initialized."""
        if not self._initialized:
            self._initialize()
            self._initialized = True
    
    def _initialize(self) -> None:
        """Initialize the vector store. Override in subclasses."""
        pass
    
    def get_collection_info(self) -> Dict[str, Any]:
        """Get collection information. Override in subclasses."""
        return {
            "store_type": self.get_store_name(),
            "initialized": self._initialized,
            "config": self.config
        }
