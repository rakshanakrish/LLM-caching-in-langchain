# Import necessary libraries
from dotenv import load_dotenv
import os

import langchain
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.cache import InMemoryCache
from langchain_community.callbacks.manager import get_openai_callback
from langchain_community.llms import OpenAI

# Load environment variables from .env file
load_dotenv()

# Set up in-memory cache
langchain.llm_cache = InMemoryCache()

# Retrieve the API key from environment variables
api_key = os.getenv("GOOGLE_API_KEY")

# Initialize the Gemini LLM (Google Generative AI)
llm = ChatGoogleGenerativeAI(
    model="gemini-pro",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2)

# Make a simple request to test if the setup works
response = llm.invoke("Tell about INDIA")
print(response.content)
