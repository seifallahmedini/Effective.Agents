"""
Azure OpenAI Tool Calling Framework

This package provides a framework for handling tool-enabled conversations with Azure OpenAI,
supporting function calling capabilities.
"""

from .src.core import (
    ToolCallingService,
    create_default_service,
    OpenAIClient,
    ToolExecutor,
    ToolProvider,
    ChatCompletionParams,
    AzureOpenAIClient
)

from .src.tools import (
    AVAILABLE_TOOLS,
    DefaultToolProvider,
    DefaultToolExecutor,
    FUNCTION_REGISTRY
)

# Main exports
__all__ = [
    'ToolCallingService',
    'create_default_service',
    'OpenAIClient',
    'ToolExecutor',
    'ToolProvider',
    'ChatCompletionParams',
    'AzureOpenAIClient',
    'AVAILABLE_TOOLS',
    'DefaultToolProvider',
    'DefaultToolExecutor',
    'FUNCTION_REGISTRY'
]