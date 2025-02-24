import re
# from linebot.models import TextSendMessage
from services.calendar import get_available_time 

def handle_text_message(event, line_bot_api):
    """Handle incoming text messages."""
    user_message = event.message.text
    
    try:
        if "今日" in user_message:
            free_days = get_available_time(time_range="today")
            reply_text = "今日空いている時間:\n" + "\n".join(free_days) if free_days else "今日は空いていません。"
        
        elif "明日" in user_message:
            free_days = get_available_time(time_range="tomorrow")
            reply_text = "明日空いている時間:\n" + "\n".join(free_days) if free_days else "明日は空いていません。"
        
        elif "今週" in user_message:
            free_days = get_available_time(time_range="this_week")
            reply_text = "今週空いている時間:\n" + "\n".join(free_days) if free_days else "今週は空いていません。"
        
        elif "来週" in user_message:
            free_days = get_available_time(time_range="next_week")
            reply_text = "来週空いている時間:\n" + "\n".join(free_days) if free_days else "来週は空いていません。"

        elif "今月" in user_message:
            free_days = get_available_time(time_range="this_month")
            reply_text = "今月空いている時間:\n" + "\n".join(free_days) if free_days else "今月は空いていません。"
        
        elif "来月" in user_message:
            free_days = get_available_time(time_range="next_month")
            reply_text = "来月空いている時間:\n" + "\n".join(free_days) if free_days else "来月は空いていません。"
        
        elif "いつ空いている" in user_message or "空いている日" in user_message:
            free_days = get_available_time(time_range="anytime")
            reply_text = "空いている日:\n" + "\n".join(free_days) if free_days else "直近1ヶ月で空いている日はありません。"
        
        elif re.search(r"(\d{1,2})月(\d{1,2})日 はいつ空いてる\?|(\d{1,2})/(\d{1,2})に空いてる日", user_message):
            date_match = re.search(r"(\d{1,2})月(\d{1,2})日 はいつ空いてる\?|(\d{1,2})/(\d{1,2})に空いてる日", user_message)
            
            if date_match.group(1) and date_match.group(2):  # Case for "？月？日 はいつ空いてる？"
                month = date_match.group(1)
                day = date_match.group(2)
            else:  # Case for "MM/DDに空いてる日"
                month = date_match.group(3)
                day = date_match.group(4)
            
            specific_date = f"2025-{month.zfill(2)}-{day.zfill(2)}"  # Format it as a full date (e.g., "2025-03-10")
            free_times = get_available_time(specific_date=specific_date)
            reply_text = f"{specific_date}の空いている時間:\n" + "\n".join(free_times) if free_times else f"{specific_date}には空いている時間がありません。"
        
        else:
            reply_text = "日付や期間を指定してください。例えば、'今週'、'明日'、'来週'、'03/10'、'3月10日' などです。"
    
    except Exception as e:
        reply_text = f"エラーが発生しました: {str(e)}"

    print(user_message)
    print(reply_text)
    
    # LINEとの連携時は以下を実行？
    # line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))