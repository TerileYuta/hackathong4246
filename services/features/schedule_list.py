from services.google_calendar_api.calendarManager import create_google_calendar_service  
# Google Calendar API の接続(/services/google_calendar_api/calendarManagerから)
from datetime import datetime, timedelta
from pytz import timezone

def get_events_for_date(date):
    """
    指定した日のイベントを取得する関数
    :param date: 取得したい日付(YYYY-MM-DD形式)
    :return: 取得したイベントのリスト
        list:{dict}
        [{"id": "abc123",
        "summary": "ミーティング",
        "start": {"dateTime": "2025-02-24T10:00:00+09:00"},
        "end": {"dateTime": "2025-02-24T11:00:00+09:00"},
        "location": "東京オフィス",
        "attendees": ["user1@example.com", "user2@example.com"]
        }]
    """ 
    # 日本時間 (Asia/Tokyo) を設定
    jst = timezone('Asia/Tokyo')  # 日本時間のタイムゾーンを指定
    
    # 指定した日付を datetime オブジェクトに変換
    date_dt = datetime.strptime(date, '%Y-%m-%d')  # 入力された日付文字列を datetime オブジェクトに変換

    # 検索する範囲を timeMin と timeMax に設定（指定した日付の 00:00:00 と 23:59:59）
    time_min = date_dt.replace(tzinfo=jst).isoformat()  # 開始日時を 00:00:00 に設定し、ISO 8601 形式に変換
    time_max = (date_dt.replace(tzinfo=jst) + timedelta(days=1)).isoformat()  # 終了日時を 23:59:59 に設定（+1日して 23:59:59 に）

    events = get_events_from_GcalenderAPI(time_min,time_max) #予定を検索    
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
    return extracted_events

def get_events_from_GcalenderAPI(time_min,time_max):
    """
    指定した時間範囲のイベントをGoogle Calender APIで取得する関数
    :param time_min: 取得開始時刻(IAPISO 8601形式)
    :param time_max: 取得終了時刻(ISO 8601形式)
    :return: 取得したイベントのリスト
    """
    service = create_google_calendar_service()  # Google Calendar API サービスオブジェクトを取得

    # Google カレンダー API でイベントを取得
    events_result = service.events().list(
        calendarId='primary',  # 'primary' はメインカレンダーを指定
        timeMin=time_min,  # 開始日時（指定した日の 00:00:00）
        timeMax=time_max,  # 終了日時（指定した日の 23:59:59）
        singleEvents=True,  # 繰り返しイベントも単一イベントとして扱う
        orderBy='startTime'  # イベントを開始時刻でソート
    ).execute()  # API を実行してイベントを取得

    return events_result.get('items', [])  # イベント情報を取得

if __name__ == '__main__': #テスト用　実際はformatterなどにget_e_f_d()が呼び出される
    date = input("イベントを取得する日付を入力してください(YYYY-MM-DD形式): ")  # ユーザーから日付を入力
    print(get_events_for_date(date))  # 入力された日付でイベントを取得
