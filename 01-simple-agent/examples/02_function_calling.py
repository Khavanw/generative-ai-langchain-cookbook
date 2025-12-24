import json
from openai import AzureOpenAI
from examples.settings import APP_SETTINGS


# Define functions that can be called by the model
def get_weather(location: str) -> str:
    """Get the current weather for a location."""
    # Mock weather data
    return json.dumps({
        "location": location,
        "temperature": "25",
        "unit": "celsius",
        "forecast": "sunny"
    })


def calculate_sum(a: float, b: float) -> float:
    """Calculate the sum of two numbers."""
    return a + b


def get_current_time(timezone: str = "UTC") -> str:
    """Get the current time in a specific timezone."""
    from datetime import datetime
    return json.dumps({
        "timezone": timezone,
        "time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })


# Define function schemas for OpenAI
functions = [
    {
        "name": "get_weather",
        "description": "Get the current weather for a location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city name to get weather for"
                }
            },
            "required": ["location"]
        }
    },
    {
        "name": "calculate_sum",
        "description": "Calculate the sum of two numbers",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {
                    "type": "number",
                    "description": "First number"
                },
                "b": {
                    "type": "number",
                    "description": "Second number"
                }
            },
            "required": ["a", "b"]
        }
    },
    {
        "name": "get_current_time",
        "description": "Get the current time in a specific timezone",
        "parameters": {
            "type": "object",
            "properties": {
                "timezone": {
                    "type": "string",
                    "description": "The timezone (default: UTC)"
                }
            },
            "required": []
        }
    }
]


# Map function names to actual functions
available_functions = {
    "get_weather": get_weather,
    "calculate_sum": calculate_sum,
    "get_current_time": get_current_time
}


def run_conversation(user_message: str):
    """Run a conversation with function calling."""
    # Initialize Azure OpenAI client
    client = AzureOpenAI(
        api_version=APP_SETTINGS.AZURE_OPENAI_API_VERSION,
        azure_endpoint=APP_SETTINGS.AZURE_OPENAI_ENDPOINT,
        api_key=APP_SETTINGS.AZURE_OPENAI_API_KEY,
    )
    
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant with access to functions."
        },
        {
            "role": "user",
            "content": user_message
        }
    ]
    
    # First API call: send message and functions to model
    response = client.chat.completions.create(
        model=APP_SETTINGS.AZURE_OPENAI_DEPLOYMENT_NAME,
        messages=messages,
        functions=functions,
        function_call="auto"
    )
    
    response_message = response.choices[0].message
    print(f"AI Response: {response_message.content}")
    
    # Check if the model wants to call a function
    if response_message.function_call:
        function_name = response_message.function_call.name
        function_args = json.loads(response_message.function_call.arguments)
        
        print(f"\nFunction Call: {function_name}")
        print(f"Arguments: {function_args}")
        
        # Call the function
        function_to_call = available_functions[function_name]
        function_response = function_to_call(**function_args)
        
        print(f"Function Result: {function_response}")
        
        # Add function call and response to messages
        messages.append({
            "role": "assistant",
            "content": response_message.content,
            "function_call": {
                "name": function_name,
                "arguments": response_message.function_call.arguments
            }
        })
        messages.append({
            "role": "function",
            "name": function_name,
            "content": str(function_response)
        })
        
        # Second API call: get final response with function result
        second_response = client.chat.completions.create(
            model=APP_SETTINGS.AZURE_OPENAI_DEPLOYMENT_NAME,
            messages=messages
        )
        
        print(f"\nFinal Response: {second_response.choices[0].message.content}")
        return second_response.choices[0].message.content
    
    return response_message.content


def main():
    print("=" * 50)
    print("Function Calling Demo")
    print("=" * 50)
    print("\nAvailable functions:")
    print("- get_weather: Get weather for a location")
    print("- calculate_sum: Calculate sum of two numbers")
    print("- get_current_time: Get current time")
    print("\nType 'exit' or 'quit' to end the conversation\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ['exit', 'quit']:
                print("Goodbye!")
                break
            
            print()
            run_conversation(user_input)
            print("\n" + "-" * 50 + "\n")
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")
            print("Please try again.\n")


if __name__ == "__main__":
    main()
