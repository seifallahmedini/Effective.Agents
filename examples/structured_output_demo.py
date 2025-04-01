"""Example demonstrating structured output with Pydantic models."""
from typing import List, Optional
from pydantic import BaseModel, Field
from basic_llm_call.core import call_azure_openai_with_structured_output

class ProductFeature(BaseModel):
    """A feature of a product with its rating."""
    name: str = Field(..., description="Name of the feature")
    rating: float = Field(..., ge=0.0, le=5.0, description="Rating from 0-5")
    description: str = Field(..., description="Feature description")

class ProductReview(BaseModel):
    """A product review with features and metadata."""
    product_name: str = Field(..., description="Name of the product")
    features: List[ProductFeature] = Field(..., description="List of product features")
    overall_rating: float = Field(..., ge=0.0, le=5.0, description="Overall product rating")
    purchase_date: Optional[str] = Field(None, description="Date of purchase in ISO format")

class ProductResponse(BaseModel):
    """Detailed product analysis response."""
    product_name: str = Field(..., description="Name of the product")
    category: str = Field(..., description="Product category")
    features: List[ProductFeature] = Field(..., description="List of product features")
    reviews: List[ProductReview] = Field(..., description="List of product reviews")
    average_rating: float = Field(..., ge=0.0, le=5.0, description="Average rating")
    recommendation: str = Field(..., description="Overall recommendation")
    timestamp: str = Field(..., description="ISO format timestamp of the analysis")

def run_structured_output_example():
    """
    Example: Using structured output with custom Pydantic models
    This example demonstrates how to use structured output with custom schemas
    to get detailed, strongly-typed responses from the model.
    """
    # Example 1: Using the default StructuredResponse model
    query = "Explain the benefits of using Model Context Protocol (MCP) in AI applications."
    
    print("\n=== Structured Output Example: Default Schema ===")
    result = call_azure_openai_with_structured_output(query)
    
    print("\nQuery:", result.query)
    print("\nItems:")
    for item in result.items:
        print(f"\n- {item.title} (Confidence: {item.confidence:.2f})")
        print(f"  Description: {item.description}")
        if item.tags:
            print(f"  Tags: {', '.join(item.tags)}")
    
    print(f"\nSummary: {result.summary}")
    print(f"Timestamp: {result.timestamp}")
    
    # Example 2: Using a custom schema for product analysis
    product_query = "Analyze the Sony WH-1000XM4 noise-cancelling headphones, including features and user reviews."
    
    print("\n=== Structured Output Example: Custom Product Schema ===")
    product_result = call_azure_openai_with_structured_output(
        query=product_query,
        output_schema=ProductResponse,
        temperature=0.5
    )
    
    print(f"\nProduct: {product_result.product_name}")
    print(f"Category: {product_result.category}")
    print(f"\nFeatures:")
    for feature in product_result.features:
        print(f"- {feature.name}: {feature.rating}/5")
        print(f"  {feature.description}")
    
    print(f"\nAverage Rating: {product_result.average_rating:.1f}/5.0")
    print(f"Reviews: {len(product_result.reviews)} total")
    for review in product_result.reviews:
        print(f"\n- {review.title} ({review.rating}/5)")
        print(f"  Pros: {', '.join(review.pros)}")
        print(f"  Cons: {', '.join(review.cons)}")
    
    print(f"\nRecommendation: {product_result.recommendation}")
    print(f"Analysis Time: {product_result.timestamp}")
    
    return {
        "default_result": result,
        "product_result": product_result
    }

if __name__ == "__main__":
    run_structured_output_example()