"""
The MIT License (MIT)

Copyright (c) 2014 Sindre Knudsen Smistad

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

__author__ = 'Sindre Smistad'


import ts3
from kaosu.models.client import Client
from kaosu.models.server import Server
from kaosu.models.channel import Channel


class TSWrapper(ts3.TS3Server):
    def __init__(self, *args):
        ts3.TS3Server.__init__(self, *args)

    @staticmethod
    def get_client(ts3server, clid):
        respone = ts3server.send_command("clientinfo", keys={'clid': clid}).data[0]

        return Client(**respone)

    @staticmethod
    def get_clientsinfo(ts3server):
        clients = []
        clients_raw = ts3server.clientlist()

        for client in clients_raw:
            clients.append(TSWrapper.get_client(ts3server, clients_raw[client]["clid"]))

        return clients

    @staticmethod
    def populate_channels(channels, clients):
        for client in clients:
            for channel in channels:
                if client.cid == channel.cid:
                    channel.clients.append(client)

    @staticmethod
    def get_serverinfo(ts3server):
        respone = ts3server.send_command("serverinfo").data[0]

        return Server(**respone)

    @staticmethod
    def get_channelsinfo(ts3server):
        channels_raw = ts3server.send_command("channellist").data
        channels = [Channel(**channel) for channel in channels_raw]

        return channels
