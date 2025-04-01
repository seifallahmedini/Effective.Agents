import logging
import datetime
from typing import Dict, Any

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_weather(location: str, unit: str = "celsius") -> Dict[str, Any]:
    """Mock function to get weather data for a location."""
    logger.info(f"Getting weather for {location} in {unit}")
    
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
    """Mock function to check calendar events."""
    logger.info(f"Checking calendar for date: {date}")
    
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
    """Mock function to set a reminder."""
    logger.info(f"Setting reminder: {title} at {time}")
    
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
    """Get the current date and time."""
    logger.info(f"Getting datetime information for timezone: {timezone}, format: {format}")
    
    try:
        import pytz
        from datetime import datetime
        
        now_utc = datetime.now(pytz.UTC)
        
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
            now = datetime.now()
            timezone_name = "Local"
        
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