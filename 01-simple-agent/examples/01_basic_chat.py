import os
from openai import AzureOpenAI
from examples.settings import APP_SETTINGS 

client = AzureOpenAI(
    api_version=APP_SETTINGS.AZURE_OPENAI_API_VERSION,
    azure_endpoint=APP_SETTINGS.AZURE_OPENAI_ENDPOINT,
    api_key=APP_SETTINGS.AZURE_OPENAI_API_KEY,
)

response = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant.",
        },
        {
            "role": "user",
            "content": "Xin chào?",
        }
    ],
    max_completion_tokens=13107,
    temperature=1.0,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0,
    model=APP_SETTINGS.AZURE_OPENAI_DEPLOYMENT_NAME,
)

print(response.choices[0].message.content)