import asyncio

import websockets

async def sender(websocket):
    while True:
        message = await asyncio.to_thread(input, "Client. Enter message: ")
        await websocket.send(message)


async def receiver(websocket):
    async for message in websocket:
        print(f"\nReceived from Server : {message}")
        print(f"Enter message: ", end="", flush=True)

async def client():
    uri = "ws://localhost:9900"
    async with websockets.connect(uri) as websocket:
        await asyncio.gather(
            sender(websocket),
            receiver(websocket)
        )

if __name__ == "__main__":
    asyncio.run(client())




# async def client():
#     uri = "ws://localhost:9090"
#     async with websockets.connect(uri) as websocket:
#         while True:
#             message = input("Client. Enter message: ")
#             await websocket.send(message)
#             response = await websocket.recv()
#             print("Received from Server:", response)
#
# if __name__ == "__main__":
#     asyncio.run(client())

