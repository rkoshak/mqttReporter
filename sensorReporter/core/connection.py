# Copyright 2020 Richard Koshak
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Contains the parent Connection class.

Classes: Connections
"""
from abc import ABC, abstractmethod
import logging
from core.utils import set_log_level

class Connection(ABC):
    """Parent class that all connections must implement. It provides a default
    implementation for all methods except publish which must be overridden.
    """

    def __init__(self, msg_processor, conn_cfg):
        """Stores the passed in arguments as data members.

        Arguments:
        - msg_processor: Connections will subscribe to a destination for
        communication to the program overall, not an individual actuator or
        sensor. This is the method that gets called when a message is received.
        - conn_cfg: set of properties from the loaded yaml file.
        """
        self.log = logging.getLogger(type(self).__name__)
        self.msg_processor = msg_processor
        self.conn_cfg = conn_cfg
        self.registered = {}
        set_log_level(conn_cfg, self.log)

    @abstractmethod
    def publish(self, message, comm_conn, output_name=None):
        """Abstract method that must be overriden. When called, send the passed
        in message to the passed in comm(unication)_conn(ection) related dictionary.
        An output_name can be specified optional to set a output channel to publish to.

        Arguments:
        - message:     the message to process / publish
        - comm_conn:   dictionary containing only the parameters for the called connection,
                       e. g. information where to publish
        - output_name: optional, the output channel to publish the message to,
                       defines the subdirectory in comm_conn to look for the return topic.
                       When defined the output_name must be present
                       in the sensor YAML configuration:
                       Connections:
                           <connection_name>:
                                <output_name>:
        """

    def publish_device_properties(self):
        """Method is intended for connections with auto discover of sensors
        and actuators. Such a connection can place the necessary code for auto
        discover inside this method. It is called after all connections, sensors
        and actuators are created and running.

        Since not all connections support autodiscover the default implementation is empty.
        """

    def disconnect(self):
        """Disconnect from the connection and release any resources."""

    def register(self, comm_conn, handler):
        """Set up the passed in handler to be called for any message on the
        destination. Default implementation assumes topic 'CommandSrc'

        Arguments:
            - comm_conn: the dictionary containing the connection related parameters
            - handler: handles the incomming commands, if None the registration
                      of a sensor is assumed
        """
        if handler:
            self.log.info("Registering destination %s", comm_conn['CommandSrc'])
            self.registered[comm_conn['CommandSrc']] = handler
