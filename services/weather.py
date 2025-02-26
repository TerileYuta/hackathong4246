import requests
import datetime

def get_weather(city, dt):
    API_KEY = "f876f83f4fdae211dfb31f2cd260d9aa"  # OpenWeatherMapのAPIキーを入力
    URL = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric&lang=ja"

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

# 例: 2025年2月27日の12:30の天気を取得（東京）
city_name = "Tokyo"
target_date = "2025-02-27 12:30"  # YYYY-MM-DD HH:MM の形式で入力

result = get_weather(city_name, target_date)

# 結果を表示
if "error" in result:
    print(result["error"])
else:
    print(f"天気: {result['weather']}, 気温: {result['temp']}°C")