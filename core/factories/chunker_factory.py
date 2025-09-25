"""
Factory for creating chunker instances.
"""
from typing import Dict, Any, Type
from core.interfaces.chunker_interface import ChunkerInterface
from core.config.base_config import ChunkerConfig


class ChunkerFactory:
    """Factory for creating chunker instances."""
    
    _chunkers: Dict[str, Type[ChunkerInterface]] = {}
    
    @classmethod
    def register_chunker(cls, name: str, chunker_class: Type[ChunkerInterface]) -> None:
        """
        Register a chunker class.
        
        Args:
            name: Chunker name
            chunker_class: Chunker class to register
        """
        cls._chunkers[name] = chunker_class
    
    @classmethod
    def create_chunker(cls, name: str, config: Dict[str, Any]) -> ChunkerInterface:
        """
        Create a chunker instance.
        
        Args:
            name: Chunker name
            config: Chunker configuration
            
        Returns:
            Chunker instance
        """
        if name not in cls._chunkers:
            raise ValueError(f"Unknown chunker: {name}")
        
        chunker_class = cls._chunkers[name]
        return chunker_class(**config)
    
    @classmethod
    def create_from_config(cls, chunker_config: ChunkerConfig, chunker_name: str = None) -> ChunkerInterface:
        """
        Create chunker from configuration.
        
        Args:
            chunker_config: Chunker configuration
            chunker_name: Specific chunker name, uses default if None
            
        Returns:
            Chunker instance
        """
        name = chunker_name or chunker_config.default
        
        if name not in chunker_config.available:
            raise ValueError(f"Chunker '{name}' not found in configuration")
        
        chunker_info = chunker_config.available[name]
        chunker_class_name = chunker_info["class"]
        chunker_config_dict = chunker_info.get("config", {})
        
        return cls.create_chunker(chunker_class_name, chunker_config_dict)
    
    @classmethod
    def get_available_chunkers(cls) -> list[str]:
        """
        Get list of available chunker names.
        
        Returns:
            List of chunker names
        """
        return list(cls._chunkers.keys())
