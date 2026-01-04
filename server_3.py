# Вносим изменения в сервер:
# 1 - отлавливание ошибок для стабильной работы сервера +
# 2 - создаем список клиентов которые отключены +

import asyncio
import websockets

connected_clients = set()

async def server(websocket):
    connected_clients.add(websocket) # добавляем в наше множество соединение websocket
    print("Client connected")

    try:
        async for message in websocket:
            print(f"Received: {message}")
            disconnected = []

            for client in connected_clients:
                try:
                     await client.send(f'Echo: {message}')
                except websockets.exceptions.ConnectionClosedOK:
                    disconnected.append(client)
            for client in disconnected:
                connected_clients.remove(client)
    except websocket.exceptions.ConnectionClosedOK:
        pass

    finally:
        connected_clients.remove(websocket)
        print("Client disconnected")

async def main():
    async with websockets.serve(server, 'localhost', 8765):
        print("Server started on ws://localhost:8765")
        await asyncio.Future() # что бы сервер работал бесконечно

if __name__ == "__main__":
    asyncio.run(main()) # asyncio.run
