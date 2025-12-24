# Multi-Agent System Workflows

Visual representation of the three workflow patterns implemented in this system.

## Sequential Workflow

The sequential workflow processes tasks linearly, with each agent building on the previous agent's work.

```
┌─────────────────────────────────────────────────────────────────┐
│                      SEQUENTIAL WORKFLOW                         │
└─────────────────────────────────────────────────────────────────┘

User Input: "Task Description"
    ↓
┌───────────────────┐
│  Research Agent   │  - Gathers information
│                   │  - Identifies key facts
│  Specialist:      │  - Creates structured summary
│  Information      │
└────────┬──────────┘
         │ Output: Research findings
         ↓
┌───────────────────┐
│  Analysis Agent   │  - Evaluates research
│                   │  - Identifies patterns
│  Specialist:      │  - Provides insights
│  Evaluation       │
└────────┬──────────┘
         │ Output: Analysis and insights
         ↓
┌───────────────────┐
│  Writer Agent     │  - Creates content
│                   │  - Organizes information
│  Specialist:      │  - Adapts style
│  Content Creation │
└────────┬──────────┘
         │ Output: Complete article
         ↓
┌───────────────────┐
│  Critic Agent     │  - Reviews quality
│                   │  - Checks consistency
│  Specialist:      │  - Suggests improvements
│  Quality Assurance│
└────────┬──────────┘
         │ Output: Critique and feedback
         ↓
    Final Result
```

**Use Cases:**
- Blog post creation
- Research reports
- Technical documentation
- Comprehensive analysis

**Advantages:**
- Each agent benefits from previous work
- Progressive refinement
- High-quality output

**Disadvantages:**
- Sequential processing (slower)
- Blocked if one agent fails

## Parallel Workflow

The parallel workflow executes multiple research tasks simultaneously, then aggregates results.

```
┌─────────────────────────────────────────────────────────────────┐
│                       PARALLEL WORKFLOW                          │
└─────────────────────────────────────────────────────────────────┘

User Input: "Main Task" + [Subtask 1, Subtask 2, Subtask 3]
    ↓
┌─────────────────────────────────────────────────────────────────┐
│                    PARALLEL RESEARCH PHASE                       │
└─────────────────────────────────────────────────────────────────┘

Subtask 1           Subtask 2           Subtask 3
    ↓                   ↓                   ↓
┌──────────┐       ┌──────────┐       ┌──────────┐
│Research  │       │Research  │       │Research  │
│Agent #1  │       │Agent #2  │       │Agent #3  │
└────┬─────┘       └────┬─────┘       └────┬─────┘
     │                  │                  │
     │    Findings 1    │    Findings 2    │    Findings 3
     └──────────────────┴──────────────────┘
                        ↓
            ┌───────────────────────┐
            │  AGGREGATION PHASE    │
            │  Combine all findings │
            └───────────┬───────────┘
                        ↓
            ┌───────────────────────┐
            │  Analysis Agent       │
            │  Analyze combined     │
            │  research             │
            └───────────┬───────────┘
                        ↓
            ┌───────────────────────┐
            │  Writer Agent         │
            │  Create comprehensive │
            │  report               │
            └───────────┬───────────┘
                        ↓
                  Final Result
```

**Use Cases:**
- Comparative analysis
- Multi-source research
- Market research
- Technology comparisons

**Advantages:**
- Faster execution (concurrent)
- Handles complex, divisible tasks
- Efficient resource usage

**Disadvantages:**
- Requires independent subtasks
- Higher API usage

## Hierarchical Workflow

The hierarchical workflow includes a supervisor (Critic Agent) that reviews and approves output.

```
┌─────────────────────────────────────────────────────────────────┐
│                     HIERARCHICAL WORKFLOW                        │
└─────────────────────────────────────────────────────────────────┘

User Input: "Task Description"
    ↓
┌─────────────────────────────────────────────────────────────────┐
│                       ITERATION LOOP                             │
│                    (Max 2 iterations)                            │
└─────────────────────────────────────────────────────────────────┘

┌───────────────────┐
│  Research Agent   │  - Gathers information
│                   │  - Creates knowledge base
└────────┬──────────┘
         │
         ↓
┌───────────────────┐
│  Writer Agent     │  - Creates content
│                   │  - Uses research data
└────────┬──────────┘
         │
         ↓
┌───────────────────────────────────────────────────────────────┐
│                   SUPERVISOR REVIEW                            │
│  ┌───────────────────┐                                        │
│  │  Critic Agent     │  - Reviews content                     │
│  │  (Supervisor)     │  - Checks quality                      │
│  │                   │  - Makes decision                      │
│  └────────┬──────────┘                                        │
│           │                                                    │
│           ├──────────┐                                        │
│           ↓          ↓                                        │
│     ┌─────────┐  ┌──────────┐                               │
│     │APPROVED │  │NOT       │                               │
│     │         │  │APPROVED  │                               │
│     └────┬────┘  └────┬─────┘                               │
│          │            │                                      │
│          │            └─→ Feedback ─→ Iterate with          │
│          │                            improvements           │
│          ↓                            (Back to Research)     │
│    Final Result                                              │
└───────────────────────────────────────────────────────────────┘
```

**Use Cases:**
- Quality-controlled content
- Iterative improvement
- High-stakes documents
- Regulated content

**Advantages:**
- Built-in quality control
- Iterative refinement
- Supervisor oversight

**Disadvantages:**
- Potentially slower
- May require multiple iterations
- Higher API usage if not approved

## Agent Roles and Responsibilities

### Research Agent
```
┌─────────────────────────────────────┐
│        RESEARCH AGENT               │
├─────────────────────────────────────┤
│ Primary Role:                       │
│ • Information gathering             │
│ • Fact identification               │
│ • Source compilation                │
│                                     │
│ Input:                              │
│ • Task description                  │
│ • Research scope                    │
│                                     │
│ Output:                             │
│ • Structured findings               │
│ • Key facts and data                │
│ • Source references                 │
└─────────────────────────────────────┘
```

### Analysis Agent
```
┌─────────────────────────────────────┐
│        ANALYSIS AGENT               │
├─────────────────────────────────────┤
│ Primary Role:                       │
│ • Data evaluation                   │
│ • Pattern recognition               │
│ • Critical insights                 │
│                                     │
│ Input:                              │
│ • Research findings                 │
│ • Raw data                          │
│                                     │
│ Output:                             │
│ • Analyzed insights                 │
│ • Identified patterns               │
│ • Recommendations                   │
└─────────────────────────────────────┘
```

### Writer Agent
```
┌─────────────────────────────────────┐
│         WRITER AGENT                │
├─────────────────────────────────────┤
│ Primary Role:                       │
│ • Content creation                  │
│ • Information organization          │
│ • Style adaptation                  │
│                                     │
│ Input:                              │
│ • Research data                     │
│ • Analysis insights                 │
│ • Writing requirements              │
│                                     │
│ Output:                             │
│ • Well-structured content           │
│ • Clear narratives                  │
│ • Audience-appropriate style        │
└─────────────────────────────────────┘
```

### Critic Agent
```
┌─────────────────────────────────────┐
│         CRITIC AGENT                │
├─────────────────────────────────────┤
│ Primary Role:                       │
│ • Quality assurance                 │
│ • Consistency checking              │
│ • Improvement suggestions           │
│                                     │
│ Input:                              │
│ • Content to review                 │
│ • Quality criteria                  │
│                                     │
│ Output:                             │
│ • Critique and feedback             │
│ • Approval/rejection                │
│ • Specific improvements             │
└─────────────────────────────────────┘
```

## Workflow Selection Guide

```
┌─────────────────────────────────────────────────────────────────┐
│                  WORKFLOW SELECTION GUIDE                        │
└─────────────────────────────────────────────────────────────────┘

Question 1: Is your task divisible into independent subtasks?
    ├─ YES → Consider PARALLEL workflow
    └─ NO  → Go to Question 2

Question 2: Do you need iterative improvement with approval?
    ├─ YES → Use HIERARCHICAL workflow
    └─ NO  → Go to Question 3

Question 3: Do you need progressive refinement?
    ├─ YES → Use SEQUENTIAL workflow
    └─ NO  → Use simplest workflow (SEQUENTIAL)

Special Cases:
    • Time-sensitive + divisible → PARALLEL
    • High quality requirements → HIERARCHICAL
    • Complex analysis needed → SEQUENTIAL
    • Multiple perspectives → PARALLEL
```

## Data Flow Patterns

### Context Passing
```
Agent A → Output
    ↓
    Stored in context dict: {"agent_a_result": "..."}
    ↓
Agent B → Receives context → Processes with additional info
```

### Response Format
```python
AgentResponse(
    agent_name: str,      # "ResearchAgent"
    content: str,         # "Actual output text..."
    metadata: dict        # {"model": "gpt-4", ...}
)
```

### History Tracking
```
Orchestrator.history = [
    AgentResponse(...),  # First agent
    AgentResponse(...),  # Second agent
    AgentResponse(...),  # Third agent
    ...
]
```

## Performance Characteristics

| Workflow      | Speed    | Quality | API Calls | Use Case          |
|---------------|----------|---------|-----------|-------------------|
| Sequential    | Moderate | High    | 4         | Single task       |
| Parallel      | Fast     | High    | N + 2     | Multiple subtasks |
| Hierarchical  | Slow     | Highest | 3-6       | Quality-critical  |

## Error Handling

```
Try:
    Agent.process(task)
    ↓
    Success → Continue to next agent
    ↓
    Error → Log error → Return partial result

Orchestrator catches errors and:
    • Logs failure
    • Returns available results
    • Provides error context
```

## Extending Workflows

### Add New Agent to Sequential
```python
def custom_sequential_workflow(self, task):
    research = self.research_agent.process(task)
    data = self.data_agent.process(task, context={...})  # NEW
    analysis = self.analysis_agent.process(...)
    ...
```

### Create Hybrid Workflow
```python
def hybrid_workflow(self, task, subtasks):
    # Parallel research
    research_results = [self.research_agent.process(st) for st in subtasks]
    
    # Sequential processing
    analysis = self.analysis_agent.process(...)
    draft = self.writer_agent.process(...)
    
    # Hierarchical review
    approved = False
    while not approved:
        critique = self.critic_agent.process(...)
        ...
```

This visual guide helps understand how agents collaborate in different workflow patterns.
