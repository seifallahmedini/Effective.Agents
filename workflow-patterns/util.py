import os
import openai
from openai import AzureOpenAI
import logging
from typing import Dict, List, Union, Optional

# Make tenacity import optional
try:
    from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
    TENACITY_AVAILABLE = True
except ImportError:
    TENACITY_AVAILABLE = False
    print("Warning: tenacity package not found. Retry functionality will not be available.")
    print("To install tenacity, run: pip install tenacity")

logger = logging.getLogger(__name__)

# Error classes for the new OpenAI API
from openai import APIError, RateLimitError, APITimeoutError as Timeout
# ServiceUnavailableError is now covered by APIError in the newer versions
ServiceUnavailableError = APIError

def llm_call(
    prompt: Union[str, List[Dict]],
    model: str = None,
    temperature: float = 0.7,
    max_tokens: int = 1000,
    top_p: float = 1.0,
    frequency_penalty: float = 0.0,
    presence_penalty: float = 0.0,
    stop: Optional[List[str]] = None,
    api_key: str = None,
    api_base: str = None,
    api_version: str = None,
    api_type: str = "azure",
    deployment_name: str = None
) -> dict:
    """
    Makes a call to the Azure OpenAI model with the given prompt and parameters.
    
    Args:
        prompt: Either a string prompt or a list of message dictionaries for chat models
        model: The name of the model to use (for deployment_name if not specified)
        temperature: Controls randomness (0-1)
        max_tokens: Maximum number of tokens to generate
        top_p: Controls diversity via nucleus sampling
        frequency_penalty: Penalizes repeated tokens
        presence_penalty: Penalizes repeated topics
        stop: List of tokens that stop generation when encountered
        api_key: Azure OpenAI API key (defaults to environment variable)
        api_base: Azure OpenAI endpoint (defaults to environment variable)
        api_version: Azure OpenAI API version (defaults to environment variable)
        api_type: API type, defaults to "azure"
        deployment_name: The deployment name to use (if different from model)
        
    Returns:
        The response from the OpenAI API
    """
    try:
        # Get credentials from parameters or environment variables
        api_key = api_key or os.environ.get("AZURE_OPENAI_API_KEY")
        api_base = api_base or os.environ.get("AZURE_OPENAI_ENDPOINT")
        api_version = api_version or os.environ.get("AZURE_OPENAI_API_VERSION", "2023-05-15")
        
        if not model:
            model = os.environ.get("AZURE_OPENAI_MODEL", "gpt-4o")
            
        # Azure OpenAI uses deployment names, which may be the same as the model name
        if not deployment_name:
            deployment_name = os.environ.get("AZURE_OPENAI_DEPLOYMENT", model)
            
        # Check if we have the necessary credentials
        if not api_key or not api_base:
            raise ValueError("Azure OpenAI API key and endpoint must be provided either as parameters or environment variables")
        
        logger.info(f"Using Azure OpenAI endpoint: {api_base}")
        logger.info(f"Using deployment: {deployment_name}")
        
        # Initialize the AzureOpenAI client with the credentials
        client = AzureOpenAI(
            api_key=api_key,
            api_version=api_version,
            azure_endpoint=api_base,
        )
        
        # Determine if we're using chat completion or completion based on prompt type
        if isinstance(prompt, list):
            # Chat completion
            response = client.chat.completions.create(
                model=deployment_name,  # Use deployment name for Azure
                messages=prompt,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p,
                frequency_penalty=frequency_penalty,
                presence_penalty=presence_penalty,
                stop=stop
            )
            return response
        else:
            # For regular completion in the new API, we need to use chat completions with a user message
            response = client.chat.completions.create(
                model=deployment_name,  # Use deployment name for Azure
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p,
                frequency_penalty=frequency_penalty,
                presence_penalty=presence_penalty,
                stop=stop
            )
            return response
            
    except Exception as e:
        logger.error(f"Error calling Azure OpenAI: {str(e)}")
        raise

# Conditionally define the retry-enabled function
if TENACITY_AVAILABLE:
    @retry(
        retry=retry_if_exception_type((APIError, RateLimitError, ServiceUnavailableError, Timeout)),
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=2, max=60)
    )
    def llm_call_with_retry(*args, **kwargs):
        """
        A wrapper around llm_call with automatic retries for transient errors.
        Takes the same parameters as llm_call.
        """
        return llm_call(*args, **kwargs)
else:
    # Fallback version without retries
    def llm_call_with_retry(*args, **kwargs):
        """
        A fallback version of the retry function when tenacity is not available.
        Takes the same parameters as llm_call.
        """
        print("Warning: Using llm_call without retry support. Install tenacity for retry capabilities.")
        return llm_call(*args, **kwargs)
