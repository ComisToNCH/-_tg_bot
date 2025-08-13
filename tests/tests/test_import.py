import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import bot


def test_import_only():
    assert hasattr(bot, 'fetch_weather')