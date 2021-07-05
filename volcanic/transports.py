# Client Transports

import struct
import logging

from . import protocol as PROTOCOL # Constant

# Websockets
import asyncio
import websockets
import websockets.exceptions
import websockets.client
from websockets.client import connect as ws_connect # for autocomplete satsifacation

pingByte = struct.pack(">i",PROTOCOL.PING)
class Transport:
    async def ping(self):
        await self.send_raw(pingByte)
    def __init__(self,ping_interval = 1000):
        self.closed = False
        self.lc = None
        self.ping_interval = ping_interval
    def after_connect(self):
        asyncio.create_task(self.perodicPing(self.ping_interval))
    def on_close(self):
        if self.lc != None:
            self.lc.transport_close(self)
    def on_close_custom(self):
        pass
    def set_closed(self, newValue):
        if self.closed != newValue:
            if newValue:
                self.closed = True
                self.on_close()
                self.on_close_custom()
            else:
                self.closed = newValue
            
    async def send_internal(self, data):
        raise NotImplementedError("Implemented in subclass only")
    async def send_raw(self, byteData):
        if isinstance(byteData, str):
            byteData = bytes(byteData, PROTOCOL.ENCODING)
        await self.send_internal(byteData)
    async def perodicPing(self, interval):
        while not self.closed:
            await self.ping()
            await asyncio.sleep(interval)
    async def close(self):
        '''
        Note: this does not trigger on close handlers as this is a intentional close
        '''
        # No close. dummy
        pass

async def create_connection(address):
    # Mirror method
    print("Trying to connect to",address)
    connection = await ws_connect(address)
    print("Established connection")
    return connection

class WebsocketTransport(Transport):
    def __init__(self, address):
        super(WebsocketTransport, self).__init__()
        # Synchronous Init
        logging.info("Synchronously Starting Connection")
        print("Running create connection")
        # connectionCorountine = create_connection(connectionDesc)
        # print(":P",connectionCorountine)
        # print("waiting for corountine to finish")
        # self.ws = asyncio.run_coroutine_threadsafe(create_connection(connectionDesc), asyncio.get_event_loop()).result()
        self.address = address
    async def connect(self):
        self.ws = await ws_connect(self.address)
        self.after_connect()
    async def send_internal(self, data):
        try:
            await self.ws.ensure_open()
            await self.ws.send(data)
        except websockets.exceptions.ConnectionClosed:
            # Pretend like the message was lost
            self.set_closed(True)
            return
    async def loop(self):
        for message in self.ws:
            print(message)
    async def close(self):
        await self.ws.close()