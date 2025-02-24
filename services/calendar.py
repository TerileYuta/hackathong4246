import datetime
import os
import dateparser
import pytz
from dateutil.relativedelta import relativedelta
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def get_available_time(time_range="tomorrow", specific_date=None, timezone="Asia/Tokyo"):
    """Fetch available time slots from Google Calendar for a specified time range or specific date."""
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "wb") as token:
            token.write(creds.to_json().encode())

    service = build("calendar", "v3", credentials=creds)

    # Parse the provided date (if any)
    if specific_date:
        parsed_date = dateparser.parse(specific_date)
        if parsed_date:
            start_date = parsed_date
            end_date = start_date.replace(hour=23, minute=59, second=59, microsecond=999999)  # End of tomorrow
        else:
            raise ValueError("Could not parse the date.")
    else:
        # Use pytz to convert to the specified timezone
        local_tz = pytz.timezone(timezone)
        now = datetime.datetime.now(local_tz)  # Get the current local time
        print("Current local time:", now)

        # Initialize end_date to ensure it exists in every condition
        start_date = now
        end_date = None

        # Default handling for specific time range (e.g., "tomorrow", "this week")
        if time_range == "today":
            end_date = start_date.replace(hour=23, minute=59, second=59, microsecond=999999)
        elif time_range == "tomorrow":
            start_date = now + datetime.timedelta(days=1)
            end_date = start_date.replace(hour=23, minute=59, second=59, microsecond=999999)  # End of tomorrow
        elif time_range == "this_week":
            week_start = now - datetime.timedelta(days=now.weekday())  # Start of the current week (Monday)
            end_date = week_start + datetime.timedelta(days=6)  # End of the week (Sunday)
            end_date = end_date.replace(hour=23, minute=59, second=59, microsecond=999999)  # Set to end of Sunday
        elif time_range == "next_week":
            start_date = now + datetime.timedelta(days=(7 - now.weekday()))  # Start of the next week (Monday)
            end_date = start_date + datetime.timedelta(days=6)  # End of the next week (Sunday)
            end_date = end_date.replace(hour=23, minute=59, second=59, microsecond=999999)  # Set to end of Sunday
            start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)  # Set to start of Monday
        elif time_range == "this_month":
            first_day_next_month = now.replace(day=1) + relativedelta(months=1)
            end_date = first_day_next_month - datetime.timedelta(days=1)
            end_date = end_date.replace(hour=23, minute=59, second=59, microsecond=999999)
        elif time_range == "next_month":
            start_date = now.replace(day=1) + relativedelta(months=1)
            end_date = (start_date + relativedelta(months=1)) - datetime.timedelta(days=1)
            end_date = end_date.replace(hour=23, minute=59, second=59, microsecond=999999)
        elif time_range == "anytime":
            start_date = now
            end_date = start_date + relativedelta(months=1)
            end_date = end_date.replace(hour=23, minute=59, second=59, microsecond=999999)  # End of the day
        else:
            start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = start_date.replace(hour=23, minute=59, second=59, microsecond=999999)

    # Debugging: Print the calculated start and end date
    print("Start date:", start_date)
    print("End date:", end_date)

    # Format start and end date for API request (convert to UTC for Google API)
    start_date_utc = start_date.astimezone(pytz.utc)
    end_date_utc = end_date.astimezone(pytz.utc)
    
    time_min = start_date_utc.isoformat()
    time_max = end_date_utc.isoformat()

    # Make the API request to Google Calendar
    events_result = service.events().list(
        calendarId="primary", timeMin=time_min, timeMax=time_max,
        singleEvents=True, orderBy="startTime"
    ).execute()

    # Debugging: Check the events returned from Google Calendar
    # print("Events result:", events_result)

    events = events_result.get("items", [])
    busy_times = [(e["start"].get("dateTime", e["start"].get("date")),
                   e["end"].get("dateTime", e["end"].get("date"))) for e in events]

    # Debugging: Check the busy times detected
    print("Busy times:", busy_times)

    # Create a time range from the start date to the end date (in the local timezone)
    local_start = start_date.astimezone(local_tz)
    local_end = end_date.astimezone(local_tz)
    
    # Create a dictionary to store the free times for each day in the date range
    available_times = {}

    # Iterate through each day in the range
    current_day = local_start
    while current_day <= local_end:
        day_str = current_day.date().strftime("%Y-%m-%d")
        available_times[day_str] = []

        # Default available times from 00:00 to 23:59
        available_times[day_str].append({"start": current_day.replace(hour=0, minute=0),
                                         "end": current_day.replace(hour=23, minute=59, second=59, microsecond=999999)})
        
        current_day += datetime.timedelta(days=1)
    
    # Mark the busy times as unavailable
    for start, end in busy_times:
        busy_start = dateparser.parse(start)
        busy_end = dateparser.parse(end)

        if busy_start and busy_end:
            busy_start = busy_start.astimezone(local_tz)
            busy_end = busy_end.astimezone(local_tz)
            busy_day = busy_start.date().strftime("%Y-%m-%d")
            
            # Remove busy time from the available times
            if busy_day in available_times:
                updated_times = []
                for time_slot in available_times[busy_day]:
                    # If the busy time overlaps with the available time, split it into free slots
                    if busy_start < time_slot["end"] and busy_end > time_slot["start"]:
                        if busy_start > time_slot["start"]:
                            updated_times.append({"start": time_slot["start"], "end": busy_start})
                        if busy_end < time_slot["end"]:
                            updated_times.append({"start": busy_end, "end": time_slot["end"]})
                    else:
                        updated_times.append(time_slot)
                available_times[busy_day] = updated_times

    # Debugging: Check the available times
    # print("Available times:", available_times)

    # Flatten the times into a simple list of free time ranges
    free_times = []
    for day, slots in available_times.items():
        for slot in slots:
            free_times.append(f"{day} {slot['start'].strftime('%H:%M')} - {slot['end'].strftime('%H:%M')}")

    return free_times

# Example usage:
""" print(get_free_times(time_range="tomorrow"))
print("\n")
print(get_free_times(time_range="tomorrow"))
print("\n")
print(get_free_times(time_range="this_week"))
print("\n")
print(get_free_times(time_range="next_week"))
print("\n")
print(get_free_times(time_range="this_month"))
print("\n")
print(get_free_times(time_range="next_month")) """