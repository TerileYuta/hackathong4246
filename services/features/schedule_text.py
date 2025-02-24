#もうちょっと機能追加するかもしれないです。一週間分をまとめて出力とか
from services.google_calendar_api.calendarManager import create_google_calendar_service  
# Google Calendar API の接続(/services/google_calendar_api/calendarManagerから)
from datetime import datetime, timedelta
from pytz import timezone

def get_events_for_date(time_min, time_max):
    """
    指定した時間範囲のイベントを取得する関数
    :param time_min: 取得開始時刻(ISO 8601形式)
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


def format_events(date):
    """
    指定した日付のイベントを整形する関数
    :param date: 取得したい日付（YYYY-MM-DD形式）
    :return: 整形されたイベント情報の文字列
    """

    # 日本時間 (Asia/Tokyo) を設定
    jst = timezone('Asia/Tokyo')  # 日本時間のタイムゾーンを指定
    
    # 指定した日付を datetime オブジェクトに変換
    date_dt = datetime.strptime(date, '%Y-%m-%d')  # 入力された日付文字列を datetime オブジェクトに変換

    # 検索する範囲を timeMin と timeMax に設定（指定した日付の 00:00:00 と 23:59:59）
    time_min = date_dt.replace(tzinfo=jst).isoformat()  # 開始日時を 00:00:00 に設定し、ISO 8601 形式に変換
    time_max = (date_dt.replace(tzinfo=jst) + timedelta(days=1)).isoformat()  # 終了日時を 23:59:59 に設定（+1日して 23:59:59 に）

    events = get_events_for_date(time_min,time_max) #予定を検索    

    #ここからLINEで返信されるテキストを整形
    formatted_text = ""

    # 日付を "2025年2月24日（月）" の形式に変換
    formatted_date = date_dt.strftime("%Y年%m月%d日（%a）")
    formatted_text = f'{formatted_date} の予定'

    # イベントがない場合
    if not events:
        formatted_text += 'はありません。'  # イベントがなければ、その旨を表示

    # イベントがあれば
    for event in events:
        # 開始・終了時刻の取得（dateTime または date のキーを持つ）
        start = event["start"].get("dateTime", event["start"].get("date"))
        end = event["end"].get("dateTime", event["end"].get("date"))

        # ISO 8601 形式の日時を datetime オブジェクトに変換
        start_dt = datetime.fromisoformat(start) if "T" in start else datetime.strptime(start, "%Y-%m-%d")
        end_dt = datetime.fromisoformat(end) if "T" in end else datetime.strptime(end, "%Y-%m-%d")

        # 時刻を "10:00" の形式に変換（終日イベントの場合は時間を表示しない）
        formatted_start = start_dt.strftime("%H:%M") if "T" in start else "終日"
        formatted_end = end_dt.strftime("%H:%M") if "T" in end else ""

        # 予定の基本情報をformatted_textに追加していく
        formatted_text += "\n"  
        formatted_text += f"{formatted_start} {f' - {formatted_end}' if formatted_end else ''}\n"  # 時間を表示 00:00 - 00:00 または 終日 と表示される
        formatted_text += f"  {event['summary']}\n"  # イベントのタイトルを表示

        # 場所情報がある場合、追加
        if "location" in event and event["location"]:
            formatted_text += f"  場所: {event['location']}\n"

        # 参加者情報がある場合、追加
        if "attendees" in event and len(event["attendees"]) > 0:
            attendees_text = ", ".join(event["attendees"])  # リスト内の参加者をカンマ区切りで結合
            formatted_text += +f"  参加者: {attendees_text}\n"

    return formatted_text.strip()  # 最後の余計な改行を削除して整形したテキストを返す


if __name__ == '__main__':
    date = input("イベントを取得する日付を入力してください（YYYY-MM-DD形式）: ")  # ユーザーから日付を入力
    print(format_events(date))  # 入力された日付でイベントを取得