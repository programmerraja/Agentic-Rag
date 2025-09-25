"""
Factory for creating vector store instances.
"""
from typing import Dict, Any, Type
from core.interfaces.vector_store_interface import VectorStoreInterface
from core.config.base_config import VectorStoreConfig


class VectorStoreFactory:
    """Factory for creating vector store instances."""
    
    _vector_stores: Dict[str, Type[VectorStoreInterface]] = {}
    
    @classmethod
    def register_vector_store(cls, name: str, vector_store_class: Type[VectorStoreInterface]) -> None:
        """
        Register a vector store class.
        
        Args:
            name: Vector store name
            vector_store_class: Vector store class to register
        """
        cls._vector_stores[name] = vector_store_class
    
    @classmethod
    def create_vector_store(cls, name: str, config: Dict[str, Any]) -> VectorStoreInterface:
        """
        Create a vector store instance.
        
        Args:
            name: Vector store name
            config: Vector store configuration
            
        Returns:
            Vector store instance
        """
        if name not in cls._vector_stores:
            raise ValueError(f"Unknown vector store: {name}")
        
        vector_store_class = cls._vector_stores[name]
        return vector_store_class(**config)
    
    @classmethod
    def create_from_config(cls, vector_store_config: VectorStoreConfig, vector_store_name: str = None) -> VectorStoreInterface:
        """
        Create vector store from configuration.
        
        Args:
            vector_store_config: Vector store configuration
            vector_store_name: Specific vector store name, uses default if None
            
        Returns:
            Vector store instance
        """
        name = vector_store_name or vector_store_config.default
        
        if name not in vector_store_config.available:
            raise ValueError(f"Vector store '{name}' not found in configuration")
        
        vector_store_info = vector_store_config.available[name]
        vector_store_class_name = vector_store_info["class"]
        vector_store_config_dict = vector_store_info.get("config", {})
        
        return cls.create_vector_store(vector_store_class_name, vector_store_config_dict)
    
    @classmethod
    def get_available_vector_stores(cls) -> list[str]:
        """
        Get list of available vector store names.
        
        Returns:
            List of vector store names
        """
        return list(cls._vector_stores.keys())
