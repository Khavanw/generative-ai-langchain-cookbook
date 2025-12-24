from langchain_openai import AzureOpenAIEmbeddings
from settings import APP_SETTINGS

embeddings = AzureOpenAIEmbeddings(
    azure_endpoint=APP_SETTINGS.AZURE_OPENAI_ENDPOINT,
    api_key=APP_SETTINGS.AZURE_OPENAI_API_KEY,
    api_version=APP_SETTINGS.AZURE_OPENAI_API_VERSION,
    azure_deployment="text-embedding-3-small"  # Change to your embedding deployment name
)

# Define function specifications for function calling
test = ["ABC", "ấnnsnansans"]
print(embeddings.embed_documents(test))