import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import bot


def test_fetch_weather_without_api_key(monkeypatch):
    monkeypatch.setattr(bot, "OPENWEATHER_API_KEY", None)
    result = bot.fetch_weather("London")
    assert result == "Weather service is not configured."