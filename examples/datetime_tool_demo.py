"""Example demonstrating datetime tool usage."""
import json
from basic_llm_call.core import create_default_service

def run_datetime_tool_demo():
    """Run the datetime tool demo."""
    datetime_query = "What time is it in Tokyo right now?"
    
    print("\n=== Tool Calling Example: DateTime Operations ===")
    service = create_default_service()
    result = service.process_query(datetime_query)
    
    if result["function_calls"]:
        for i, call in enumerate(result["function_calls"]):
            print(f"\nTool {i+1}: {call['function_name']}")
            print(f"Arguments: {call['function_args']}")
            print(f"Response: {json.dumps(call['function_response'], indent=2)}")
    else:
        print("No tools called")
    
    print(f"\nFinal response: {result['final_response']}")
    
    return result

if __name__ == "__main__":
    run_datetime_tool_demo()