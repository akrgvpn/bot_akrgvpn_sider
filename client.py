import asyncio  
from typing import Dict, Any  
from marzban_client import MarzbanClient  
from config import LIMIT_IP  
from logger import logger  

class MarzbanClientManager:  
    def __init__(self, marzban_client: MarzbanClient):  
        self.client = marzban_client  

    async def add_client(  
        self,  
        username: str,  
        email: str,  
        tg_id: str,  
        total_gb: int,  
        expiry_time: int,  
        service_name: str = 'default'  
    ) -> Dict[str, Any]:  
        """  
        Добавление нового клиента в Marzban  
        """  
        try:  
            # Подготовка данных для создания пользователя  
            user_data = {  
                'username': username,  
                'email': email,  
                'service': service_name,  
                'data_limit': total_gb * 1024 * 1024 * 1024,  # Конвертация ГБ в байты  
                'expire': expiry_time,  
                'proxies': {  
                    'vless': {},  
                    'vmess': {},  
                    'trojan': {}  
                },  
                'status': 'active',  
                'note': f'Telegram ID: {tg_id}'  
            }  

            # Создание пользователя  
            response = await self.client.create_user(user_data)  
            
            logger.info(f"Клиент {username} успешно добавлен в Marzban.")  
            return {"status": "success", "data": response}  

        except Exception as e:  
            logger.error(f"Ошибка при добавлении клиента {username}: {e}")  
            return {"status": "failed", "error": str(e)}  

    async def extend_client(  
        self,  
        username: str,  
        total_gb: int,  
        expiry_time: int  
    ) -> Dict[str, Any]:  
        """  
        Продление подписки клиента в Marzban  
        """  
        try:  
            # Получение текущих данных пользователя  
            user = await self.client.get_user(username)  

            # Подготовка данных для обновления  
            update_data = {  
                'data_limit': total_gb * 1024 * 1024 * 1024,  # Конвертация ГБ в байты  
                'expire': expiry_time,  
                'status': 'active'  
            }  

            # Обновление пользователя  
            response = await self.client.modify_user(username, update_data)  
            
            logger.info(f"Подписка клиента {username} успешно продлена.")  
            return {"status": "success", "data": response}  

        except Exception as e:  
            logger.error(f"Ошибка при продлении подписки для {username}: {e}")  
            return {"status": "failed", "error": str(e)}  

    async def delete_client(self, username: str) -> Dict[str, Any]:  
        """  
        Удаление клиента из Marzban  
        """  
        try:  
            # Удаление пользователя  
            await self.client.delete_user(username)  
            
            logger.info(f"Клиент {username} успешно удален из Marzban.")  
            return {"status": "success"}  

        except Exception as e:  
            logger.error(f"Ошибка при удалении клиента {username}: {e}")  
            return {"status": "failed", "error": str(e)}  

    async def get_client_info(self, username: str) -> Dict[str, Any]:  
        """  
        Получение информации о клиенте  
        """  
        try:  
            user_info = await self.client.get_user(username)  
            return {"status": "success", "data": user_info}  
        except Exception as e:  
            logger.error(f"Ошибка при получении информации о клиенте {username}: {e}")  
            return {"status": "failed", "error": str(e)}