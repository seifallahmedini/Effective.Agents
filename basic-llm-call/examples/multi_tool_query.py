import sys
import os
import json

# Add parent directory to path to import functions
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from function_calling import call_azure_openai_with_tools

def run_multi_tool_query_example():
    """
    Example 4: Multi-function query (should trigger multiple tool calls)
    This example demonstrates a complex query that should trigger multiple tool calls
    in a single conversation, showcasing the parallel tool calling capability.
    """
    multi_query = "Set a reminder for my dentist appointment tomorrow at 11 AM, and check the weather for tomorrow and tell me if I need to take an umbrella with me. Also, what's on my calendar tomorrow?"
    
    print("\n=== Tool Calling Example: Multi-Tool Query ===")
    multi_result = call_azure_openai_with_tools(multi_query)
    
    print(f"Number of tool calls: {len(multi_result['function_calls'])}")
    for i, call in enumerate(multi_result["function_calls"]):
        print(f"\nTool {i+1}: {call['function_name']}")
        print(f"Arguments: {call['function_args']}")
        print(f"Response: {json.dumps(call['function_response'], indent=2)}")
    
    print(f"\nFinal response: {multi_result['final_response']}")
    
    return multi_result

if __name__ == "__main__":
    run_multi_tool_query_example()