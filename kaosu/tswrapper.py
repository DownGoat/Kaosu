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
import re
from kaosu.models.client import Client
from kaosu.models.server import Server
from kaosu.models.channel import Channel


img_regex = "\[IMG\](.*?)\[\/IMG\]"


class TSWrapper(ts3.TS3Server):
    def __init__(self, *args):
        ts3.TS3Server.__init__(self, *args)

    @staticmethod
    def get_client(ts3server, clid):
        response = ts3server.send_command("clientinfo", keys={'clid': clid}).data[0]
        response["clid"] = clid
        return Client(**response)

    @staticmethod
    def get_clientsinfo(ts3server):
        clients = []
        clients_raw = ts3server.clientlist()

        for client in clients_raw:

            # Exclude serveradmin from the list.
            if clients_raw[client]["client_database_id"] == "1":
                continue

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
        response = ts3server.send_command("serverinfo").data[0]

        return Server(**response)

    @staticmethod
    def get_channel(ts3server, cid):
        response = ts3server.send_command("channelinfo", keys={'cid': cid}).data[0]
        channel = Channel(**response)
        channel.cid = cid

        return channel

    @staticmethod
    def get_channelsinfo(ts3server):
        channels = []
        channels_raw = ts3server.send_command("channellist").data

        for channel in channels_raw:
            tmp = TSWrapper.get_channel(ts3server, channel["cid"])
            if tmp.channel_description == None:
                tmp.channel_description = ""

            # If description, turn img tag to real html.
            else:
                match = re.search(img_regex, tmp.channel_description)
                if match:
                    tmp.channel_description = tmp.channel_description.replace(
                        match.group(0),
                        "<img src='%s' />" % match.group(1)
                    )

            channels.append(tmp)

        return channels

    @staticmethod
    def kick_user(ts3server, clid):
       ts3server.send_command('clientkick', keys={'clid': clid, 'reasonid': 5})
