import asyncio
import httpx

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from fastapi import status

from .logger import get_logger
from app.settings import settings 

logger = get_logger(__name__)

bot  = Bot(token=str(settings.BOT_TOKEN))

dp = Dispatcher()

@dp.message(CommandStart())
async def handle_start(message: Message):
	chat_id = message.from_user.id
	url =f"{settings.HOST}/check_user/{chat_id}"

	async with httpx.AsyncClient() as client: 
		user = await client.get(url=url)
		if user.status_code == status.HTTP_200_OK:
			await message.answer(text="🚫 Siz xali royxatdan otmagansiz. \nRo'yxatdan otish uchun telefon raqamingizni kiriting👇")
			return
		
		keyboard = ReplyKeyboardMarkup(
			keyboard = [
					[KeyboardButton(text="📞 Telefon raqamini yuborish", request_contact=True)]
			], resize_keyboard=True
		)


		text = f""""
			🇺🇿
			Salom {message.from_user.first_name} 👋
			testning rasmiy botiga xush kelibsiz
			
			⬇️ Kontaktingizni yuboring (tugmani bosib)
			
			🇺🇸
			Hi {message.from_user.first_name} 👋 
			Welcome to test's official bot
			
			⬇️ Send your contact (by clicking button)
		
		"""

	await message.answer(text=text, reply_markup=keyboard)




@dp.message(F.contact)
async def handle_contact(message: Message, ):
	chat_id  = message.from_user.id 
	phone_number = message.contact.phone_number

	if  not phone_number.startswith("+"): 
		phone_number = "+" +  phone_number

	first_name = message.from_user.first_name
	last_name = message.from_user.last_name  if message.from_user.last_name is not None else f"username_{chat_id}" 
	username = message.from_user.username if message.from_user.username is not None else f"username_{chat_id}" 
	print(f"first_name:{first_name} - last_name:{last_name} - {username}")


async def main():
	await dp.start_polling(bot)
	logger.info("Bot runnned")

if __name__ == "__main__": 
	asyncio.run(main())