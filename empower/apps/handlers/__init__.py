#!/usr/bin/env python3
#
# Copyright (c) 2018 Pedro Heleno Isolani
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

"""A LVAP stats handler."""

# the manifest
MANIFEST = {
    "name": "empower.apps.handlers.lvapstatshandler",
    "desc": "A LVAP stats handler REST API.",
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
        "polling": {
            "desc": "The polling frequency period (in ms).",
            "mandatory": False,
            "default": 1000,
            "type": "int"
        }
    }
}

"""Uplink stats handler."""

# the manifest
MANIFEST = {
    "name": "empower.apps.handlers.uplinkstatshandler",
    "desc": "An Uplink Stats handler REST API.",
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
        "active": {
            "desc": "The flag used to activate/deactivate uplink statistics.",
            "mandatory": True,
            "default": True,
            "type": "bool"
        }
    }
}