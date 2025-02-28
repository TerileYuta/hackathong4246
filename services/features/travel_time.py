from bs4 import BeautifulSoup
import re 
import requests
from datetime import datetime, timedelta

from utils.env import get_env

GOOGLE_API_KEY = get_env("GOOGLE_MAP_API")

def getRoute(from_place:str, to_place:str, query_time: datetime = None, type:str = "出発"):
    """
    
    ある地点からある地点への経路と必要な時間を返す関数

    Parameters
    ----------
        from_place(str) : 出発地
        to_place(str) : 到着地
        query_time(datetime) : 出発時刻または到着時刻
        type(str) : 出発または到着 # timeがどちらを表しているかを示している。

    Returns
    ----------
        str : 経路と所要時間

    """

    # 最寄り駅を取得する（新しい関数を使用）
    home_station = get_nearest_station(from_place)  # 出発地の最寄り駅を取得
    destination_station = get_nearest_station(to_place)  # 目的地の最寄り駅を取得

    # 最寄り駅が見つからない場合、エラーメッセージを返す
    if not home_station or not destination_station:
        return False, "最寄り駅を見つけることができませんでした。"

    # 徒歩経路と電車経路の計算を行う
    _, walk1_time = get_walking_route(from_place, home_station)  # 出発地から最寄り駅までの徒歩時間を計算
    _, walk2_time = get_walking_route(destination_station, to_place)  # 目的地最寄り駅から目的地までの徒歩時間を計算

    query_time = datetime.now() if query_time is None else query_time
    if(type == "出発"):
        query_time += timedelta(minutes=walk1_time)
        type = "1"
    else:
        query_time -= timedelta(minutes=walk2_time)
        type = "4"
    
    transit_route, train_time = get_transit_route_yahoo(home_station, destination_station, query_time, type)  # 最寄り駅から目的地最寄り駅までの電車経路と所要時間を取得

    # 合計所要時間を計算
    total_time = walk1_time + train_time + walk2_time
    total_time_str = f"{total_time // 60}時間{total_time % 60}分" if total_time >= 60 else f"{total_time}分"  # 時間と分に変換

    # ユーザーに返すレスポンスを作成
    response = """自宅: {from_palce}\n最寄り駅: {home_station}\n徒歩所要時間: {walk1_time}分
                \n\n目的地: {to_palce}\n最寄り駅: {destination_station}\n徒歩所要時間: {walk2_time}分
                \n\n電車経路: {transit_route}\n所要時間: {train_time}分
                \n\n合計所要時間: {total_time_str}"""
    
    response = response.format(
        from_palce = from_place,
        home_station = home_station,
        walk1_time = walk1_time,
        to_palce = to_place,
        destination_station = destination_station,
        walk2_time = walk2_time,
        transit_route = transit_route,
        train_time = train_time,
        total_time_str = total_time_str
    )
    
    return True, response  

def get_latlng_from_place(place_name):
    """
    
    Google Geocoding API で地名から緯度経度を取得
    
    Parameters
    ----------
        palce_name(str) : 地名

    Returns
    ----------
        str : 緯度、軽度

    """

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
    """
    
    Google Places API を使って、指定した場所の最寄り駅を段階的な半径で検索し、見つかれば返す。
    
    Parameters
    ----------
        place_name(str) : 地名

    Returns
    ----------
        str : 最も近い駅名

    """
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

def get_transit_route_yahoo(from_station, to_station, query_time, type):
    """
    
    Yahoo! 乗換案内をスクレイピングして経路情報を取得
    
    Parameters
    ----------
        from_station(str) : 出発地
        to_station(str) : 到着地
        query_time(datetime) : 出発時刻または到着時刻
        type(str) : 出発または到着 # timeがどちらを表しているかを示している。

    Returns
    ----------  
        str : 経路情報

    """

    url = f"https://transit.yahoo.co.jp/search/print"

    params = {
        "from": from_station,
        "to": to_station,
        "time": query_time.strftime('%H:%M'),
        "type": type
    }

    response = requests.get(url, params=params)
    soup = BeautifulSoup(response.text, "html.parser")

    route_summary = soup.find("div", class_="routeSummary")
    if not route_summary:
        return "⚠ 経路が見つかりません", 0

    required_time = route_summary.find("li", class_="time").get_text()
    transfer_count = route_summary.find("li", class_="transfer").get_text()
    fare = route_summary.find("li", class_="fare").get_text()

    return f"🚆 {from_station} → {to_station}: {required_time}（乗換: {transfer_count}） 料金: {fare}", parse_time_to_minutes(required_time)

def get_walking_route(from_place, to_place):
    """
    
    Google Directions API を使って徒歩経路を取得
    
    Parameters
    ----------
        from_place(str) : 出発地
        to_place(str) : 到着地

    Returns
    ---------
        str : 徒歩経路

    """
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
    """
    
    「〇時間△分」を分に変換する関数
    
    Paramters
    ---------
        time_str(str) : 時間

    Returns
    ---------
        

    """
    
    hours = re.search(r"(\d+)時間", time_str)
    minutes = re.search(r"(\d+)分", time_str)

    total_minutes = 0
    if hours:
        total_minutes += int(hours.group(1)) * 60
    if minutes:
        total_minutes += int(minutes.group(1))
    
    return total_minutes
