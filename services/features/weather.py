import re
import requests
import datetime
from .parse_date import parse_date

def get_weather(city, dt):
    """
    指定された都市と日時に基づいて天気予報を取得する
    Parameters
    ----------
        city(str) : 都市名
        dt(str) : 調べたい日時（YYYY-MM-DD HH:MM形式）
        
    Returns
    ----------
        dict : 天気と気温の情報（エラーがあればエラーメッセージ）
    """
    API_KEY = "f876f83f4fdae211dfb31f2cd260d9aa"  # OpenWeatherMapのAPIキーを入力
    URL = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric&lang=ja"

    # APIリクエストを送信
    response = requests.get(URL)
    data = response.json()

    # エラーハンドリング
    if response.status_code != 200:
        return {"error": f"APIリクエスト失敗: {data}"}

    # 入力日時をdatetime形式に変換
    input_dt = datetime.datetime.strptime(dt, "%Y-%m-%d %H:%M")

    # 予報データを datetime 形式で取得
    forecast_data = []
    for forecast in data["list"]:
        forecast_time = datetime.datetime.strptime(forecast["dt_txt"], "%Y-%m-%d %H:%M:%S")
        weather = forecast["weather"][0]["description"]
        temp = forecast["main"]["temp"]
        forecast_data.append((forecast_time, weather, temp))

    # 未来のデータがない場合
    if input_dt > forecast_data[-1][0]:
        return {"error": f"未来すぎて予報データがありません: {dt}"}

    # 指定日時に最も近いデータを探す
    nearest_forecast = min(forecast_data, key=lambda x: abs(x[0] - input_dt))

    return {
        "weather": nearest_forecast[1],
        "temp": nearest_forecast[2]
    }

def reply_weather(text, user_id, state):
    """
    メッセージと状態に基づいて天気の問い合わせを処理する
    
    Parameters
    ----------
        text(str) : ユーザーからのメッセージ
        user_id(str) : ユーザーのID
        state(str) : 現在の状態（"waiting_for_city", "waiting_for_date"など）
        
    Returns
    ----------
        list : リプライメッセージのリスト
    """
    from handlers.message_receive_handler import update_user_state, get_user_state

    # 状態がNoneまたは"waiting_for_city"の場合、都市名を尋ねる
    if state == "waiting_for_city":
        city_pattern = r"([一-龯]+|[A-Za-z]+)"
        match_city = re.search(city_pattern, text)

        if match_city:
            city = match_city.group(1)
            update_user_state(user_id, "waiting_for_date", None)
            return [{
                "type": "text",
                "text": f"{city}の天気を調べます。日付を教えてください。例: 今日, 明日, 3月1日"
            }]
        else:
            return [{
                "type": "text",
                "text": "都市名を認識できませんでした。もう一度都市名を入力してください。"
            }]
    
    # 状態が"waiting_for_date"の場合、日付の入力を処理
    elif state == "waiting_for_date":
        date = parse_date(text)
        if date:
            user_state = get_user_state(user_id)
            city = user_state["context"].get("city", None)  # コンテキストから都市を取得
            target_date = date.strftime("%Y-%m-%d 12:00")  # 便宜的に正午を使用
            result = get_weather(city, target_date)
            if "error" in result:
                reply_text = result["error"]
            else:
                reply_text = f"{text}の天気: {result['weather']}, 気温: {result['temp']}°C"
                # 天気の問い合わせが完了したので、状態を"completed"に更新
                update_user_state(user_id, "completed", None)
            return [{
                "type": "text",
                "text": reply_text
            }]
        else:
            return [{
                "type": "text",
                "text": "無効な日付です。日付をもう一度確認してください。"
            }]

    # 状態がNoneの場合、都市名の入力を求める
    elif state is None:
        return [{
            "type": "text",
            "text": "都市名を教えてください。"
        }]
    
    return [{
        "type": "text",
        "text": "不明なエラーが発生しました。"
    }]
