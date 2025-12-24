from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import (
    PromptTemplate,
    ChatPromptTemplate,
    FewShotPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain_core.messages import HumanMessage, AIMessage
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from settings import APP_SETTINGS


class PromptTemplateExamples:
    """Demonstrates different types of prompt templates"""

    def __init__(self):
        self.llm = AzureChatOpenAI(
            azure_endpoint=APP_SETTINGS.AZURE_OPENAI_ENDPOINT,
            api_key=APP_SETTINGS.AZURE_OPENAI_API_KEY,
            azure_deployment=APP_SETTINGS.AZURE_OPENAI_DEPLOYMENT_NAME,
            api_version=APP_SETTINGS.AZURE_OPENAI_API_VERSION,
            temperature=0.7,
        )

    def example_1_basic_template(self):
        """Basic string prompt template with single variable"""
        print("\n=== Example 1: Basic Prompt Template ===")
        print("Simple template with variables: Tell me a {adjective} joke about {topic}\n")

        template = "Tell me a {adjective} joke about {topic}."
        prompt = PromptTemplate.from_template(template)

        adjective = input("Enter an adjective (e.g., funny, short): ").strip()
        topic = input("Enter a topic (e.g., programming, cats): ").strip()

        formatted_prompt = prompt.format(adjective=adjective, topic=topic)
        response = self.llm.invoke(formatted_prompt)
        print(f"\n{response.content}")

    def example_2_chat_prompt_template(self):
        """Chat prompt template with system and user messages"""
        print("\n=== Example 2: Chat Prompt Template ===")
        print("Structured chat with system and user messages\n")

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "You are a helpful {role} assistant. Your tone is {tone}."),
                ("user", "{user_input}"),
            ]
        )

        role = input("Enter assistant role (e.g., Python expert, teacher): ").strip()
        tone = input("Enter tone (e.g., professional, friendly): ").strip()
        user_input = input("Enter your question: ").strip()

        messages = prompt.format_messages(role=role, tone=tone, user_input=user_input)
        response = self.llm.invoke(messages)
        print(f"\n{response.content}")

    def example_3_few_shot_template(self):
        """Few-shot learning with examples"""
        print("\n=== Example 3: Few-Shot Prompt Template ===")
        print("Teaching patterns through examples: happy->sad, tall->short, hot->cold\n")

        examples = [
            {"input": "happy", "output": "sad"},
            {"input": "tall", "output": "short"},
            {"input": "hot", "output": "cold"},
        ]

        example_template = """
Input: {input}
Output: {output}"""

        example_prompt = PromptTemplate(
            input_variables=["input", "output"], template=example_template
        )

        few_shot_prompt = FewShotPromptTemplate(
            examples=examples,
            example_prompt=example_prompt,
            prefix="Give the antonym of every input\n",
            suffix="\nInput: {adjective}\nOutput:",
            input_variables=["adjective"],
        )

        adjective = input("Enter an adjective: ").strip()
        formatted_prompt = few_shot_prompt.format(adjective=adjective)
        response = self.llm.invoke(formatted_prompt)
        print(f"\nAntonym: {response.content}")

    def example_4_partial_variables(self):
        """Template with partial variables pre-filled"""
        print("\n=== Example 4: Partial Variables ===")
        print("Pre-filled variables like current date\n")

        from datetime import datetime

        def get_current_date():
            return datetime.now().strftime("%Y-%m-%d")

        prompt = PromptTemplate(
            template="Today is {date}. {instruction}",
            input_variables=["instruction"],
            partial_variables={"date": get_current_date},
        )

        instruction = input("Enter your instruction: ").strip()
        formatted_prompt = prompt.format(instruction=instruction)
        response = self.llm.invoke(formatted_prompt)
        print(f"\n{response.content}")

    def example_5_template_composition(self):
        """Combining multiple templates"""
        print("\n=== Example 5: Template Composition ===")
        print("Combining system and user message templates\n")

        system_prompt = SystemMessagePromptTemplate.from_template(
            "You are an expert {domain} consultant."
        )

        human_prompt = HumanMessagePromptTemplate.from_template(
            "Context: {context}\n\nQuestion: {question}"
        )

        chat_prompt = ChatPromptTemplate.from_messages([system_prompt, human_prompt])

        domain = input("Enter domain (e.g., finance, health): ").strip()
        context = input("Enter context information: ").strip()
        question = input("Enter your question: ").strip()

        messages = chat_prompt.format_messages(
            domain=domain, context=context, question=question
        )
        response = self.llm.invoke(messages)
        print(f"\n{response.content}")

    def example_6_message_placeholder(self):
        """Template with message history placeholder"""
        print("\n=== Example 6: Messages Placeholder ===")
        print("Template with conversation history\n")

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "You are a helpful assistant."),
                MessagesPlaceholder(variable_name="chat_history"),
                ("user", "{user_input}"),
            ]
        )

        chat_history = [
            HumanMessage(content="My name is Alice"),
            AIMessage(content="Hello Alice! Nice to meet you."),
            HumanMessage(content="I like Python programming"),
            AIMessage(content="That's great! Python is a powerful language."),
        ]

        print("Previous conversation:")
        print("  User: My name is Alice")
        print("  Assistant: Hello Alice!")
        print("  User: I like Python programming")
        print("  Assistant: That's great!\n")

        user_input = input("Enter your message: ").strip()
        messages = prompt.format_messages(
            chat_history=chat_history, user_input=user_input
        )
        response = self.llm.invoke(messages)
        print(f"\n{response.content}")

    def run(self):
        """Run interactive prompt template examples"""
        print("=" * 60)
        print("Prompt Templates Examples")
        print("=" * 60)

        examples = {
            "1": ("Basic Prompt Template", self.example_1_basic_template),
            "2": ("Chat Prompt Template", self.example_2_chat_prompt_template),
            "3": ("Few-Shot Template", self.example_3_few_shot_template),
            "4": ("Partial Variables", self.example_4_partial_variables),
            "5": ("Template Composition", self.example_5_template_composition),
            "6": ("Messages Placeholder", self.example_6_message_placeholder),
        }

        while True:
            print("\n" + "=" * 60)
            print("Available Examples:")
            for key, (name, _) in examples.items():
                print(f"  {key}. {name}")
            print("  q. Quit")
            print("=" * 60)

            choice = input("\nSelect an example (1-6) or 'q' to quit: ").strip().lower()

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
                print("\nInvalid choice. Please select 1-6 or 'q'.")


def main():
    """Main entry point"""
    examples = PromptTemplateExamples()
    examples.run()


if __name__ == "__main__":
    main()
