from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.output_parsers import (
    JsonOutputParser,
    StrOutputParser,
    CommaSeparatedListOutputParser,
)
from pydantic import BaseModel, Field
from typing import List
import sys
from pathlib import Path
import json

sys.path.append(str(Path(__file__).parent.parent))
from settings import APP_SETTINGS


# Pydantic models for structured output
class Person(BaseModel):
    """Information about a person"""

    name: str = Field(description="The person's full name")
    age: int = Field(description="The person's age in years")
    occupation: str = Field(description="The person's job or profession")
    hobbies: List[str] = Field(description="List of the person's hobbies")


class BookReview(BaseModel):
    """Book review structure"""

    title: str = Field(description="Book title")
    author: str = Field(description="Book author")
    rating: int = Field(description="Rating from 1 to 5")
    summary: str = Field(description="Brief summary of the review")
    pros: List[str] = Field(description="Positive aspects")
    cons: List[str] = Field(description="Negative aspects")


class Recipe(BaseModel):
    """Recipe structure"""

    name: str = Field(description="Recipe name")
    cuisine: str = Field(description="Type of cuisine")
    ingredients: List[str] = Field(description="List of ingredients")
    instructions: List[str] = Field(description="Step-by-step cooking instructions")
    prep_time: int = Field(description="Preparation time in minutes")
    cook_time: int = Field(description="Cooking time in minutes")


class OutputParserExamples:
    """Demonstrates different types of output parsers"""

    def __init__(self):
        self.llm = AzureChatOpenAI(
            azure_endpoint=APP_SETTINGS.AZURE_OPENAI_ENDPOINT,
            api_key=APP_SETTINGS.AZURE_OPENAI_API_KEY,
            azure_deployment=APP_SETTINGS.AZURE_OPENAI_DEPLOYMENT_NAME,
            api_version=APP_SETTINGS.AZURE_OPENAI_API_VERSION,
            temperature=0.7,
        )

    def example_1_json_parser(self):
        """Parse JSON output with Pydantic model"""
        print("\n=== Example 1: JSON Output Parser ===")
        print("Extract structured data: name, age, occupation, hobbies\n")

        parser = JsonOutputParser(pydantic_object=Person)

        prompt = PromptTemplate(
            template="Generate information about a fictional {profession}.\n{format_instructions}\n",
            input_variables=["profession"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        profession = input("Enter a profession: ").strip()
        chain = prompt | self.llm | parser
        result = chain.invoke({"profession": profession})

        print(f"\nName: {result['name']}")
        print(f"Age: {result['age']}")
        print(f"Occupation: {result['occupation']}")
        print(f"Hobbies: {', '.join(result['hobbies'])}")

    def example_2_list_parser(self):
        """Parse comma-separated list output"""
        print("\n=== Example 2: List Output Parser ===")
        print("Extract list of items\n")

        parser = CommaSeparatedListOutputParser()

        prompt = PromptTemplate(
            template="List {count} {category}.\n{format_instructions}\n",
            input_variables=["count", "category"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        count = input("How many items? ").strip()
        category = input("What category (e.g., countries, programming languages)? ").strip()

        chain = prompt | self.llm | parser
        result = chain.invoke({"count": count, "category": category})

        print()
        for i, item in enumerate(result, 1):
            print(f"  {i}. {item}")

    def example_3_book_review_parser(self):
        """Parse structured book review"""
        print("\n=== Example 3: Book Review Parser ===")

        parser = JsonOutputParser(pydantic_object=BookReview)

        prompt = PromptTemplate(
            template="Write a review for the book '{book_title}' by {author}.\n{format_instructions}\n",
            input_variables=["book_title", "author"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        print("Generate structured book review\n")

        book_title = input("Enter book title: ").strip()
        author = input("Enter author name: ").strip()

        chain = prompt | self.llm | parser
        result = chain.invoke({"book_title": book_title, "author": author})

        print("\n" + "=" * 60)
        print(f"Book Review: {result['title']}")
        print("=" * 60)
        print(f"Author: {result['author']}")
        print(f"Rating: {'*' * result['rating']} ({result['rating']}/5)")
        print(f"\nSummary:\n{result['summary']}")
        print("\nPros:")
        for pro in result["pros"]:
            print(f"  + {pro}")
        print("\nCons:")
        for con in result["cons"]:
            print(f"  - {con}")

    def example_4_recipe_parser(self):
        """Parse structured recipe"""
        print("\n=== Example 4: Recipe Parser ===")

        parser = JsonOutputParser(pydantic_object=Recipe)

        prompt = PromptTemplate(
            template="Create a {cuisine} recipe for {dish}.\n{format_instructions}\n",
            input_variables=["cuisine", "dish"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        print("Generate structured recipe\n")

        cuisine = input("Enter cuisine type (e.g., Italian, Mexican): ").strip()
        dish = input("Enter dish name: ").strip()

        chain = prompt | self.llm | parser
        result = chain.invoke({"cuisine": cuisine, "dish": dish})

        print("\n" + "=" * 60)
        print(f"Recipe: {result['name']}")
        print("=" * 60)
        print(f"Cuisine: {result['cuisine']}")
        print(f"Prep time: {result['prep_time']} minutes")
        print(f"Cook time: {result['cook_time']} minutes")
        print(f"Total time: {result['prep_time'] + result['cook_time']} minutes")

        print("\nIngredients:")
        for ingredient in result["ingredients"]:
            print(f"  - {ingredient}")

        print("\nInstructions:")
        for i, instruction in enumerate(result["instructions"], 1):
            print(f"  {i}. {instruction}")

    def example_5_string_parser(self):
        """Simple string output parser"""
        print("\n=== Example 5: String Output Parser ===")
        print("Basic text output\n")

        parser = StrOutputParser()

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "You are a helpful assistant that answers questions concisely."),
                ("user", "{question}"),
            ]
        )

        question = input("Enter your question: ").strip()
        chain = prompt | self.llm | parser
        result = chain.invoke({"question": question})

        print(f"\n{result}")

    def example_6_error_handling(self):
        """Demonstrate parser error handling"""
        print("\n=== Example 6: Parser Error Handling ===")
        print("Testing output validation\n")

        parser = JsonOutputParser(pydantic_object=Person)

        prompt = PromptTemplate(
            template="Tell me about {name} in a casual way. Include their name, age, occupation, and hobbies.\n{format_instructions}\n",
            input_variables=["name"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        name = input("Enter a person's name: ").strip()
        chain = prompt | self.llm | parser

        try:
            result = chain.invoke({"name": name})
            print(f"\nName: {result['name']}")
            print(f"Age: {result['age']}")
            print(f"Occupation: {result['occupation']}")
            print(f"Hobbies: {', '.join(result['hobbies'])}")
        except Exception as e:
            print(f"\nParser error: {e}")

    def run(self):
        """Run interactive output parser examples"""
        print("=" * 60)
        print("Output Parsers Examples")
        print("=" * 60)

        examples = {
            "1": ("JSON Parser (Person)", self.example_1_json_parser),
            "2": ("List Parser", self.example_2_list_parser),
            "3": ("JSON Parser (Book Review)", self.example_3_book_review_parser),
            "4": ("JSON Parser (Recipe)", self.example_4_recipe_parser),
            "5": ("String Parser", self.example_5_string_parser),
            "6": ("Error Handling", self.example_6_error_handling),
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
    examples = OutputParserExamples()
    examples.run()


if __name__ == "__main__":
    main()
