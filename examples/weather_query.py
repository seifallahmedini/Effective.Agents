"""Example demonstrating weather query tool usage."""
import json
from basic_llm_call.core import create_default_service

def run_weather_query_example():
    """
    Example 1: Weather query (should trigger single function call)
    This example demonstrates a simple query about weather that should trigger
    the get_weather tool function.
    """
    weather_query = "What's the weather like in London today?"
    
    print("\n=== Tool Calling Example: Weather Query (Single Tool) ===")
    service = create_default_service()
    result = service.process_query(weather_query)
    
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
    run_weather_query_example()