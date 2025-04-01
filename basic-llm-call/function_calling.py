import os
import json
import logging
import datetime
from typing import List, Dict, Any, Union, Optional, Callable
from pydantic import BaseModel, Field
from openai import AzureOpenAI
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

class FunctionDefinition(BaseModel):
    """Definition of a function that the model can call."""
    name: str
    description: str
    parameters: Dict[str, Any]
    required: List[str] = Field(default_factory=list)

# Example function definitions that can be used with the model
WEATHER_TOOL = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get the current weather for a specific location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string", 
                    "description": "The city and state or country, e.g., 'San Francisco, CA' or 'Paris, France'"
                },
                "unit": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "description": "The temperature unit to use"
                }
            },
            "required": ["location"]
        }
    }
}

CALENDAR_TOOL = {
    "type": "function",
    "function": {
        "name": "check_calendar",
        "description": "Check the user's calendar for events on a specific date",
        "parameters": {
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "description": "The date to check, in ISO format (YYYY-MM-DD)"
                }
            },
            "required": ["date"]
        }
    }
}

REMINDER_TOOL = {
    "type": "function",
    "function": {
        "name": "set_reminder",
        "description": "Set a reminder for the user",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "The title or subject of the reminder"
                },
                "time": {
                    "type": "string",
                    "description": "The time for the reminder in ISO format (YYYY-MM-DDTHH:MM:SS)"
                },
                "description": {
                    "type": "string",
                    "description": "Optional additional details for the reminder"
                }
            },
            "required": ["title", "time"]
        }
    }
}

# New datetime function definition
DATETIME_TOOL = {
    "type": "function",
    "function": {
        "name": "get_datetime",
        "description": "Get the current date and time or convert between time zones",
        "parameters": {
            "type": "object",
            "properties": {
                "timezone": {
                    "type": "string",
                    "description": "The timezone to get the time for (e.g., 'UTC', 'America/New_York', 'Europe/London', 'Asia/Tokyo'). Default is local system time."
                },
                "format": {
                    "type": "string",
                    "description": "The format for the datetime output. Options: 'full' (date and time), 'date' (date only), 'time' (time only), 'iso' (ISO 8601 format). Default is 'full'."
                }
            }
        }
    }
}

# Example function implementations
def get_weather(location: str, unit: str = "celsius") -> Dict[str, Any]:
    """
    Mock function to get weather data for a location.
    In a real implementation, this would call a weather API.
    """
    logger.info(f"Getting weather for {location} in {unit}")
    
    # Mock response - in a real implementation, call a weather API
    if "london" in location.lower():
        temp = 15 if unit == "celsius" else 59
        condition = "Rainy"
    elif "tokyo" in location.lower():
        temp = 20 if unit == "celsius" else 68
        condition = "Clear"
    elif "new york" in location.lower():
        temp = 22 if unit == "celsius" else 72
        condition = "Partly Cloudy"
    else:
        temp = 25 if unit == "celsius" else 77
        condition = "Sunny"
    
    return {
        "location": location,
        "temperature": temp,
        "unit": unit,
        "condition": condition,
        "humidity": 65,
        "wind_speed": 10,
        "updated_at": datetime.datetime.now().isoformat()
    }

def check_calendar(date: str) -> Dict[str, Any]:
    """
    Mock function to check calendar events.
    In a real implementation, this would access the user's calendar.
    """
    logger.info(f"Checking calendar for date: {date}")
    
    # Mock response - in a real implementation, query a calendar API
    events = []
    if date == datetime.date.today().isoformat():
        events = [
            {"time": "09:00-10:00", "title": "Team meeting"},
            {"time": "12:00-13:00", "title": "Lunch with client"},
            {"time": "15:00-16:30", "title": "Project review"}
        ]
    elif date == (datetime.date.today() + datetime.timedelta(days=1)).isoformat():
        events = [
            {"time": "11:00-12:00", "title": "Dentist appointment"},
            {"time": "14:00-15:00", "title": "Weekly sync"}
        ]
    
    return {
        "date": date,
        "events": events,
        "total_events": len(events)
    }

def set_reminder(title: str, time: str, description: str = "") -> Dict[str, Any]:
    """
    Mock function to set a reminder.
    In a real implementation, this would create a reminder in a system.
    """
    logger.info(f"Setting reminder: {title} at {time}")
    
    # Mock response - in a real implementation, create a real reminder
    reminder_id = hash(f"{title}:{time}") % 10000
    
    return {
        "reminder_id": str(reminder_id),
        "title": title,
        "time": time,
        "description": description,
        "created_at": datetime.datetime.now().isoformat(),
        "status": "scheduled"
    }

def get_datetime(timezone: str = None, format: str = "full") -> Dict[str, Any]:
    """
    Get the current date and time, optionally in a specified timezone.
    
    Args:
        timezone: The timezone to get the time for (e.g., 'UTC', 'America/New_York')
                 If None, uses the local system timezone.
        format: The format for the output. Options: 'full', 'date', 'time', 'iso'
    
    Returns:
        Dictionary with datetime information
    """
    logger.info(f"Getting datetime information for timezone: {timezone}, format: {format}")
    
    try:
        # Import the module only when the function is called to avoid unnecessary dependencies
        import pytz
        from datetime import datetime
        
        # Get the current time in UTC
        now_utc = datetime.now(pytz.UTC)
        
        # Convert to the requested timezone if specified
        if timezone:
            try:
                tz = pytz.timezone(timezone)
                now = now_utc.astimezone(tz)
                timezone_name = timezone
            except pytz.exceptions.UnknownTimeZoneError:
                logger.warning(f"Unknown timezone: {timezone}, using UTC")
                now = now_utc
                timezone_name = "UTC"
        else:
            # Use the local timezone if none specified
            now = datetime.now()
            timezone_name = "Local"
        
        # Format the datetime according to the requested format
        if format.lower() == "date":
            formatted_date = now.strftime("%Y-%m-%d")
            formatted_time = None
        elif format.lower() == "time":
            formatted_date = None
            formatted_time = now.strftime("%H:%M:%S")
        elif format.lower() == "iso":
            formatted_date = now.strftime("%Y-%m-%d")
            formatted_time = now.strftime("%H:%M:%S")
            iso_format = now.isoformat()
        else:  # default to "full"
            formatted_date = now.strftime("%Y-%m-%d")
            formatted_time = now.strftime("%H:%M:%S")
        
        # Build the response
        response = {
            "timezone": timezone_name,
            "date": formatted_date,
            "time": formatted_time,
            "weekday": now.strftime("%A"),
            "timestamp": int(now.timestamp())
        }
        
        if format.lower() == "iso":
            response["iso_format"] = iso_format
            
        return response
        
    except ImportError:
        logger.error("pytz module not installed. Install with 'pip install pytz'")
        return {
            "error": "Missing dependency: pytz",
            "message": "The pytz module is not installed. Install with 'pip install pytz'",
            "current_system_time": datetime.datetime.now().isoformat()
        }

# Function registry maps function names to their implementations
FUNCTION_REGISTRY = {
    "get_weather": get_weather,
    "check_calendar": check_calendar,
    "set_reminder": set_reminder,
    "get_datetime": get_datetime
}

def call_azure_openai_with_tools(
    query: str,
    available_tools: List[Dict] = None,
    function_registry: Dict[str, Callable] = None,
    model: str = None,
    temperature: float = 0.7,
    max_tokens: int = 1000,
    api_key: str = None,
    api_base: str = None,
    api_version: str = None,
    deployment_name: str = None,
    max_function_calls: int = 5,  # Limit to prevent infinite loops
    parallel_tool_calls: bool = True  # Enable parallel tool calls
) -> Dict[str, Any]:
    """
    Call Azure OpenAI with tool capabilities for function calling.
    Supports multiple function calls in a single conversation.
    
    Args:
        query: The user query/message
        available_tools: List of tool definitions available to the model
        function_registry: Dictionary mapping function names to their implementations
        model: The model to use
        temperature: Controls randomness (0-1)
        max_tokens: Maximum number of tokens to generate
        api_key: Azure OpenAI API key
        api_base: Azure OpenAI endpoint
        api_version: Azure OpenAI API version
        deployment_name: The deployment name to use
        max_function_calls: Maximum number of function calls allowed in one conversation
        parallel_tool_calls: Enable parallel tool calling
        
    Returns:
        A dictionary with the conversation and function call results
    """
    # Use default functions if none provided
    if available_tools is None:
        available_tools = [WEATHER_TOOL, CALENDAR_TOOL, REMINDER_TOOL, DATETIME_TOOL]
        
    # Use default registry if none provided
    if function_registry is None:
        function_registry = FUNCTION_REGISTRY
        
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
    
    # Initialize the conversation history
    conversation = []
    # Track function calls for return value
    function_calls = []
    
    try:
        # Initialize the AzureOpenAI client
        client = AzureOpenAI(
            api_key=api_key,
            api_version=api_version,
            azure_endpoint=api_base,
        )
        
        # Start the conversation with the user query
        conversation.append({"role": "user", "content": query})
        
        # Loop to allow multiple function calls
        call_count = 0
        while call_count < max_function_calls:
            # Make an API call with tool definitions
            response = client.chat.completions.create(
                model=deployment_name,
                messages=conversation,
                tools=available_tools,
                tool_choice="auto",  # Let the model decide when to use tools
                parallel_tool_calls=parallel_tool_calls,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            message = response.choices[0].message
            conversation.append({"role": message.role, "content": message.content or ""})
            
            # Check if the model wants to call a tool
            if message.tool_calls:
                call_count += len(message.tool_calls)
                
                # Update the last message to include tool_calls details
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
                        } for tc in message.tool_calls
                    ]
                }
                
                # Process each tool call
                for tool_call in message.tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                    
                    logger.info(f"Model called function ({call_count}/{max_function_calls}): {function_name}")
                    
                    # Call the function if it exists in the registry
                    if function_name in function_registry:
                        function_to_call = function_registry[function_name]
                        function_response = function_to_call(**function_args)
                        
                        # Save function call information
                        function_calls.append({
                            "function_name": function_name,
                            "function_args": function_args,
                            "function_response": function_response
                        })
                        
                        # Add the function response to the conversation
                        conversation.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "name": function_name,
                            "content": json.dumps(function_response)
                        })
                    else:
                        logger.error(f"Function {function_name} not found in registry")
                        function_response = {"error": f"Function {function_name} not implemented"}
                        function_calls.append({
                            "function_name": function_name,
                            "function_args": function_args,
                            "function_response": function_response
                        })
                        
                        conversation.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "name": function_name,
                            "content": json.dumps(function_response)
                        })
            else:
                # No tool call, this is the final response
                return {
                    "conversation": conversation,
                    "function_calls": function_calls,
                    "final_response": message.content
                }
        
        # If we've reached max function calls, get a final response from the model
        final_response = client.chat.completions.create(
            model=deployment_name,
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
        logger.error(f"Error calling Azure OpenAI with tools: {str(e)}")
        raise


# For backwards compatibility, keep the old function name as an alias
call_azure_openai_with_functions = call_azure_openai_with_tools