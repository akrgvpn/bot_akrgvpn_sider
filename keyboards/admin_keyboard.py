from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup  

def get_admin_menu_keyboard() -> InlineKeyboardMarkup:  
    """Клавиатура администратора"""  
    builder = InlineKeyboardBuilder()  
    builder.button(text="👥 Список пользователей", callback_data="admin_users_list")  
    builder.button(text="🌐 Статистика серверов", callback_data="admin_server_stats")  
    builder.button(text="🔑 Генерация ключей", callback_data="admin_key_generation")  
    builder.adjust(2)  
    return builder.as_markup()  

def get_users_list_keyboard() -> InlineKeyboardMarkup:  
    """Клавиатура списка пользователей"""  
    builder = InlineKeyboardBuilder()  
    builder.button(text="⬅️ Предыдущие", callback_data="users_list_prev")  
    builder.button(text="Следующие ➡️", callback_data="users_list_next")  
    builder.button(text="🔙 Назад", callback_data="back_to_admin_menu")  
    builder.adjust(2)  
    return builder.as_markup()  

def get_key_generation_keyboard() -> InlineKeyboardMarkup:  
    """Клавиатура генерации ключей"""  
    builder = InlineKeyboardBuilder()  
    builder.button(text="VLESS", callback_data="generate_key_vless")  
    builder.button(text="VMESS", callback_data="generate_key_vmess")  
    builder.button(text="Trojan", callback_data="generate_key_trojan")  
    builder.button(text="🔙 Назад", callback_data="back_to_admin_menu")  
    builder.adjust(2)  
    return builder.as_markup()  

def get_server_stats_keyboard() -> InlineKeyboardMarkup:  
    """Клавиатура статистики серверов"""  
    builder = InlineKeyboardBuilder()  
    builder.button(text="🔄 Обновить", callback_data="refresh_server_stats")  
    builder.button(text="🔙 Назад", callback_data="back_to_admin_menu")  
    builder.adjust(2)  
    return builder.as_markup()