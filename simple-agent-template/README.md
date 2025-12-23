# Single Agent Template with Azure OpenAI

A comprehensive template for building AI agents using Azure OpenAI with different approaches: basic chat, function calling, tool calling, and RAG.

## Project Structure

```
single-agent-template/
├── examples/
│   ├── 01_basic_chat.py           # Simple chat completion example
│   ├── 02_function_calling.py     # OpenAI function calling (manual)
│   ├── 03_tool_calling.py         # LangChain tool calling (automated)
│   ├── 04_single_agent.py         # Complete single agent with memory
│   ├── 05_rag_basic.py            # RAG with in-memory vector store
│   ├── 06_short_term_memory.py    # Conversation history management
│   ├── 07_prompt_templates.py     # Prompt template patterns
│   ├── 08_output_parsers.py       # Structured output parsing
│   ├── 09_lcel_chains.py          # LangChain Expression Language chains
│   └── 10_streaming.py            # Token streaming responses
├── settings.py                     # Configuration management
├── pyproject.toml                  # Project dependencies
├── .env                           # Environment variables (create from .env.example)
└── README.md                      # This file
```

## Prerequisites

- Python 3.13 or higher
- Azure OpenAI account with API key and deployments
- UV package manager (recommended) or pip

## Setup Instructions

### 1. Install UV Package Manager (if not installed)

```bash
# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Configure Environment Variables

Create a `.env` file in the project root:

```env
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_API_VERSION=2024-08-01-preview
AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment-name
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-ada-002
LOG_LEVEL=INFO
```

### 3. Install Dependencies

```bash
# Using UV (recommended)
uv sync

# Or using pip
pip install -e .
```

## Examples Overview

### 01. Basic Chat

Simple Azure OpenAI chat completion without any tools or functions.

**Run:** `uv run examples/01_basic_chat.py`

**Features:**
- Basic chat completion
- Simple request/response pattern
- Good for understanding Azure OpenAI basics

---

### 02. Function Calling

OpenAI function calling with manual handling using pure OpenAI SDK.

**Run:** `uv run examples/02_function_calling.py`

**Features:**
- Manual function schema definition
- Two-step API call process
- Direct control over function execution
- Interactive terminal input

**Available Functions:**
- `get_weather(location)` - Get weather information
- `calculate_sum(a, b)` - Calculate sum of two numbers
- `get_current_time(timezone)` - Get current time

---

### 03. Tool Calling

LangChain tool calling with automated agent workflow using LangChain v1.0.

**Run:** `uv run examples/03_tool_calling.py`

**Features:**
- Automatic tool schema generation
- Agent-based execution with `create_agent`
- Single invoke handles entire workflow
- Tool call tracking and display

---

### 04. Single Agent

Complete single agent implementation with conversation memory and multiple tools.

**Run:** `uv run examples/04_single_agent.py`

**Features:**
- Conversation history tracking
- Multiple specialized tools (5 tools)
- Class-based architecture
- Command system (history, clear, tools)
- Rich response formatting

**Available Tools:**
- `get_weather(location)` - Get weather with mock data
- `calculate(expression)` - Safe mathematical calculations
- `get_current_time(timezone)` - Get current time
- `search_knowledge(query)` - Search knowledge base
- `create_reminder(task, time)` - Create reminders

**Special Commands:**
- `history` - View conversation history
- `clear` - Clear conversation memory
- `tools` - List all available tools

---

### 05. RAG Basic

Retrieval-Augmented Generation implementation using in-memory vector store.

**Run:** `uv run examples/05_rag_basic.py`

**Features:**
- In-memory vector store (no external database needed)
- Azure OpenAI embeddings
- Document chunking with RecursiveCharacterTextSplitter
- Similarity search for relevant context
- RAG tool integration with agent
- Sample document loading

**Commands:**
- `load` - Load 5 sample documents about AI/ML topics
- `add` - Manually add a document to knowledge base
- `stats` - View knowledge base statistics

**Example queries (after loading):**
- "What is LangChain?"
- "Explain how RAG works"
- "Tell me about Azure OpenAI"
- "What are vector databases?"

**How it works:**
1. Documents are split into chunks
2. Chunks are converted to embeddings
3. Embeddings stored in InMemoryVectorStore
4. User queries trigger similarity search
5. Relevant chunks retrieved and used as context
6. LLM generates response based on retrieved context

**Note:** Requires Azure OpenAI embedding deployment

---

### 06. Short-Term Memory Short Memory |
|--------|-----------|-----------------|--------------|--------------|-----------|--------------|
| **Framework** | OpenAI SDK | OpenAI SDK | LangChain | LangChain | LangChain | LangChain |
| **Tools** | None | Manual | Automated | Multiple | RAG tool | None |
| **Memory** | None | None | None | Built-in | None | Conversation |
| **Knowledge** | None | None | None | None | Vector store | None |
| **Context** | Single turn | Single turn | Single turn | Multi-turn | Document-based | Conversation |
| **Complexity** | Simplest | Medium | Medium | High | High | Medium |
| **Best For** | Testing | Fine control | Automation | Real apps | Doc Q&A | Chatbots
- Configurable max messages limit
- Automatic history trimming when limit exceeded
- Message timestamp tracking
- Conversation statistics and summary
- Export conversation to file

**Commands:**
- `history [n]` - Show last n messages (default: all)
- `summary` - Show conversation statistics
- `clear` - Clear conversation history
- `export` - Export conversation to text file

**Example interactions:**
```
You: My name is John
Assistant: Nice to meet you, John! How can I help you today?

You: What's my name?
Assistant: Your name is John, as you just told me.

You: Tell me about Python
Assistant: [explains Python...]

You: summary
--- Shows conversation stats ---
```

**Key Concepts:**
- **Short-term memory**: Conversation history within current session
- **Context window**: Limited number of messages kept in memory
- **Automatic trimming**: Oldest messages removed when limit reached
- **Token estimation**: Track approximate token usage

**Use Cases:**
- Conversational chatbots
- Customer support bots
- Interactive assistants
- Tutorial/teaching bots
- Any application needing conversation context

---

### 07. Prompt Templates

Various prompt template patterns and composition techniques in LangChain.

**Run:** `uv run examples/07_prompt_templates.py`

**Features:**
- Basic string templates with variables
- Chat prompt templates (system + user messages)
- Few-shot learning templates
- Partial variables (pre-filled values)
- Template composition
- Message placeholders for history

**Examples Included:**
1. **Basic Template** - Simple string template with input variables
2. **Chat Template** - Structured system and user messages
3. **Few-Shot Template** - Learning from examples (antonyms)
4. **Partial Variables** - Pre-fill values like current date
5. **Template Composition** - Combine multiple templates
6. **Message Placeholder** - Include conversation history

**Key Concepts:**
- **Input variables**: Dynamic values in templates
- **Format instructions**: Guide LLM output format
- **Few-shot learning**: Teach patterns through examples
- **Partial variables**: Pre-computed or static values
- **Message roles**: System, user, assistant messages

**Why Templates Matter:**
- Consistency across prompts
- Reusable prompt structures
- Easy experimentation with prompt engineering
- Type-safe input validation
- Dynamic prompt composition

---

### 08. Output Parsers

Structured output parsing to extract typed data from LLM responses.

**Run:** `uv run examples/08_output_parsers.py`

**Features:**
- JSON parsing with Pydantic models
- Comma-separated list parsing
- String output parsing
- Error handling for invalid outputs
- Multiple schema examples (Person, BookReview, Recipe)

**Examples Included:**
1. **JSON Parser** - Parse structured person data
2. **List Parser** - Extract comma-separated lists
3. **Book Review Parser** - Complex nested structure
4. **Recipe Parser** - Multi-field structured data
5. **String Parser** - Simple text extraction
6. **Error Handling** - Handle parsing failures gracefully

**Sample Schemas:**
- **Person**: name, age, occupation, hobbies
- **BookReview**: title, author, rating, pros/cons
- **Recipe**: ingredients, instructions, timing

**Key Concepts:**
- **Pydantic models**: Type-safe data structures
- **Format instructions**: Tell LLM expected output format
- **Validation**: Automatic type checking
- **Error recovery**: Handle malformed responses

**Use Cases:**
- Extract structured data from text
- Build type-safe applications
- Create consistent API responses
- Validate LLM outputs
- Generate reports and summaries

---

### 09. LCEL Chains

LangChain Expression Language for composing complex chains.

**Run:** `uv run examples/09_lcel_chains.py`

**Features:**
- Simple sequential chains (pipe operator |)
- Parallel execution with RunnableParallel
- Data passthrough with RunnablePassthrough
- Field extraction with itemgetter
- Custom transformations with RunnableLambda
- Complex multi-step workflows

**Examples Included:**
1. **Simple Chain** - prompt | llm | parser pattern
2. **Sequential Chain** - Multi-step processing
3. **Parallel Chain** - Execute multiple chains simultaneously
4. **Passthrough Chain** - Pass data while adding derived values
5. **ItemGetter Chain** - Extract specific fields from dict
6. **Lambda Transform** - Custom transformation functions
7. **Structured Output** - Parse complex analysis results
8. **Complex Chain** - Combine multiple patterns

**Key Concepts:**
- **Pipe operator (|)**: Chain components sequentially
- **RunnableParallel**: Execute chains in parallel
- **RunnablePassthrough**: Pass input through unchanged
- **itemgetter**: Extract dictionary fields
- **RunnableLambda**: Custom Python functions in chains

**Chain Patterns:**
- Sequential: A → B → C
- Parallel: A → (B + C + D) → E
- Branching: A → B if condition else C
- Composition: Combine chains into larger workflows

**Benefits:**
- Declarative chain composition
- Easy to read and maintain
- Efficient parallel execution
- Type-safe data flow
- Reusable components

---

### 10. Streaming

Token-by-token streaming for real-time responses and better UX.

**Run:** `uv run examples/10_streaming.py`

**Features:**
- Basic token streaming
- Streaming with prompt templates
- Batch streaming for multiple inputs
- Parallel chain streaming
- Progress tracking (token count, speed)
- Interactive streaming conversations
- Long-form content streaming
- Real-time formatting

**Examples Included:**
1. **Basic Streaming** - Simple token-by-token output
2. **Streaming with Prompt** - Template-based streaming
3. **Multiple Inputs** - Batch process with streaming
4. **Parallel Streaming** - Stream from parallel chains
5. **Progress Tracking** - Track tokens and speed
6. **Streaming Conversation** - Interactive chat mode
7. **Long-Form Streaming** - Handle large content generation
8. **Streaming with Formatting** - Real-time formatting

**Key Concepts:**
- **Token streaming**: Display tokens as they're generated
- **Chunks**: Small pieces of text from LLM
- **Flush**: Immediately display output without buffering
- **Progress tracking**: Monitor generation speed
- **Async streaming**: Non-blocking streaming operations

**Benefits:**
- Improved user experience (no waiting for full response)
- Lower perceived latency
- Real-time feedback
- Better for long responses
- Cancellable operations

**Use Cases:**
- Chatbots and conversational AI
- Content generation tools
- Real-time translation
- Live coding assistants
- Interactive tutorials

## Key Differences

| Aspect | Basic | Functions | Tools | Agent | RAG | Memory | Templates | Parsers | Chains | Streaming |
|--------|-------|-----------|-------|-------|-----|--------|-----------|---------|--------|-----------|
| **Framework** | OpenAI | OpenAI | LangChain | LangChain | LangChain | LangChain | LangChain | LangChain | LangChain | LangChain |
| **Main Focus** | Chat | Functions | Tools | Complete | Documents | History | Prompts | Output | Composition | Real-time |
| **Complexity** | Simplest | Low | Medium | High | High | Medium | Low | Medium | Medium | Low |
| **Best For** | Testing | Control | Automation | Production | Doc Q&A | Chatbots | Prompt eng. | Data extract | Workflows | UX |

## Learning Path

Follow examples in order for progressive learning:

```
01_basic_chat.py
    ↓
02_function_calling.py
    ↓
03_tool_calling.py
    ↓
04_single_agent.py
    ↓
05_rag_basic.py
    ↓
06_short_term_memory.py
    ↓
07_prompt_templates.py
    ↓
08_output_parsers.py
    ↓
09_lcel_chains.py
    ↓
10_streaming.py
```

**What you'll learn:**
1. Azure OpenAI basics and chat completion
2. Function schemas and manual handling
3. LangChain tools and automated execution
4. Production patterns with memory and multiple tools
5. RAG architecture with embeddings and vector stores
6. Conversation history and context window management
7. Prompt engineering with templates
8. Structured output parsing with type safety
9. Chain composition with LCEL
10. Real-time streaming for better UX

## Common Commands

```bash
# Run an example
uv run examples/01_basic_chat.py

# Add a new dependency
uv add package-name

# Update dependencies
uv sync

# Check Python version
python --version
```

## Troubleshooting

### API Key Issues
- Verify your `.env` file exists and has correct values
- Check that `AZURE_OPENAI_API_KEY` is set correctly
- Ensure your Azure OpenAI resource is active

### Import Errors
- Run `uv sync` to install all dependencies
- Check Python version is 3.13 or higher

### RAG Issues
- Ensure you have an embedding deployment configured
- Update embedding deployment name in code if different
- Load sample documents first with `load` command

## Learn More

- [Azure OpenAI Documentation](https://learn.microsoft.com/en-us/azure/ai-services/openai/)
- [LangChain Documentation](https://python.langchain.com/)
- [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling)
- [RAG Overview](https://python.langchain.com/docs/tutorials/rag/)

## License

MIT License - Feel free to use this template for your projects.
