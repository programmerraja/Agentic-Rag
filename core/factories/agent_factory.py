"""
Factory for creating agent instances.
"""
from typing import Dict, Any, Type
from core.interfaces.agent_interface import AgentInterface
from core.config.base_config import AgentConfig


class AgentFactory:
    """Factory for creating agent instances."""
    
    _agents: Dict[str, Type[AgentInterface]] = {}
    
    @classmethod
    def register_agent(cls, name: str, agent_class: Type[AgentInterface]) -> None:
        """
        Register an agent class.
        
        Args:
            name: Agent name
            agent_class: Agent class to register
        """
        cls._agents[name] = agent_class
    
    @classmethod
    def create_agent(cls, name: str, config: Dict[str, Any]) -> AgentInterface:
        """
        Create an agent instance.
        
        Args:
            name: Agent name
            config: Agent configuration
            
        Returns:
            Agent instance
        """
        if name not in cls._agents:
            raise ValueError(f"Unknown agent: {name}")
        
        agent_class = cls._agents[name]
        return agent_class(**config)
    
    @classmethod
    def create_from_config(cls, agent_config: AgentConfig, agent_name: str) -> AgentInterface:
        """
        Create agent from configuration.
        
        Args:
            agent_config: Agent configuration
            agent_name: Agent name (manager or assistant)
            
        Returns:
            Agent instance
        """
        if agent_name not in ["manager", "assistant"]:
            raise ValueError(f"Unknown agent type: {agent_name}")
        
        agent_info = getattr(agent_config, agent_name)
        agent_class_name = agent_info["class"]
        agent_config_dict = agent_info.get("config", {})
        
        return cls.create_agent(agent_class_name, agent_config_dict)
    
    @classmethod
    def get_available_agents(cls) -> list[str]:
        """
        Get list of available agent names.
        
        Returns:
            List of agent names
        """
        return list(cls._agents.keys())
