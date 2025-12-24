from typing import List, Dict, Any
from src.orchestrator import MultiAgentOrchestrator


def example_research_pipeline():
    """
    Advanced example: Research pipeline with multiple phases.
    
    Demonstrates how to chain workflows for complex tasks.
    """
    orchestrator = MultiAgentOrchestrator()
    
    # Phase 1: Parallel research on multiple aspects
    research_result = orchestrator.parallel_workflow(
        "AI in healthcare applications",
        subtasks=[
            "AI for medical diagnosis and imaging",
            "AI for drug discovery and development",
            "AI for patient care and monitoring",
            "Ethical considerations in healthcare AI"
        ]
    )
    
    # Phase 2: Deep analysis
    orchestrator.clear_history()  # Start fresh for next phase
    
    analysis_result = orchestrator.sequential_workflow(
        f"Analyze and synthesize these findings:\n{research_result['final_output']}"
    )
    
    print("FINAL COMPREHENSIVE REPORT:")
    print(analysis_result["article"])
    print("QUALITY REVIEW:")
    print(analysis_result["critique"])
    
    return {
        "phase1": research_result,
        "phase2": analysis_result
    }


def example_iterative_improvement():
    """
    Advanced example: Iterative content improvement.
    
    Uses hierarchical workflow to refine content through iterations.
    """
    orchestrator = MultiAgentOrchestrator()
    
    result = orchestrator.hierarchical_workflow(
        "Create a technical guide on implementing RAG (Retrieval Augmented Generation)"
    )
    
    print("FINAL APPROVED CONTENT:")
    print(result["final_output"])
    print("APPROVAL DETAILS:")
    print(f"Status: {'APPROVED' if result['approved'] else 'NOT APPROVED'}")
    print(f"Iterations Required: {result['iterations']}")
    print(f"\nFinal Critique:\n{result['final_critique']}")
    
    return result


def example_custom_agent_workflow():
    """
    Advanced example: Custom workflow with specific agent sequence.
    
    Shows how to create custom workflows beyond the standard patterns.
    """
    print("\nAdvanced Example: Custom Agent Workflow")

    
    orchestrator = MultiAgentOrchestrator()
    # Custom workflow: Research -> Write -> Critique -> Revise
    task = "Best practices for Python async programming"

    print("\n[Step 1] Initial research...")
    research = orchestrator.research_agent.process(task)

    print("\n[Step 2] Draft writing...")
    draft = orchestrator.writer_agent.process(
        f"Write a guide on: {task}",
        context={"research": research.content}
    )
    
    print("\n[Step 3] Critical review...")
    critique = orchestrator.critic_agent.process(
        "Identify specific areas that need improvement",
        context={"draft": draft.content}
    )
    
    print("\n[Step 4] Revised writing based on feedback...")
    final = orchestrator.writer_agent.process(
        f"Revise this content based on feedback:\n\nOriginal: {draft.content}\n\nFeedback: {critique.content}",
        context={"research": research.content}
    )
    

    print("ORIGINAL DRAFT:")
    print(draft.content[:500] + "...")
    print("CRITIQUE:")
    print(critique.content)
    print("FINAL REVISED VERSION:")
    print(final.content)
    
    return {
        "research": research.content,
        "draft": draft.content,
        "critique": critique.content,
        "final": final.content
    }


def example_batch_processing():
    """
    Advanced example: Batch process multiple tasks.
    
    Demonstrates efficient processing of multiple independent tasks.
    """
    orchestrator = MultiAgentOrchestrator()
    
    tasks = [
        "Summarize microservices architecture",
        "Explain event-driven design patterns",
        "Overview of API security best practices"
    ]
    
    results = []
    
    for i, task in enumerate(tasks, 1):
        print(f"\n[Task {i}/{len(tasks)}] Processing: {task}")
        print("-" * 60)
        
        result = orchestrator.sequential_workflow(task)
        results.append(result)
        
        print(f"Completed: {len(result['article'])} chars")
        
        # Clear history between tasks
        orchestrator.clear_history()
    

    print("BATCH RESULTS SUMMARY:")

    
    for i, (task, result) in enumerate(zip(tasks, results), 1):
        print(f"\n[{i}] {task}")
        print(f"    Article Length: {len(result['article'])} chars")
        print(f"    Critique Summary: {result['critique'][:100]}...")
    
    return results


def main():
    """Run all advanced examples."""
    print("\nMULTI-AGENT SYSTEM - ADVANCED EXAMPLES")

    
    examples = {
        "1": ("Multi-Phase Research Pipeline", example_research_pipeline),
        "2": ("Iterative Content Improvement", example_iterative_improvement),
        "3": ("Custom Agent Workflow", example_custom_agent_workflow),
        "4": ("Batch Task Processing", example_batch_processing)
    }
    
    print("\nAvailable Examples:")
    for key, (name, _) in examples.items():
        print(f"{key}. {name}")
    print("5. Run All Examples")
    print("6. Exit")
    
    choice = input("\nSelect example (1-6): ").strip()
    
    if choice in examples:
        name, func = examples[choice]
        print(f"\nRunning: {name}")
        func()
    elif choice == "5":
        for name, func in examples.values():
            print(f"\n\nRunning: {name}")
        
            func()
            input("\nPress Enter to continue to next example...")
    elif choice == "6":
        print("Exiting...")
    else:
        print("Invalid choice")


if __name__ == "__main__":
    main()
