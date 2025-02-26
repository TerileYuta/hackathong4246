from datetime import datetime
from langchain.tools import StructuredTool
from pydantic import BaseModel
from langgraph.prebuilt import ToolNode

class addEventArgs(BaseModel):
    summary: str
    start_time: datetime
    end_time: datetime
    description: str = ""
    location: str = ""

def addEvent(
    summary: str,
    start_time: datetime,
    end_time: datetime, 
    description: str = "", 
    location: str = ""
):

    return "予定登録完了"

class updateEventArgs(BaseModel):
    event_id:str
    summary:str = None
    start_time:datetime = None
    end_time:datetime = None
    description:str = None
    location:str = None

def updateEvent(
    event_id,
    summary:str = None,
    start_time:datetime = None,
    end_time:datetime = None,
    description:str = None,
    location:str = None
):

    return "編集完了"

class deleteEventArgs(BaseModel):
    event_id:str 

def deleteEvent(
    event_id
):
    
    return "予定の削除完了"

class listEventArgs(BaseModel):
    max_results: int

def listEvents(   
   max_results:int =10       
):

    return """
        1. 会議
   開始時刻: 2025-03-03 10:00
   終了時刻: 2025-03-03 11:00

2. 会議
   開始時刻: 2025-03-05 10:00
   終了時刻: 2025-03-06 11:00
"""

class findAvailableTimeArgs(BaseModel):
    pass

def findAvailableTime(
        
):

    return "空き時間取得成功"

def askUser():
    return "Think about what you would like to confirm or ask the user."

tool_list = [
    StructuredTool.from_function(
        name = "addEvent",
        func = addEvent,
        args_schema = addEventArgs,
        description = "Adds a new event to the calendar with the specified details."
    ),
    StructuredTool.from_function(
        name = "updateEvent",
        func = updateEvent,
        args_schema = updateEventArgs,
        description = "Edits an existing event by modifying its details based on the provided parameters."
    ),
    StructuredTool.from_function(
        name = "deleteEvent",
        func = deleteEvent,
        args_schema = deleteEventArgs,
        description = "Removes a specified event from the calendar."
    ),
    StructuredTool.from_function(
        name = "listEvents",
        func = listEvents,
        args_schema = listEventArgs,
        description = "Retrieves and displays a list of scheduled events."
    ),
    StructuredTool.from_function(
        name = "findAvailableTime",
        func = findAvailableTime,
        args_schema = findAvailableTimeArgs,
        description = "Searches for available time slots based on the given constraints.",
    ),
    StructuredTool.from_function(
        name = "askUser",
        func = askUser,
        args_schema = None,
        description = "Now users can confirm or ask questions when information is unclear or ambiguous.",
    )
]

tool_node = ToolNode(tool_list)
