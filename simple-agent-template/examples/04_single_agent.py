from langchain_openai import AzureChatOpenAI
from langchain.tools import tool
from langchain.agents import create_agent
from typing import List, Dict, Any
from datetime import datetime
from examples.settings import APP_SETTINGS


# Define comprehensive tools for the agent
@tool
def get_weather(location: str) -> str:
    """Get the current weather for a location.
    
    Args:
        location: The city name to get weather for
    """
    # Mock weather data - in production, integrate with real weather API
    weather_data = {
        "hanoi": {"temp": 25, "condition": "sunny"},
        "tokyo": {"temp": 18, "condition": "cloudy"},
        "new york": {"temp": 15, "condition": "rainy"},
        "london": {"temp": 12, "condition": "foggy"},
    }
    
    loc = location.lower()
    if loc in weather_data:
        data = weather_data[loc]
        return f"The weather in {location} is {data['condition']} with a temperature of {data['temp']} degrees C"
    return f"Weather data not available for {location}. Using default: sunny, 22 degrees C"


@tool
def calculate(expression: str) -> str:
    """Calculate a mathematical expression safely.
    
    Args:
        expression: Mathematical expression to evaluate (e.g., "2 + 2", "10 * 5")
    """
    try:
        # Safe evaluation of mathematical expressions
        allowed_chars = set("0123456789+-*/.() ")
        if not all(c in allowed_chars for c in expression):
            return "Error: Expression contains invalid characters"
        
        result = eval(expression, {"__builtins__": {}}, {})
        return f"Result: {result}"
    except Exception as e:
        return f"Error calculating expression: {str(e)}"


@tool
def get_current_time(timezone: str = "UTC") -> str:
    """Get the current time in a specific timezone.
    
    Args:
        timezone: The timezone name (e.g., UTC, Asia/Ho_Chi_Minh)
    """
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return f"Current time in {timezone}: {current_time}"


@tool
def search_knowledge(query: str) -> str:
    """Search the knowledge base for information.
    
    Args:
        query: The search query
    """
    # Mock knowledge base - in production, integrate with vector DB or search engine
    knowledge_base = {
        "ai": "Artificial Intelligence is the simulation of human intelligence by machines.",
        "langchain": "LangChain is a framework for building applications with large language models.",
        "azure": "Azure is Microsoft's cloud computing platform providing various services.",
        "python": "Python is a high-level programming language known for its simplicity and readability.",
    }
    
    query_lower = query.lower()
    for key, value in knowledge_base.items():
        if key in query_lower:
            return f"Knowledge: {value}"
    
    return f"No specific knowledge found for '{query}'. This is a general topic that may require web search."


@tool
def create_reminder(task: str, time: str) -> str:
    """Create a reminder for a task.
    
    Args:
        task: The task to be reminded about
        time: When to be reminded (e.g., "tomorrow", "in 1 hour")
    """
    return f"Reminder created: '{task}' scheduled for {time}"


class SingleAgent:
    """A comprehensive single agent with memory and multiple tools."""
    
    def __init__(self, verbose: bool = False):
        """Initialize the agent with tools and configuration.
        
        Args:
            verbose: Whether to show detailed execution logs
        """
        self.verbose = verbose
        self.conversation_history: List[Dict[str, str]] = []
        
        # Initialize Azure OpenAI model
        self.llm = AzureChatOpenAI(
            azure_endpoint=APP_SETTINGS.AZURE_OPENAI_ENDPOINT,
            api_key=APP_SETTINGS.AZURE_OPENAI_API_KEY,
            api_version=APP_SETTINGS.AZURE_OPENAI_API_VERSION,
            deployment_name=APP_SETTINGS.AZURE_OPENAI_DEPLOYMENT_NAME,
            temperature=0.7,
        )
        
        # Define all available tools
        self.tools = [
            get_weather,
            calculate,
            get_current_time,
            search_knowledge,
            create_reminder
        ]
        
        # Create the agent
        self.agent = create_agent(
            model=self.llm,
            tools=self.tools,
            system_prompt=self._create_system_prompt()
        )
    
    def _create_system_prompt(self) -> str:
        """Create a comprehensive system prompt for the agent."""
        return """You are a helpful AI assistant with access to multiple tools.

Your capabilities:
- Get weather information for any city
- Perform mathematical calculations
- Get current time in any timezone
- Search knowledge base for information
- Create reminders for tasks

Guidelines:
- Use tools when they can help answer the user's question
- Be concise and clear in your responses
- If you're unsure, ask for clarification
- Always explain what you're doing when using tools
- Maintain a friendly and professional tone

When the user asks a question:
1. Analyze what information or action is needed
2. Use appropriate tools to gather information
3. Synthesize the results into a helpful response"""
    
    def invoke(self, user_input: str) -> Dict[str, Any]:
        """Process user input and return agent response.
        
        Args:
            user_input: The user's question or request
            
        Returns:
            Dictionary containing response and metadata
        """
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_input
        })
        
        # Invoke the agent
        result = self.agent.invoke({
            "messages": [{"role": "user", "content": user_input}]
        })
        
        # Extract tool calls and final response
        tool_calls = []
        tool_results = []
        
        for msg in result["messages"]:
            if hasattr(msg, "tool_calls") and msg.tool_calls:
                for tool_call in msg.tool_calls:
                    tool_calls.append({
                        "name": tool_call["name"],
                        "args": tool_call["args"]
                    })
            elif hasattr(msg, "name") and msg.name:
                tool_results.append({
                    "tool": msg.name,
                    "result": msg.content
                })
        
        # Get final response
        final_response = result["messages"][-1].content
        
        # Add assistant response to history
        self.conversation_history.append({
            "role": "assistant",
            "content": final_response
        })
        
        return {
            "response": final_response,
            "tool_calls": tool_calls,
            "tool_results": tool_results,
            "message_count": len(result["messages"])
        }
    
    def display_response(self, result: Dict[str, Any]) -> None:
        """Display the agent's response in a formatted way.
        
        Args:
            result: The result dictionary from invoke()
        """
        # Display tool usage
        if result["tool_calls"]:
            print("\n--- Tools Used ---")
            for i, tool_call in enumerate(result["tool_calls"], 1):
                print(f"{i}. {tool_call['name']}")
                print(f"   Arguments: {tool_call['args']}")
            
            if result["tool_results"]:
                print("\n--- Tool Results ---")
                for tool_result in result["tool_results"]:
                    print(f"- {tool_result['tool']}: {tool_result['result'][:100]}...")
            print("-" * 20)
        else:
            print("\n--- No Tools Used ---")
            print("Direct response without tool usage")
            print("-" * 20)
        
        # Display final response
        print(f"\nAssistant: {result['response']}")
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Get the conversation history.
        
        Returns:
            List of message dictionaries
        """
        return self.conversation_history
    
    def clear_history(self) -> None:
        """Clear the conversation history."""
        self.conversation_history = []
        print("Conversation history cleared.")


def main():
    """Main function to run the single agent demo."""
    print("=" * 60)
    print("Single Agent Demo with Azure OpenAI")
    print("=" * 60)
    print("\nThis agent has access to multiple tools:")
    print("- Weather information")
    print("- Mathematical calculations")
    print("- Current time")
    print("- Knowledge base search")
    print("- Reminder creation")
    print("\nCommands:")
    print("- 'history' - Show conversation history")
    print("- 'clear' - Clear conversation history")
    print("- 'tools' - List available tools")
    print("- 'exit' or 'quit' - End conversation")
    print("\n" + "=" * 60 + "\n")
    
    # Create agent instance
    agent = SingleAgent(verbose=False)
    
    # Main interaction loop
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            # Handle commands
            if user_input.lower() in ['exit', 'quit']:
                print("\nThank you for using Single Agent. Goodbye!")
                break
            
            elif user_input.lower() == 'history':
                print("\n--- Conversation History ---")
                history = agent.get_conversation_history()
                if not history:
                    print("No conversation history yet.")
                else:
                    for i, msg in enumerate(history, 1):
                        role = msg["role"].capitalize()
                        content = msg["content"][:100] + "..." if len(msg["content"]) > 100 else msg["content"]
                        print(f"{i}. {role}: {content}")
                print("-" * 30)
                continue
            
            elif user_input.lower() == 'clear':
                agent.clear_history()
                continue
            
            elif user_input.lower() == 'tools':
                print("\n--- Available Tools ---")
                for i, tool in enumerate(agent.tools, 1):
                    print(f"{i}. {tool.name}: {tool.description}")
                print("-" * 30)
                continue
            
            # Process user input with agent
            print()
            result = agent.invoke(user_input)
            agent.display_response(result)
            print("\n" + "-" * 60 + "\n")
            
        except KeyboardInterrupt:
            print("\n\nInterrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\nError: {str(e)}")
            print("Please try again or type 'exit' to quit.\n")


if __name__ == "__main__":
    main()
