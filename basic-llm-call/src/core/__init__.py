"""
Core package for handling Azure OpenAI API interactions and base functionality.
"""

from .client import AzureOpenAIClient
from .interfaces import OpenAIClient, ToolExecutor, ToolProvider, ChatCompletionParams
from .function_calling import ToolCallingService, create_default_service
from .structured_output import (
    ResponseItem,
    StructuredResponse,
    call_azure_openai_with_structured_output
)

__all__ = [
    'AzureOpenAIClient',
    'OpenAIClient',
    'ToolExecutor',
    'ToolProvider',
    'ChatCompletionParams',
    'ToolCallingService',
    'create_default_service',
    'ResponseItem',
    'StructuredResponse',
    'call_azure_openai_with_structured_output'
]