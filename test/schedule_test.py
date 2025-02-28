from pathlib import Path
import sys

# 親ディレクトリをパスに追加
sys.path.append(str(Path(__file__).resolve().parent.parent))

from services.features.weather import get_weather
from datetime import datetime

print(get_weather("長野県", datetime(2025, 3, 1, 15, 0, 0)))