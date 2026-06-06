import os
import asyncio
from dotenv import load_dotenv
from telegram import Bot

# 1. Carga las variables una sola vez al inicio
load_dotenv()
TOKEN = os.getenv('TOKEN_TEL')
CHAT_ID = os.getenv('CHAT_ID')

# 2. Instancia el bot una sola vez (es un objeto persistente)
bot = Bot(token=TOKEN)

async def send_message_async(texto):
    try:
        # Reutilizamos el objeto bot ya instanciado
        await bot.send_message(chat_id=CHAT_ID, text=texto)
    except Exception as e:
        print(f"Error en Telegram: {e}")

def alert(texto):
    # Solo disparas el envío
    asyncio.run(send_message_async(texto))