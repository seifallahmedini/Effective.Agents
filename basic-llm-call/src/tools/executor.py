import json
import logging
from typing import Dict, Any, Callable, Tuple

from ..core.interfaces import ToolExecutor

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DefaultToolExecutor(ToolExecutor):
    def __init__(self, function_registry: Dict[str, Callable]):
        self.function_registry = function_registry

    def execute_tool(self, tool_call: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Execute a tool call and handle its response.
        
        Args:
            tool_call: The tool call details from the model
        
        Returns:
            Tuple of (function call result, conversation message)
        """
        function_name = tool_call["function"]["name"]
        function_args = json.loads(tool_call["function"]["arguments"])

        logger.info(f"Model called function: {function_name}")

        if function_name in self.function_registry:
            function_to_call = self.function_registry[function_name]
            function_response = function_to_call(**function_args)

            return {
                "function_name": function_name,
                "function_args": function_args,
                "function_response": function_response,
            }, {
                "role": "tool",
                "tool_call_id": tool_call["id"],
                "name": function_name,
                "content": json.dumps(function_response),
            }
        else:
            logger.error(f"Function {function_name} not found in registry")
            function_response = {"error": f"Function {function_name} not implemented"}
            return {
                "function_name": function_name,
                "function_args": function_args,
                "function_response": function_response,
            }, {
                "role": "tool",
                "tool_call_id": tool_call["id"],
                "name": function_name,
                "content": json.dumps(function_response),
            }