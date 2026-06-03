import asyncio
import dotenv
from telegram import Bot


dotenv.load_dotenv()
TOKEN = dotenv.get_key('.env', 'TOKEN_TEL')
CHAT_ID = dotenv.get_key('.env', 'CHAT_ID')


async def enviar_mensaje_async(texto):
    bot = Bot(token=TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text=texto)





def alert (texto):
    try:
        asyncio.run(enviar_mensaje_async(texto))
    except Exception as e:
        print(f"Error sending message: {e}")



