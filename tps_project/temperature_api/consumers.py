import asyncio
import websockets
from channels.generic.websocket import AsyncWebsocketConsumer


class TemperatureConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Replace with your external WebSocket URL
        self.websocket_url = "ws://localhost:4000/graphql"
        await self.accept()

        try:
            async with websockets.connect(self.websocket_url) as ws:
                while True:
                    data = await ws.recv()
                    await self.send(data)
        except websockets.WebSocketException as e:
            print(f"WebSocket communication error: {e}")
