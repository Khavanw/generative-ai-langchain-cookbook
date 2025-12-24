from langchain_openai import AzureChatOpenAI
from langchain.tools import tool
from langchain.agents import create_agent
from examples.settings import APP_SETTINGS


# Define tools using LangChain decorator
@tool
def get_weather(location: str) -> str:
    """Get the current weather for a location.
    
    Args:
        location: The city name to get weather for
    """
    # Mock weather data
    return f"The weather in {location} is sunny with a temperature of 25 degrees C"


@tool
def calculate_sum(a: float, b: float) -> float:
    """Calculate the sum of two numbers.
    
    Args:
        a: First number
        b: Second number
    """
    return a + b


@tool
def get_current_time(timezone: str = "UTC") -> str:
    """Get the current time in a specific timezone.
    
    Args:
        timezone: The timezone (default: UTC)
    """
    from datetime import datetime
    return f"Current time in {timezone}: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"


def create_simple_agent():
    """Create a LangChain agent with tool calling capability."""
    # Initialize Azure OpenAI model
    llm = AzureChatOpenAI(
        azure_endpoint=APP_SETTINGS.AZURE_OPENAI_ENDPOINT,
        api_key=APP_SETTINGS.AZURE_OPENAI_API_KEY,
        api_version=APP_SETTINGS.AZURE_OPENAI_API_VERSION,
        deployment_name=APP_SETTINGS.AZURE_OPENAI_DEPLOYMENT_NAME,
        temperature=0.7,
    )
    
    # Define tools
    tools = [get_weather, calculate_sum, get_current_time]
    
    # Create agent using LangChain v1 create_agent
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt="You are a helpful assistant with access to tools. Use tools when needed to answer questions."
    )
    
    return agent


def main():
    print("=" * 50)
    print("Tool Calling Demo with LangChain Agent")
    print("=" * 50)
    print("\nAvailable tools:")
    print("- get_weather: Get weather for a location")
    print("- calculate_sum: Calculate sum of two numbers")
    print("- get_current_time: Get current time")
    print("\nType 'exit' or 'quit' to end the conversation\n")
    
    # Create agent
    agent_executor = create_simple_agent()
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ['exit', 'quit']:
                print("Goodbye!")
                break
            
            print()
            result = agent_executor.invoke({
                "messages": [{"role": "user", "content": user_input}]
            })
            
            # Display tool calls if any
            print("\n--- Tool Calls ---")
            tool_called = False
            for msg in result["messages"]:
                if hasattr(msg, "tool_calls") and msg.tool_calls:
                    for tool_call in msg.tool_calls:
                        tool_called = True
                        print(f"Tool: {tool_call['name']}")
                        print(f"Arguments: {tool_call['args']}")
                elif hasattr(msg, "name") and msg.name:
                    # Tool response message
                    print(f"Tool '{msg.name}' returned: {msg.content}")
            
            if not tool_called:
                print("No tools were called")
            print("-" * 18)
            
            # Get the last message from the agent
            final_message = result["messages"][-1].content
            print(f"\nFinal Answer: {final_message}")
            print("\n" + "-" * 50 + "\n")
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")
            print("Please try again.\n")

if __name__ == "__main__":
    main()