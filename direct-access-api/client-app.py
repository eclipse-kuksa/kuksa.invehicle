from autobahn.asyncio.websocket import WebSocketClientProtocol, \
    WebSocketClientFactory

import json
import random

try:
    import asyncio
except ImportError:
    import trollius as asyncio


class MyClientProtocol(WebSocketClientProtocol):

    def onConnect(self, response):
        print("Server connected: {0}".format(response.peer))

    async def onOpen(self):
        print("WebSocket connection open.")

        resp = json.loads('{"appid" : "", "secret" : ""}')
        resp["action"] = "create"
        #  resp["vchannel"] = "vcan83"
        resp["channel"] = "CAN0"
        resp["appid"] = "ks-app1"
        resp["secret"] = "d6d6846a-646a-4d70-ae86-91d3a4eeea79"

        dictionaryToJson = json.dumps(resp)
        self.sendMessage(dictionaryToJson.encode('utf8'))
        await asyncio.sleep(1)

    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            # print("Text message received: {0}".format(payload.decode('utf8')))
            resp = json.loads(payload.decode('utf8'))
            print(resp)

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))


if __name__ == '__main__':
    factory = WebSocketClientFactory(u"ws://127.0.0.1:9000/vss")
    factory.protocol = MyClientProtocol

    loop = asyncio.get_event_loop()
    coro = loop.create_connection(factory, '127.0.0.1', 9000)
    loop.run_until_complete(coro)
    loop.run_forever()
loop.close()