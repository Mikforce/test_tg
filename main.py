import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from telegram import Bot
from dotenv import load_dotenv
from typing import Dict, Optional
import json

# Загрузка переменных окружения
load_dotenv()

app = FastAPI()

# Словарь для хранения активных кампаний
active_campaigns: Dict[str, Dict] = {}

# Получение токена бота из переменных окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)

@app.get("/")
async def root():
    return {"message": "Webhook server is running"}

@app.post("/webhook/{campaign_id}")
async def webhook_handler(campaign_id: str, request: Request):
    data = await request.json()
    
    # Проверка на тестовый запрос
    if "TGSTAT_VERIFY_CODE" in str(data):
        verify_code = str(data).split("TGSTAT_VERIFY_CODE_")[1].split("'")[0]
        return JSONResponse(content={"code": verify_code})
    
    # Обработка обычного вебхука
    if campaign_id in active_campaigns:
        campaign = active_campaigns[campaign_id]
        target_chat = campaign.get("target_chat")
        
        if target_chat:
            message = format_message(data)
            await bot.send_message(chat_id=target_chat, text=message)
    
    return {"status": "success"}

@app.post("/start_campaign")
async def start_campaign(campaign_id: str, target_chat: str):
    active_campaigns[campaign_id] = {
        "target_chat": target_chat,
        "status": "active"
    }
    await bot.send_message(
        chat_id=target_chat,
        text=f"Кампания {campaign_id} успешно подключена и готова к работе!"
    )
    return {"status": "success", "message": f"Campaign {campaign_id} started"}

def format_message(data: dict) -> str:
    """Форматирование сообщения из вебхука"""
    return f"""
📝 Новый пост:
{data.get('postText', 'Нет текста')}

🔗 Ссылка: {data.get('postLink', 'Нет ссылки')}
👁 Просмотры: {data.get('postViews', 0)}
📅 Дата: {data.get('postDate', 'Не указана')}
"""

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 