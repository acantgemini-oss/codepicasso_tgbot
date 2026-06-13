import asyncio
import os
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from dotenv import load_dotenv

from api_fetcher import get_market_data

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# --- Keyboard Generator ---
def get_main_keyboard():
    buttons = [
        [InlineKeyboardButton(text="🔄 دریافت قیمت‌های لحظه‌ای", callback_data="fetch_prices")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# --- Handlers ---
@dp.message(CommandStart())
async def command_start_handler(message: types.Message) -> None:
    welcome_text = (
        "سلام! من «صراف‌باشی» هستم؛ دستیار سریع و رایگان شما برای چک کردن بازار. 💸\n\n"
        "اینجا می‌تونی در کسری از ثانیه قیمت لحظه‌ای این موارد رو به **ریال / دلار** ببینی:\n"
        "🇺🇸 دلار\n"
        "🇪🇺 یورو\n"
        "🥇 طلای ۱۸ عیار\n"
        "🥈 انس نقره\n\n"
        "برای دریافت آخرین قیمت‌ها، روی دکمه زیر کلیک کنید 👇"
    )
    await message.answer(welcome_text, reply_markup=get_main_keyboard())

@dp.callback_query(F.data == "fetch_prices")
async def handle_fetch_prices(callback: CallbackQuery):
    await callback.message.edit_text("⏳ در حال دریافت اطلاعات از بازار... لطفا کمی صبر کنید.")
    
    # Call the API
    data = await get_market_data()
    
    if data:
        result_text = (
            "📊 <b>قیمت‌های لحظه‌ای بازار:</b>\n\n"
            f"🇺🇸 <b>دلار آمریکا:</b> {data['usd']}\n"
            f"🇪🇺 <b>یورو:</b> {data['eur']}\n"
            f"🥇 <b>طلای 18 عیار:</b> {data['gold_18k']}\n"
            f"🥈 <b>انس نقره:</b> {data['silver_ounce']}\n\n"
            "⏱ <i>به‌روزرسانی شده از سرور صراف‌باشی</i>"
        )
    else:
        result_text = "❌ متاسفانه در ارتباط با سرور قیمت‌ها مشکلی پیش آمد. لطفا دقایقی دیگر دوباره تلاش کنید."
        
    await callback.message.edit_text(result_text, reply_markup=get_main_keyboard(), parse_mode="HTML")

# --- Startup ---
async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    print("صراف‌باشی در حال اجراست... (Bot is starting...)")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())