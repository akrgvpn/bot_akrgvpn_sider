import aiohttp  
import asyncio  
from typing import Dict, Any  
from config import MARZBAN_URL, MARZBAN_USERNAME, MARZBAN_PASSWORD  

class MarzbanClient:  
    def __init__(  
        self,   
        base_url: str = MARZBAN_URL,   
        username: str = MARZBAN_USERNAME,   
        password: str = MARZBAN_PASSWORD  
    ):  
        self.base_url = base_url.rstrip('/')  
        self.username = username  
        self.password = password  
        self.access_token = None  
        self.refresh_token = None  

    async def _get_token(self) -> None:  
        """Получение токена авторизации"""  
        async with aiohttp.ClientSession() as session:  
            try:  
                async with session.post(  
                    f"{self.base_url}/api/admin/token",   
                    json={  
                        "username": self.username,   
                        "password": self.password  
                    }  
                ) as response:  
                    if response.status == 200:  
                        tokens = await response.json()  
                        self.access_token = tokens.get('access_token')  
                        self.refresh_token = tokens.get('refresh_token')  
                    else:  
                        raise Exception("Не удалось получить токен")  
            except Exception as e:  
                raise Exception(f"Ошибка аутентификации: {e}")  

    async def _ensure_token(self):  
        """Проверка и обновление токена"""  
        if not self.access_token:  
            await self._get_token()  

    async def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:  
        """Создание нового пользователя"""  
        await self._ensure_token()  
        
        async with aiohttp.ClientSession() as session:  
            headers = {"Authorization": f"Bearer {self.access_token}"}  
            async with session.post(  
                f"{self.base_url}/api/users",   
                json=user_data,   
                headers=headers  
            ) as response:  
                if response.status in [200, 201]:  
                    return await response.json()  
                else:  
                    error_text = await response.text()  
                    raise Exception(f"Ошибка создания пользователя: {error_text}")  

    async def get_user(self, username: str) -> Dict[str, Any]:  
        """Получение информации о пользователе"""  
        await self._ensure_token()  
        
        async with aiohttp.ClientSession() as session:  
            headers = {"Authorization": f"Bearer {self.access_token}"}  
            async with session.get(  
                f"{self.base_url}/api/users/{username}",   
                headers=headers  
            ) as response:  
                if response.status == 200:  
                    return await response.json()  
                else:  
                    error_text = await response.text()  
                    raise Exception(f"Ошибка получения пользователя: {error_text}")  

    async def modify_user(self, username: str, user_data: Dict[str, Any]) -> Dict[str, Any]:  
        """Изменение данных пользователя"""  
        await self._ensure_token()  
        
        async with aiohttp.ClientSession() as session:  
            headers = {"Authorization": f"Bearer {self.access_token}"}  
            async with session.put(  
                f"{self.base_url}/api/users/{username}",   
                json=user_data,   
                headers=headers  
            ) as response:  
                if response.status == 200:  
                    return await response.json()  
                else:  
                    error_text = await response.text()  
                    raise Exception(f"Ошибка изменения пользователя: {error_text}")  

    async def delete_user(self, username: str) -> bool:  
        """Удаление пользователя"""  
        await self._ensure_token()  
        
        async with aiohttp.ClientSession() as session:  
            headers = {"Authorization": f"Bearer {self.access_token}"}  
            async with session.delete(  
                f"{self.base_url}/api/users/{username}",   
                headers=headers  
            ) as response:  
                if response.status == 204:  
                    return True  
                else:  
                    error_text = await response.text()  
                    raise Exception(f"Ошибка удаления пользователя: {error_text}")  

    async def get_user_subscription_link(self, username: str) -> str:  
        """Получение ссылки на подписку"""  
        await self._ensure_token()  
        
        async with aiohttp.ClientSession() as session:  
            headers = {"Authorization": f"Bearer {self.access_token}"}  
            async with session.get(  
                f"{self.base_url}/api/user/{username}/subscription",   
                headers=headers  
            ) as response:  
                if response.status == 200:  
                    data = await response.json()  
                    return data.get('subscription_link', '')  
                else:  
                    error_text = await response.text()  
                    raise Exception(f"Ошибка получения ссылки подписки: {error_text}")