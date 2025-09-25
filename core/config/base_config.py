"""
Base configuration classes for the Agentic RAG system.
"""
from typing import Dict, Any, Optional
from dataclasses import dataclass
import json
import os
from pathlib import Path


@dataclass
class SystemConfig:
    """System configuration."""
    name: str
    version: str
    debug: bool = False


@dataclass
class ParserConfig:
    """Parser configuration."""
    default: str
    available: Dict[str, Dict[str, Any]]


@dataclass
class ChunkerConfig:
    """Chunker configuration."""
    default: str
    available: Dict[str, Dict[str, Any]]


@dataclass
class VectorStoreConfig:
    """Vector store configuration."""
    default: str
    available: Dict[str, Dict[str, Any]]


@dataclass
class AgentConfig:
    """Agent configuration."""
    manager: Dict[str, Any]
    assistant: Dict[str, Any]


@dataclass
class RAGConfig:
    """Main RAG system configuration."""
    system: SystemConfig
    parsers: ParserConfig
    chunkers: ChunkerConfig
    vector_stores: VectorStoreConfig
    agents: AgentConfig


class ConfigManager:
    """Configuration manager for the RAG system."""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize configuration manager.
        
        Args:
            config_path: Path to configuration file. If None, uses default.
        """
        self.config_path = config_path or "config.json"
        self._config: Optional[RAGConfig] = None
    
    def load_config(self) -> RAGConfig:
        """
        Load configuration from file.
        
        Returns:
            Loaded configuration object
        """
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        
        with open(self.config_path, 'r') as f:
            config_data = json.load(f)
        
        self._config = self._parse_config(config_data)
        return self._config
    
    def save_config(self, config: RAGConfig) -> None:
        """
        Save configuration to file.
        
        Args:
            config: Configuration object to save
        """
        config_data = self._serialize_config(config)
        
        with open(self.config_path, 'w') as f:
            json.dump(config_data, f, indent=2)
        
        self._config = config
    
    def get_config(self) -> RAGConfig:
        """
        Get current configuration.
        
        Returns:
            Current configuration object
        """
        if self._config is None:
            self._config = self.load_config()
        return self._config
    
    def _parse_config(self, data: Dict[str, Any]) -> RAGConfig:
        """Parse configuration data into objects."""
        return RAGConfig(
            system=SystemConfig(**data["system"]),
            parsers=ParserConfig(**data["parsers"]),
            chunkers=ChunkerConfig(**data["chunkers"]),
            vector_stores=VectorStoreConfig(**data["vector_stores"]),
            agents=AgentConfig(**data["agents"])
        )
    
    def _serialize_config(self, config: RAGConfig) -> Dict[str, Any]:
        """Serialize configuration object to dictionary."""
        return {
            "system": {
                "name": config.system.name,
                "version": config.system.version,
                "debug": config.system.debug
            },
            "parsers": {
                "default": config.parsers.default,
                "available": config.parsers.available
            },
            "chunkers": {
                "default": config.chunkers.default,
                "available": config.chunkers.available
            },
            "vector_stores": {
                "default": config.vector_stores.default,
                "available": config.vector_stores.available
            },
            "agents": {
                "manager": config.agents.manager,
                "assistant": config.agents.assistant
            }
        }
    
    def create_default_config(self) -> RAGConfig:
        """Create a default configuration."""
        return RAGConfig(
            system=SystemConfig(
                name="agentic-rag",
                version="1.0.0",
                debug=False
            ),
            parsers=ParserConfig(
                default="docling",
                available={
                    "docling": {
                        "class": "DoclingParser",
                        "config": {
                            "enable_ocr": True,
                            "table_structure": True
                        }
                    }
                }
            ),
            chunkers=ChunkerConfig(
                default="semantic",
                available={
                    "semantic": {
                        "class": "SemanticChunker",
                        "config": {
                            "buffer_size": 1,
                            "threshold": 0.75
                        }
                    }
                }
            ),
            vector_stores=VectorStoreConfig(
                default="qdrant",
                available={
                    "qdrant": {
                        "class": "QdrantStore",
                        "config": {
                            "url": "http://localhost:6333",
                            "collection_name": "documents"
                        }
                    }
                }
            ),
            agents=AgentConfig(
                manager={
                    "class": "ManagerAgent",
                    "config": {
                        "model": "gemini-2.5-flash",
                        "tools": ["get_context", "search_documents"]
                    }
                },
                assistant={
                    "class": "AssistantAgent",
                    "config": {
                        "model": "gemini-2.5-flash",
                        "specialization": "health_insurance"
                    }
                }
            )
        )
