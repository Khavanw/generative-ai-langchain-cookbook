# Multi-Agent System - File Structure

## Overview

Complete multi-agent system with LangChain featuring specialized agents, multiple workflow patterns, and comprehensive tooling.

## Core Files

### `agents.py`
Defines all agent types and their behaviors.

**Classes:**
- `BaseAgent`: Foundation for all agents with LLM integration
- `ResearchAgent`: Specialized in information gathering
- `AnalysisAgent`: Expert in data analysis and evaluation
- `WriterAgent`: Content creation specialist
- `CriticAgent`: Quality assurance and review

**Key Features:**
- Azure OpenAI integration
- Context-aware processing
- Standardized response format (AgentResponse)

### `orchestrator.py`
Manages multi-agent workflows and coordination.

**Class:**
- `MultiAgentOrchestrator`: Coordinates agent interactions

**Workflows:**
- `sequential_workflow()`: Linear processing pipeline
- `parallel_workflow()`: Concurrent task execution
- `hierarchical_workflow()`: Supervisor-based approval

**Features:**
- Execution history tracking
- Context passing between agents
- Workflow metrics

### `main.py`
Interactive entry point with demo workflows.

**Functions:**
- `demo_sequential()`: Sequential workflow demonstration
- `demo_parallel()`: Parallel workflow demonstration
- `demo_hierarchical()`: Hierarchical workflow demonstration
- `interactive_mode()`: Custom task interface
- `main()`: Menu-driven interface

### `settings.py`
Configuration management using Pydantic.

**Class:**
- `Settings`: Environment-based configuration

**Configuration:**
- Azure OpenAI credentials
- API versioning
- Logging levels
- Application metadata

## Utility Files

### `utils.py`
Helper functions and utilities.

**Classes:**
- `MetricsTracker`: Workflow execution metrics
- `WorkflowMetrics`: Metrics data structure

**Functions:**
- `format_response()`: Text formatting for display
- `save_result()`: Save workflow results to JSON
- `load_result()`: Load workflow results from file
- `validate_env()`: Environment validation

### `cli.py`
Command-line interface for workflows.

**Commands:**
- `sequential`: Run sequential workflow
- `parallel`: Run parallel workflow
- `hierarchical`: Run hierarchical workflow
- `validate`: Validate environment

**Usage:**
```bash
python cli.py sequential "Your task"
python cli.py parallel "Main task" --subtasks "Task 1" "Task 2"
python cli.py hierarchical "Your task" --output result.json
```

## Example Files

### `examples.py`
Advanced usage examples and patterns.

**Functions:**
- `example_research_pipeline()`: Multi-phase research
- `example_iterative_improvement()`: Iterative refinement
- `example_custom_agent_workflow()`: Custom agent sequences
- `example_batch_processing()`: Batch task processing

## Test Files

### `test_agents.py`
Unit tests for agent functionality.

**Test Classes:**
- `TestBaseAgent`: Base agent functionality
- `TestSpecializedAgents`: Specialized agent types
- `TestAgentResponse`: Response data structure

### `test_orchestrator.py`
Unit tests for orchestrator.

**Test Classes:**
- `TestMultiAgentOrchestrator`: Orchestrator functionality
- `TestWorkflowType`: Workflow type enum

**Run Tests:**
```bash
pytest
pytest --cov=.
pytest -v
```

## Configuration Files

### `pyproject.toml`
Python project configuration.

**Sections:**
- Project metadata
- Dependencies (LangChain, OpenAI, etc.)
- Optional dev dependencies (pytest, black, ruff)

**Install:**
```bash
pip install -e .
pip install -e ".[dev]"
```

### `.env.example`
Environment variable template.

**Required Variables:**
- `AZURE_OPENAI_ENDPOINT`
- `AZURE_OPENAI_API_KEY`
- `AZURE_OPENAI_API_VERSION`
- `AZURE_OPENAI_DEPLOYMENT_NAME`
- `LOG_LEVEL`

### `.gitignore`
Git ignore patterns for Python projects.

**Ignores:**
- Virtual environments (.venv, venv)
- Python cache (__pycache__, *.pyc)
- Environment files (.env)
- IDE files (.vscode, .idea)
- Build artifacts

## Documentation Files

### `README.md`
Comprehensive project documentation.

**Sections:**
- Overview and architecture
- Installation instructions
- Usage examples
- Feature descriptions
- Extending the system
- Best practices
- Troubleshooting

### `QUICKSTART.md`
Quick setup guide for new users.

**Sections:**
- Prerequisites
- Installation steps
- Configuration
- Running the system
- Common tasks
- Troubleshooting
- Next steps

### `STRUCTURE.md` (this file)
Project structure documentation.

## Directory Structure

```
multi-agent-template/
├── agents.py              # Agent definitions
├── orchestrator.py        # Workflow orchestration
├── main.py               # Interactive entry point
├── settings.py           # Configuration
├── utils.py              # Utility functions
├── cli.py                # Command-line interface
├── examples.py           # Advanced examples
├── test_agents.py        # Agent tests
├── test_orchestrator.py  # Orchestrator tests
├── pyproject.toml        # Project config
├── .env.example          # Environment template
├── .env                  # Environment config (not in git)
├── .gitignore           # Git ignore rules
├── .python-version      # Python version
├── README.md            # Main documentation
├── QUICKSTART.md        # Quick start guide
├── STRUCTURE.md         # This file
└── outputs/             # Output directory (created on first use)
    └── *.json           # Saved workflow results
```

## Workflow Patterns

### Sequential Workflow
```
User Task → ResearchAgent → AnalysisAgent → WriterAgent → CriticAgent → Result
```

### Parallel Workflow
```
Main Task → [ResearchAgent 1, ResearchAgent 2, ..., ResearchAgent N]
         → Aggregate → AnalysisAgent → WriterAgent → Result
```

### Hierarchical Workflow
```
Task → ResearchAgent → WriterAgent → CriticAgent (Supervisor)
                                    ↓ if not approved
                                    Iterate with feedback
```

## Agent Communication

Agents communicate through:
1. **Direct invocation**: Orchestrator calls agent.process()
2. **Context passing**: Results from previous agents passed as context
3. **Response format**: Standardized AgentResponse objects
4. **History tracking**: All interactions logged in orchestrator.history

## Extension Points

### Add New Agent Type
1. Create class inheriting from `BaseAgent`
2. Define specialized system prompt
3. Register in orchestrator
4. Add to workflow methods

### Add New Workflow
1. Define method in `MultiAgentOrchestrator`
2. Implement agent coordination logic
3. Add to main.py menu
4. Document in README.md

### Custom Tools
1. Extend BaseAgent with tool methods
2. Integrate with LangChain tools
3. Update agent prompts to use tools
4. Add tool documentation

## Development Workflow

1. **Setup**: Follow QUICKSTART.md
2. **Development**: Modify agents.py or orchestrator.py
3. **Testing**: Run pytest to verify changes
4. **Formatting**: Use black for code formatting
5. **Linting**: Use ruff for code quality
6. **Documentation**: Update README.md for new features

## Best Practices

1. **Follow Style Guide**: See PYTHON_STYLE_GUIDE.md in project root
2. **Type Hints**: Use for public APIs and complex functions
3. **Documentation**: Add docstrings to all public functions
4. **Testing**: Write tests for new functionality
5. **Error Handling**: Use specific exceptions with clear messages
6. **Logging**: Use Python logging module, not print statements
7. **Configuration**: Use settings.py for all config
8. **Output**: Avoid emojis and decorative characters

## Dependencies

**Core:**
- langchain: LLM orchestration
- langchain-openai: Azure OpenAI integration
- langgraph: Multi-agent graphs
- pydantic: Data validation
- openai: OpenAI API client

**Development:**
- pytest: Testing framework
- black: Code formatting
- ruff: Linting
- pytest-cov: Coverage reporting

## Performance Considerations

1. **Parallel workflows**: Use for independent tasks
2. **Token usage**: Monitor context size in sequential workflows
3. **API limits**: Be mindful of rate limits
4. **Caching**: Consider caching research results
5. **Timeouts**: Implement timeouts for long-running tasks

## Security Notes

1. **API Keys**: Never commit .env file
2. **Credentials**: Use environment variables
3. **Input validation**: Validate user inputs
4. **Output sanitization**: Clean outputs before saving
5. **Access control**: Implement if deploying as service

## Future Enhancements

Potential additions:
- Web interface with Gradio/Streamlit
- Database integration for history
- Advanced tool integration (web search, APIs)
- Multi-LLM support (GPT-4, Claude, etc.)
- Async execution for better performance
- Monitoring and observability
- Production deployment guides
