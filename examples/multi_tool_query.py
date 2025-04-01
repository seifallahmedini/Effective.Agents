"""Example demonstrating multi-tool query usage."""
import json
from basic_llm_call.core import create_default_service

def run_multi_tool_query_example():
    """
    Example 4: Multi-tool query
    This example demonstrates a complex query that should trigger multiple tool
    functions in parallel (weather and calendar).
    """
    multi_query = "What's the weather like today and what's on my calendar?"
    
    print("\n=== Tool Calling Example: Multi-Tool Query ===")
    service = create_default_service()
    result = service.process_query(multi_query)
    
    print(f"Number of tool calls: {len(result['function_calls'])}")
    for i, call in enumerate(result["function_calls"]):
        print(f"\nTool {i+1}: {call['function_name']}")
        print(f"Arguments: {call['function_args']}")
        print(f"Response: {json.dumps(call['function_response'], indent=2)}")
    
    print(f"\nFinal response: {result['final_response']}")
    
    return result

if __name__ == "__main__":
    run_multi_tool_query_example()