"""
Assistant agent implementation.
"""
import logging
from typing import List, Dict, Any, Optional
from google import genai
from google.genai import types
from agents.base_agent import BaseAgent
from llama_index.core.schema import NodeWithScore

logger = logging.getLogger(__name__)


class AssistantAgent(BaseAgent):
    """Assistant agent specialized in answering health insurance questions."""
    
    def __init__(self, model: str = "gemini-2.5-flash", specialization: str = "health_insurance", **kwargs):
        """
        Initialize assistant agent.
        
        Args:
            model: LLM model to use
            specialization: Agent specialization
            **kwargs: Additional configuration
        """
        super().__init__(**kwargs)
        self.model = model
        self.specialization = specialization
        self._client = None
        self._system_prompt = None
    
    def _get_client(self) -> genai.Client:
        """Get or create GenAI client."""
        if self._client is None:
            self._client = genai.Client()
        return self._client
    
    def _get_system_prompt(self) -> str:
        """Get system prompt for the assistant agent."""
        if self._system_prompt is None:
            try:
                with open("prompt/assistant.md", "r") as f:
                    self._system_prompt = f.read()
            except FileNotFoundError:
                self._system_prompt = f"""You are an assistant agent specialized in {self.specialization}.
                Your role is to:
                1. Answer user questions about health insurance policies
                2. Provide detailed explanations of coverage, benefits, and terms
                3. Help users understand policy documents
                4. Offer guidance on insurance-related decisions
                
                Always be helpful, accurate, and professional in your responses.
                If you don't know something, say so and suggest how the user might find the information.
                """
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
        
        try:
            response = client.models.generate_content(
                model=self.model,
                contents=messages,
            )
            return response.text
        except Exception as e:
            raise RuntimeError(f"Failed to process query with assistant agent: {str(e)}")
    
    def get_agent_name(self) -> str:
        """Get agent name."""
        return "AssistantAgent"
    
    def register_context_tool(self, vector_store) -> None:
        """
        Register context retrieval tool.
        
        Args:
            vector_store: Vector store instance for context retrieval
        """
        def get_context(question: str) -> str:
            """Get context for a question."""
            try:
                results = vector_store.search(question, top_k=5)
                logger.info(f"Context for question: {question} is {results}")
                return self._format_context(results)
            except Exception as e:
                return f"Error retrieving context: {str(e)}"
        
        self.register_tool("get_context", get_context)
    