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

from flask import *
from kaosu import ts3server
from kaosu.models.client import Client
from kaosu.database import db_session
from kaosu.models.vote_kick import VoteKick


mod = Blueprint('functions', __name__)


@mod.route("/functions", methods=["GET", "POST"])
def functions():
    ts3server.validate_connection()

    server = ts3server.get_serverinfo(ts3server)

    return render_template("server.html", server=server)

@mod.route("/functions/kick", methods=["GET", "POST"])
def get_kick():
    ts3server.validate_connection()

    if request.method == "GET":
        clients = ts3server.get_clientsinfo(ts3server)

        for client in clients:
            votes = db_session.query(VoteKick).filter(VoteKick.clid == client.clid).count()
            client.votes = votes

        return render_template("kick.html", clients=clients)
    else:
        clid = int(request.form.get("clid"))

        votes = db_session.query(VoteKick).filter(VoteKick.clid == clid).count()
        if votes == 4:
            ts3server.kick_user(ts3server, clid, "Vote kick.")
        else:
            db_session.add(VoteKick(clid))
            db_session.commit()

        return jsonify(clid=clid)