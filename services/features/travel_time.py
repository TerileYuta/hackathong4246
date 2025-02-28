# モジュールとして扱うためのファイル
from bs4 import BeautifulSoup
import re  # 追加
import requests

GOOGLE_API_KEY = "AIzaSyB-jnFU1PRHagvMFdUFtfejuCJRQYZCzgk"

def get_latlng_from_place(place_name):
    """Google Geocoding API で地名から緯度経度を取得"""
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": place_name,
        "key": GOOGLE_API_KEY,
        "language": "ja",
        "region": "JP"  # 日本に限定
    }
    response = requests.get(url, params=params)
    data = response.json()

    if data["status"] == "OK":
        location = data["results"][0]["geometry"]["location"]
        return f"{location['lat']},{location['lng']}"  # 緯度,経度を返す
    else:
        print(f"⚠ {place_name} の座標が取得できません。")
        return None

def get_nearest_station(place_name):
    """Google Places API を使って、指定した場所の最寄り駅を段階的な半径で検索し、見つかれば返す。"""
    latlng = get_latlng_from_place(place_name)
    if not latlng:
        return None  # 座標が取得できない場合、最寄り駅検索をスキップ

    # 検索する半径リスト（200m から順に広げる）
    radii = [200, 400, 600, 800, 1000, 2000, 3000]

    for radius in radii:
        url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        params = {
            "location": latlng,
            "radius": radius,
            "type": "train_station",
            "key": GOOGLE_API_KEY,
            "language": "ja"
        }
        response = requests.get(url, params=params)
        data = response.json()

        if data["status"] == "OK" and data["results"]:
            # 最も近い駅を返す
            return data["results"][0]["name"]
    return None

def get_transit_route_yahoo(from_station, to_station):
    """Yahoo! 乗換案内をスクレイピングして経路情報を取得"""
    url = f"https://transit.yahoo.co.jp/search/print?from={from_station}&to={to_station}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    route_summary = soup.find("div", class_="routeSummary")
    if not route_summary:
        return "⚠ 経路が見つかりません", 0

    required_time = route_summary.find("li", class_="time").get_text()
    transfer_count = route_summary.find("li", class_="transfer").get_text()
    fare = route_summary.find("li", class_="fare").get_text()

    return f"🚆 {from_station} → {to_station}: {required_time}（乗換: {transfer_count}） 料金: {fare}", parse_time_to_minutes(required_time)

def get_walking_route(from_place, to_place):
    """Google Directions API を使って徒歩経路を取得"""
    url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        "origin": from_place,
        "destination": to_place,
        "mode": "walking",
        "key": GOOGLE_API_KEY,
        "language": "ja"
    }
    response = requests.get(url, params=params)
    data = response.json()

    if data["status"] == "OK":
        duration = data["routes"][0]["legs"][0]["duration"]["text"]
        return f"🏃 {from_place} → {to_place}: {duration}", parse_time_to_minutes(duration)
    else:
        return "⚠ 徒歩経路が見つかりません", 0

def parse_time_to_minutes(time_str):
    """「〇時間△分」を分に変換する関数"""
    hours = re.search(r"(\d+)時間", time_str)
    minutes = re.search(r"(\d+)分", time_str)

    total_minutes = 0
    if hours:
        total_minutes += int(hours.group(1)) * 60
    if minutes:
        total_minutes += int(minutes.group(1))
    
    return total_minutes

def reply_travel_time(message):
    try:
            home_name, destination_name = message.split("から")  # 「から」で分割して出発地と目的地を取得
    except ValueError:
        # 「から」区切りが正しくない場合、エラーメッセージを返す
        return [
            {
                "type": "text",
                "text": "経路の形式が正しくありません。例えば「渋谷から東京タワー」といった形式で入力してください。"
            }
        ]

    # 最寄り駅を取得する（新しい関数を使用）
    home_station = get_nearest_station(home_name)  # 出発地の最寄り駅を取得
    destination_station = get_nearest_station(destination_name)  # 目的地の最寄り駅を取得

    # 最寄り駅が見つからない場合、エラーメッセージを返す
    if not home_station or not destination_station:
        return [
            {
                "type": "text",
                "text": "最寄り駅が見つかりませんでした。もう一度試してください。"
            }
        ]

    # 徒歩経路と電車経路の計算を行う
    home_to_station, walk1_time = get_walking_route(home_name, home_station)  # 出発地から最寄り駅までの徒歩時間を計算
    transit_route, train_time = get_transit_route_yahoo(home_station, destination_station)  # 最寄り駅から目的地最寄り駅までの電車経路と所要時間を取得
    station_to_destination, walk2_time = get_walking_route(destination_station, destination_name)  # 目的地最寄り駅から目的地までの徒歩時間を計算

    # 合計所要時間を計算
    total_time = walk1_time + train_time + walk2_time
    total_time_str = f"{total_time // 60}時間{total_time % 60}分" if total_time >= 60 else f"{total_time}分"  # 時間と分に変換

    # ユーザーに返すレスポンスを作成
    response = [
        {
            "type": "text",
            "text": f"自宅: {home_name}\n最寄り駅: {home_station}\n徒歩所要時間: {walk1_time}分"
        },
        {
            "type": "text",
            "text": f"目的地: {destination_name}\n最寄り駅: {destination_station}\n徒歩所要時間: {walk2_time}分"
        },
        {
            "type": "text",
            "text": f"電車経路: {transit_route}\n所要時間: {train_time}分"
        },
        {
            "type": "text",
            "text": f"合計所要時間: {total_time_str}"
        }
    ]

    return response  # 作成したレスポンスを返す