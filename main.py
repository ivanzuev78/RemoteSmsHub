import os
from typing import Optional

from aiogram import Bot
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

TG_TOKEN = os.getenv('TG_TOKEN')
TG_NOTIFY_CHAT_ID = os.getenv('TG_NOTIFY_CHAT_ID')
if TG_NOTIFY_CHAT_ID:
    TG_NOTIFY_CHAT_ID = int(TG_NOTIFY_CHAT_ID)

if not TG_TOKEN:
    # for dev
    print('Токен не задан')
    TG_TOKEN = '1234567899:AA***'
    TG_NOTIFY_CHAT_ID = 123456789

bot = Bot(token=TG_TOKEN)


class SMSRequest(BaseModel):
    sender: str
    message: str
    who: str | None = None
    timestamp: Optional[int | str] = None


@app.post("/receive-sms/")
async def receive_sms(data: SMSRequest):
    print(f"Получено SMS {data}")
    text = f'Кто: {data.who}\nОтправитель: {data.sender}\n\n{data.message}'
    await bot.send_message(TG_NOTIFY_CHAT_ID, text)

    return {"status": "SMS получено"}


if __name__ == "__main__":
    # for dev
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=7837)
