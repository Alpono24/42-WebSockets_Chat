# Вносим изменения в сервер чтобы он смог обрабатывать более одного клиента
import asyncio
import websockets

connected_clients = set()

async def server(websocket):
    connected_clients.add(websocket)
    print("Client connected")
    try:
        async for message in websocket:
            print(f"Received: {message}")
            for client in connected_clients:
                 await client.send(f'Echo: {message}')
    finally:
        connected_clients.remove(websocket)
        print("Client disconnected")

async def main():
    async with websockets.serve(server, 'localhost', 9900):
        print("Server started on ws://localhost:9900")
        await asyncio.Future() # что бы сервер работал бесконечно

if __name__ == "__main__":
    asyncio.run(main()) # asyncio.run

