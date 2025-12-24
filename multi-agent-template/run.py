from src.orchestrator import MultiAgentOrchestrator
from utils import save_result


def quick_test():
    """Run a quick test of the system."""    
    # Create orchestrator
    orchestrator = MultiAgentOrchestrator()
    print("Agents ready: Research, Analysis, Writer, Critic")
    try:
        result = orchestrator.sequential_workflow(
            "Explain the concept of prompt engineering"
        )
        
        print("SUCCESS! Test completed.")
        print(f"\nArticle length: {len(result['article'])} characters")
        
        # Show excerpt
        print("ARTICLE EXCERPT:")
        print(result['article'][:500] + "...\n")
        
        # Save result
        save_result(result, "test_result.json")
        
        return True
        
    except Exception as e:
        print(f"\nError: {e}")
        print("\nPlease check:")
        print("1. Azure OpenAI credentials are correct")
        print("2. Deployment name matches your resource")
        print("3. You have sufficient API quota")
        return False


if __name__ == "__main__":
    success = quick_test()
    exit(0 if success else 1)
