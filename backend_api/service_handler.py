import asyncio
import json
from aiohttp import web
from .send_message_to_telegram import send_message_to_telegram
from log_config import get_logger

logger = get_logger(__name__)

async def service_handler(request):
    try:
        logger.info("Service_handler Working--->(UI)")
        data = await request.json()
        required_fields = ["full_name", "email", "phone", "service"]
        if not all(field in data for field in required_fields):
            return web.json_response(
                data={
                    "status": "error",
                    "message": {
                        "ru": "Заполните все поля!",
                        "en": "Fill in all fields!",
                        "kz": "Барлық өрістерді толтырыңыз!"
                    }
                },
                status=400)

        asyncio.create_task(send_message_to_telegram(data, "service"))
        logger.info("Service_handler End--->(UI)")

        return web.json_response(
            data={
                "status": "success",
                "message": {
                    "ru": "Сообщение успешно отправлено!",
                    "en": "Message sent successfully!",
                    "kz": "Хабарлама сәтті жіберілді!"
                }
            },
            status=201)
    except json.JSONDecodeError:
        logger.info("Service_handler Exception Working--->(UI)")
        return web.json_response(
            data={
                "status": "error",
                "message": {
                    "ru": "Произошла ошибка!",
                    "en": " An error occurred!",
                    "kz": "Қате орын алды!"
                }
            },
            status=400)


