"""
Base agent implementation.
"""
from typing import List, Dict, Any, Optional, Callable
from core.interfaces.agent_interface import AgentInterface
from llama_index.core.schema import NodeWithScore


class BaseAgent(AgentInterface):
    """Base agent implementation with common functionality."""
    
    def __init__(self, **kwargs):
        """Initialize base agent."""
        self.config = kwargs
        self._tools: Dict[str, Callable] = {}
        self._model = None
    
    def register_tool(self, tool_name: str, tool_function: Callable) -> None:
        """
        Register a new tool with the agent.
        
        Args:
            tool_name: Name of the tool
            tool_function: Function to execute when tool is called
        """
        self._tools[tool_name] = tool_function
    
    def execute_tool(self, tool_name: str, **kwargs) -> Any:
        """
        Execute a tool by name.
        
        Args:
            tool_name: Name of the tool to execute
            **kwargs: Tool arguments
            
        Returns:
            Tool execution result
        """
        if tool_name not in self._tools:
            raise ValueError(f"Tool '{tool_name}' not found")
        
        try:
            return self._tools[tool_name](**kwargs)
        except Exception as e:
            raise RuntimeError(f"Failed to execute tool '{tool_name}': {str(e)}")
    
    def get_available_tools(self) -> List[str]:
        """Get list of available tools."""
        return list(self._tools.keys())
    
    def _format_context(self, context: Optional[List[NodeWithScore]]) -> str:
        """
        Format context nodes into a string.
        
        Args:
            context: List of context nodes
            
        Returns:
            Formatted context string
        """
        if not context:
            return ""
        
        context_parts = []
        for i, node in enumerate(context, 1):
            context_parts.append(f"Context {i}:\n{node.text}\n")
        
        return "\n".join(context_parts)
