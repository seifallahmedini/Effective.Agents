import sys
import os
import json
import datetime

# Add parent directory to path to import functions
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from function_calling import call_azure_openai_with_tools

def run_calendar_query_example():
    """
    Example 2: Calendar query (should trigger single function call)
    This example demonstrates a query about calendar events that should trigger
    the check_calendar tool function.
    """
    today = datetime.date.today().isoformat()
    calendar_query = f"What's on my calendar for {today}?"
    
    print("\n=== Tool Calling Example: Calendar Query (Single Tool) ===")
    calendar_result = call_azure_openai_with_tools(calendar_query)
    
    if calendar_result["function_calls"]:
        for i, call in enumerate(calendar_result["function_calls"]):
            print(f"Tool {i+1}: {call['function_name']}")
            print(f"Arguments: {call['function_args']}")
            print(f"Response: {json.dumps(call['function_response'], indent=2)}")
    else:
        print("No tools called")
    
    print(f"Final response: {calendar_result['final_response']}")
    
    return calendar_result

if __name__ == "__main__":
    run_calendar_query_example()