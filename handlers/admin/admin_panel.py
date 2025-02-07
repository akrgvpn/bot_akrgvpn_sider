from aiogram import Router, F  
from aiogram.types import Message, CallbackQuery  
from aiogram.filters import Command  

from config import TELEGRAM_ADMIN_IDS  
from user_manager import UserManager  
from marzban_client import MarzbanClient  
from keyboards.admin_keyboard import (  
    get_admin_menu_keyboard,  
    get_users_list_keyboard,  
    get_server_stats_keyboard  
)  

admin_router = Router()  

def admin_only():  
    async def predicate(message: Message):  
        return message.from_user.id in TELEGRAM_ADMIN_IDS  
    return predicate  

@admin_router.message(Command("admin"), admin_only())  
async def admin_panel(  
    message: Message,   
    user_manager: UserManager  
):  
    """  
    Главное меню администратора  
    """  
    admin_menu_text = (  
        "🛠 Панель администратора:\n\n"  
        "• Статистика пользователей\n"  
        "• Управление подписками\n"  
        "• Генерация ключей\n"  
        "• Мониторинг серверов"  
    )  
    
    await message.answer(  
        admin_menu_text,   
        reply_markup=get_admin_menu_keyboard()  
    )  

@admin_router.callback_query(F.data == "admin_users_list")  
async def admin_users_list(  
    callback: CallbackQuery,   
    user_manager: UserManager  
):  
    """  
    Список пользователей  
    """  
    try:  
        users = await user_manager.get_users_list()  

        users_text = "👥 Список пользователей:\n\n"  
        for user in users:  
            users_text += (  
                f"🆔 Telegram ID: {user['telegram_id']}\n"  
                f"👤 Username: @{user['username'] or 'Не указан'}\n"  
                f"🔑 VPN Логин: `{user['marzban_username']}`\n"  
                f"📅 Дата регистрации: {user['registration_date']}\n\n"  
            )  

        await callback.message.edit_text(  
            users_text,   
            parse_mode='Markdown',  
            reply_markup=get_users_list_keyboard()  
        )  
        await callback.answer()  

    except Exception as e:  
        await callback.message.answer(  
            f"❌ Ошибка получения списка: {e}"  
        )