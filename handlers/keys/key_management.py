from aiogram import Router, F  
from aiogram.types import CallbackQuery  
from aiogram.fsm.context import FSMContext  

from user_manager import UserManager  
from keyboards.admin_keyboard import get_key_generation_keyboard  

key_router = Router()  

@key_router.callback_query(F.data.startswith("generate_key_"))  
async def generate_vpn_key(  
    callback: CallbackQuery,   
    user_manager: UserManager,  
    state: FSMContext  
):  
    """  
    Генерация VPN ключей с различными параметрами  
    """  
    try:  
        # Извлечение параметров из колбэка  
        key_type = callback.data.split("_")[2]  
        
        # Генерация ключа  
        generated_key = await user_manager.generate_admin_key(  
            key_type=key_type,  
            admin_id=callback.from_user.id  
        )  

        await callback.message.edit_text(  
            f"🔑 Сгенерирован ключ:\n`{generated_key}`\n\n"  
            "Используйте этот ключ для подключения.",  
            parse_mode='Markdown',  
            reply_markup=get_key_generation_keyboard()  
        )  
        await callback.answer()  

    except Exception as e:  
        await callback.message.answer(  
            f"❌ Ошибка генерации ключа: {e}"  
        )