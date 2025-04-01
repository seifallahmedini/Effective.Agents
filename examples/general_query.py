"""Example demonstrating general query handling without tool calls."""
from basic_llm_call.core import create_default_service

def run_general_query_example():
    """
    Example 3: General query (shouldn't trigger tool call)
    This example demonstrates a general knowledge query that should NOT trigger
    any tool functions, as the model can answer directly.
    """
    general_query = "Tell me about artificial intelligence."
    
    print("\n=== Tool Calling Example: General Query (No Tools) ===")
    service = create_default_service()
    result = service.process_query(general_query)
    
    if result["function_calls"]:
        for i, call in enumerate(result["function_calls"]):
            print(f"Tool {i+1}: {call['function_name']}")
    else:
        print("No tools called (as expected)")
    
    print(f"Final response: {result['final_response']}")
    
    return result

if __name__ == "__main__":
    run_general_query_example()