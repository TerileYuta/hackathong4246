import requests
from datetime import datetime
import pytz
from utils.env import get_env

def get_weather(city:str, dt:datetime):
    """
    
    指定された都市と日時に基づいて天気予報を取得する

    Parameters
    ----------
        city(str) : 都市名
        dt(datetime) : 調べたい日時（YYYY-MM-DD HH:MM形式）
        
    Returns
    ----------
        dict : 天気と気温の情報（エラーがあればエラーメッセージ）

    """

    japan_tz = pytz.timezone('Asia/Tokyo')
    dt = dt.replace(tzinfo=pytz.utc).astimezone(japan_tz)

    API_KEY = get_env("OPENWEATHER_API_KEY")  # OpenWeatherMapのAPIキーを入力
    URL = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric&lang=ja"

    # APIリクエストを送信
    response = requests.get(URL)
    data = response.json()

    # エラーハンドリング
    if response.status_code != 200:
        return False, {"error": f"APIリクエスト失敗: {data}"}

    # 予報データを datetime 形式で取得
    forecast_data = []
    for forecast in data["list"]:
        forecast_time = japan_tz.localize(datetime.strptime(forecast["dt_txt"], "%Y-%m-%d %H:%M:%S",))
        
        weather = forecast["weather"][0]["description"]
        temp = forecast["main"]["temp"]
        
        forecast_data.append((forecast_time, weather, temp))

    # 未来のデータがない場合
    if dt > forecast_data[-1][0]:
        return False, {"error": f"予報データがありません: {dt}"}

    # 指定日時に最も近いデータを探す
    nearest_forecast = min(forecast_data, key=lambda x: abs(x[0] - dt))

    return True, {
        "weather": nearest_forecast[1],
        "temp": nearest_forecast[2]
    }