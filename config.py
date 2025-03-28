import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Token
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Настройки сервера
HOST = "0.0.0.0"
PORT = 8000

# Базовый URL для вебхуков
BASE_WEBHOOK_URL = "http://your-domain.com/webhook"  # Замените на ваш домен 