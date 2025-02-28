from datetime import datetime

from pydantic import BaseModel

from langchain.tools import StructuredTool
from langgraph.prebuilt import ToolNode

from services.features.schedule import add_event, update_event, delete_event, getEvents
from services.features.weather import get_weather
from services.features.get_available_time import get_available_time

class addEventArgs(BaseModel):
    line_id: str
    summary: str
    start_time: datetime
    end_time: datetime
    description: str = ""
    location: str = ""

class updateEventArgs(BaseModel):
    line_id: str
    event_id:str
    summary:str = None
    start_datetime:datetime = None
    end_datetime:datetime = None
    description:str = None
    location:str = None

class deleteEventArgs(BaseModel):
    line_id: str
    event_id:str 

class getEventArgs(BaseModel):
    line_id: str
    start_datetime: datetime
    end_datetime: datetime

class get_available_timeArgs(BaseModel):
    line_id: str
    time_range:str = "tomorrow",
    specific_date:str = None
    timezone:str = "Asia/Tokyo"

class get_weatherArgs(BaseModel):
    city: str
    dt:datetime

def askUser():
    return True, "Think about what you would like to confirm or ask the user."

def confirmUser():
    return True, "Ask the user to confirm that the process is correct before executing the function"

tool_list = [
    StructuredTool.from_function(
        name = "addEvent",
        func = add_event,
        args_schema = addEventArgs,
        description = "Add new events to the calendar based on detailed information."
    ),

    StructuredTool.from_function(
        name = "updateEvent",
        func = update_event,
        args_schema = updateEventArgs,
        description = "Edit existing events by modifying event details based on the parameters provided."
    ),

    StructuredTool.from_function(
        name = "deleteEvent",
        func = delete_event,
        args_schema = deleteEventArgs,
        description = "Delete the events."
    ),

    StructuredTool.from_function(
        name = "getEvents",
        func = getEvents,
        args_schema = getEventArgs,
        description = "Retrieves and displays a list of scheduled events."
    ),

    StructuredTool.from_function(
        name = "GetAvailableTime",
        func = get_available_time,
        args_schema = get_available_timeArgs,
        description = "Get the calendar for available times.time_rage=today,tomorrow,this_week,next_week,this_month,next_month",
    ),

    StructuredTool.from_function(
        name = "getWeather",
        func = get_weather,
        args_schema = get_weatherArgs,
        description = "Once you specify the area, date and time, you can get the weather there.",
    ),
]

tool_node = ToolNode(tool_list)
