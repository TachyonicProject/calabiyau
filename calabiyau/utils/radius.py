# -*- coding: utf-8 -*-
# Copyright (c) 2018-2019 Christiaan Frans Rademan.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holders nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
# THE POSSIBILITY OF SUCH DAMAGE.
import socket

from luxon import g
from luxon.utils.encoding import if_unicode_to_bytes

from calabiyau import constants as const
from calabiyau.exceptions import TimeoutError
from calabiyau.core.handlers.radius.client import Client


def pod(nas, secret, username, session):
    secret = if_unicode_to_bytes(secret)
    srv = Client(server=nas, secret=secret, debug=g.app.debug)
    req = srv.pod(code=const.RAD_DISCONNECTREQUEST)
    req['Acct-Session-Id'] = session
    req['User-Name'] = username
    req['NAS-IP-Address'] = nas
    try:
        reply = srv.send_packet(req)
    except TimeoutError:
        reply = None
    except socket.error:
        reply = None

    if reply and reply.code == const.RAD_DISCONNECTACK:
        return True
    else:
        return False


def coa(nas, secret, username, session, attributes):
    secret = if_unicode_to_bytes(secret)
    srv = Client(server=nas, secret=secret, debug=g.app.debug)
    req = srv.coa(code=const.RAD_COAREQUEST)
    req['Acct-Session-Id'] = session
    req['User-Name'] = username
    req['NAS-IP-Address'] = nas
    for attr in attributes:
        req[attr] = attributes[attr]

    try:
        reply = srv.send_packet(req)
    except TimeoutError:
        reply = None
    except socket.error:
        reply = None

    if reply and reply.code == const.RAD_COAACK:
        return True
    else:
        return False
