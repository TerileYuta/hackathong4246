from ..google_calendar_api import GoogleCalendarAPI
from datetime import datetime, timedelta
from pytz import timezone

from config import Config

def add_event(line_id: str, summary: str, start_time: datetime, end_time: datetime, description: str = "", location: str = "",):
    """
    
    予定の追加処理

    Parameters
    ----------
        line_id(str) : LINE ID
        summary(str) : 予定のタイトル
        start_time(datetime) : 開始時間
        end_time(dateime) : 終了時刻
        description(str) : 予定の説明
        location (str) : 場所

    Returns
    ----------
        dict : 作成された予定の情報


    """

    calendar_api = GoogleCalendarAPI(line_id)
    auth = calendar_api.authenticate()

    if auth:
        return False, Config.auth_error_msg
    
    service = calendar_api.calendar

    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {
            'dateTime': start_time.isoformat(),
            'timeZone': 'Asia/Tokyo',
        },
        'end': {
            'dateTime': end_time.isoformat(),
            'timeZone': 'Asia/Tokyo',
        },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()

    return True, event

def update_event(line_id:str, event_id, summary=None, start_datetime:datetime=None, end_datetime:datetime=None, description=None, location=None):
    """
    
    予定の編集処理

    Parameters
    ----------
        line_id(str) : LINE ID
        event_id(str) : 更新するイベントのID
        summary (str): 新しいタイトル
        start_datetime (datetime): 新しい開始時刻
        end_datetime (datetime): 新しい終了時刻
        description (str): 新しい説明
        location (str): 新しい場所

    Returns
    ----------
        dict: 更新されたイベントの情報

    """

    calendar = GoogleCalendarAPI(line_id)
    auth = calendar.authenticate()

    if auth:
        return False, Config.auth_error_msg
    
    service = calendar.calendar

    jst = timezone('Asia/Tokyo')  # 日本時間のタイムゾーンを指定


    event = service.events().get(calendarId='primary', eventId=event_id).execute()

    # 更新する項目のみを変更
    if summary:
        event['summary'] = summary
    if location:
        event['location'] = location
    if description:
        event['description'] = description
    if start_datetime:
        if start_datetime.tzinfo is None:
            start_datetime =jst.localize(start_datetime)
  

        event['start']['dateTime'] = start_datetime.isoformat()
    if end_datetime:
        if end_datetime.tzinfo is None:
            end_datetime = jst.localize(end_datetime)
        event['end']['dateTime'] = end_datetime.isoformat()

    new_event = service.events().update(calendarId='primary', eventId=event_id, body=event).execute()
    
    return True, new_event

def delete_event(line_id, event_id):
    """

    予定を削除する
    
    Parameters
    ----------
        line_id(str) : LINE ID
        event_id (str): 削除するイベントのID

    Returns
    ---------
        event

    """

    calendar = GoogleCalendarAPI(line_id)
    auth = calendar.authenticate()

    if auth:
        return False, Config.auth_error_msg
    
    service = calendar.calendar
    
    event = service.events().delete(calendarId='primary', eventId=event_id).execute()

    return True, event

def getEvents(line_id:str, start_datetime:datetime, end_datetime:datetime):
    """

    指定した日のイベントを取得する関数
    Parameters
    ----------
        line_id(str) : Line ID
        start_date(datetime) : 予定を取得したい範囲の下限
        end_date(datetime) : 予定を取得したい範囲の上限


    Returns
    ---------- 
        list/dict : 取得したイベントのリスト
            [{"id": "abc123",
                "summary": "ミーティング",
                "start": {"dateTime": "2025-02-24T10:00:00+09:00"},
                "end": {"dateTime": "2025-02-24T11:00:00+09:00"},
                "location": "東京オフィス",
                "attendees": ["user1@example.com", "user2@example.com"]
            }]
  
    """ 

    calendar = GoogleCalendarAPI(line_id)
    auth = calendar.authenticate()

    # 認証に失敗した場合
    if auth:
        return False, Config.auth_error_msg
    
    # 認証に成功した場合
    service = calendar.calendar

    jst = timezone('Asia/Tokyo')  # 日本時間のタイムゾーンを指定

    if start_datetime.tzinfo is None:
        start_datetime =jst.localize(start_datetime)
    if end_datetime.tzinfo is None:
        end_datetime = jst.localize(end_datetime)

    events = get_events_from_GcalenderAPI(service, start_datetime, end_datetime) #予定を検索    

    extracted_events = []

    for event in events:
        extracted_events.append({
            "id": event.get("id"),
            "summary": event.get("summary", "（無題）"),
            "start": event.get("start", {}),
            "end": event.get("end", {}),
            "location": event.get("location", "未設定"),
            "attendees": [attendee["email"] for attendee in event.get("attendees", [])]
        })

    return True, extracted_events

def get_events_from_GcalenderAPI(service, time_min,time_max):
    """
    
    指定した時間範囲のイベントをGoogle Calender APIで取得する関数

    Parameters
    ----------
        time_min: 取得開始時刻(IAPISO 8601形式)
        time_max: 取得終了時刻(ISO 8601形式)
    
    Returns
    ----------
        return: 取得したイベントのリスト
    
    """

    # Google カレンダー API でイベントを取得
    events_result = service.events().list(
        calendarId='primary',  # 'primary' はメインカレンダーを指定
        timeMin=time_min.isoformat(),  # 開始日時（指定した日の 00:00:00）
        timeMax=time_max.isoformat(),  # 終了日時（指定した日の 23:59:59）
        singleEvents=True,  # 繰り返しイベントも単一イベントとして扱う
        orderBy='startTime'  # イベントを開始時刻でソート
    ).execute()  # API を実行してイベントを取得

    return events_result.get('items', [])  # イベント情報を取得