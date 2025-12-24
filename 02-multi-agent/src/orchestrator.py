from typing import List, Dict, Any
from enum import Enum
from src.agents import (
    ResearchAgent, 
    AnalysisAgent, 
    WriterAgent, 
    CriticAgent,
    AgentResponse
)


class WorkflowType(Enum):
    """Types of multi-agent workflows."""
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    HIERARCHICAL = "hierarchical"


class MultiAgentOrchestrator:
    """Orchestrates multiple agents to complete complex tasks."""
    
    def __init__(self):
        self.research_agent = ResearchAgent()
        self.analysis_agent = AnalysisAgent()
        self.writer_agent = WriterAgent()
        self.critic_agent = CriticAgent()
        self.history: List[AgentResponse] = []
    
    def sequential_workflow(self, task: str) -> Dict[str, Any]:
        """
        Execute agents sequentially, each building on previous results.
        
        Flow: Research -> Analysis -> Writing -> Critique
        
        Args:
            task: The main task to complete
            
        Returns:
            Dictionary containing all agent responses and final output
        """
        # Step 1: Research
        print("\n[1/4] Research Agent working...")
        research_response = self.research_agent.process(task)
        self.history.append(research_response)
        
        # Step 2: Analysis
        print("\n[2/4] Analysis Agent working...")
        analysis_response = self.analysis_agent.process(
            f"Analyze this research on: {task}",
            context={"research": research_response.content}
        )
        self.history.append(analysis_response)
        
        # Step 3: Writing
        print("\n[3/4] Writer Agent working...")
        writer_response = self.writer_agent.process(
            f"Write a comprehensive article on: {task}",
            context={
                "research": research_response.content,
                "analysis": analysis_response.content
            }
        )
        self.history.append(writer_response)
        
        # Step 4: Critique
        print("\n[4/4] Critic Agent reviewing...")
        critique_response = self.critic_agent.process(
            "Review and critique this article",
            context={"article": writer_response.content}
        )
        self.history.append(critique_response)
        
        return {
            "task": task,
            "workflow": "sequential",
            "research": research_response.content,
            "analysis": analysis_response.content,
            "article": writer_response.content,
            "critique": critique_response.content,
            "final_output": writer_response.content
        }
    
    def parallel_workflow(self, task: str, subtasks: List[str]) -> Dict[str, Any]:
        """
        Execute multiple research agents in parallel for different subtasks.
        
        Args:
            task: The main task
            subtasks: List of subtasks to research in parallel
            
        Returns:
            Dictionary containing aggregated results
        """
        # Parallel research phase
        print("\n[Phase 1] Parallel research on subtasks...")
        research_results = []
        for i, subtask in enumerate(subtasks, 1):
            print(f"  [{i}/{len(subtasks)}] Researching: {subtask[:50]}...")
            response = self.research_agent.process(subtask)
            research_results.append(response)
            self.history.append(response)
        
        # Aggregate results
        print("\n[Phase 2] Aggregating research results...")
        combined_research = "\n\n".join([r.content for r in research_results])
        
        # Analysis phase
        print("\n[Phase 3] Analyzing aggregated research...")
        analysis_response = self.analysis_agent.process(
            f"Analyze all research findings for: {task}",
            context={"combined_research": combined_research}
        )
        self.history.append(analysis_response)
        
        # Writing phase
        print("\n[Phase 4] Writing final output...")
        writer_response = self.writer_agent.process(
            f"Create a comprehensive report on: {task}",
            context={
                "research": combined_research,
                "analysis": analysis_response.content
            }
        )
        self.history.append(writer_response)
        
        return {
            "task": task,
            "workflow": "parallel",
            "subtasks": subtasks,
            "research_count": len(research_results),
            "analysis": analysis_response.content,
            "final_output": writer_response.content
        }
    
    def hierarchical_workflow(self, task: str) -> Dict[str, Any]:
        """
        Execute workflow with supervisor making decisions.
        
        The supervisor (critic) reviews and decides if iteration is needed.
        
        Args:
            task: The main task to complete
            
        Returns:
            Dictionary containing final approved output
        """
        print(f"Starting hierarchical workflow: {task}")        
        max_iterations = 2
        iteration = 0
        approved = False
        
        while not approved and iteration < max_iterations:
            iteration += 1
            print(f"\n=== Iteration {iteration} ===")
            
            # Research
            print("\n[Step 1] Research phase...")
            research_response = self.research_agent.process(task)
            self.history.append(research_response)
            
            # Write
            print("\n[Step 2] Writing phase...")
            writer_response = self.writer_agent.process(
                f"Write about: {task}",
                context={"research": research_response.content}
            )
            self.history.append(writer_response)
            
            # Supervisor review
            print("\n[Step 3] Supervisor review...")
            critique_response = self.critic_agent.process(
                "Review this content. Respond with 'APPROVED' if good, or specific improvements needed.",
                context={"content": writer_response.content}
            )
            self.history.append(critique_response)
            
            if "APPROVED" in critique_response.content.upper():
                approved = True
                print("Content approved by supervisor")
            else:
                print(f"Improvements requested, iteration {iteration + 1} starting...")
                task = f"{task}\n\nImprovement feedback: {critique_response.content}"
        
        return {
            "task": task,
            "workflow": "hierarchical",
            "iterations": iteration,
            "approved": approved,
            "final_output": writer_response.content,
            "final_critique": critique_response.content
        }
    
    def get_history(self) -> List[Dict[str, Any]]:
        """Get the execution history of all agents."""
        return [
            {
                "agent": response.agent_name,
                "content_length": len(response.content),
                "metadata": response.metadata
            }
            for response in self.history
        ]
    
    def clear_history(self):
        """Clear execution history."""
        self.history.clear()
