from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Tuple, TypedDict, Literal

class ChatCompletionParams(TypedDict, total=False):
    """Parameters for chat completion requests."""
    model: str
    messages: List[Dict[str, str]]
    temperature: float
    max_tokens: int
    tools: Optional[List[Dict[str, Any]]]
    tool_choice: Literal["none", "auto"]
    parallel_tool_calls: bool
    stop: Optional[List[str]]
    presence_penalty: Optional[float]
    frequency_penalty: Optional[float]
    response_format: Optional[Dict[str, str]]

class ToolExecutor(ABC):
    @abstractmethod
    def execute_tool(self, tool_call: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Execute a tool call and return the result and conversation message."""
        pass

class OpenAIClient(ABC):
    @abstractmethod
    def create_chat_completion(self, **params: ChatCompletionParams) -> Any:
        """Create a chat completion with optional tools."""
        pass

class ToolProvider(ABC):
    @abstractmethod
    def get_available_tools(self) -> List[Dict[str, Any]]:
        """Get the list of available tools."""
        pass

    @abstractmethod
    def get_function_registry(self) -> Dict[str, Any]:
        """Get the function registry mapping names to implementations."""
        pass