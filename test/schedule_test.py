from pathlib import Path
import sys

# 親ディレクトリをパスに追加
sys.path.append(str(Path(__file__).resolve().parent.parent))

from services.features import Schedule
from datetime import datetime


sche = Schedule("lineID")

sche.delete_event(
    "j59ruh72hgepuvt8prdt1g26ec",
)