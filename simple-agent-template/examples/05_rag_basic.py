from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from langchain.tools import tool
from langchain.agents import create_agent
from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List, Optional
from pathlib import Path
from settings import APP_SETTINGS


def load_documents_from_directory(directory: str = "data") -> List[tuple[str, str]]:
    """Load all text files from a directory.
    
    Args:
        directory: Directory path containing text files
        
    Returns:
        List of tuples (content, filename)
    """
    documents = []
    
    # Get the script's directory and construct path to data folder
    script_dir = Path(__file__).parent.parent  # Go up to project root
    data_dir = script_dir / directory
    
    if not data_dir.exists():
        print(f"Warning: Directory '{data_dir}' not found.")
        return documents
    
    for file_path in data_dir.glob("*.txt"):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                documents.append((content, file_path.name))
            print(f"  Loading: {file_path.name}")
        except Exception as e:
            print(f"Error reading {file_path.name}: {e}")
    
    return documents


class RAGAgent:
    """A RAG (Retrieval-Augmented Generation) agent with in-memory vector store."""
    
    def __init__(self):
        """Initialize the RAG agent with embeddings and vector store."""
        # Initialize Azure OpenAI for chat
        self.llm = AzureChatOpenAI(
            azure_endpoint=APP_SETTINGS.AZURE_OPENAI_ENDPOINT,
            api_key=APP_SETTINGS.AZURE_OPENAI_API_KEY,
            api_version=APP_SETTINGS.AZURE_OPENAI_API_VERSION,
            deployment_name=APP_SETTINGS.AZURE_OPENAI_DEPLOYMENT_NAME,
            temperature=0.7,
        )
        
        # Initialize Azure OpenAI Embeddings
        self.embeddings = AzureOpenAIEmbeddings(
            azure_endpoint=APP_SETTINGS.AZURE_OPENAI_ENDPOINT,
            api_key=APP_SETTINGS.AZURE_OPENAI_API_KEY,
            api_version=APP_SETTINGS.AZURE_OPENAI_API_VERSION,
            azure_deployment="text-embedding-3-small"  # Change to your embedding deployment name
        )
        
        # Initialize in-memory vector store
        self.vector_store = InMemoryVectorStore(self.embeddings)
        
        # Text splitter for chunking documents
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        
        # Store document count
        self.doc_count = 0
        
        # Create RAG tool for the agent
        self.agent = self._create_agent()
    
    def _create_rag_tool(self):
        """Create a RAG retrieval tool."""
        @tool
        def search_documents(query: str) -> str:
            """Search the document knowledge base for relevant information.
            
            Args:
                query: The search query to find relevant documents
            """
            if self.doc_count == 0:
                return "No documents have been added to the knowledge base yet."
            
            try:
                # Retrieve relevant documents
                results = self.vector_store.similarity_search(query, k=3)
                
                if not results:
                    return "No relevant documents found."
                
                # Format results
                context = "\n\n".join([
                    f"Document {i+1}:\n{doc.page_content}"
                    for i, doc in enumerate(results)
                ])
                
                return f"Found {len(results)} relevant documents:\n\n{context}"
            except Exception as e:
                return f"Error searching documents: {str(e)}"
        
        return search_documents
    
    def _create_agent(self):
        """Create the agent with RAG capabilities."""
        search_tool = self._create_rag_tool()
        
        agent = create_agent(
            model=self.llm,
            tools=[search_tool],
            system_prompt="""You are a helpful AI assistant with access to a document knowledge base.

When answering questions:
1. Use the search_documents tool to find relevant information
2. Base your answers on the retrieved documents
3. If no relevant documents are found, say so clearly
4. Cite which document you're using when answering
5. Be concise and accurate

Always search the knowledge base before answering questions about specific topics."""
        )
        
        return agent
    
    def add_documents(self, texts: List[str], metadatas: Optional[List[dict]] = None) -> int:
        """Add documents to the vector store.
        
        Args:
            texts: List of text content to add
            metadatas: Optional list of metadata dicts for each text
            
        Returns:
            Number of chunks added
        """
        documents = []
        
        for i, text in enumerate(texts):
            # Split text into chunks
            chunks = self.text_splitter.split_text(text)
            
            # Create documents
            for chunk in chunks:
                metadata = metadatas[i].copy() if metadatas and i < len(metadatas) else {}
                metadata["source"] = metadata.get("source", f"document_{self.doc_count + i + 1}")
                documents.append(Document(page_content=chunk, metadata=metadata))
        
        # Add to vector store
        try:
            self.vector_store.add_documents(documents)
            self.doc_count += len(texts)
            print(f"  ✓ Successfully indexed {len(documents)} chunks into vector store")
            return len(documents)
        except Exception as e:
            print(f"  ✗ Error adding documents to vector store: {e}")
            raise
    
    def add_text(self, text: str, source: str = "manual_input") -> int:
        """Add a single text to the knowledge base.
        
        Args:
            text: Text content to add
            source: Source identifier for the text
            
        Returns:
            Number of chunks created
        """
        return self.add_documents([text], [{"source": source}])
    
    def query(self, question: str) -> dict:
        """Query the RAG agent with a question.
        
        Args:
            question: The question to ask
            
        Returns:
            Dictionary with response and metadata
        """
        result = self.agent.invoke({
            "messages": [{"role": "user", "content": question}]
        })
        
        # Extract tool calls
        tool_calls = []
        for msg in result["messages"]:
            if hasattr(msg, "tool_calls") and msg.tool_calls:
                for tool_call in msg.tool_calls:
                    tool_calls.append({
                        "name": tool_call["name"],
                        "args": tool_call["args"]
                    })
        
        # Get final response
        final_response = result["messages"][-1].content
        
        return {
            "response": final_response,
            "tool_calls": tool_calls,
            "used_rag": len(tool_calls) > 0
        }
    
    def get_stats(self) -> dict:
        """Get statistics about the knowledge base.
        
        Returns:
            Dictionary with statistics
        """
        return {
            "total_documents": self.doc_count,
            "vector_store_type": "InMemoryVectorStore",
            "embedding_model": "text-embedding-3-small"
        }
    
    def list_indexed_documents(self) -> List[dict]:
        """List all documents currently indexed in the vector store.
        
        Returns:
            List of document information dictionaries
        """
        if self.doc_count == 0:
            return []
        
        try:
            # Try to get a sample of documents using similarity search with a generic query
            # This is a workaround since InMemoryVectorStore doesn't expose all documents directly
            sample_results = self.vector_store.similarity_search("information", k=20)
            
            docs_info = []
            seen_sources = set()
            
            for doc in sample_results:
                source = doc.metadata.get('source', 'unknown')
                if source not in seen_sources:
                    seen_sources.add(source)
                    docs_info.append({
                        'source': source,
                        'preview': doc.page_content[:150] + "..." if len(doc.page_content) > 150 else doc.page_content,
                        'chunk_example': doc.page_content
                    })
            
            return docs_info
        except Exception as e:
            print(f"Error accessing documents: {e}")
            return []


def load_sample_documents() -> List[str]:
    """Load sample documents for demonstration."""
    return [
        """LangChain is a framework for developing applications powered by large language models (LLMs). 
        It provides tools for building context-aware applications that can reason and take actions. 
        Key features include chains for combining components, agents for autonomous decision-making, 
        and memory for maintaining conversation state. LangChain supports various LLM providers 
        including OpenAI, Azure OpenAI, and open-source models.""",
        
        """Retrieval-Augmented Generation (RAG) is a technique that enhances LLM responses by 
        retrieving relevant information from a knowledge base. The process involves three steps: 
        1) Converting documents into embeddings and storing them in a vector database, 
        2) Retrieving relevant documents based on user queries, 
        3) Augmenting the LLM prompt with retrieved context to generate accurate responses. 
        RAG is particularly useful for domain-specific applications and reduces hallucinations.""",
        
        """Azure OpenAI Service provides REST API access to OpenAI's powerful language models 
        including GPT-4, GPT-3.5-Turbo, and embedding models. It offers enterprise-grade security, 
        compliance, and regional availability. Key features include content filtering, 
        private networking, and integration with Azure services. The service supports both 
        chat completions and embeddings for building AI applications.""",
        
        """Vector databases are specialized databases designed to store and query high-dimensional 
        vectors (embeddings). They enable efficient similarity search using algorithms like 
        approximate nearest neighbor (ANN). Popular vector databases include Pinecone, Weaviate, 
        Qdrant, and Chroma. In-memory solutions like LangChain's InMemoryVectorStore are ideal 
        for development and small-scale applications.""",
        
        """Python is a high-level programming language known for its simplicity and readability. 
        It has become the primary language for AI and machine learning development due to its 
        extensive ecosystem of libraries. Key libraries include NumPy for numerical computing, 
        Pandas for data manipulation, TensorFlow and PyTorch for deep learning, and LangChain 
        for LLM application development."""
    ]


def main():
    """Main function to run the RAG demo."""
    print("=" * 60)
    print("RAG Agent with In-Memory Vector Store")
    print("=" * 60)
    print("\nInitializing RAG agent...")
    
    # Initialize RAG agent
    rag_agent = RAGAgent()
    
    print("\nCommands:")
    print("- 'add' - Add a document to knowledge base")
    print("- 'load' - Load documents from data folder")
    print("- 'list' - Show indexed documents")
    print("- 'stats' - Show knowledge base statistics")
    print("- 'exit' or 'quit' - End session")
    print("\nOtherwise, ask any question and the agent will search the knowledge base.")
    print("\n" + "=" * 60 + "\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            # Handle exit
            if user_input.lower() in ['exit', 'quit']:
                print("\nGoodbye!")
                break
            
            # Handle add document
            elif user_input.lower() == 'add':
                print("\nEnter document text (press Enter twice to finish):")
                lines = []
                while True:
                    line = input()
                    if not line:
                        break
                    lines.append(line)
                
                if lines:
                    text = "\n".join(lines)
                    chunks = rag_agent.add_text(text)
                    print(f"\nAdded document with {chunks} chunks to knowledge base.")
                else:
                    print("\nNo text entered.")
                continue
            
            # Handle load sample documents
            elif user_input.lower() == 'load':
                print("\n" + "=" * 50)
                print("Loading documents from data folder...")
                print("=" * 50)
                
                # Try to load from files first
                file_docs = load_documents_from_directory("data")
                
                if file_docs:
                    print(f"\nFound {len(file_docs)} text files")
                    texts = [content for content, _ in file_docs]
                    metadatas = [{"source": filename} for _, filename in file_docs]
                    
                    try:
                        chunks = rag_agent.add_documents(texts, metadatas)
                        print(f"\n✓ Successfully loaded {len(file_docs)} documents ({chunks} chunks).")
                        print("\nAvailable topics:")
                        print("- LangChain framework and components")
                        print("- RAG (Retrieval-Augmented Generation) technique")
                        print("- Azure OpenAI Service features")
                        print("- Vector databases and embeddings")
                        print("- Python for AI/ML development")
                        print("\nTry 'list' to see indexed documents or start asking questions!")
                    except Exception as e:
                        print(f"\n✗ Error loading documents: {e}")
                        print("Please check your Azure OpenAI embedding deployment configuration.")
                else:
                    # Fallback to sample documents
                    print("\nData folder not found, loading sample documents...")
                    sample_docs = load_sample_documents()
                    metadatas = [
                        {"source": "langchain_info"},
                        {"source": "rag_info"},
                        {"source": "azure_openai_info"},
                        {"source": "vector_db_info"},
                        {"source": "python_info"}
                    ]
                    
                    try:
                        chunks = rag_agent.add_documents(sample_docs, metadatas)
                        print(f"\n✓ Loaded {len(sample_docs)} sample documents ({chunks} chunks).")
                    except Exception as e:
                        print(f"\n✗ Error loading documents: {e}")
                
                continue
            
            # Handle stats
            elif user_input.lower() == 'stats':
                stats = rag_agent.get_stats()
                print("\n--- Knowledge Base Statistics ---")
                print(f"Total Documents: {stats['total_documents']}")
                print(f"Vector Store: {stats['vector_store_type']}")
                print(f"Embedding Model: {stats['embedding_model']}")
            
            # Handle list indexed documents
            elif user_input.lower() == 'list':
                docs = rag_agent.list_indexed_documents()
                if not docs:
                    print("\nNo documents indexed yet. Use 'load' to add documents.")
                else:
                    print("\n--- Indexed Documents ---")
                    for i, doc_info in enumerate(docs, 1):
                        print(f"\n{i}. Source: {doc_info['source']}")
                        print(f"   Preview: {doc_info['preview']}")
                    print("\n" + "-" * 25)
                continue
            
            # Query the agent
            print()
            result = rag_agent.query(user_input)
            
            # Display tool usage
            if result["used_rag"]:
                print("--- RAG Search Performed ---")
                for tool_call in result["tool_calls"]:
                    print(f"Query: {tool_call['args'].get('query', 'N/A')}")
                print("-" * 28)
            else:
                print("--- Direct Response (No RAG) ---")
            
            # Display response
            print(f"\nAssistant: {result['response']}")
            print("\n" + "-" * 60 + "\n")
            
        except KeyboardInterrupt:
            print("\n\nInterrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\nError: {str(e)}")
            print("Please try again.\n")


if __name__ == "__main__":
    main()
