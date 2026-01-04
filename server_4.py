# Вносим изменения в сервер:
# 1 - создаем словарь с пользователями

import asyncio
import websockets

connected_clients = {}

async  def broadcast(message):
    disconnected = []

    for client in connected_clients:
        try:
            await client.send(f'{message}')
        except websockets.exceptions.ConnectionClosedOK:
            disconnected.append(client)

    for client in disconnected:
        connected_clients.pop(client)


async def server(websocket):
    await websocket.send("📌 Введите ваше имя: ")
    username = await websocket.recv()
    connected_clients[websocket] = username
    print(f"✅ {username} онлайн")
    await broadcast(f"👤 {username} подключен к чату")

    try:
        async for message in websocket:
            print(f"{username}: {message}")
            await broadcast(f"{username}: {message}")

    except websockets.exceptions.ConnectionClosedOK:
        pass

    finally:
        connected_clients.pop(websocket)
        print(f"❌ {username} отключено")
        await broadcast(f" 👋 {username} покинул чат")

async def main():
    async with websockets.serve(server, 'localhost', 8765):
        print("🚀 Сервер запущен на ws://localhost:8765")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
