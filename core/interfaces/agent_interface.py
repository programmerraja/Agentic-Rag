"""
Agent interface for the multi-agent system.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Callable
from llama_index.core.schema import NodeWithScore


class AgentInterface(ABC):
    """Abstract base class for agents."""
    
    @abstractmethod
    def process_query(self, query: str, context: Optional[List[NodeWithScore]] = None) -> str:
        """
        Process a user query and return a response.
        
        Args:
            query: User query
            context: Optional context from vector store
            
        Returns:
            Agent response
        """
        pass
    
    @abstractmethod
    def get_agent_name(self) -> str:
        """
        Get the name of this agent.
        
        Returns:
            Agent name
        """
        pass
    
    @abstractmethod
    def get_available_tools(self) -> List[str]:
        """
        Get list of available tools for this agent.
        
        Returns:
            List of tool names
        """
        pass
    
    @abstractmethod
    def register_tool(self, tool_name: str, tool_function: Callable) -> None:
        """
        Register a new tool with the agent.
        
        Args:
            tool_name: Name of the tool
            tool_function: Function to execute when tool is called
        """
        pass
    
    @abstractmethod
    def execute_tool(self, tool_name: str, **kwargs) -> Any:
        """
        Execute a tool by name.
        
        Args:
            tool_name: Name of the tool to execute
            **kwargs: Tool arguments
            
        Returns:
            Tool execution result
        """
        pass
