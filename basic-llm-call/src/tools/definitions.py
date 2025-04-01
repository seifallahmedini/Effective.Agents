from typing import List, Dict, Any
from ..core.interfaces import ToolProvider
from .implementations import FUNCTION_REGISTRY

# Tool definitions
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

# List of all available tools
AVAILABLE_TOOLS = [WEATHER_TOOL, CALENDAR_TOOL, REMINDER_TOOL, DATETIME_TOOL]

class DefaultToolProvider(ToolProvider):
    """Default implementation of the ToolProvider interface."""
    
    def get_available_tools(self) -> List[Dict[str, Any]]:
        """Get the list of available tools."""
        return AVAILABLE_TOOLS
    
    def get_function_registry(self) -> Dict[str, Any]:
        """Get the function registry mapping names to implementations."""
        return FUNCTION_REGISTRY