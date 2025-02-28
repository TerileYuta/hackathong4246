# services/features/get_available_time.py
# 空き時間検索機能

import re
import pytz
import datetime
import dateparser
from dateutil.relativedelta import relativedelta
from services.google_calendar_api.calendar_api_connection import  GoogleCalendarAPI
from config import Config

def get_available_time(line_id, time_range="tomorrow", specific_date=None, timezone="Asia/Tokyo"):
    """

    指定された期間または日付の空き時間を Google カレンダーから取得する

    Parameters
    ----------
        line_id(str) : LINEのユーザーID
        time_range(str) : 検索したい期間（例: "today", "tomorrow", "this_week", "next_month"）
        specific_date(str, optional) : 特定の日付（例: "2025-03-10"）
        timezone(str) : タイムゾーン（デフォルトは "Asia/Tokyo"）

    Returns
    ----------
        list : 空き時間のリスト（例: ["2025-03-10 09:00 - 10:00", ...]）

    """
    calendar_api = GoogleCalendarAPI(line_id)
    not_auth = calendar_api.authenticate()

    # Oauth承認が必要になった場合
    if not_auth:
        return False, Config.auth_error_msg
    
    service = calendar_api.calendar
    local_tz = pytz.timezone(timezone)
    now = datetime.datetime.now(local_tz)
    start_date, end_date = calculate_date_range(time_range, now, specific_date, local_tz)

    start_date_utc = start_date.astimezone(pytz.utc)
    end_date_utc = end_date.astimezone(pytz.utc)

    events_result = service.events().list(
        calendarId="primary", timeMin=start_date_utc.isoformat(), timeMax=end_date_utc.isoformat(),
        singleEvents=True, orderBy="startTime"
    ).execute()

    busy_times = [
        (e["start"].get("dateTime", e["start"].get("date")), e["end"].get("dateTime", e["end"].get("date")))
        for e in events_result.get("items", [])
    ]
    
    return True, calculate_free_time_ranges(start_date, end_date, busy_times, local_tz)


def calculate_date_range(time_range, now, specific_date, local_tz):
    """

    指定された期間または日付に基づいて開始日と終了日を計算する

    Parameters
    ----------
        time_range(str) : 検索したい期間（例: "today", "tomorrow", "this_week", "next_month"）
        now(datetime) : 現在の日時
        specific_date(str, optional) : 特定の日付（例: "2025-03-10"）
        local_tz(pytz.timezone) : ローカルタイムゾーン

    Returns
    ----------
        tuple : 計算された開始日と終了日 (datetime, datetime)

    """

    if specific_date:
        parsed_date = dateparser.parse(specific_date)
        if parsed_date:
            return parsed_date, parsed_date.replace(hour=23, minute=59, second=59, microsecond=999999)

        raise ValueError("Could not parse the date.")

    date_calculations = {
        "today": lambda: (now, now.replace(hour=23, minute=59, second=59, microsecond=999999)),
        "tomorrow": lambda: (now + datetime.timedelta(days=1), (now + datetime.timedelta(days=1)).replace(hour=23, minute=59, second=59, microsecond=999999)),
        "this_week": lambda: (now - datetime.timedelta(days=now.weekday()), (now - datetime.timedelta(days=now.weekday()) + datetime.timedelta(days=6)).replace(hour=23, minute=59, second=59, microsecond=999999)),
        "next_week": lambda: (now + datetime.timedelta(days=(7 - now.weekday())), (now + datetime.timedelta(days=(7 - now.weekday()) + 6)).replace(hour=23, minute=59, second=59, microsecond=999999)),
        "this_month": lambda: (now.replace(day=1), (now.replace(day=1) + relativedelta(months=1) - datetime.timedelta(days=1)).replace(hour=23, minute=59, second=59, microsecond=999999)),
        "next_month": lambda: (now.replace(day=1) + relativedelta(months=1), (now.replace(day=1) + relativedelta(months=2) - datetime.timedelta(days=1)).replace(hour=23, minute=59, second=59, microsecond=999999)),
    }

    return date_calculations.get(time_range, lambda: (now, now.replace(hour=23, minute=59, second=59, microsecond=999999)))()


def calculate_free_time_ranges(start_date, end_date, busy_times, local_tz):
    """

    予約済みの時間を除外して、空き時間を計算する

    Parameters
    ----------
        start_date(datetime) : 検索開始日時
        end_date(datetime) : 検索終了日時
        busy_times(list) : 予約済みの時間（(start, end)のタプルリスト）
        local_tz(pytz.timezone) : ローカルタイムゾーン

    Returns
    ----------
        list : 空き時間のリスト（例: ["2025-03-10 09:00 - 10:00", ...])

    """

    available_times = {current_day.date().strftime("%Y-%m-%d"): [{"start": current_day.replace(hour=0, minute=0),
                                                                 "end": current_day.replace(hour=23, minute=59, second=59, microsecond=999999)}]
                       for current_day in [start_date.astimezone(local_tz) + datetime.timedelta(days=i) for i in range((end_date - start_date).days + 1)]}

    for start, end in busy_times:
        busy_start = dateparser.parse(start).astimezone(local_tz)
        busy_end = dateparser.parse(end).astimezone(local_tz)
        busy_day = busy_start.date().strftime("%Y-%m-%d")

        if busy_day in available_times:
            updated_times = []
            for time_slot in available_times[busy_day]:
                if busy_start < time_slot["end"] and busy_end > time_slot["start"]:
                    if busy_start > time_slot["start"]:
                        updated_times.append({"start": time_slot["start"], "end": busy_start})
                    if busy_end < time_slot["end"]:
                        updated_times.append({"start": busy_end, "end": time_slot["end"]})
                else:
                    updated_times.append(time_slot)
            available_times[busy_day] = updated_times

    return [
        f"{day} {slot['start'].strftime('%H:%M')} - {slot['end'].strftime('%H:%M')}"
        for day, slots in available_times.items() for slot in slots
    ]


def search_available_time(line_id, user_message):
    """

    メッセージを解析して、空き時間を検索

    Parameters
    ----------
        line_id(str) : LINEのユーザーID
        user_message(str) : ユーザーからのメッセージ（例: "今週の空き時間を教えて")

    Returns
    ----------
        str : 空き時間のリストまたはエラーメッセージ

    """

    time_map = {
        "今日": "today",
        "明日": "tomorrow",
        "今週": "this_week",
        "来週": "next_week",
        "今月": "this_month",
        "来月": "next_month"
    }

    for key, value in time_map.items():
        if key in user_message:
            available_times = get_available_time(line_id, time_range=value)

            # Flatten the list if there are nested lists and ensure all items are strings
            available_times_flat = []
            for item in available_times:
                if isinstance(item, list):  # If the item is a list, flatten it
                    available_times_flat.extend([str(subitem) for subitem in item if subitem != True])  # Avoid adding `True`
                elif item != True:  # If the item is not `True`, add it to the list
                    available_times_flat.append(str(item))

            return "\n".join(available_times_flat)

    match = re.search(r"(\d{1,2})月(\d{1,2})日|(\d{1,2})/(\d{1,2})", user_message)
    if match:
        month = match.group(1) or match.group(3)
        day = match.group(2) or match.group(4)
        specific_date = f"2025-{month.zfill(2)}-{day.zfill(2)}"
        return "\n".join(get_available_time(specific_date=specific_date))

    return "日付や期間を指定してください。例: '今週', '明日', '3月10日'"
