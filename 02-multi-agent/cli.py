"""
Command-line interface for running multi-agent workflows.

Usage:
    python cli.py sequential "Your task here"
    python cli.py parallel "Main task" --subtasks "Task 1" "Task 2" "Task 3"
    python cli.py hierarchical "Your task here"
    python cli.py validate
"""
import sys
import argparse
from src.orchestrator import MultiAgentOrchestrator
from utils import save_result, format_response


def run_sequential(args):
    """Run sequential workflow."""
    orchestrator = MultiAgentOrchestrator()
    result = orchestrator.sequential_workflow(args.task)
    print("FINAL ARTICLE:")
    print(format_response(result["article"]))
    
    if args.output:
        save_result(result, args.output)
    
    return 0


def run_parallel(args):
    """Run parallel workflow."""
    
    if not args.subtasks or len(args.subtasks) < 2:
        print("Error: Parallel workflow requires at least 2 subtasks")
        print("Usage: python cli.py parallel 'Main task' --subtasks 'Task 1' 'Task 2'")
        return 1
    
    print(f"\nRunning Parallel Workflow")
    print(f"Task: {args.task}")
    print(f"Subtasks: {len(args.subtasks)}")
    
    orchestrator = MultiAgentOrchestrator()
    result = orchestrator.parallel_workflow(args.task, args.subtasks)
    
    print("FINAL REPORT:")
    print(format_response(result["final_output"]))
    
    if args.output:
        save_result(result, args.output)
    
    return 0


def run_hierarchical(args):
    """Run hierarchical workflow."""
    print(f"\nRunning Hierarchical Workflow")
    print(f"Task: {args.task}")
    
    orchestrator = MultiAgentOrchestrator()
    result = orchestrator.hierarchical_workflow(args.task)
    
    print("FINAL OUTPUT:")
    print(format_response(result["final_output"]))
    
    print("WORKFLOW INFO:")
    print(f"Approved: {result['approved']}")
    print(f"Iterations: {result['iterations']}")
    
    if args.output:
        save_result(result, args.output)
    
    return 0



def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Multi-Agent System CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli.py sequential "Explain microservices"
  python cli.py parallel "Cloud comparison" --subtasks "AWS" "Azure" "GCP"
  python cli.py hierarchical "Python best practices" --output result.json
  python cli.py validate
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Sequential workflow
    sequential_parser = subparsers.add_parser(
        "sequential",
        help="Run sequential workflow (Research -> Analysis -> Writing -> Critique)"
    )
    sequential_parser.add_argument("task", help="Task description")
    sequential_parser.add_argument("--output", "-o", help="Output file path")
    
    # Parallel workflow
    parallel_parser = subparsers.add_parser(
        "parallel",
        help="Run parallel workflow (Multiple research tasks)"
    )
    parallel_parser.add_argument("task", help="Main task description")
    parallel_parser.add_argument(
        "--subtasks",
        nargs="+",
        required=True,
        help="Subtasks to process in parallel"
    )
    parallel_parser.add_argument("--output", "-o", help="Output file path")
    
    # Hierarchical workflow
    hierarchical_parser = subparsers.add_parser(
        "hierarchical",
        help="Run hierarchical workflow (Supervisor approves output)"
    )
    hierarchical_parser.add_argument("task", help="Task description")
    hierarchical_parser.add_argument("--output", "-o", help="Output file path")
    
    
    if len(sys.argv) == 1:
        parser.print_help()
        return 1
    
    args = parser.parse_args()
    
    if args.command == "sequential":
        return run_sequential(args)
    elif args.command == "parallel":
        return run_parallel(args)
    elif args.command == "hierarchical":
        return run_hierarchical(args)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
