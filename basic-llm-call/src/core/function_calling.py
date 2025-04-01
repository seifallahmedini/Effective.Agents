import logging
from typing import List, Dict, Any, Optional, cast
from openai import AzureOpenAI

from .interfaces import OpenAIClient, ToolExecutor, ToolProvider, ChatCompletionParams
from .client import AzureOpenAIClient
from ..tools.definitions import DefaultToolProvider
from ..tools.executor import DefaultToolExecutor

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ToolCallingService:
    """Service for handling tool-enabled conversations with OpenAI."""

    def __init__(
        self,
        client: OpenAIClient,
        tool_provider: ToolProvider,
        tool_executor: ToolExecutor,
        max_function_calls: int = 5
    ):
        """Initialize the service with its dependencies."""
        self.client = client
        self.tool_provider = tool_provider
        self.tool_executor = tool_executor
        self.max_function_calls = max_function_calls

    def process_query(
        self,
        query: str,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        parallel_tool_calls: bool = True,
    ) -> Dict[str, Any]:
        """Process a query using the tool-enabled language model."""
        conversation = []
        function_calls = []

        try:
            conversation.append({"role": "user", "content": query})

            call_count = 0
            while call_count < self.max_function_calls:
                # Create completion params with strict typing
                completion_params: ChatCompletionParams = {
                    "messages": conversation,
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                }

                # Add tool-related parameters if tools are available
                tools = self.tool_provider.get_available_tools()
                if tools:
                    completion_params.update({
                        "tools": tools,
                        "tool_choice": "auto",
                        "parallel_tool_calls": parallel_tool_calls
                    })

                # Make an API call with tool definitions
                response = self.client.create_chat_completion(**completion_params)

                message = response.choices[0].message
                conversation.append({"role": message.role, "content": message.content or ""})

                if message.tool_calls:
                    tool_calls_list = message.tool_calls
                    call_count += len(tool_calls_list)

                    conversation[-1] = {
                        "role": message.role,
                        "content": message.content or "",
                        "tool_calls": [
                            {
                                "id": tc.id,
                                "type": tc.type,
                                "function": {
                                    "name": tc.function.name,
                                    "arguments": tc.function.arguments
                                }
                            } for tc in tool_calls_list
                        ]
                    }

                    for tool_call in tool_calls_list:
                        (function_call_result, conversation_add) = self.tool_executor.execute_tool(
                            {
                                "id": tool_call.id,
                                "function": {
                                    "name": tool_call.function.name,
                                    "arguments": tool_call.function.arguments
                                }
                            }
                        )
                        function_calls.append(function_call_result)
                        conversation.append(conversation_add)
                else:
                    return {
                        "conversation": conversation,
                        "function_calls": function_calls,
                        "final_response": message.content
                    }

            # If we've reached max function calls, get a final response
            final_response = self.client.create_chat_completion(
                messages=conversation,
                temperature=temperature,
                max_tokens=max_tokens
            )

            final_message = final_response.choices[0].message
            conversation.append({"role": final_message.role, "content": final_message.content})

            return {
                "conversation": conversation,
                "function_calls": function_calls,
                "max_calls_reached": True,
                "final_response": final_message.content
            }

        except Exception as e:
            logger.error(f"Error in tool-enabled conversation: {str(e)}")
            raise

def create_default_service(
    api_key: str = None,
    api_base: str = None,
    api_version: str = None,
    deployment_name: str = None,
    max_function_calls: int = 5
) -> ToolCallingService:
    """Create a ToolCallingService with default implementations."""
    client = AzureOpenAIClient(api_key, api_base, api_version, deployment_name)
    tool_provider = DefaultToolProvider()
    tool_executor = DefaultToolExecutor(tool_provider.get_function_registry())
    
    return ToolCallingService(
        client=client,
        tool_provider=tool_provider,
        tool_executor=tool_executor,
        max_function_calls=max_function_calls
    )