import os
from datetime import time as dtime

import requests
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

load_dotenv()
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")


def fetch_weather(city: str) -> str:
    """Return a short weather summary for ``city``."""
    if not OPENWEATHER_API_KEY:
        return "Weather service is not configured."

    params = {
        "q": city,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric",
        "lang": "en",
    }
    try:
        response = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params=params,
            timeout=10,
        )
        response.raise_for_status()
    except requests.RequestException:
        return f"Cannot retrieve weather for {city}."

    data = response.json()
    description = data["weather"][0]["description"]
    temp = data["main"]["temp"]
    return f"Weather in {city}: {description}, {temp}°C"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Greet the user."""
    await update.message.reply_text(
        "Use /weather <city> for current weather and /set <HH:MM> <city> "
        "to schedule daily updates."
    )


async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send weather for a given city."""
    if not context.args:
        await update.message.reply_text("Usage: /weather <city>")
        return
    city = " ".join(context.args)
    await update.message.reply_text(fetch_weather(city))


async def send_scheduled(context: ContextTypes.DEFAULT_TYPE) -> None:
    job = context.job
    chat_id = job.context["chat_id"]
    city = job.context["city"]
    await context.bot.send_message(chat_id, text=fetch_weather(city))


async def set_timer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Schedule daily weather notification."""
    if len(context.args) < 2:
        await update.message.reply_text("Usage: /set <HH:MM> <city>")
        return

    time_str = context.args[0]
    city = " ".join(context.args[1:])
    try:
        hour, minute = map(int, time_str.split(":"))
        notify_time = dtime(hour=hour, minute=minute)
    except Exception:
        await update.message.reply_text("Time format should be HH:MM")
        return

    chat_id = update.effective_chat.id
    context.job_queue.run_daily(
        send_scheduled,
        notify_time,
        context={"chat_id": chat_id, "city": city},
        name=str(chat_id),
    )
    await update.message.reply_text(
        f"Daily weather for {city} scheduled at {time_str}"
    )


async def unset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Cancel scheduled notifications."""
    chat_id = update.effective_chat.id
    jobs = context.job_queue.get_jobs_by_name(str(chat_id))
    for job in jobs:
        job.schedule_removal()
    if jobs:
        await update.message.reply_text("Notifications cancelled.")
    else:
        await update.message.reply_text("No active notifications.")


def main() -> None:
    """Run the bot."""
    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        raise RuntimeError("TELEGRAM_TOKEN is not set")

    application = ApplicationBuilder().token(token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("weather", weather))
    application.add_handler(CommandHandler("set", set_timer))
    application.add_handler(CommandHandler("unset", unset))

    application.run_polling()


if __name__ == "__main__":
    main()