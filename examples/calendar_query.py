"""Example demonstrating calendar query tool usage."""
import json
import datetime
from basic_llm_call.core import create_default_service

def run_calendar_query_example():
    """
    Example 2: Calendar query (should trigger single function call)
    This example demonstrates a query about calendar events that should trigger
    the check_calendar tool function.
    """
    today = datetime.date.today().isoformat()
    calendar_query = f"What's on my calendar for {today}?"
    
    print("\n=== Tool Calling Example: Calendar Query (Single Tool) ===")
    service = create_default_service()
    result = service.process_query(calendar_query)
    
    if result["function_calls"]:
        for i, call in enumerate(result["function_calls"]):
            print(f"Tool {i+1}: {call['function_name']}")
            print(f"Arguments: {call['function_args']}")
            print(f"Response: {json.dumps(call['function_response'], indent=2)}")
    else:
        print("No tools called")
    
    print(f"Final response: {result['final_response']}")
    
    return result

if __name__ == "__main__":
    run_calendar_query_example()