import os
from dotenv import load_dotenv
load_dotenv()


import asyncio
import multiprocessing
from aiohttp import web
import aiohttp_cors
from tg_bot import main_bot
from backend_api import contact_handler, service_handler

PORT = os.getenv("PORT")

async def index(request):
    return web.FileResponse("templates/index.html")

async def about(request):
    return web.FileResponse("templates/about.html")

async def service(request):
    return web.FileResponse("templates/service.html")

async def contact(request):
    return web.FileResponse("templates/contact.html")


async def start_server():
    app = web.Application()

    app.router.add_get("/", index)
    app.router.add_get("/about", about)
    app.router.add_get("/service", service)
    app.router.add_get("/contact", contact)

    app.router.add_post("/contact", contact_handler)
    app.router.add_post("/service", service_handler)

    app.router.add_static("/static/", path="static", name="static")


    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
            allow_methods=["GET", "POST", "OPTIONS"]
        )
    })

    for route in list(app.router.routes()):
        cors.add(route)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()
    print(f" Server is working ---------> (UI) ")
    while True:
        await asyncio.sleep(3600)


if __name__ == "__main__":
    def start_bot():
        asyncio.run(main_bot())

    def run_server():
        asyncio.run(start_server())

    server_process = multiprocessing.Process(target=run_server)
    bot_process = multiprocessing.Process(target=start_bot)

    server_process.start()
    bot_process.start()

    server_process.join()
    bot_process.join()
