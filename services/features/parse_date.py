import re
import datetime

def parse_date(message):
    """
    メッセージから日付を解析する
    Parameters
    ----------
        message(str) : ユーザーからのメッセージ（例: "3月1日", "今日", "明日"）
    Returns
    ----------
        datetime : 解析された日付（無効な日付の場合はNone）
    """
    # "YYYY-MM-DD" フォーマットをチェック
    try:
        date = datetime.datetime.strptime(message.strip(), "%Y-%m-%d")
        return date
    except ValueError:
        pass  # "YYYY-MM-DD" フォーマットでない場合は次のチェックへ

    # "3月1日" のような日本語の日付フォーマットをチェック
    month_day_pattern = r"(\d{1,2})月\s*(\d{1,2})日"
    match = re.match(month_day_pattern, message.strip())
    
    if match:
        month = int(match.group(1))
        day = int(match.group(2))
        current_year = datetime.datetime.now().year
        date = datetime.datetime(current_year, month, day)
        return date

    # "今日" のチェック
    if "今日" in message:
        return datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    # "明日" のチェック
    elif "明日" in message:
        return (datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + datetime.timedelta(days=1))
    
    return None