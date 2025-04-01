import sys
import os
import json

# Add parent directory to path to import functions
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from function_calling import call_azure_openai_with_tools

def run_datetime_tool_demo():
    """
    Example 6: DateTime tool demo
    This example demonstrates the use of the get_datetime function to retrieve
    current time information across multiple time zones and day of week information.
    """
    datetime_query = "What's the current time in New York, Tokyo, and London? Also tell me what day of the week it is."
    
    print("\n=== Tool Calling Example: DateTime Tool Demo ===")
    datetime_result = call_azure_openai_with_tools(datetime_query)
    
    print(f"Number of tool calls: {len(datetime_result['function_calls'])}")
    for i, call in enumerate(datetime_result["function_calls"]):
        print(f"\nTool {i+1}: {call['function_name']}")
        print(f"Arguments: {call['function_args']}")
        print(f"Response: {json.dumps(call['function_response'], indent=2)}")
    
    print(f"\nFinal response: {datetime_result['final_response']}")
    
    return datetime_result

if __name__ == "__main__":
    run_datetime_tool_demo()