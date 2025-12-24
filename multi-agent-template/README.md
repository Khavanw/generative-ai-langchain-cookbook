# Multi-Agent Template

A comprehensive multi-agent system built with LangChain, featuring specialized agents that collaborate to complete complex tasks.

## Overview

This template demonstrates three types of multi-agent workflows:

1. **Sequential Workflow**: Agents work in sequence, each building on previous results
2. **Parallel Workflow**: Multiple agents work simultaneously on different subtasks
3. **Hierarchical Workflow**: A supervisor agent reviews and approves work

## Architecture

### Specialized Agents

- **ResearchAgent**: Gathers and analyzes information
- **AnalysisAgent**: Evaluates and identifies patterns in data
- **WriterAgent**: Creates high-quality content
- **CriticAgent**: Reviews work and provides feedback

### Orchestrator

The `MultiAgentOrchestrator` coordinates agent interactions and manages workflows.

## Installation

1. Create a virtual environment:
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
```

2. Install dependencies:
```bash
pip install -e .
```

3. Configure environment:
```bash
cp .env.example .env
# Edit .env with your Azure OpenAI credentials
```

## Configuration

Required environment variables in `.env`:

```env
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_API_VERSION=2024-08-01-preview
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4
LOG_LEVEL=INFO
```

## Usage

### Run Demo

```bash
python main.py
```

The interactive menu provides:
- Demo workflows (sequential, parallel, hierarchical)
- Interactive mode for custom tasks
- Execution history tracking

### Sequential Workflow Example

```python
from orchestrator import MultiAgentOrchestrator

orchestrator = MultiAgentOrchestrator()

result = orchestrator.sequential_workflow(
    "Explain the benefits of microservices architecture"
)

print(result["article"])
print(result["critique"])
```

**Flow:**
1. ResearchAgent researches the topic
2. AnalysisAgent analyzes findings
3. WriterAgent creates article
4. CriticAgent reviews quality

### Parallel Workflow Example

```python
result = orchestrator.parallel_workflow(
    "Compare cloud service providers",
    subtasks=[
        "Research AWS services and pricing",
        "Research Azure services and pricing",
        "Research Google Cloud services and pricing"
    ]
)

print(result["final_output"])
```

**Flow:**
1. Multiple ResearchAgents work on subtasks simultaneously
2. Results are aggregated
3. AnalysisAgent analyzes combined research
4. WriterAgent creates comprehensive report

### Hierarchical Workflow Example

```python
result = orchestrator.hierarchical_workflow(
    "Write a guide on Python best practices"
)

print(f"Approved: {result['approved']}")
print(f"Iterations: {result['iterations']}")
print(result["final_output"])
```

**Flow:**
1. ResearchAgent researches topic
2. WriterAgent creates content
3. CriticAgent (supervisor) reviews
4. If not approved, iterate with feedback
5. Maximum 2 iterations

## Project Structure

```
multi-agent-template/
├── main.py              # Entry point with demos
├── orchestrator.py      # Workflow orchestration
├── agents.py            # Specialized agent definitions
├── settings.py          # Configuration management
├── .env.example         # Environment template
├── pyproject.toml       # Dependencies
└── README.md           # Documentation
```

## Features

### Agent Capabilities

**BaseAgent**
- Azure OpenAI integration
- Context-aware processing
- Standardized response format

**ResearchAgent**
- Information gathering
- Fact identification
- Structured summaries

**AnalysisAgent**
- Pattern recognition
- Critical evaluation
- Data-driven insights

**WriterAgent**
- Content creation
- Logical organization
- Audience adaptation

**CriticAgent**
- Quality assurance
- Consistency checking
- Improvement suggestions

### Workflow Types

**Sequential**
- Linear processing
- Each agent builds on previous work
- Suitable for tasks requiring progressive refinement

**Parallel**
- Concurrent execution
- Independent subtask processing
- Efficient for divisible tasks

**Hierarchical**
- Supervisor oversight
- Iterative improvement
- Quality control through review cycles

## Extending the System

### Add New Agent

```python
from agents import BaseAgent

class DataAgent(BaseAgent):
    def __init__(self):
        system_prompt = """You are a Data Agent specialized in data processing."""
        super().__init__("DataAgent", system_prompt)
```

### Custom Workflow

```python
def custom_workflow(self, task: str) -> Dict[str, Any]:
    # Research phase
    research = self.research_agent.process(task)
    
    # Custom processing
    data = self.data_agent.process(
        "Process this data",
        context={"research": research.content}
    )
    
    return {"result": data.content}
```

## Response Format

All agents return `AgentResponse` objects:

```python
@dataclass
class AgentResponse:
    agent_name: str        # Agent identifier
    content: str          # Response content
    metadata: Dict        # Additional info (model, etc.)
```

## Execution History

Track agent interactions:

```python
history = orchestrator.get_history()
for entry in history:
    print(f"{entry['agent']}: {entry['content_length']} chars")
```

## Best Practices

1. **Clear Task Definition**: Provide specific, well-defined tasks
2. **Context Management**: Pass relevant context between agents
3. **Error Handling**: Monitor agent responses for issues
4. **Resource Management**: Be mindful of API usage in parallel workflows
5. **Iteration Limits**: Set reasonable limits for hierarchical workflows

## Examples

### Research and Report

```python
# Parallel research, comprehensive report
result = orchestrator.parallel_workflow(
    "AI trends in 2025",
    ["Machine learning advances", "LLM developments", "AI ethics"]
)
```

### Quality-Controlled Writing

```python
# Hierarchical with supervisor approval
result = orchestrator.hierarchical_workflow(
    "Technical documentation for API"
)
```

### Analysis Pipeline

```python
# Sequential processing pipeline
result = orchestrator.sequential_workflow(
    "Market analysis for product launch"
)
```

## Troubleshooting

**Issue**: Agent responses are empty
- Check Azure OpenAI credentials
- Verify deployment name matches your resource

**Issue**: Slow parallel execution
- Adjust number of parallel tasks
- Consider API rate limits

**Issue**: Hierarchical workflow not approving
- Review CriticAgent prompt
- Adjust approval criteria
- Increase max iterations

## Dependencies

- **langchain**: LLM orchestration framework
- **langchain-openai**: Azure OpenAI integration
- **langgraph**: Multi-agent workflow graphs
- **pydantic**: Settings and data validation
- **python-dotenv**: Environment configuration

## License

MIT License - See project root for details

## Contributing

Follow the Python Style Guide in the root directory when contributing.

## Support

For issues or questions, refer to the main project documentation.
