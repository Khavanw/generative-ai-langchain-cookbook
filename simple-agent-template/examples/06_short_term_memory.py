from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from typing import List, Dict, Optional
from datetime import datetime
from settings import APP_SETTINGS


class ShortTermMemoryAgent:
    """An agent with short-term memory (conversation history) management."""
    
    def __init__(self, max_messages: int = 20, system_prompt: Optional[str] = None):
        """Initialize the agent with short-term memory.
        
        Args:
            max_messages: Maximum number of messages to keep in history
            system_prompt: Optional custom system prompt
        """
        # Initialize Azure OpenAI
        self.llm = AzureChatOpenAI(
            azure_endpoint=APP_SETTINGS.AZURE_OPENAI_ENDPOINT,
            api_key=APP_SETTINGS.AZURE_OPENAI_API_KEY,
            api_version=APP_SETTINGS.AZURE_OPENAI_API_VERSION,
            deployment_name=APP_SETTINGS.AZURE_OPENAI_DEPLOYMENT_NAME,
            temperature=0.7,
        )
        
        # Memory settings
        self.max_messages = max_messages
        self.conversation_history: List[Dict[str, str]] = []
        
        # System prompt
        self.system_prompt = system_prompt or """You are a helpful AI assistant with memory of our conversation.
You can remember what we discussed earlier in this conversation and reference it in your responses.
Be conversational and use context from previous messages when relevant."""
    
    def add_message(self, role: str, content: str) -> None:
        """Add a message to conversation history.
        
        Args:
            role: Message role (user or assistant)
            content: Message content
        """
        self.conversation_history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        
        # Trim history if exceeds max_messages
        if len(self.conversation_history) > self.max_messages:
            # Keep system message if exists, trim oldest messages
            self.conversation_history = self.conversation_history[-self.max_messages:]
    
    def get_messages_for_llm(self) -> List:
        """Convert conversation history to LangChain message format.
        
        Returns:
            List of LangChain message objects
        """
        messages = [SystemMessage(content=self.system_prompt)]
        
        for msg in self.conversation_history:
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                messages.append(AIMessage(content=msg["content"]))
        
        return messages
    
    def chat(self, user_input: str) -> str:
        """Send a message and get a response.
        
        Args:
            user_input: User's message
            
        Returns:
            Assistant's response
        """
        # Add user message to history
        self.add_message("user", user_input)
        
        # Get messages in LangChain format
        messages = self.get_messages_for_llm()
        
        # Get response from LLM
        response = self.llm.invoke(messages)
        assistant_message = response.content
        
        # Add assistant message to history
        self.add_message("assistant", assistant_message)
        
        return assistant_message
    
    def get_conversation_summary(self) -> Dict[str, any]:
        """Get summary statistics about the conversation.
        
        Returns:
            Dictionary with conversation statistics
        """
        total_messages = len(self.conversation_history)
        user_messages = sum(1 for msg in self.conversation_history if msg["role"] == "user")
        assistant_messages = sum(1 for msg in self.conversation_history if msg["role"] == "assistant")
        
        total_tokens = sum(len(msg["content"].split()) for msg in self.conversation_history)
        
        return {
            "total_messages": total_messages,
            "user_messages": user_messages,
            "assistant_messages": assistant_messages,
            "estimated_tokens": total_tokens,
            "max_messages": self.max_messages,
            "memory_usage": f"{total_messages}/{self.max_messages}"
        }
    
    def get_history(self, last_n: Optional[int] = None) -> List[Dict[str, str]]:
        """Get conversation history.
        
        Args:
            last_n: Optional number of last messages to retrieve
            
        Returns:
            List of message dictionaries
        """
        if last_n:
            return self.conversation_history[-last_n:]
        return self.conversation_history
    
    def clear_history(self) -> None:
        """Clear all conversation history."""
        self.conversation_history = []
    
    def export_conversation(self, filename: Optional[str] = None) -> str:
        """Export conversation to a text file.
        
        Args:
            filename: Optional filename (default: conversation_TIMESTAMP.txt)
            
        Returns:
            Filename of exported conversation
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"conversation_{timestamp}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("Conversation Export\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 60 + "\n\n")
            
            for msg in self.conversation_history:
                role = msg["role"].capitalize()
                content = msg["content"]
                timestamp = msg.get("timestamp", "")
                
                f.write(f"{role} [{timestamp}]:\n")
                f.write(f"{content}\n\n")
                f.write("-" * 60 + "\n\n")
        
        return filename


def main():
    """Main function to run the short-term memory demo."""
    print("=" * 60)
    print("Short-Term Memory Agent Demo")
    print("=" * 60)
    print("\nThis agent maintains conversation history and can reference")
    print("previous messages in the conversation.")
    print("\nCommands:")
    print("- 'history' [n] - Show last n messages (default: all)")
    print("- 'summary' - Show conversation statistics")
    print("- 'clear' - Clear conversation history")
    print("- 'export' - Export conversation to file")
    print("- 'exit' or 'quit' - End conversation")
    print("\n" + "=" * 60 + "\n")
    
    # Create agent with short-term memory
    agent = ShortTermMemoryAgent(max_messages=20)
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            # Handle exit
            if user_input.lower() in ['exit', 'quit']:
                print("\nGoodbye!")
                break
            
            # Handle history command
            elif user_input.lower().startswith('history'):
                parts = user_input.split()
                last_n = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else None
                
                history = agent.get_history(last_n)
                if not history:
                    print("\nNo conversation history yet.")
                else:
                    print("\n--- Conversation History ---")
                    for i, msg in enumerate(history, 1):
                        role = msg["role"].capitalize()
                        content = msg["content"][:100] + "..." if len(msg["content"]) > 100 else msg["content"]
                        print(f"{i}. {role}: {content}")
                    print("-" * 30)
                continue
            
            # Handle summary command
            elif user_input.lower() == 'summary':
                summary = agent.get_conversation_summary()
                print("\n--- Conversation Summary ---")
                print(f"Total Messages: {summary['total_messages']}")
                print(f"User Messages: {summary['user_messages']}")
                print(f"Assistant Messages: {summary['assistant_messages']}")
                print(f"Estimated Tokens: {summary['estimated_tokens']}")
                print(f"Memory Usage: {summary['memory_usage']}")
                print("-" * 30)
                continue
            
            # Handle clear command
            elif user_input.lower() == 'clear':
                agent.clear_history()
                print("\nConversation history cleared.")
                continue
            
            # Handle export command
            elif user_input.lower() == 'export':
                filename = agent.export_conversation()
                print(f"\nConversation exported to: {filename}")
                continue
            
            # Regular chat
            print()
            response = agent.chat(user_input)
            print(f"Assistant: {response}")
            print()
            
        except KeyboardInterrupt:
            print("\n\nInterrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\nError: {str(e)}")
            print("Please try again.\n")


if __name__ == "__main__":
    main()
