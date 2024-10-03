# Import necessary libraries
from dotenv import load_dotenv
import os
import langchain
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.cache import InMemoryCache

# Load environment variables from env file
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
    max_retries=2
)

# Define the Callback Function
def handle_response(response):
    """Callback function to handle the response from the LLM."""
    try:
        # Debugging: Print the raw response for verification
        print("Raw response:", response)  
        print("Response received:")
        print(response.content)  # Process and print the content of the response
        
        # Check if content is empty
        if not response.content:
            print("No content received in response.")
            return
        
        token_count = count_tokens(response.content)  # Count tokens in the response content
        print(f"Number of tokens: {token_count}")  # Print the number of tokens
    except Exception as e:
        print(f"Error processing response: {e}")  # Error handling for response processing

# Function to count tokens based on whitespace (a rough estimate)
def count_tokens(text):
    """Estimate the token count based on the number of words."""
    tokens = text.split()  # Split text into tokens based on whitespace
    return len(tokens)  # Return the number of tokens

# Create an Event System for managing the invocation of the LLM
class EventSystem:
    def __init__(self):
        self.callbacks = {}  # Dictionary to hold callbacks for different events

    def register_callback(self, event_name, callback):
        """Register a callback for a specific event."""
        if event_name not in self.callbacks:
            self.callbacks[event_name] = []  # Create a new list for callbacks if it doesn't exist
        self.callbacks[event_name].append(callback)  # Add the callback to the list

    def trigger_event(self, event_name, *args, **kwargs):
        """Trigger an event and call all registered callbacks."""
        if event_name in self.callbacks:  # Check if any callbacks are registered for the event
            for callback in self.callbacks[event_name]:
                try:
                    callback(*args, **kwargs)  # Call the callback with the provided arguments
                except Exception as e:
                    print(f"Error in callback for {event_name}: {e}")  # Handle errors in callback execution

# Create an Instance of the Event System
event_system = EventSystem()

# Register the Callback Function for LLM response handling
event_system.register_callback('response_received', handle_response)

# Function to invoke the LLM and trigger the response event
def invoke_llm(prompt):
    """Function to invoke the LLM with a given prompt."""
    response = llm.invoke(prompt)  # Invoke the LLM with the given prompt
    event_system.trigger_event('response_received', response)  # Trigger the response handling event

# Invoke the LLM with the first prompt and handle the response
invoke_llm("Tell about INDIA")

# Invoke the LLM with a second prompt and handle the response
invoke_llm("What doesn't fall from the tree?")