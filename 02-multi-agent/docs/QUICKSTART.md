# Quick Start Guide

This guide will help you set up and run the multi-agent system in minutes.

## Prerequisites

- Python 3.13 or higher
- Azure OpenAI account with API access
- pip or uv package manager

## Installation Steps

### 1. Create Virtual Environment

```bash
# Navigate to project directory
cd 02-multi-agent

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

### 2. Install Dependencies

```bash
# Install package in editable mode
pip install -e .

# Or install with development dependencies
pip install -e ".[dev]"
```

### 3. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your credentials
# Use your favorite editor: notepad, nano, vim, etc.
notepad .env
```

Required settings in `.env`:

```env
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-actual-api-key
AZURE_OPENAI_API_VERSION=2024-08-01-preview
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4
LOG_LEVEL=INFO
```

### 4. Verify Installation

```bash
# Test configuration
python -c "from utils import validate_env; validate_env()"
```

If successful, you'll see: "Environment configuration validated successfully"

## Running the System

### Interactive Demo

```bash
python main.py
```

This launches an interactive menu with:
1. Sequential workflow demo
2. Parallel workflow demo
3. Hierarchical workflow demo
4. Custom interactive mode

### Advanced Examples

```bash
python examples.py
```

Choose from:
1. Multi-phase research pipeline
2. Iterative content improvement
3. Custom agent workflow
4. Batch task processing

### Quick Test

Test a simple workflow:

```python
from orchestrator import MultiAgentOrchestrator

orchestrator = MultiAgentOrchestrator()
result = orchestrator.sequential_workflow(
    "Explain the benefits of using type hints in Python"
)

print(result["article"])
```

## Common Tasks

### Run Tests

```bash
# Install dev dependencies first
pip install -e ".[dev]"

# Run all tests
pytest

# Run with coverage
pytest --cov=.

# Run specific test file
pytest test_agents.py -v
```

### Format Code

```bash
# Format with black
black .

# Lint with ruff
ruff check .
```

### Save Results

Results can be saved automatically:

```python
from utils import save_result

result = orchestrator.sequential_workflow("Your task")
save_result(result, "my_result.json")
```

## Troubleshooting

### Issue: ModuleNotFoundError

**Solution**: Ensure virtual environment is activated and dependencies installed

```bash
.venv\Scripts\activate
pip install -e .
```

### Issue: Authentication Error

**Solution**: Verify Azure OpenAI credentials in `.env`

```bash
# Check if .env exists
ls .env

# Verify credentials format
python -c "from settings import settings; print(settings.AZURE_OPENAI_ENDPOINT)"
```

### Issue: Empty Responses

**Solution**: Check deployment name matches your Azure resource

```python
from settings import settings
print(f"Using deployment: {settings.AZURE_OPENAI_DEPLOYMENT_NAME}")
```

### Issue: Rate Limiting

**Solution**: Add delays in parallel workflows or reduce concurrency

```python
import time
# Add delay between agent calls
time.sleep(1)
```

## Next Steps

1. **Customize Agents**: Modify agent prompts in [agents.py](agents.py)
2. **Add New Workflows**: Create custom workflows in [orchestrator.py](orchestrator.py)
3. **Extend Functionality**: Add new agent types or tools
4. **Production Use**: Implement error handling, retries, and monitoring

## Example Workflows

### Research Task

```python
orchestrator = MultiAgentOrchestrator()
result = orchestrator.parallel_workflow(
    "Compare database technologies",
    ["PostgreSQL features", "MongoDB features", "Redis features"]
)
print(result["final_output"])
```

### Content Creation

```python
result = orchestrator.hierarchical_workflow(
    "Write a blog post about async Python programming"
)
print(f"Approved: {result['approved']}")
print(result["final_output"])
```

### Analysis Pipeline

```python
result = orchestrator.sequential_workflow(
    "Analyze trends in cloud computing for 2025"
)
print("Research:", result["research"])
print("Analysis:", result["analysis"])
print("Article:", result["article"])
```

## Resources

- Full documentation: [README.md](README.md)
- Advanced examples: [examples.py](examples.py)
- Test suite: [test_agents.py](test_agents.py) and [test_orchestrator.py](test_orchestrator.py)
- LangChain docs: https://python.langchain.com/
- Azure OpenAI docs: https://learn.microsoft.com/azure/ai-services/openai/

## Getting Help

1. Check [README.md](README.md) for detailed documentation
2. Review [examples.py](examples.py) for usage patterns
3. Run tests to verify setup: `pytest -v`
4. Check Azure OpenAI quotas and limits

## Success Checklist

- [ ] Virtual environment created and activated
- [ ] Dependencies installed
- [ ] `.env` file configured with valid credentials
- [ ] Environment validation passed
- [ ] Demo workflows run successfully
- [ ] Tests pass (optional but recommended)

Congratulations! Your multi-agent system is ready to use.
