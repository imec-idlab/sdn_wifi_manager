#!/usr/bin/env python3
#
# Copyright (c) 2016 Roberto Riggio
#               2019 Pedro Heleno Isolani
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the
# specific language governing permissions and limitations
# under the License.

"""A HelloWorld manager."""

# the manifest
MANIFEST = {
    "name": "empower.apps.helloworld.helloworld",
    "desc": "A simple helloworld manager.",
    "params": {
        "tenant_id": {
            "desc": "The tenant on which this app must be loaded.",
            "mandatory": True,
            "type": "UUID"
        },
        "every": {
            "desc": "The control loop period (in ms).",
            "mandatory": False,
            "default": 5000,
            "type": "int"
        },
        "message": {
            "desc": "Hello World through REST API.",
            "mandatory": False,
            "default": "Hello REST API",
            "type": "string"
        }
    }
}