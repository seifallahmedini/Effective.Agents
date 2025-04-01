import sys
import os
import json

# Add parent directory to path to import functions
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from function_calling import call_azure_openai_with_tools

def run_general_query_example():
    """
    Example 3: General query (shouldn't trigger tool call)
    This example demonstrates a general knowledge query that should NOT trigger
    any tool functions, as the model can answer directly.
    """
    general_query = "Tell me about artificial intelligence."
    
    print("\n=== Tool Calling Example: General Query (No Tools) ===")
    general_result = call_azure_openai_with_tools(general_query)
    
    if general_result["function_calls"]:
        for i, call in enumerate(general_result["function_calls"]):
            print(f"Tool {i+1}: {call['function_name']}")
    else:
        print("No tools called (as expected)")
    
    print(f"Final response: {general_result['final_response']}")
    
    return general_result

if __name__ == "__main__":
    run_general_query_example()