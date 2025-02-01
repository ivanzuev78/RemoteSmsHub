import os
from typing import Optional

from aiogram import Bot
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

token = os.getenv('TG_TOKEN')
main_chat_id = os.getenv('TG_CHAT_ID')
if main_chat_id:
    main_chat_id = int(main_chat_id)

if not token:
    # for dev
    print('Токен не задан')
    token = '1234567899:AA***'
    main_chat_id = 123456789

bot = Bot(token=token)


class SMSRequest(BaseModel):
    sender: str  # Номер отправителя
    message: str  # Текст сообщения
    who: str | None = None  # Кто отправил (необязательно)
    timestamp: Optional[int | str] = None  # Время отправки (необязательно)


@app.post("/receive-sms/")
async def receive_sms(data: SMSRequest):
    print(f"Получено SMS {data}")
    text = f'Кто: {data.who}\nОтправитель: {data.sender}\n\n{data.message}'
    await bot.send_message(main_chat_id, text)

    return {"status": "SMS получено"}


if __name__ == "__main__":
    # for dev
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=7837)
