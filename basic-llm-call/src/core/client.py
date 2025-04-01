import os
import logging
from typing import Dict, Any, List, Optional, cast
from openai import AzureOpenAI
from dotenv import load_dotenv

from .interfaces import OpenAIClient, ChatCompletionParams

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

class AzureOpenAIClient(OpenAIClient):
    def __init__(self, api_key: str = None, api_base: str = None, api_version: str = None, deployment_name: str = None):
        """Initialize the Azure OpenAI client with configuration."""
        self.api_key = api_key or os.environ.get("AZURE_OPENAI_API_KEY")
        self.api_base = api_base or os.environ.get("AZURE_OPENAI_ENDPOINT")
        self.api_version = api_version or os.environ.get("AZURE_OPENAI_API_VERSION", "2023-05-15")
        self.deployment_name = deployment_name or self._get_deployment_name()

        if not self.api_key or not self.api_base:
            raise ValueError("Azure OpenAI API key and endpoint must be provided")

        logger.info(f"Using Azure OpenAI endpoint: {self.api_base}")
        self.client = AzureOpenAI(
            api_key=self.api_key,
            api_version=self.api_version,
            azure_endpoint=self.api_base,
        )

    def _get_deployment_name(self, model: str = None) -> str:
        """Get the deployment name to use for Azure OpenAI."""
        model = model or os.environ.get("AZURE_OPENAI_MODEL", "gpt-4o")
        return os.environ.get("AZURE_OPENAI_DEPLOYMENT", model)

    def create_chat_completion(self, **params: Any) -> Any:
        """
        Create a chat completion with optional tools.
        Enforces strict parameter checking using ChatCompletionParams.
        """
        # Cast the params to our TypedDict to ensure type safety
        chat_params = cast(ChatCompletionParams, params)
        
        # Set required parameters
        chat_params["model"] = self.deployment_name
        
        # Validate required parameters
        if "messages" not in chat_params:
            raise ValueError("messages parameter is required")
            
        # Filter out None values to avoid API errors
        filtered_params = {k: v for k, v in chat_params.items() if v is not None}
        
        # Create completion with validated parameters
        return self.client.chat.completions.create(**filtered_params)