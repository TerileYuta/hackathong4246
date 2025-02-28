def open_text_file(filename: str):
    """
    
    textファイルを開き、内容を返すヘルパー関数

    Parameters
    ----------
        filename(str) : ファイル名
    
    Returns
    ----------
        str : ファイルの中身

    """
    text = ""

    with open(filename, 'r') as f:
        text = f.read()

    return text