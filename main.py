import asyncio  
import logging  
from aiogram import Bot, Dispatcher  
from aiogram.fsm.storage.memory import MemoryStorage  
from aiogram.types import BotCommand  

from config import TELEGRAM_BOT_TOKEN, TELEGRAM_ADMIN_IDS  
from database import Database  
from user_manager import UserManager  
from marzban_client import MarzbanClient  

# Импорт всех роутеров  
from handlers.start import start_router  
from handlers.profile import profile_router  
from handlers.admin.admin_panel import admin_router  
from handlers.keys.key_management import key_router  

# Настройка логирования  
logging.basicConfig(  
    level=logging.INFO,  
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'  
)  
logger = logging.getLogger(__name__)  

async def set_commands(bot: Bot):  
    """Установка команд бота"""  
    commands = [  
        BotCommand(command="start", description="Начать работу"),  
        BotCommand(command="profile", description="Мой профиль"),  
        BotCommand(command="admin", description="Панель администратора")  
    ]  
    await bot.set_my_commands(commands)  

async def main():  
    # Инициализация компонентов  
    db = Database('database.db')  
    await db.create_tables()  

    marzban_client = MarzbanClient()  
    user_manager = UserManager(db, marzban_client)  

    # Инициализация бота и диспетчера  
    bot = Bot(token=TELEGRAM_BOT_TOKEN)  
    storage = MemoryStorage()  
    dp = Dispatcher(storage=storage)  

    # Внедрение зависимостей  
    dp.workflow_data.update({  
        'db': db,  
        'user_manager': user_manager,  
        'marzban_client': marzban_client  
    })  

    # Регистрация роутеров  
    dp.include_routers(  
        start_router,   
        profile_router,   
        admin_router,  
        key_router  
    )  

    # Установка команд  
    await set_commands(bot)  

    # Уведомление администраторов о старте  
    for admin_id in TELEGRAM_ADMIN_IDS:  
        try:  
            await bot.send_message(  
                admin_id,   
                "✅ Бот успешно запущен и готов к работе!"  
            )  
        except Exception as e:  
            logger.error(f"Не удалось отправить уведомление администратору {admin_id}: {e}")  

    # Запуск бота  
    try:  
        await dp.start_polling(  
            bot,   
            allowed_updates=dp.resolve_used_update_types()  
        )  
    except Exception as e:  
        logger.error(f"Ошибка при запуске бота: {e}")  
    finally:  
        await bot.session.close()  
        await db.close()  

if __name__ == '__main__':  
    try:  
        asyncio.run(main())  
    except (KeyboardInterrupt, SystemExit):  
        logger.info("Бот остановлен")