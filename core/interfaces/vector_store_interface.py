"""
Vector store interface for document storage and retrieval.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Tuple
from llama_index.core.schema import BaseNode, NodeWithScore


class VectorStoreInterface(ABC):
    """Abstract base class for vector stores."""
    
    @abstractmethod
    def add(self, nodes: List[BaseNode], **kwargs) -> List[str]:
        """
        Add nodes to the vector store.
        
        Args:
            nodes: List of nodes to add
            **kwargs: Additional storage options
            
        Returns:
            List of node IDs that were added
        """
        pass
    
    @abstractmethod
    def search(self, query: str, top_k: int = 5, **kwargs) -> List[NodeWithScore]:
        """
        Search for similar nodes.
        
        Args:
            query: Search query
            top_k: Number of results to return
            **kwargs: Additional search options
            
        Returns:
            List of nodes with similarity scores
        """
        pass
    
    @abstractmethod
    def delete(self, node_ids: List[str]) -> bool:
        """
        Delete nodes by their IDs.
        
        Args:
            node_ids: List of node IDs to delete
            
        Returns:
            True if deletion was successful
        """
        pass
    
    @abstractmethod
    def get_store_name(self) -> str:
        """
        Get the name of this vector store.
        
        Returns:
            Vector store name
        """
        pass
    
    @abstractmethod
    def get_collection_info(self) -> Dict[str, Any]:
        """
        Get information about the current collection.
        
        Returns:
            Dictionary with collection information
        """
        pass
    
    @abstractmethod
    def clear_collection(self) -> bool:
        """
        Clear all data from the collection.
        
        Returns:
            True if clearing was successful
        """
        pass
