import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message

TOKEN = "9290937877:AAF131scLcc50oA-65aHFKiMMhenrK1uUR8"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Привіт! Я твій бот для обробки фотографій товарів і деталей. "
        "Надішли мені фото, і я оброблю його відповідно до навички."
    )

@dp.message(lambda message: message.photo is not None)
async def handle_photo(message: Message):
    processing_msg = await message.answer("Обробляю зображення...")

    try:
        photo = message.photo[-1]
        file_info = await bot.get_file(photo.file_id)

        os.makedirs("downloads", exist_ok=True)
        downloaded_file_path = f"downloads/{photo.file_id}.jpg"
        await bot.download_file(file_info.file_path, downloaded_file_path)

        await message.answer("Фото успішно отримано! Готово до інтеграції обробки.")

    except Exception as e:
        await message.answer(f"Сталася помилка: {e}")
    finally:
        if os.path.exists(downloaded_file_path):
            os.remove(downloaded_file_path)
        await bot.delete_message(chat_id=message.chat.id, message_id=processing_msg.message_id)

async def main():
    print("Бот запущено і готовий до роботи...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
