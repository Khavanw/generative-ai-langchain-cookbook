import logging
from src.orchestrator import MultiAgentOrchestrator
from settings import settings


logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def demo_sequential():
    """Demonstrate sequential workflow."""
    orchestrator = MultiAgentOrchestrator()
    
    result = orchestrator.sequential_workflow(
        "Explain the benefits of microservices architecture"
    )
    
    print("FINAL ARTICLE:")
    print(result["article"])
    
    print("CRITIQUE:")
    print(result["critique"])
    
    return result


def demo_parallel():
    """Demonstrate parallel workflow."""
    orchestrator = MultiAgentOrchestrator()
    
    result = orchestrator.parallel_workflow(
        "Compare cloud service providers",
        subtasks=[
            "Research AWS services and pricing",
            "Research Azure services and pricing",
            "Research Google Cloud services and pricing"
        ]
    )
    
    print("FINAL REPORT:")
    print(result["final_output"])
    
    return result


def demo_hierarchical():
    """Demonstrate hierarchical workflow with supervisor."""
    orchestrator = MultiAgentOrchestrator()
    
    result = orchestrator.hierarchical_workflow(
        "Write a guide on Python best practices for AI development"
    )
    
    print("FINAL OUTPUT:")
    print(result["final_output"])
    
    print("SUPERVISOR DECISION:")
    print(f"Approved: {result['approved']}")
    print(f"Iterations: {result['iterations']}")
    
    return result


def interactive_mode():
    """Interactive mode for custom tasks."""
    orchestrator = MultiAgentOrchestrator()
    
    print("\nAvailable workflows:")
    print("1. Sequential (Research -> Analysis -> Writing -> Critique)")
    print("2. Parallel (Multiple research tasks simultaneously)")
    print("3. Hierarchical (Supervisor reviews and approves)")
    
    choice = input("\nSelect workflow (1-3): ").strip()
    task = input("Enter your task: ").strip()
    
    if choice == "1":
        result = orchestrator.sequential_workflow(task)

        print("RESULT:")
        print(result["final_output"])
        
    elif choice == "2":
        num_subtasks = int(input("How many subtasks? "))
        subtasks = []
        for i in range(num_subtasks):
            subtask = input(f"Subtask {i+1}: ").strip()
            subtasks.append(subtask)
        
        result = orchestrator.parallel_workflow(task, subtasks)

        print("RESULT:")
        print(result["final_output"])
        
    elif choice == "3":
        result = orchestrator.hierarchical_workflow(task)

        print("RESULT:")    
        print(result["final_output"])
        
    else:
        print("Invalid choice")
        return
    
    print("EXECUTION HISTORY:")

    for entry in orchestrator.get_history():
        print(f"- {entry['agent']}: {entry['content_length']} chars")


def main():
    """Main entry point."""
    print(f"\n{settings.APP_NAME} v{settings.APP_VERSION}")
    print("Multi-Agent System with LangChain")
    
    while True:

        print("MENU")
    
        print("1. Demo: Sequential Workflow")
        print("2. Demo: Parallel Workflow")
        print("3. Demo: Hierarchical Workflow")
        print("4. Interactive Mode")
        print("5. Exit")
        
        choice = input("\nSelect option (1-5): ").strip()
        
        if choice == "1":
            demo_sequential()
        elif choice == "2":
            demo_parallel()
        elif choice == "3":
            demo_hierarchical()
        elif choice == "4":
            interactive_mode()
        elif choice == "5":
            print("\nExiting...")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
