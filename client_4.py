import asyncio
import websockets
import re
from datetime import datetime


red_words = ["qwe", "qwer", "qwert", "qwerty"]
red_symbols = r"[\\$\\@\\&\\-\\=\\+]"


async def sender(websocket):
    while True:
        message = await asyncio.to_thread(input, "Введите сообщение: ")

        # Ограничение на ввод определенных символов или слов
        for word in red_words:
            if word.lower() in message.lower():
                print(f"⚠️ Сообщение содержит недопустимое слово: '{word}'")
                break
        else:
            if re.search(red_symbols, message):
                print("⚠️ Cообщение содержит недопустимые символы.")
            else:
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                full_message = f"{current_time}: {message}"
                await websocket.send(full_message)


async def receiver(websocket):
    async for message in websocket:
        print(f"\n ✅ Получено: {message}")
        print("Введите сообщение: ", end="", flush=True)


async def client():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        prompt = await  websocket.recv()
        print(prompt)

        # Обеспечить обязательный ввод имени пользователя чата
        while True:
            name = input().strip()
            if name:
                break
            else:
                print("⚠️ ️Имя обязательно для заполнения.")

        await websocket.send(name)
        await asyncio.gather(sender(websocket), receiver(websocket))

if __name__ == "__main__":
    asyncio.run(client())

