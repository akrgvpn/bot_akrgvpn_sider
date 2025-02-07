from aiogram.types import ReplyKeyboardMarkup, KeyboardButton  
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder, InlineKeyboardMarkup  

def get_start_keyboard() -> ReplyKeyboardMarkup:  
    """Основная клавиатура для обычных пользователей"""  
    builder = ReplyKeyboardBuilder()  
    builder.button(text="👤 Профиль")  
    builder.button(text="🌐 Мои подключения")  
    builder.button(text="💰 Продлить подписку")  
    builder.adjust(2)  
    return builder.as_markup(resize_keyboard=True)  

def get_admin_start_keyboard() -> ReplyKeyboardMarkup:  
    """Клавиатура для администраторов"""  
    builder = ReplyKeyboardBuilder()  
    builder.button(text="👤 Профиль")  
    builder.button(text="🌐 Мои подключения")  
    builder.button(text="💰 Продлить подписку")  
    builder.button(text="🛠 Панель администратора")  
    builder.adjust(2)  
    return builder.as_markup(resize_keyboard=True)  

def get_referral_keyboard() -> InlineKeyboardMarkup:  
    """Клавиатура для реферальной программы"""  
    builder = InlineKeyboardBuilder()  
    builder.button(text="🤝 Реферальная программа", callback_data="show_referral_info")  
    return builder.as_markup()