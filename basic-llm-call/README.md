# Basic LLM Call

A framework for handling tool-enabled conversations and structured outputs with Azure OpenAI, supporting advanced features like function calling and strongly-typed responses.

## Project Structure

```
basic-llm-call/
├── src/
│   ├── core/                 # Core functionality
│   │   ├── __init__.py
│   │   ├── client.py        # Azure OpenAI client
│   │   ├── interfaces.py    # Abstract base classes
│   │   ├── function_calling.py # Tool calling service
│   │   └── structured_output.py # Structured response handling
│   └── tools/               # Tool implementations
│       ├── __init__.py
│       ├── definitions.py   # Tool schemas and provider
│       ├── executor.py      # Tool execution logic
│       └── implementations.py # Concrete tool implementations
├── examples/               # Usage examples
│   ├── weather_query.py   # Basic tool usage
│   ├── calendar_query.py  # Calendar integration
│   ├── datetime_tool_demo.py # DateTime operations
│   ├── general_query.py   # Non-tool queries
│   ├── multi_tool_query.py # Parallel tool calls
│   ├── complex_scenario.py # Multi-step interactions
│   └── structured_output_demo.py # Typed response examples
├── requirements.txt       # Direct dependency installation
└── setup.py             # Package installation config
```

## Features

- **Type-safe Function Calling**: Strictly typed interfaces for tool definition and execution
- **Structured Output**: Pydantic model support for strongly-typed responses
- **Parallel Tool Execution**: Support for concurrent tool calls
- **Dependency Injection**: Extensible architecture for custom tools
- **Built-in Tools**: Ready-to-use implementations for common tasks:
  - Weather information
  - Calendar management
  - Reminder setting
  - DateTime operations

## Installation

### Using pip (recommended)

```bash
pip install -e .
```

### Direct Dependencies

```bash
pip install -r requirements.txt
```

## Quick Start

### Basic Tool Usage

```python
from src.core import create_default_service

# Create service with default implementations
service = create_default_service()

# Process a query
result = service.process_query("What's the weather like in London?")

print(f"Response: {result['final_response']}")
```

### Structured Output

```python
from src.core import call_azure_openai_with_structured_output
from pydantic import BaseModel, Field
from typing import List

class CustomResponse(BaseModel):
    title: str = Field(..., description="Response title")
    items: List[str] = Field(..., description="List of items")
    confidence: float = Field(..., ge=0.0, le=1.0)

# Get strongly-typed response
result = call_azure_openai_with_structured_output(
    "Analyze the text...",
    output_schema=CustomResponse
)

print(f"Title: {result.title}")
print(f"Confidence: {result.confidence}")
```

### Custom Tool Implementation

```python
from src.core import ToolProvider, ToolExecutor
from typing import List, Dict, Any

class MyToolProvider(ToolProvider):
    def get_available_tools(self) -> List[Dict[str, Any]]:
        return [{
            "type": "function",
            "function": {
                "name": "my_tool",
                "description": "Custom tool description",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "param1": {
                            "type": "string",
                            "description": "Parameter description"
                        }
                    },
                    "required": ["param1"]
                }
            }
        }]

    def get_function_registry(self) -> Dict[str, Any]:
        return {
            "my_tool": self.my_tool_implementation
        }

    def my_tool_implementation(self, param1: str) -> Dict[str, Any]:
        return {"result": f"Processed {param1}"}
```

## Configuration

The package uses environment variables for Azure OpenAI configuration:

```env
AZURE_OPENAI_API_KEY=your_api_key
AZURE_OPENAI_ENDPOINT=your_endpoint
AZURE_OPENAI_API_VERSION=2024-12-01-preview
AZURE_OPENAI_MODEL=gpt-4o
AZURE_OPENAI_DEPLOYMENT=gpt-4o
```

You can also pass these values directly to `create_default_service()` or individual client constructors.

## Development

Install development dependencies:

```bash
pip install -e ".[dev]"
```

This includes:
- pytest for testing
- black for code formatting
- isort for import sorting
- mypy for type checking

## Examples

The `examples/` directory contains various usage scenarios:

1. `weather_query.py`: Basic tool usage with weather information
2. `calendar_query.py`: Calendar integration example
3. `datetime_tool_demo.py`: DateTime operations across timezones
4. `general_query.py`: Non-tool query handling
5. `multi_tool_query.py`: Parallel tool execution
6. `complex_scenario.py`: Multi-step interaction flow
7. `structured_output_demo.py`: Strongly-typed response handling

Run any example:

```bash
python examples/weather_query.py
```

## License

MIT License - feel free to use this code in your projects.