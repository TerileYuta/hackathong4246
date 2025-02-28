import requests
from datetime import datetime
from utils.env import get_env

def get_weather(city:str, dt:datetime):
    """
    
    天気予報を取得する

    Parameters
    ----------
        city(str) : 場所
        dt(datetime) : 日時

    Returns
    ----------
        

    """
    API_KEY = get_env("OPENWEATHER_API_KEY")  
    URL = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric&lang=ja"

    response = requests.get(URL)
    data = response.json()

    # エラーハンドリング
    if response.status_code != 200:
        return False, "失敗"

    # 予報データを datetime 形式で取得
    forecast_data = []
    for forecast in data["list"]:
        forecast_time = datetime.strptime(forecast["dt_txt"], "%Y-%m-%d %H:%M:%S")
        weather = forecast["weather"][0]["description"]
        temp = forecast["main"]["temp"]
        forecast_data.append((forecast_time, weather, temp))

    # 未来のデータがない場合
    if dt > forecast_data[-1][0]:
        return True, {"error": f"未来すぎて予報データがありません: {dt}"}

    # 指定日時に最も近いデータを探す
    nearest_forecast = min(forecast_data, key=lambda x: abs(x[0] - dt))

    return True, {
        "weather": nearest_forecast[1],
        "temp": nearest_forecast[2]
    }