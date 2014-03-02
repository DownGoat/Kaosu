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

import logging
from datetime import date


version = "0.01"


ts3admin_user = "serveradmin"
ts3admin_pass = "password"


config = {
    # DB config
    "db_user": "root",
    "db_pass": "",
    "db_host": "127.0.0.1",
    "db_name": "perceive",
    "db_type": "postgresql",
    "db_port": "3306",

    "version": version,

    "log_app": "perceive",
    "log_file": "preceive_{0}.log".format(date.today().isoformat()),
    "log_level": logging.DEBUG,
    #"log_level":    logging.INFO,
}

config["db_connector"] = "{0}://{1}:{2}@{3}:{4}/{5}".format(
    config.get("db_type"),
    config.get("db_user"),
    config.get("db_pass"),
    config.get("db_host"),
    config.get("db_port"),
    config.get("db_name")
)
