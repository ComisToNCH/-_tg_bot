# Weather Telegram Bot

A Telegram bot that provides current weather information for a given city and can send scheduled daily updates.

## Setup

1. Copy `.env.example` to `.env` and fill in your `TELEGRAM_TOKEN` and `OPENWEATHER_API_KEY`.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the bot:
   ```bash
   python bot.py
   ```

## Commands

- `/weather <city>` – get current weather for the city.
- `/set <HH:MM> <city>` – schedule a daily weather message at the specified time.
- `/unset` – cancel scheduled notifications.

## Project structure

```
.
├── bot.py            # bot implementation and entry point
├── requirements.txt  # Python dependencies
├── .env.example      # template for required environment variables
└── tests/            # Pytest-based test suite
```

## Testing

Run the tests to check that the project is installed correctly:

```bash
pytest -q
```

## Next steps

- Add more commands or handlers as needed.
- Dive into the [python-telegram-bot](https://docs.python-telegram-bot.org/) documentation for advanced usage.
- Consider adding persistence, databases or deployment scripts when the bot grows.

