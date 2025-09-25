"""
Factory for creating parser instances.
"""
from typing import Dict, Any, Type
from core.interfaces.parser_interface import ParserInterface
from core.config.base_config import ParserConfig


class ParserFactory:
    """Factory for creating parser instances."""
    
    _parsers: Dict[str, Type[ParserInterface]] = {}
    
    @classmethod
    def register_parser(cls, name: str, parser_class: Type[ParserInterface]) -> None:
        """
        Register a parser class.
        
        Args:
            name: Parser name
            parser_class: Parser class to register
        """
        cls._parsers[name] = parser_class
    
    @classmethod
    def create_parser(cls, name: str, config: Dict[str, Any]) -> ParserInterface:
        """
        Create a parser instance.
        
        Args:
            name: Parser name
            config: Parser configuration
            
        Returns:
            Parser instance
        """
        if name not in cls._parsers:
            raise ValueError(f"Unknown parser: {name}")
        
        parser_class = cls._parsers[name]
        return parser_class(**config)
    
    @classmethod
    def create_from_config(cls, parser_config: ParserConfig, parser_name: str = None) -> ParserInterface:
        """
        Create parser from configuration.
        
        Args:
            parser_config: Parser configuration
            parser_name: Specific parser name, uses default if None
            
        Returns:
            Parser instance
        """
        name = parser_name or parser_config.default
        
        if name not in parser_config.available:
            raise ValueError(f"Parser '{name}' not found in configuration")
        
        parser_info = parser_config.available[name]
        parser_class_name = parser_info["class"]
        parser_config_dict = parser_info.get("config", {})
        
        return cls.create_parser(parser_class_name, parser_config_dict)
    
    @classmethod
    def get_available_parsers(cls) -> list[str]:
        """
        Get list of available parser names.
        
        Returns:
            List of parser names
        """
        return list(cls._parsers.keys())
