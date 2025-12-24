from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel
import sys
from pathlib import Path
import time

sys.path.append(str(Path(__file__).parent.parent))
from settings import APP_SETTINGS


class StreamingExamples:
    """Demonstrates different streaming patterns"""

    def __init__(self):
        self.llm = AzureChatOpenAI(
            azure_endpoint=APP_SETTINGS.AZURE_OPENAI_ENDPOINT,
            api_key=APP_SETTINGS.AZURE_OPENAI_API_KEY,
            azure_deployment=APP_SETTINGS.AZURE_OPENAI_DEPLOYMENT_NAME,
            api_version=APP_SETTINGS.AZURE_OPENAI_API_VERSION,
            temperature=0.7,
            streaming=True,
        )

    def example_1_basic_streaming(self):
        """Basic token-by-token streaming"""
        print("\n=== Example 1: Basic Streaming ===")
        prompt = input("\nEnter your prompt: ").strip()

        print("\n" + "-" * 60)
        for chunk in self.llm.stream(prompt):
            print(chunk.content, end="", flush=True)
        print("\n" + "-" * 60)

    def example_2_streaming_with_prompt(self):
        """Streaming with prompt template"""
        print("\n=== Example 2: Streaming with Prompt Template ===")

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "You are a {role} assistant."),
                ("user", "{question}"),
            ]
        )

        chain = prompt | self.llm | StrOutputParser()

        role = input("\nEnter assistant role: ").strip()
        question = input("Enter your question: ").strip()

        print("\n" + "-" * 60)
        for chunk in chain.stream({"role": role, "question": question}):
            print(chunk, end="", flush=True)
        print("\n" + "-" * 60)

    def example_3_streaming_multiple(self):
        """Streaming with batch processing"""
        print("\n=== Example 3: Streaming Multiple Inputs ===")

        prompt = ChatPromptTemplate.from_template("Tell me about {topic} in one sentence.")
        chain = prompt | self.llm | StrOutputParser()

        print("\nEnter 3 topics:")
        topics = []
        for i in range(3):
            topic = input(f"  Topic {i + 1}: ").strip()
            topics.append({"topic": topic})

        print("\n" + "=" * 60)
        for i, topic_input in enumerate(topics, 1):
            print(f"\n[{i}. {topic_input['topic']}]")
            for chunk in chain.stream(topic_input):
                print(chunk, end="", flush=True)
            print()
        print("=" * 60)

    def example_4_parallel_streaming(self):
        """Streaming from parallel chains"""
        print("\n=== Example 4: Parallel Chain Streaming ===")
        topic = input("\nEnter a topic: ").strip()

        joke_prompt = ChatPromptTemplate.from_template("Tell a short joke about {topic}.")
        fact_prompt = ChatPromptTemplate.from_template("Tell a brief fact about {topic}.")

        joke_chain = joke_prompt | self.llm | StrOutputParser()
        fact_chain = fact_prompt | self.llm | StrOutputParser()

        parallel_chain = RunnableParallel(joke=joke_chain, fact=fact_chain)

        print("\n" + "=" * 60)
        for chunk in parallel_chain.stream({"topic": topic}):
            if "joke" in chunk:
                print("[JOKE] ", end="", flush=True)
                print(chunk["joke"], end="", flush=True)
            if "fact" in chunk:
                print("\n[FACT] ", end="", flush=True)
                print(chunk["fact"], end="", flush=True)
        print("\n" + "=" * 60)

    def example_5_streaming_with_callback(self):
        """Streaming with progress tracking"""
        print("\n=== Example 5: Streaming with Progress Tracking ===")

        prompt = ChatPromptTemplate.from_template("Write a short story about {topic}.")
        chain = prompt | self.llm | StrOutputParser()

        topic = input("\nEnter story topic: ").strip()

        print("\n" + "-" * 60)
        token_count = 0
        start_time = time.time()

        for chunk in chain.stream({"topic": topic}):
            print(chunk, end="", flush=True)
            token_count += len(chunk.split())

        elapsed_time = time.time() - start_time
        print("\n" + "-" * 60)
        print(f"Stats: ~{token_count} tokens | {elapsed_time:.1f}s | ~{token_count / elapsed_time:.0f} tokens/sec")

    def example_6_streaming_conversation(self):
        """Interactive streaming conversation"""
        print("\n=== Example 6: Streaming Conversation ===")
        print("Type 'quit' to exit\n")

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "You are a helpful assistant."),
                ("user", "{input}"),
            ]
        )

        chain = prompt | self.llm | StrOutputParser()

        while True:
            print("=" * 60)
            user_input = input("You: ").strip()

            if user_input.lower() in ["quit", "exit", "q"]:
                print("\nGoodbye!")
                break

            print("\nAssistant: ", end="", flush=True)
            for chunk in chain.stream({"input": user_input}):
                print(chunk, end="", flush=True)
            print("\n")

    def example_7_streaming_long_form(self):
        """Streaming long-form content generation"""
        print("\n=== Example 7: Long-Form Content Streaming ===")

        prompt = ChatPromptTemplate.from_template(
            "Write a detailed {content_type} about {topic}. "
            "Include multiple sections and be comprehensive."
        )

        chain = prompt | self.llm | StrOutputParser()

        content_type = input("\nContent type (e.g., essay, article, guide): ").strip()
        topic = input("Topic: ").strip()

        print("\n" + "=" * 60)
        char_count = 0

        for chunk in chain.stream({"content_type": content_type, "topic": topic}):
            print(chunk, end="", flush=True)
            char_count += len(chunk)

        print("\n" + "=" * 60)
        print(f"Generated {char_count} characters")

    def example_8_streaming_with_formatting(self):
        """Streaming with real-time formatting"""
        print("\n=== Example 8: Streaming with Formatting ===")

        prompt = ChatPromptTemplate.from_template(
            "Write a numbered list of {count} {category}. "
            "Format each item on a new line with a number."
        )

        chain = prompt | self.llm | StrOutputParser()

        count = input("\nHow many items: ").strip()
        category = input("Category: ").strip()

        print("\n" + "=" * 60)
        for chunk in chain.stream({"count": count, "category": category}):
            print(chunk, end="", flush=True)
        print("\n" + "=" * 60)

    def run(self):
        """Run interactive streaming examples"""
        print("=" * 60)
        print("Streaming Examples")
        print("=" * 60)

        examples = {
            "1": ("Basic Streaming", self.example_1_basic_streaming),
            "2": ("Streaming with Prompt", self.example_2_streaming_with_prompt),
            "3": ("Streaming Multiple Inputs", self.example_3_streaming_multiple),
            "4": ("Parallel Streaming", self.example_4_parallel_streaming),
            "5": ("Progress Tracking", self.example_5_streaming_with_callback),
            "6": ("Streaming Conversation", self.example_6_streaming_conversation),
            "7": ("Long-Form Streaming", self.example_7_streaming_long_form),
            "8": ("Streaming with Formatting", self.example_8_streaming_with_formatting),
        }

        while True:
            print("\n" + "=" * 60)
            print("Available Examples:")
            for key, (name, _) in examples.items():
                print(f"  {key}. {name}")
            print("  q. Quit")
            print("=" * 60)

            choice = input("\nSelect an example (1-8) or 'q' to quit: ").strip().lower()

            if choice == "q":
                print("\nGoodbye!")
                break

            if choice in examples:
                _, func = examples[choice]
                try:
                    func()
                except Exception as e:
                    print(f"\nError: {e}")
            else:
                print("\nInvalid choice. Please select 1-8 or 'q'.")


def main():
    """Main entry point"""
    examples = StreamingExamples()
    examples.run()


if __name__ == "__main__":
    main()
