import os
import logging
from dotenv import load_dotenv
from util import llm_call_with_retry

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

def multi_step_workflow(user_query: str) -> dict:
    """
    A more complex workflow that uses multiple calls to process information.
    
    Args:
        user_query: The user's question or instruction
    
    Returns:
        A dictionary with the results of the multi-step process
    """
    logger.info(f"Starting multi-step workflow for query: {user_query}")
    results = {}
    
    # Step 1: Analyze the query to determine intent
    analysis_prompt = [
        {"role": "system", "content": "You are an AI assistant that analyzes user queries to determine their intent."},
        {"role": "user", "content": f"Analyze this query and categorize the primary intent: {user_query}"}
    ]
    
    try:
        analysis_response = llm_call_with_retry(prompt=analysis_prompt)
        # Updated to work with the new OpenAI API response format
        intent_analysis = analysis_response.choices[0].message.content.strip()
        results["intent_analysis"] = intent_analysis
        logger.info(f"Query intent analyzed: {intent_analysis[:50]}...")
        
        # Step 2: Generate a response based on the intent
        response_prompt = [
            {"role": "system", "content": "You are a helpful assistant providing information."},
            {"role": "user", "content": user_query},
            {"role": "assistant", "content": f"I understand your intent is related to: {intent_analysis}"},
            {"role": "user", "content": "Please provide a helpful response to my query."}
        ]
        
        response = llm_call_with_retry(prompt=response_prompt)
        # Updated to work with the new OpenAI API response format
        final_answer = response.choices[0].message.content.strip()
        results["final_answer"] = final_answer
        logger.info("Multi-step workflow completed successfully")
        
        return results
    except Exception as e:
        logger.error(f"Error in multi-step workflow: {str(e)}")
        return {"error": str(e)}


if __name__ == "__main__":
    # Example usage
    query = "What is an MCP (Model Context Protocol)?"
    
    print("\n=== Multi-step Workflow ===")
    multi_step_result = multi_step_workflow(query)
    print("Intent Analysis:", multi_step_result.get("intent_analysis", "Error"))
    print("Final Answer:", multi_step_result.get("final_answer", "Error"))