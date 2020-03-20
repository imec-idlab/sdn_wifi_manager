#!/usr/bin/env python3
#
# Copyright (c) 2020 Pedro Heleno Isolani
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

"""WiFi Slice Manager App."""

from empower.core.app import EmpowerApp
from empower.core.app import DEFAULT_PERIOD
from empower.datatypes.dscp import DSCP
from empower.main import RUNTIME

from empower.apps.sandbox.managers.wifislicemanager.parsers.sliceconfigrequest import *


class WiFiSliceManager(EmpowerApp):
    """WiFi Slice Manager App

    Command Line Parameters:
        tenant_id: tenant id
        every: loop period in ms (optional, default 5000ms)

    Example:
        ./empower-runtime.py apps.sandbox.managers.wifislicemanager.wifislicemanager \
            --tenant_id=52313ecb-9d00-4b7d-b873-b55d3d9ada26D
            /
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__wifi_slice_manager = {"message": "WiFi Slice Manager is online!"}
        self.__slice_stats_handler = None
        self.__active_flows_handler = None
        self.__minimum_quantum = self.minimum_quantum
        self.__default_maximum_quantum = 12000
        self.__quantum_decrease_rate = self.quantum_decrease_rate
        self.__quantum_increase_rate = self.quantum_increase_rate

    def loop(self):
        """Periodic job."""
        self.log.debug("WiFi Slice Manager APP loop...")
        if self.get_slice_stats() and self.get_active_flows():
            self.log.debug("WiFi Slice Manager is ready!")
            # Is there QoS flows active?
            for crr_wtp_addr in self.__active_flows_handler['wtps']:
                decrease_quantum = False  #
                if self.__active_flows_handler['wtps'][crr_wtp_addr]['active_flows']['QoS']:
                    for qos_flow in self.__active_flows_handler['wtps'][crr_wtp_addr]['active_flows']['QoS']:
                        if qos_flow['req_queue_delay_ms'] is not None:
                            if self.__slice_stats_handler['wtps'][crr_wtp_addr]['slices'][qos_flow['dscp']] is not None:
                                if self.__slice_stats_handler['wtps'][crr_wtp_addr]['slices'][qos_flow['dscp']]['queue_delay_ms']['median'] is not None:
                                    if qos_flow['req_queue_delay_ms'] > self.__slice_stats_handler['wtps'][crr_wtp_addr]['slices'][qos_flow['dscp']]['queue_delay_ms']['median']:
                                        decrease_quantum = True

                if self.__active_flows_handler['wtps'][crr_wtp_addr]['active_flows']['BE']:
                    for be_flow in self.__active_flows_handler['wtps'][crr_wtp_addr]['active_flows']['BE']:
                        current_quantum = self.tenant.slices[DSCP(be_flow['dscp'])].wifi['static-properties']['quantum']
                        if decrease_quantum:
                            adapted_quantum = int(current_quantum - (current_quantum * self.__quantum_decrease_rate))
                            if adapted_quantum < self.__minimum_quantum:
                                adapted_quantum = self.__minimum_quantum
                        else:
                            adapted_quantum = int(current_quantum - (current_quantum * self.__quantum_increase_rate))
                            if adapted_quantum > self.__default_maximum_quantum:
                                adapted_quantum = self.__default_maximum_quantum
                        if adapted_quantum != current_quantum:
                            self.send_slice_config_to_wtp(
                                dscp=be_flow['dscp'],
                                new_quantum=adapted_quantum)

    def send_slice_config_to_wtp(self, dscp, new_quantum):
        new_slice = format_slice_config_request(tenant_id=self.tenant_id,
                                                dscp=dscp,
                                                default_quantum=new_quantum)
        self.log.debug("Sending new slice configurations to APs")
        self.tenant.set_slice(DSCP(dscp), new_slice)

    def get_active_flows(self):
        if 'empower.apps.sandbox.managers.mcdamanager' in RUNTIME.tenants[self.tenant_id].components:
            self.__active_flows_handler = RUNTIME.tenants[self.tenant_id].components[
                'empower.apps.sandbox.managers.mcdamanager'].to_dict()
            return True
        else:
            raise ValueError("APP 'empower.apps.sandbox.managers.mcdamanager' is not online!")
            return False

    def get_slice_stats(self):
        if 'empower.apps.handlers.slicestatshandler' in RUNTIME.tenants[self.tenant_id].components:
            self.__slice_stats_handler = RUNTIME.tenants[self.tenant_id].components[
                'empower.apps.handlers.slicestatshandler'].to_dict()
            return True
        else:
            raise ValueError("APP 'empower.apps.handlers.slicestatshandler' is not online!")
            return False

    @property
    def active_flows_handler(self):
        """Return default active_flows_handler"""
        return self.__active_flows_handler

    @active_flows_handler.setter
    def active_flows_handler(self, value):
        """Set active_flows_handler"""
        self.__active_flows_handler = value

    @property
    def slice_stats_handler(self):
        """Return default slice_stats_handler"""
        return self.__slice_stats_handler

    @slice_stats_handler.setter
    def slice_stats_handler(self, value):
        """Set slice_stats_handler"""
        self.__slice_stats_handler = value

    @property
    def every(self):
        """Return loop period."""
        return self.__every

    @every.setter
    def every(self, value):
        """Set loop period."""
        self.log.info("Setting control loop interval to %ums", int(value))
        self.__every = int(value)
        super().restart(self.__every)

    @property
    def wifi_slice_manager(self):
        """Return default WiFi Slice Manager"""
        return self.__wifi_slice_manager

    @wifi_slice_manager.setter
    def wifi_slice_manager(self, value):
        """Set WiFi Slice Manager"""
        self.__wifi_slice_manager = value

    @property
    def minimum_quantum(self):
        """Return minimum quantum"""
        return self.__minimum_quantum

    @minimum_quantum.setter
    def minimum_quantum(self, value):
        """Set minimum_quantum"""
        if value is not None:
            try:
                self.__minimum_quantum = int(value)
            except TypeError:
                raise ValueError("Invalid value type for minimum_quantum, should be an integer!")
        else:
            self.__minimum_quantum = None

    @property
    def quantum_decrease_rate(self):
        """Return quantum_decrease_rate"""
        return self.__quantum_decrease_rate

    @quantum_decrease_rate.setter
    def quantum_decrease_rate(self, value):
        """Set quantum_decrease_rate"""
        if value is not None:
            try:
                self.__quantum_decrease_rate = float(value)
            except TypeError:
                raise ValueError("Invalid value type for quantum_decrease_rate, should be a float!")
        else:
            self.__quantum_decrease_rate = None

    @property
    def quantum_increase_rate(self):
        """Return quantum_increase_rate"""
        return self.__quantum_increase_rate

    @quantum_increase_rate.setter
    def quantum_increase_rate(self, value):
        """Set quantum_increase_rate"""
        if value is not None:
            try:
                self.__quantum_increase_rate = float(value)
            except TypeError:
                raise ValueError("Invalid value type for quantum_increase_rate, should be a float!")
        else:
            self.__quantum_increase_rate = None

    def to_dict(self):
        """ Return a JSON-serializable."""
        return self.__wifi_slice_manager


def launch(tenant_id, minimum_quantum, quantum_decrease_rate, quantum_increase_rate, every=DEFAULT_PERIOD):
    """ Initialize the module. """

    return WiFiSliceManager(tenant_id=tenant_id,
                            minimum_quantum=minimum_quantum,
                            quantum_decrease_rate=quantum_decrease_rate,
                            quantum_increase_rate=quantum_increase_rate,
                            every=every)