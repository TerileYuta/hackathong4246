from ..google_calendar_api import GoogleCalendarAPI
from datetime import datetime

class Schedule:
    def __init__(self, line_id : str):
        calendar = GoogleCalendarAPI(line_id)
        self.service = calendar.authenticate()

    def add_event(self, summary: str, start_time: datetime, end_time: datetime, description: str = "", location: str = "",):
        """
        
        予定の追加処理

        Parameters
        ----------
            summary(str) : 予定のタイトル
            start_time(datetime) : 開始時間
            end_time(dateime) : 終了時刻
            description(str) : 予定の説明
            location (str) : 場所

        Returns
        ----------
            dict : 作成された予定の情報


        """

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

        event = self.service.events().insert(calendarId='primary', body=event).execute()

        return event
    
    def update_event(self, event_id, summary=None, start_time=None, end_time=None, description=None, location=None):
        """
        
        予定の編集処理

        Parameters
        ----------
            event_id(str) : 更新するイベントのID
            summary (str): 新しいタイトル
            start_time (datetime): 新しい開始時刻
            end_time (datetime): 新しい終了時刻
            description (str): 新しい説明
            location (str): 新しい場所

        Returns
        ----------
            dict: 更新されたイベントの情報

        """
         
        event = self.service.events().get(calendarId='primary', eventId=event_id).execute()

        # 更新する項目のみを変更
        if summary:
            event['summary'] = summary
        if location:
            event['location'] = location
        if description:
            event['description'] = description
        if start_time:
            event['start']['dateTime'] = start_time.isoformat()
        if end_time:
            event['end']['dateTime'] = end_time.isoformat()

        updated_event = self.service.events().update(
            calendarId='primary', eventId=event_id, body=event).execute()
        
        return updated_event
    
    def delete_event(self, event_id):
        """

        予定を削除する
        
        Parameters
        ----------
            event_id (str): 削除するイベントのID

        """
        self.service.events().delete(calendarId='primary', eventId=event_id).execute()