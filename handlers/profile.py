from aiogram import Router, F  
from aiogram.types import Message, CallbackQuery  
from aiogram.filters import Command  

from user_manager import UserManager  
from keyboards.profile_keyboard import (  
    get_profile_keyboard,   
    get_extend_subscription_keyboard  
)  

profile_router = Router()  

@profile_router.message(Command("profile"))  
async def show_profile(  
    message: Message,   
    user_manager: UserManager  
):  
    """  
    Отображение профиля пользователя  
    """  
    try:  
        user_details = await user_manager.get_user_details(  
            telegram_id=message.from_user.id  
        )  

        profile_text = (  
            "👤 Профиль пользователя:\n\n"  
            f"🆔 Telegram ID: {message.from_user.id}\n"  
            f"📧 Username: @{message.from_user.username or 'Не указан'}\n"  
            f"🔑 VPN Логин: `{user_details['marzban_username']}`\n"  
            f"📅 Дата регистрации: {user_details['registration_date']}"  
        )  

        await message.answer(  
            profile_text,   
            reply_markup=get_profile_keyboard(),  
            parse_mode='Markdown'  
        )  

    except Exception as e:  
        await message.answer(  
            "❌ Не удалось загрузить профиль. Попробуйте позже."  
        )  
        user_manager.logger.error(f"Ошибка загрузки профиля: {e}")  

@profile_router.callback_query(F.data == "extend_subscription")  
async def extend_subscription(  
    callback: CallbackQuery  
):  
    """  
    Меню продления подписки  
    """  
    await callback.message.edit_text(  
        "🆙 Выберите период продления:",  
        reply_markup=get_extend_subscription_keyboard()  
    )  
    await callback.answer()