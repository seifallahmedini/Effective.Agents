import os
import logging
from dotenv import load_dotenv
from util import llm_call

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

def single_prompt_workflow(user_query: str) -> str:
    """
    A simple workflow that sends a single prompt to the model and returns the response.
    
    Args:
        user_query: The user's question or instruction
    
    Returns:
        The model's response text
    """
    logger.info(f"Processing query: {user_query}")
    
    prompt = f"You are a helpful assistant. Please respond to this query: {user_query}"
    
    try:
        # Call the model using the basic function
        response = llm_call(prompt)
        # Updated to work with the new OpenAI API response format
        answer = response.choices[0].message.content.strip()
        logger.info("Successfully generated response")
        return answer
    except Exception as e:
        logger.error(f"Error in basic workflow: {str(e)}")
        return f"Sorry, I encountered an error: {str(e)}"


if __name__ == "__main__":
    # Example usage
    query = "What is an MCP (Model Context Protocol)?"
    
    print("\n=== Simple Prompt Workflow ===")
    simple_result = single_prompt_workflow(query)
    print(f"Result: {simple_result}\n")
