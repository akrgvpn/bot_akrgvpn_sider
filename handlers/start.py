from aiogram import Router, F  
from aiogram.types import Message, CallbackQuery  
from aiogram.filters import CommandStart  
from aiogram.fsm.context import FSMContext  

from config import TELEGRAM_ADMIN_IDS  
from user_manager import UserManager  
from keyboards.start_keyboard import (  
    get_start_keyboard,   
    get_admin_start_keyboard,  
    get_referral_keyboard  
)  

start_router = Router()  

@start_router.message(CommandStart())  
async def cmd_start(  
    message: Message,   
    state: FSMContext,   
    user_manager: UserManager  
):  
    """  
    Обработка команды /start  
    """  
    try:  
        # Извлечение реферального кода  
        referrer_id = None  
        parts = message.text.split()  
        if len(parts) > 1:  
            try:  
                referrer_id = int(parts[1])  
                # Проверка валидности реферера  
                if referrer_id in TELEGRAM_ADMIN_IDS:  
                    referrer_id = None  
            except ValueError:  
                referrer_id = None  

        # Регистрация пользователя  
        user_data = await user_manager.register_user(  
            telegram_user=message.from_user,  
            referrer_id=referrer_id  
        )  

        # Выбор клавиатуры  
        keyboard = (  
            get_admin_start_keyboard()   
            if message.from_user.id in TELEGRAM_ADMIN_IDS   
            else get_start_keyboard()  
        )  

        # Отправка приветственного сообщения  
        await message.answer(  
            f"👋 Привет, {message.from_user.first_name}!\n\n"  
            f"Твой VPN аккаунт успешно создан:\n"  
            f"🔑 Логин: `{user_data['marzban_username']}`\n\n"  
            f"Ссылка на подписку:\n"  
            f"`{user_data['subscription_link']}`",  
            reply_markup=keyboard,  
            parse_mode='Markdown'  
        )  

        # Отправка реферальной клавиатуры  
        if referrer_id:  
            await message.answer(  
                "🤝 Вы были приглашены по реферальной ссылке!",  
                reply_markup=get_referral_keyboard()  
            )  

    except Exception as e:  
        await message.answer(  
            "❌ Произошла ошибка при регистрации. "  
            "Пожалуйста, попробуйте позже или свяжитесь с поддержкой."  
        )  
        # Логирование ошибки  
        user_manager.logger.error(f"Ошибка регистрации: {e}")