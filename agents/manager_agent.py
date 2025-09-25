"""
Manager agent implementation.
"""
import logging
from typing import List, Dict, Any, Optional
from google import genai
from google.genai import types
from agents.base_agent import BaseAgent
from agents.assistant_agent import AssistantAgent
from llama_index.core.schema import NodeWithScore

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class ManagerAgent(BaseAgent):
    """Manager agent responsible for overall system flow and orchestration."""
    
    def __init__(self, model: str = "gemini-2.5-flash", tools: List[str] = None, **kwargs):
        """
        Initialize manager agent.
        
        Args:
            model: LLM model to use
            tools: List of available tools
            **kwargs: Additional configuration
        """
        super().__init__(**kwargs)
        self.model = model
        self.tools = tools or []
        self._client = None
        self._system_prompt = None
    
    def _get_client(self) -> genai.Client:
        """Get or create GenAI client."""
        if self._client is None:
            self._client = genai.Client()
        return self._client
    
    def _get_system_prompt(self) -> str:
        """Get system prompt for the manager agent."""
        if self._system_prompt is None:
            with open("prompt/manager.md", "r") as f:
                self._system_prompt = f.read()
        return self._system_prompt
    
    def process_query(self, query: str, context: Optional[List[NodeWithScore]] = None) -> str:
        """
        Process a user query and return a response.
        
        Args:
            query: User query
            context: Optional context from vector store
            
        Returns:
            Agent response
        """
        client = self._get_client()
        system_prompt = self._get_system_prompt()
        
        # Prepare tools for the model
        tools = []
        for tool_name in self.tools:
            if tool_name in self._tools:
                tools.append(self._tools[tool_name])
        
        # Format context if provided
        context_text = self._format_context(context)
        
        # Prepare messages
        messages = [
            types.Content(
                role="model", 
                parts=[types.Part.from_text(text=system_prompt)]
            ),
            types.Content(
                role="user", 
                parts=[types.Part.from_text(text=f"Query: {query}\n\nContext: {context_text}")]
            )
        ]
        
        config = types.GenerateContentConfig(tools=tools) if tools else None
        
        try:
            response = client.models.generate_content(
                model=self.model,
                contents=messages,
                config=config,
            )
            return response.text
        except Exception as e:
            raise RuntimeError(f"Failed to process query with manager agent: {str(e)}")
    
    def get_agent_name(self) -> str:
        """Get agent name."""
        return "ManagerAgent"
    
    def register_context_tool(self, vector_store) -> None:
        """
        Register context retrieval tool.
        
        Args:
            vector_store: Vector store instance for context retrieval
        """
        def get_context(question: str,plan_name: str) -> str:
            """
            Pass question and plan name if you want details for specific plan else pass None
            Supported plan name are: 
                1.familyHealthOptimaInsurancePlan 
                2.seniorCitizensRedCarpetHealthInsurancePolicy 
                3.starComprehensiveInsurancePolicy 
                4.starHealthGainInsurancePolicy
            """
            try:
                results = vector_store.search(question, top_k=5, plan_name=plan_name)
                context= self._format_context(results)
                logger.info(f"Getting context for question: {question} plan_name {plan_name} and context: {context}")
                return context
            except Exception as e:
                return f"Error retrieving context: {str(e)}"
        
        self.register_tool("get_context", get_context)
    

    def register_assistant_agents(self, assistant_agents: AssistantAgent) -> None:
        """
        Register assistant agents.
        
        Args:
            assistant_agents: Assistant agent
        """


        def get_assistant_agents(question: str) -> str:
            """Get assistant agents for a question."""
            logger.info(f"Getting assistant agents for question: {question}")
            return assistant_agents.process_query(question)
        
        self.register_tool("get_assistant_agents", get_assistant_agents)