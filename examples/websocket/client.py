import asyncio
import json
import websockets

import tkinter as tk
from tkinter import ttk

from examples.websocket.events import SumRequestEvent

class WebSocketClient:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("WebSocket Client")

        self.label_a = ttk.Label(self.root, text="Number A:")
        self.label_a.grid(row=0, column=0, padx=10, pady=10)

        self.entry_a = ttk.Entry(self.root)
        self.entry_a.grid(row=0, column=1, padx=10, pady=10)

        self.label_b = ttk.Label(self.root, text="Number B:")
        self.label_b.grid(row=1, column=0, padx=10, pady=10)

        self.entry_b = ttk.Entry(self.root)
        self.entry_b.grid(row=1, column=1, padx=10, pady=10)

        self.button = ttk.Button(self.root, text="Send", command=self.send_request)
        self.button.grid(row=2, column=0, columnspan=2, pady=20)

        self.label_result = ttk.Label(self.root, text="Result:")
        self.label_result.grid(row=3, column=0, padx=10, pady=10)

        self.result_var = tk.StringVar()
        self.result_display = ttk.Label(self.root, textvariable=self.result_var)
        self.result_display.grid(row=3, column=1, padx=10, pady=10)

    def send_request(self):
        asyncio.run(self.async_send_request())

    async def async_send_request(self):
        uri = "ws://localhost:8000/ws"
        async with websockets.connect(uri) as websocket:

            data = SumRequestEvent(a=int(self.entry_a.get()), b=int(self.entry_b.get()))
            await websocket.send(data.to_json())
            response = await websocket.recv()
            self.result_var.set(response)
            
    def run(self):
        self.root.mainloop()

client = WebSocketClient()
client.run()
