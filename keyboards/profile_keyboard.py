from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup  

def get_profile_keyboard() -> InlineKeyboardMarkup:  
    """Клавиатура профиля пользователя"""  
    builder = InlineKeyboardBuilder()  
    builder.button(text="🔑 Подписка", callback_data="show_subscription")  
    builder.button(text="💰 Продлить", callback_data="extend_subscription")  
    builder.adjust(2)  
    return builder.as_markup()  

def get_extend_subscription_keyboard() -> InlineKeyboardMarkup:  
    """Клавиатура продления подписки"""  
    builder = InlineKeyboardBuilder()  
    extend_options = [  
        ("30 дней", "extend_30"),  
        ("90 дней", "extend_90"),  
        ("180 дней", "extend_180")  
    ]  
    
    for label, callback_data in extend_options:  
        builder.button(text=label, callback_data=callback_data)  
    
    builder.button(text="🔙 Назад", callback_data="back_to_profile")  
    builder.adjust(2)  
    return builder.as_markup()