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
from kaosu.config import *
from kaosu.tswrapper import TSWrapper
import ts3


app = Flask(__name__)
app.config.from_object('kaosu.config')

# change this.
app.secret_key = "secret"

app.jinja_env.globals['static'] = (
    lambda filename: url_for('static', filename=filename))

ts3server = TSWrapper(ts3address, ts3port)
ts3server.login(ts3admin_user, ts3admin_pass)
ts3server.use(1)

testasd = "lol"

from kaosu.views import client, index, server, functions


#Register blueprints
app.register_blueprint(client.mod)
app.register_blueprint(index.mod)
app.register_blueprint(server.mod)
app.register_blueprint(functions.mod)