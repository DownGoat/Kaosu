/*
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
 */


String.prototype.format = function () {
    var formatted = this;
    for (var i = 0; i < arguments.length; i++) {
        var regexp = new RegExp('\\{' + i + '\\}', 'gi');
        formatted = formatted.replace(regexp, arguments[i]);
    }
    return formatted;
};


$(document).ready(function () {
    $.get("/server").done(function (data) {
        var json = data;
        $("#server_name").html(json.virtualserver_name);
        $("#server_name_t").html(json.virtualserver_name);
        $("#online_clients").html(json.virtualserver_clientsonline);
        $("#max_clients").html(json.virtualserver_maxclients);
        $("#platform").html(json.virtualserver_platform);
        $("#port").html(json.virtualserver_port);
        $("#status").html(json.virtualserver_status);
        $("#uptime").html(json.virtualserver_uptime);
        $("#welcome_message").html(json.virtualserver_welcomemessage);

        var $channels_container = $("#channels");
        $.each(json.channels, function (index, value) {
            var $li = $("<li/>").html(value.channel_name).appendTo($channels_container);
            $li.attr("cid", value.cid);
            $li.addClass("channel_li");

            $(document).on("click", "li.channel_li", function(e) {
                e.stopPropagation();
                $("#info_display").html(
                    "<h3>Channel Information</h3><table><tr><td class='bold'>Name:</td><td>{0}</td></tr><tr><td class='bold'>Description:</td><td>{1}</td></tr></table>".format(value.channel_name, value.channel_description)
                );
            });

            if (value.clients.length != 0) {
                var $ul = $("<ul/>").appendTo($li);
                $ul.addClass("client_ul");
                $.each(value.clients, function (i, client) {
                    var $foo = $("<li/>").html(client.client_nickname).appendTo($ul);
                    $foo.addClass("client_li");
                    $foo.attr("clid", client.clid);

                    $(document).on("click", "li.client_li", function(e) {
                        e.stopPropagation();
                        console.log("client click.");
                        $.get("/client/" + $foo.attr("clid")).done(function (data) {
                            var cjson = data;
                            $("#info_display").html(
                                "<h3>Client Information</h3><table><tr><td class='bold'>Nickname:</td><td>{0}</td></tr><tr><td class='bold'>Description:</td><td>{1}</td></tr></table>".format(cjson.client_nickname, cjson.client_description)
                            );
                        });
                    });
                });
            }
        });
    });
});

