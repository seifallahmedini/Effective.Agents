"""Example demonstrating a complex scenario with multiple steps."""
import json
from basic_llm_call.core import create_default_service

def run_complex_scenario_example():
    """
    Example 5: Complex scenario with weather decision making
    This example demonstrates a complex scenario that requires the model to first check
    calendar information, set a reminder, check the weather, and then make a decision
    based on the weather condition.
    """
    complex_query = "I have a dentist appointment tomorrow. Check my calendar to confirm the time, set a reminder for it, and check the weather. If it's going to rain, remind me to take an umbrella."
    
    print("\n=== Tool Calling Example: Complex Scenario ===")
    service = create_default_service()
    result = service.process_query(complex_query)
    
    print(f"Number of tool calls: {len(result['function_calls'])}")
    for i, call in enumerate(result["function_calls"]):
        print(f"\nTool {i+1}: {call['function_name']}")
        print(f"Arguments: {call['function_args']}")
        print(f"Response: {json.dumps(call['function_response'], indent=2)}")
        
    print(f"\nFinal response: {result['final_response']}")
    
    return result

if __name__ == "__main__":
    run_complex_scenario_example()