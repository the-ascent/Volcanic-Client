import asyncio
from nanoid import generate
from . import protocol as PROTOCOL
from .transports import *

class LogicalConnection:
    # Client Connection
    def __init__(self):
        self.transports = []
        self.seqNumberClient = 0
        self.seqNumberServer = 0
    def add_transport(self, transport):
        self.transports.append(transport)
    def remove_transport(self, transport):
        self.transports.remove(transport)
    def transport_close(self, transport):
        pass
    async def launchTransportsAsync(self):
        for transport in self.transports:
            # Slow Connection Establish
            await transport.connect()
        for transport in self.transports:
            asyncio.run_coroutine_threadsafe(transport.loop(),asyncio.get_event_loop())
    
class AutoManagedConnection(LogicalConnection):
    def __init__(self):
        super(AutoManagedConnection, self).__init__()
        self.add_transport(WebsocketTransport("ws://localhost:3001"))

    def transport_close(self, transport):
        # Recreate connection
        print(type(transport),"closed")