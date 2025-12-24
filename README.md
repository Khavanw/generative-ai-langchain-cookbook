# Generative AI LangChain Cookbook

A comprehensive collection of production-ready templates for building AI agents and multi-agent systems using Azure OpenAI and LangChain. This repository provides progressive learning paths from basic chat implementations to complex multi-agent architectures.

## Overview

This repository contains five distinct templates, each designed to teach specific aspects of generative AI application development. The templates progress from foundational concepts to advanced multi-agent systems, enabling developers to build sophisticated AI solutions.

## Project Structure

```
generative-ai-langchain-cookbook/
├── PYTHON_STYLE_GUIDE.md          # Coding standards and best practices
├── README.md                       # This file
├── 01-simple-agent/                # Single agent with comprehensive examples
├── 02-multi-agent/                 # Multi-agent collaboration system
├── 03-agentic-patterns/            # Advanced agentic patterns (planned)
├── 04-agent-to-agent/              # Agent-to-agent communication (planned)
└── 05-mcp-server/                  # Model Context Protocol server (planned)
```

## Templates

### 01. Simple Agent

A comprehensive learning resource for building single AI agents with Azure OpenAI and LangChain. This template includes 10 progressive examples covering fundamental to advanced concepts.

**Key Features:**
- Basic chat completion with Azure OpenAI
- Function calling (manual OpenAI SDK approach)
- Tool calling (automated LangChain approach)
- Complete single agent with memory and multiple tools
- Retrieval-Augmented Generation (RAG) with in-memory vector store
- Conversation history management
- Prompt template patterns and composition
- Structured output parsing with Pydantic
- LangChain Expression Language (LCEL) chains
- Token streaming for real-time responses

**What You'll Build:**
- Simple chatbots with various capabilities
- Agents with custom tools (weather, calculator, knowledge search)
- RAG systems for document-based question answering
- Conversational agents with short-term memory
- Production-ready applications with structured outputs

**Learning Path:**
1. Start with basic chat to understand Azure OpenAI integration
2. Learn function and tool calling for extending agent capabilities
3. Build complete agents with memory and multiple tools
4. Implement RAG for knowledge-grounded responses
5. Master advanced patterns: templates, parsers, chains, streaming

**Technology Stack:**
- Azure OpenAI for LLM capabilities
- LangChain for orchestration and tools
- Pydantic for structured data validation
- In-memory vector stores for RAG

**Ideal For:**
- Developers new to LLM application development
- Learning foundational AI agent patterns
- Understanding LangChain framework
- Building single-purpose AI assistants
- Prototyping AI features quickly

Refer to the template's README for detailed setup instructions and example descriptions.

---

### 02. Multi-Agent

A sophisticated multi-agent system demonstrating how specialized agents collaborate to complete complex tasks. Features three workflow patterns: sequential, parallel, and hierarchical.

**Key Features:**
- Four specialized agent types (Research, Analysis, Writer, Critic)
- Sequential workflow for step-by-step processing
- Parallel workflow for concurrent task execution
- Hierarchical workflow with supervisor approval
- Execution history tracking
- Interactive CLI and menu interfaces
- Comprehensive metrics and monitoring

**Specialized Agents:**

**ResearchAgent:**
- Gathers and analyzes information from various sources
- Identifies key facts and relevant data
- Produces structured research summaries

**AnalysisAgent:**
- Evaluates data and identifies patterns
- Provides critical insights and assessments
- Synthesizes information from multiple sources

**WriterAgent:**
- Creates high-quality content based on research and analysis
- Adapts tone and style for different audiences
- Structures information logically and clearly

**CriticAgent:**
- Reviews work quality and provides feedback
- Checks for consistency and accuracy
- Suggests improvements and refinements

**Workflow Patterns:**

**Sequential Workflow:**
Linear processing where each agent builds on previous results. Best for tasks requiring progressive refinement.

Flow: Research → Analysis → Writing → Critique

**Parallel Workflow:**
Multiple agents work simultaneously on different subtasks. Efficient for divisible tasks that can be processed independently.

Flow: Multiple Research agents → Aggregate → Analysis → Report

**Hierarchical Workflow:**
A supervisor agent reviews and approves work, enabling iterative improvement cycles.

Flow: Research → Write → Supervisor Review → (Iterate if needed) → Approved Output

**What You'll Build:**
- Multi-agent research and analysis pipelines
- Collaborative content creation systems
- Quality-controlled document generation
- Complex task orchestration systems
- Batch processing workflows

**Technology Stack:**
- LangChain for agent framework
- LangGraph for workflow coordination
- Azure OpenAI for agent intelligence
- Pydantic for configuration management

**Ideal For:**
- Building complex AI systems requiring specialization
- Tasks needing multiple perspectives or steps
- Quality-controlled content generation
- Research and analysis workflows
- Production systems with review processes

Refer to the template's README and docs/ folder for architecture details, quickstart guide, and workflow documentation.

---

### 03. Agentic Patterns

Advanced agentic patterns and architectures (in development).

This template will explore cutting-edge agentic AI patterns including:
- Planning and reasoning agents
- Self-improvement mechanisms
- Dynamic tool selection and creation
- Meta-learning capabilities
- Advanced memory architectures

**Status:** Planned for future development

---

### 04. Agent-to-Agent

Agent-to-agent communication patterns (in development).

This template will demonstrate:
- Inter-agent messaging protocols
- Distributed agent networks
- Collaborative problem-solving
- Negotiation and consensus mechanisms
- Scalable agent architectures

**Status:** Planned for future development

---

### 05. MCP Server

Model Context Protocol server implementation (in development).

This template will provide:
- MCP server architecture
- Context management strategies
- Protocol implementations
- Integration patterns
- Best practices for MCP servers

**Status:** Planned for future development

---

## Technology Stack

**Core Technologies:**
- **Python 3.13+**: Modern Python features and performance
- **Azure OpenAI**: Enterprise-grade LLM services
- **LangChain**: Framework for LLM application development
- **LangGraph**: Multi-agent workflow orchestration
- **Pydantic**: Data validation and settings management

**Key Libraries:**
- **langchain-openai**: Azure OpenAI integration
- **langchain-community**: Additional integrations and tools
- **python-dotenv**: Environment configuration
- **typing**: Type hints for code clarity

## Prerequisites

- Python 3.13 or higher
- Azure OpenAI account with API access
- Basic understanding of Python programming
- Familiarity with async/await patterns (for advanced templates)
- UV package manager (recommended) or pip

## Getting Started

### 1. Choose Your Starting Point

**New to AI Agents?**
Start with `01-simple-agent/` to learn foundational concepts.

**Building Multi-Agent Systems?**
Explore `02-multi-agent/` for collaboration patterns.

**Advanced Architectures?**
Check back for upcoming agentic patterns and A2A communication templates.

### 2. Set Up Your Environment

Each template contains detailed setup instructions in its README file. Generally, you'll need to:

1. Navigate to the template directory
2. Install dependencies using UV or pip
3. Configure environment variables with your Azure OpenAI credentials
4. Run the examples or demos

### 3. Follow the Learning Path

Templates are designed for progressive learning:

```
01. Simple Agent (Foundations)
    ↓
02. Multi-Agent (Collaboration)
    ↓
03. Agentic Patterns (Advanced Patterns)
    ↓
04. Agent-to-Agent (Distributed Systems)
    ↓
05. MCP Server (Protocol Implementation)
```

## Common Patterns

### Azure OpenAI Configuration

All templates use consistent environment configuration:

```env
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_API_VERSION=2024-08-01-preview
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4
LOG_LEVEL=INFO
```

### Project Structure

Each template follows a consistent structure:
- `README.md`: Comprehensive documentation
- `pyproject.toml`: Dependency management
- `.env.example`: Environment template
- `examples/`: Runnable code examples
- `src/` or main modules: Core implementation

## Best Practices

### Code Quality
Follow the `PYTHON_STYLE_GUIDE.md` for consistent coding standards:
- Use type hints for complex functions
- Write clear docstrings with examples
- Keep code clean and self-documenting
- Avoid emojis and visual clutter

### Configuration Management
- Never commit API keys or secrets
- Use environment variables for configuration
- Provide `.env.example` files as templates
- Validate configuration at startup

### Error Handling
- Implement proper error handling for API calls
- Provide informative error messages
- Log errors appropriately
- Handle rate limits gracefully

### Testing
- Test with small examples first
- Monitor token usage and costs
- Validate outputs for quality
- Use development deployments for experimentation

## Use Cases

### 01. Simple Agent
- Customer support chatbots
- Document Q&A systems
- Personal assistants
- Content generation tools
- Data extraction applications

### 02. Multi-Agent
- Research and analysis pipelines
- Collaborative content creation
- Complex report generation
- Quality-controlled workflows
- Multi-perspective problem solving

### Future Templates
- Planning and reasoning systems
- Distributed AI networks
- Protocol-based integrations
- Advanced agentic behaviors

## Resources

### Documentation
- [Azure OpenAI Documentation](https://learn.microsoft.com/en-us/azure/ai-services/openai/)
- [LangChain Documentation](https://python.langchain.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

### Learning Resources
- Each template's README contains detailed explanations
- Examples include inline comments and documentation
- QUICKSTART guides for rapid onboarding
- STRUCTURE documentation for architecture understanding

## Contributing

When contributing to this repository:
1. Follow the Python Style Guide
2. Include comprehensive documentation
3. Provide runnable examples
4. Test with Azure OpenAI
5. Update relevant README files

## Troubleshooting

### API Connection Issues
- Verify Azure OpenAI credentials in `.env`
- Check endpoint URL format
- Ensure API key is active
- Confirm deployment names match your Azure resource

### Dependency Issues
- Use Python 3.13 or higher
- Run `uv sync` or `pip install -e .`
- Check for conflicting package versions
- Create a fresh virtual environment if needed

### Performance Issues
- Monitor API rate limits
- Use streaming for long responses
- Implement caching for repeated queries
- Consider parallel processing for independent tasks

## License

MIT License - Use these templates freely for learning and production projects.

## Support

Each template contains specific documentation and troubleshooting guides. For general questions:
- Review the template-specific README files
- Check the PYTHON_STYLE_GUIDE for coding standards
- Examine the examples for implementation patterns
- Refer to official documentation for underlying technologies

## Roadmap

**Current Status:**
- 01-simple-agent: Complete with 10 examples
- 02-multi-agent: Complete with 3 workflow patterns

**In Development:**
- 03-agentic-patterns: Advanced reasoning and planning patterns
- 04-agent-to-agent: Agent-to-agent communication protocols
- 05-mcp-server: Model Context Protocol implementation

**Future Enhancements:**
- Additional workflow patterns
- More specialized agent types
- Performance optimization examples
- Production deployment guides
- Testing and monitoring frameworks

---

Built for developers learning and building production-grade generative AI applications with Azure OpenAI and LangChain.