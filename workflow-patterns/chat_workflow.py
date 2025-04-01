import os
import logging
from dotenv import load_dotenv
from util import llm_call_with_retry

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

def chat_workflow(messages: list) -> str:
    """
    A workflow that uses the chat format to maintain conversation context.
    
    Args:
        messages: List of message dictionaries in OpenAI chat format
    
    Returns:
        The model's response text
    """
    logger.info(f"Processing chat with {len(messages)} messages")
    
    try:
        # Use the retry version for more robust handling
        response = llm_call_with_retry(
            prompt=messages,
            temperature=0.8,
            max_tokens=500
        )
        # Updated to work with the new OpenAI API response format
        answer = response.choices[0].message.content.strip()
        logger.info("Successfully generated chat response")
        return answer
    except Exception as e:
        logger.error(f"Error in chat workflow: {str(e)}")
        return f"Sorry, I encountered an error: {str(e)}"


if __name__ == "__main__":
    # Example usage
    query = "What is an MCP (Model Context Protocol)?"
    
    print("\n=== Chat Workflow ===")
    chat_messages = [
        {"role": "system", "content": "You are a helpful assistant specializing in LLM Model Context Protocol."},
        {"role": "user", "content": query}
    ]
    chat_result = chat_workflow(chat_messages)
    print(f"Result: {chat_result}\n")