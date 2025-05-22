# aiohttp_server.py
from aiohttp import web
import aiohttp
import asyncio


async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = f"Hello, {name}"
    return web.Response(text=text)


async def fetch(client):
    async with client.get('https://example.com') as resp:
        return await resp.text()


async def init_app():
    app = web.Application()
    app.router.add_get('/', handle)
    app.router.add_get('/{name}', handle)

    # 添加一个异步HTTP客户端示例
    async def client_example(request):
        async with aiohttp.ClientSession() as client:
            html = await fetch(client)
            return web.Response(text=f"Fetched {len(html)} bytes from example.com")

    app.router.add_get('/fetch', client_example)
    return app


web.run_app(init_app(), port=8080)
print("Server running at http://localhost:8080")