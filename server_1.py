# Только одни клиент
import asyncio
import websockets

async def server_1(websocket):
    print("Client connected")
    async for message in websocket:
        print(f"Received from Client: {message}")
        await websocket.send(f'Echo: {message}')


async def main():
    async with websockets.serve(server_1, 'localhost', 8765):
        print("🚀 Server started on ws://localhost:8765")
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main()) # asyncio.run
