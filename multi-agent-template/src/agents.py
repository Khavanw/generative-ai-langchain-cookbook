from typing import Dict, List, Any
from dataclasses import dataclass
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from settings import settings


@dataclass
class AgentResponse:
    """Response from an agent."""
    agent_name: str
    content: str
    metadata: Dict[str, Any]


class BaseAgent:
    """Base class for all agents in the system."""
    
    def __init__(self, name: str, system_prompt: str):
        self.name = name
        self.system_prompt = system_prompt
        self.llm = AzureChatOpenAI(
            azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
            api_key=settings.AZURE_OPENAI_API_KEY,
            api_version=settings.AZURE_OPENAI_API_VERSION,
            azure_deployment=settings.AZURE_OPENAI_DEPLOYMENT_NAME,
            temperature=0.7,
        )
    
    def process(self, task: str, context: Dict[str, Any] = None) -> AgentResponse:
        """
        Process a task and return response.
        
        Args:
            task: The task description
            context: Additional context from other agents
            
        Returns:
            Agent response with content and metadata
        """
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=task)
        ]
        
        if context:
            context_str = "\n".join([f"{k}: {v}" for k, v in context.items()])
            messages.insert(1, HumanMessage(content=f"Context:\n{context_str}"))
        
        response = self.llm.invoke(messages)
        
        return AgentResponse(
            agent_name=self.name,
            content=response.content,
            metadata={"model": settings.AZURE_OPENAI_DEPLOYMENT_NAME}
        )


class ResearchAgent(BaseAgent):
    """Agent specialized in research and information gathering."""
    
    def __init__(self):
        system_prompt = """You are a Research Agent specialized in gathering and analyzing information.
Your responsibilities:
- Research topics thoroughly
- Identify key facts and insights
- Provide well-structured summaries
- Cite sources when possible

Be comprehensive but concise in your research."""
        super().__init__("ResearchAgent", system_prompt)


class AnalysisAgent(BaseAgent):
    """Agent specialized in data analysis and evaluation."""
    
    def __init__(self):
        system_prompt = """You are an Analysis Agent specialized in evaluating and analyzing information.
Your responsibilities:
- Analyze research findings
- Identify patterns and trends
- Evaluate quality and reliability
- Provide critical insights
- Make data-driven recommendations

Be objective and thorough in your analysis."""
        super().__init__("AnalysisAgent", system_prompt)


class WriterAgent(BaseAgent):
    """Agent specialized in content creation and writing."""
    
    def __init__(self):
        system_prompt = """You are a Writer Agent specialized in creating high-quality content.
Your responsibilities:
- Write clear and engaging content
- Organize information logically
- Adapt tone and style to audience
- Ensure accuracy and clarity
- Create well-structured documents

Be creative but maintain accuracy."""
        super().__init__("WriterAgent", system_prompt)


class CriticAgent(BaseAgent):
    """Agent specialized in reviewing and critiquing work."""
    
    def __init__(self):
        system_prompt = """You are a Critic Agent specialized in quality assurance and review.
Your responsibilities:
- Review content for accuracy
- Check for logical consistency
- Identify gaps or weaknesses
- Suggest improvements
- Ensure quality standards

Be constructive and specific in your feedback."""
        super().__init__("CriticAgent", system_prompt)
