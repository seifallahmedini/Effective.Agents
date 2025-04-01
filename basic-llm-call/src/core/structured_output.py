"""Structured output handling for Azure OpenAI responses."""
import os
import json
import logging
from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field, ValidationError
from openai import AzureOpenAI
from dotenv import load_dotenv

from .interfaces import ChatCompletionParams
from .client import AzureOpenAIClient

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

class ResponseItem(BaseModel):
    """A single item in the structured response."""
    title: str = Field(..., description="Title or name of the item")
    description: str = Field(..., description="Detailed description")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score (0.0-1.0)")
    tags: List[str] = Field(default_factory=list, description="Relevant tags or categories")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")

class StructuredResponse(BaseModel):
    """The main structured response from the model."""
    query: str = Field(..., description="The original query")
    items: List[ResponseItem] = Field(..., description="List of response items")
    summary: str = Field(..., description="Overall summary")
    timestamp: str = Field(..., description="ISO format timestamp of the response")

def call_azure_openai_with_structured_output(
    query: str,
    model: str = None,
    temperature: float = 0.7,
    max_tokens: int = 1000,
    output_schema: Union[BaseModel, Dict] = StructuredResponse,
    api_key: str = None,
    api_base: str = None,
    api_version: str = None,
    deployment_name: str = None
) -> BaseModel:
    """
    Call Azure OpenAI and return a structured response using Pydantic.

    Args:
        query: The user query to process
        model: The name of the model to use
        temperature: Controls randomness (0-1)
        max_tokens: Maximum number of tokens to generate
        output_schema: Pydantic model class or dict schema for structuring output
        api_key: Azure OpenAI API key
        api_base: Azure OpenAI endpoint
        api_version: Azure OpenAI API version
        deployment_name: The deployment name to use

    Returns:
        A structured response using the provided Pydantic model
    """
    # Initialize the client
    client = AzureOpenAIClient(api_key, api_base, api_version, deployment_name)
    
    # Get the schema as a dictionary
    if isinstance(output_schema, type) and issubclass(output_schema, BaseModel):
        schema_dict = output_schema.model_json_schema()
        schema_name = output_schema.__name__
    else:
        schema_dict = output_schema
        schema_name = "CustomSchema"
    
    # Create a system message with instructions for structured output
    system_message = f"""
    You are an AI assistant that always responds in JSON format according to this schema:
    {json.dumps(schema_dict, indent=2)}
    
    Your response must be valid JSON that conforms to this schema and can be parsed by Python's json.loads().
    Do not add any explanatory text before or after the JSON.
    Include the current time in ISO format as the timestamp.
    """
    
    # Create completion params with strict typing
    completion_params: ChatCompletionParams = {
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": query}
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
        "response_format": {"type": "json_object"}
    }
    
    # Call the OpenAI API
    response = client.create_chat_completion(**completion_params)
    
    # Extract and parse the JSON response
    json_response = response.choices[0].message.content.strip()
    parsed_response = json.loads(json_response)
    
    # Validate against the Pydantic model if provided
    if isinstance(output_schema, type) and issubclass(output_schema, BaseModel):
        try:
            validated_response = output_schema(**parsed_response)
            logger.info(f"Successfully validated response against {schema_name}")
            return validated_response
        except ValidationError as e:
            logger.error(f"Validation error: {str(e)}")
            raise
    else:
        # Return the parsed JSON directly if no Pydantic model
        logger.info("Returning unvalidated JSON response")
        return parsed_response