from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from pydantic import BaseModel, Field
from operator import itemgetter
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from settings import APP_SETTINGS


class Analysis(BaseModel):
    """Analysis result structure"""

    sentiment: str = Field(description="Sentiment: positive, negative, or neutral")
    key_points: list[str] = Field(description="Main points from the text")
    summary: str = Field(description="Brief summary")


class LCELChainExamples:
    """Demonstrates LCEL chain composition patterns"""

    def __init__(self):
        self.llm = AzureChatOpenAI(
            azure_endpoint=APP_SETTINGS.AZURE_OPENAI_ENDPOINT,
            api_key=APP_SETTINGS.AZURE_OPENAI_API_KEY,
            azure_deployment=APP_SETTINGS.AZURE_OPENAI_DEPLOYMENT_NAME,
            api_version=APP_SETTINGS.AZURE_OPENAI_API_VERSION,
            temperature=0.7,
        )

    def example_1_simple_chain(self):
        """Basic chain with prompt | model | parser"""
        print("\n=== Example 1: Simple Chain ===")
        print("Basic pattern: prompt | llm | output_parser\n")

        prompt = ChatPromptTemplate.from_template("Tell me a joke about {topic}.")
        output_parser = StrOutputParser()
        chain = prompt | self.llm | output_parser

        topic = input("Enter a topic: ").strip()
        result = chain.invoke({"topic": topic})
        print(f"\n{result}")

    def example_2_sequential_chain(self):
        """Multiple sequential processing steps"""
        print("\n=== Example 2: Sequential Chain ===")
        print("Generate paragraph then translate\n")

        prompt1 = ChatPromptTemplate.from_template(
            "Write a short paragraph about {topic}."
        )

        prompt2 = ChatPromptTemplate.from_template(
            "Translate the following text to {language}:\n\n{text}"
        )

        chain = (
            {"text": prompt1 | self.llm | StrOutputParser()}
            | prompt2
            | self.llm
            | StrOutputParser()
        )

        topic = input("Enter a topic: ").strip()
        language = input("Enter target language: ").strip()

        result = chain.invoke({"topic": topic, "language": language})
        print(f"\n{result}")

    def example_3_parallel_chain(self):
        """Execute multiple chains in parallel"""
        print("\n=== Example 3: Parallel Chain ===")
        print("Execute joke + fact + poem simultaneously\n")

        joke_chain = (
            ChatPromptTemplate.from_template("Tell a joke about {topic}.")
            | self.llm
            | StrOutputParser()
        )

        fact_chain = (
            ChatPromptTemplate.from_template("Tell an interesting fact about {topic}.")
            | self.llm
            | StrOutputParser()
        )

        poem_chain = (
            ChatPromptTemplate.from_template("Write a short poem about {topic}.")
            | self.llm
            | StrOutputParser()
        )

        parallel_chain = RunnableParallel(joke=joke_chain, fact=fact_chain, poem=poem_chain)

        topic = input("Enter a topic: ").strip()
        result = parallel_chain.invoke({"topic": topic})

        print("\n" + "=" * 60)
        print("JOKE:")
        print(result["joke"])
        print("\n" + "=" * 60)
        print("FACT:")
        print(result["fact"])
        print("\n" + "=" * 60)
        print("POEM:")
        print(result["poem"])
        print("=" * 60)

    def example_4_passthrough(self):
        """Use RunnablePassthrough to pass data through"""
        print("\n=== Example 4: Passthrough Chain ===")
        print("Pass input through while adding derived values\n")

        prompt = ChatPromptTemplate.from_template(
            "Write a {length} description of {topic}."
        )

        chain = (
            {
                "topic": RunnablePassthrough(),
                "length": lambda x: "short",
                "original": RunnablePassthrough(),
            }
            | prompt
            | self.llm
            | StrOutputParser()
        )

        topic = input("Enter a topic: ").strip()
        result = chain.invoke(topic)
        print(f"\n{result}")

    def example_5_itemgetter_chain(self):
        """Use itemgetter to extract specific fields"""
        print("\n=== Example 5: ItemGetter Chain ===")
        print("Extract specific fields from input\n")

        prompt = ChatPromptTemplate.from_template(
            "Compare {item1} and {item2}. Focus on their {aspect}."
        )

        chain = (
            {
                "item1": itemgetter("item1"),
                "item2": itemgetter("item2"),
                "aspect": itemgetter("aspect"),
            }
            | prompt
            | self.llm
            | StrOutputParser()
        )

        item1 = input("Enter first item: ").strip()
        item2 = input("Enter second item: ").strip()
        aspect = input("Enter comparison aspect (e.g., performance, price): ").strip()

        result = chain.invoke({"item1": item1, "item2": item2, "aspect": aspect})
        print(f"\n{result}")

    def example_6_lambda_transform(self):
        """Use RunnableLambda for custom transformations"""
        print("\n=== Example 6: Lambda Transform Chain ===")
        print("Apply custom transformations: uppercase + prefix\n")

        def uppercase_transform(text: str) -> str:
            return text.upper()

        def add_prefix(text: str) -> str:
            return f"IMPORTANT: {text}"

        prompt = ChatPromptTemplate.from_template("Give me a one-sentence tip about {topic}.")

        chain = (
            prompt
            | self.llm
            | StrOutputParser()
            | RunnableLambda(uppercase_transform)
            | RunnableLambda(add_prefix)
        )

        topic = input("Enter a topic: ").strip()
        result = chain.invoke({"topic": topic})
        print(f"\n{result}")

    def example_7_structured_output(self):
        """Chain with structured output parsing"""
        print("\n=== Example 7: Structured Output Chain ===")
        print("Analyze text with structured output\n")

        parser = JsonOutputParser(pydantic_object=Analysis)

        prompt = PromptTemplate(
            template="Analyze the following text:\n\n{text}\n\n{format_instructions}",
            input_variables=["text"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        chain = prompt | self.llm | parser

        text = input("Enter text to analyze: ").strip()
        result = chain.invoke({"text": text})

        print("\n" + "=" * 60)
        print(f"Sentiment: {result['sentiment']}")
        print("\nKey Points:")
        for i, point in enumerate(result["key_points"], 1):
            print(f"  {i}. {point}")
        print(f"\nSummary:\n{result['summary']}")

    def example_8_complex_chain(self):
        """Complex chain combining multiple patterns"""
        print("\n=== Example 8: Complex Chain ===")
        print("Parallel analysis (summary + keywords + sentiment) then final report\n")

        summary_prompt = ChatPromptTemplate.from_template("Summarize this in one sentence: {text}")
        keywords_prompt = ChatPromptTemplate.from_template("List 3 keywords from this text: {text}")
        sentiment_prompt = ChatPromptTemplate.from_template("What is the sentiment (positive/negative/neutral) of: {text}")

        parallel_analysis = RunnableParallel(
            summary=summary_prompt | self.llm | StrOutputParser(),
            keywords=keywords_prompt | self.llm | StrOutputParser(),
            sentiment=sentiment_prompt | self.llm | StrOutputParser(),
        )

        final_prompt = ChatPromptTemplate.from_template(
            "Based on this analysis:\n"
            "Summary: {summary}\n"
            "Keywords: {keywords}\n"
            "Sentiment: {sentiment}\n\n"
            "Write a brief report."
        )

        chain = {"text": RunnablePassthrough()} | parallel_analysis | final_prompt | self.llm | StrOutputParser()

        text = input("Enter text to analyze: ").strip()
        result = chain.invoke(text)
        print(f"\n{result}")

    def run(self):
        """Run interactive LCEL chain examples"""
        print("=" * 60)
        print("LCEL Chains Examples")
        print("=" * 60)

        examples = {
            "1": ("Simple Chain", self.example_1_simple_chain),
            "2": ("Sequential Chain", self.example_2_sequential_chain),
            "3": ("Parallel Chain", self.example_3_parallel_chain),
            "4": ("Passthrough Chain", self.example_4_passthrough),
            "5": ("ItemGetter Chain", self.example_5_itemgetter_chain),
            "6": ("Lambda Transform", self.example_6_lambda_transform),
            "7": ("Structured Output", self.example_7_structured_output),
            "8": ("Complex Chain", self.example_8_complex_chain),
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
    examples = LCELChainExamples()
    examples.run()


if __name__ == "__main__":
    main()
