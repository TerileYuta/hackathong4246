def get_user_state(line_id):
    """

    ユーザーの現在の状態と追加のコンテキスト（例: 都市名）を取得する

    Parameters
    ----------
        line_id(str) : ユーザーのID

    Returns
    ----------
        dict : ユーザーの状態とコンテキスト（ない場合はNone）

    """
    return user_states.get(line_id, None)

def update_user_state(line_id, state, context=None):
    """

    ユーザーの状態と追加のコンテキスト（例: 都市名）を更新する

    Parameters
    ----------
        line_id(str) : ユーザーのID
        state(str) : ユーザーの状態
        context(dict) : 状態に関連するコンテキスト（デフォルトはNone）

    """

    if context is None:
        context = {}  # コンテキストが提供されていない場合は空の辞書を設定
    user_states[line_id] = {"state": state, "context": context}