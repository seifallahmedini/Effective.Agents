"""
Root package for basic-llm-call framework.
"""

from .core import (
    ToolCallingService,
    create_default_service,
    OpenAIClient,
    ToolExecutor,
    ToolProvider,
    ChatCompletionParams,
    AzureOpenAIClient
)

from .tools import (
    AVAILABLE_TOOLS,
    DefaultToolProvider,
    DefaultToolExecutor,
    FUNCTION_REGISTRY
)

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