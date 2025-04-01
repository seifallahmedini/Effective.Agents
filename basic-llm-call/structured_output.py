import os
import json
import logging
from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field, ValidationError
from openai import AzureOpenAI
from dotenv import load_dotenv

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
        raise ValueError("Azure OpenAI API key and endpoint must be provided")
    
    logger.info(f"Using Azure OpenAI endpoint: {api_base}")
    logger.info(f"Using deployment: {deployment_name}")
    
    try:
        # Initialize the AzureOpenAI client
        client = AzureOpenAI(
            api_key=api_key,
            api_version=api_version,
            azure_endpoint=api_base,
        )
        
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
        
        # Create the messages for the chat completion
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": query}
        ]
        
        # Call the OpenAI API
        response = client.chat.completions.create(
            model=deployment_name,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            response_format={"type": "json_object"}
        )
        
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
        
    except Exception as e:
        logger.error(f"Error calling Azure OpenAI with structured output: {str(e)}")
        raise

# Example usage of a custom response model
class ProductRecommendation(BaseModel):
    product_name: str = Field(..., description="Name of the product")
    price: float = Field(..., description="Price of the product")
    rating: float = Field(..., ge=0, le=5, description="Rating out of 5 stars")
    pros: List[str] = Field(..., description="List of pros/benefits")
    cons: List[str] = Field(..., description="List of cons/drawbacks")

class ProductRecommendations(BaseModel):
    query: str = Field(..., description="The original query")
    product_category: str = Field(..., description="Category of products being recommended")
    recommendations: List[ProductRecommendation] = Field(..., description="List of product recommendations")
    summary: str = Field(..., description="Summary of recommendations")
    timestamp: str = Field(..., description="ISO format timestamp of the response")

if __name__ == "__main__":
    # Example 1: Using the default StructuredResponse model
    query = "Explain the benefits of using MCP (Model Context Protocol) in AI applications."
    response = call_azure_openai_with_structured_output(query)
    print("\n=== Structured Response Example ===")
    print(response.model_dump_json(indent=2))
    
    # Example 2: Using a custom response model for product recommendations
    product_query = "Recommend the best noise-cancelling headphones"
    product_response = call_azure_openai_with_structured_output(
        query=product_query,
        output_schema=ProductRecommendations,
        temperature=0.5
    )
    print("\n=== Product Recommendations Example ===")
    print(product_response.model_dump_json(indent=2))