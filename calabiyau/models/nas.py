# -*- coding: utf-8 -*-
# Copyright (c) 2018-2020 Christiaan Frans Rademan <chris@fwiw.co.za>.
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
from uuid import uuid4

from luxon import register
from luxon import SQLModel
from luxon.utils.timezone import now

from calabiyau.models.virtual import calabiyau_virtual


@register.model()
class calabiyau_nas(SQLModel):
    id = SQLModel.Uuid(default=uuid4, internal=True)
    virtual_id = SQLModel.Uuid(internal=True)
    name = SQLModel.Word(max_length=64, null=False,
                         regex=r'^[a-z0-9\._-]+$')
    nas_type = SQLModel.Word(max_length=64, upper=True, null=False,
                             regex=r'^[a-z0-9\._-]+$')
    secret = SQLModel.String(max_length=64, null=False)
    server = SQLModel.Ip4(null=False)
    description = SQLModel.Text()
    creation_time = SQLModel.DateTime(default=now, readonly=True)
    nas_virtual_ref = SQLModel.ForeignKey(virtual_id, calabiyau_virtual.id)
    nas_virtual_index = SQLModel.Index(virtual_id)
    nas_server_index = SQLModel.Index(server)
    nas_unique = SQLModel.UniqueIndex(server)
    primary_key = id
