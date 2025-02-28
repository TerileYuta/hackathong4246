def analyze_message(message):
    """

    ユーザーからのメッセージをルールーベースで分析する

    Parameters
    ----------
        message(str) : ユーザーメッセージ

    Returns
    ----------
        list : レスポンスメッセージ

    """

    """
    
    if "天気" in message:
    # 状態がNoneの場合は、都市名を尋ねて天気の検索を開始
    update_user_state(line_id, "waiting_for_city", None)  # ユーザーの状態を"waiting_for_city"に更新
    return reply_weather(message, line_id, None)  # 初回の状態で天気リプライを呼び出す
    
    elif "いつ" in message or "空いてる" in message:
        return reply_available_time(message, line_id)  # 空き時間を確認するリプライを返す
    
    elif "経路" in message:  # 経路に関するクエリに対応
        return reply_travel_time(message)
    elif "予定" in message:  # 予定に関連するクエリに対応
        return reply_events(event)
    if state == "waiting_for_city":
        return reply_weather(message, line_id, state)  # 都市名の入力を処理
    
    # ユーザーが天気情報を取得している途中で、日付を尋ねる状態
    elif state == "waiting_for_date":
        return reply_weather(message, line_id, state) 

    """

    pass