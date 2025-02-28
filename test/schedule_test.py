from pathlib import Path
import sys

# 親ディレクトリをパスに追加
sys.path.append(str(Path(__file__).resolve().parent.parent))

from services.features.schedule import getEvents
from datetime import datetime


print(getEvents("lineID", datetime(2025,1,7,0,0,0), datetime(2025,1,7,23,59,59)))