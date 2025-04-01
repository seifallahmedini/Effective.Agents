import sys
import os
import json

# Add parent directory to path to import functions
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from function_calling import call_azure_openai_with_tools

def run_weather_query_example():
    """
    Example 1: Weather query (should trigger single function call)
    This example demonstrates a simple query about weather that should trigger
    the get_weather tool function.
    """
    weather_query = "What's the weather like in London today?"
    
    print("\n=== Tool Calling Example: Weather Query (Single Tool) ===")
    weather_result = call_azure_openai_with_tools(weather_query)
    
    if weather_result["function_calls"]:
        for i, call in enumerate(weather_result["function_calls"]):
            print(f"Tool {i+1}: {call['function_name']}")
            print(f"Arguments: {call['function_args']}")
            print(f"Response: {json.dumps(call['function_response'], indent=2)}")
    else:
        print("No tools called")
    
    print(f"Final response: {weather_result['final_response']}")
    
    return weather_result

if __name__ == "__main__":
    run_weather_query_example()