#####################################################################
# secsHandler.py
#
# (c) Copyright 2013-2015, Benjamin Parzella. All rights reserved.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#####################################################################
"""Handler for SECS commands. Used in combination with :class:`secsgem.hsmsHandler.hsmsConnectionManager`"""

import logging
import threading

import traceback
import copy

from hsmsHandler import hsmsHandler

from common import StreamFunctionCallbackHandler

import secsFunctions


class secsHandler(StreamFunctionCallbackHandler, hsmsHandler):
    """Baseclass for creating Host/Equipment models. This layer contains the SECS functionality. Inherit from this class and override required functions.

    :param address: IP address of remote host
    :type address: string
    :param port: TCP port of remote host
    :type port: integer
    :param active: Is the connection active (*True*) or passive (*False*)
    :type active: boolean
    :param sessionID: session / device ID to use for connection
    :type sessionID: integer
    :param name: Name of the underlying configuration
    :type name: string
    :param eventHandler: object for event handling
    :type eventHandler: :class:`secsgem.common.EventHandler`
    :param connectionHandler: object for connection handling (ie multi server)
    :type connectionHandler: object
    """

    ceids = {}
    """Dictionary of available collection events, CEID is the key

    :param name: Name of the data value
    :type name: string
    :param CEID: Collection event the data value is used for
    :type CEID: integer
    """

    dvs = {}
    """Dictionary of available data values, DVID is the key

    :param name: Name of the collection event
    :type name: string
    :param dv: Data values available for collection event
    :type dv: list of integers
    """

    alarms = {}
    """Dictionary of available alarms, ALID is the key

    :param alarmText: Description of the alarm
    :type alarmText: string
    :param ceidOn: Collection event for activated alarm
    :type ceidOn: integer
    :param ceidOff: Collection event for deactivated alarm
    :type ceidOff: integer
    """

    rcmds = {}
    """Dictionary of available remote commands, command is the key

    :param params: description of the parameters
    :type params: list of dictionary
    :param CEID: Collection events the remote command uses
    :type CEID: list of integers
    """

    secsStreamsFunctionsHost = copy.deepcopy(secsFunctions.secsStreamsFunctionsHost)
    secsStreamsFunctionsEquipment = copy.deepcopy(secsFunctions.secsStreamsFunctionsEquipment)

    def __init__(self, address, port, active, sessionID, name, eventHandler=None, customConnectionHandler=None):
        StreamFunctionCallbackHandler.__init__(self)
        hsmsHandler.__init__(self, address, port, active, sessionID, name, eventHandler, customConnectionHandler)
        self.isHost = True

    def _runCallbacks(self, callbackIndex, response):
        handeled = False
        try:
            for callback in self.callbacks[callbackIndex]:
                if callback(self, response) != False:
                    handeled = True

            if not handeled:
                self._queuePacket(response)

        except Exception, e:
            result = 'secsHandler.CallbackRunner : exception {0}\n'.format(e)
            result += ''.join(traceback.format_stack())
            logging.error(result)

    def _onHsmsPacketReceived(self, packet):
        """Packet received from hsms layer

        :param packet: received data packet
        :type packet: object
        """
        message = self.secsDecode(packet)

        if message is None:
            logging.info("< %s", packet)
        else:
            logging.info("< %s\n%s", packet, message)

        # check if callbacks available for this stream and function
        callbackIndex = "s"+str(packet.header.stream)+"f"+str(packet.header.function)
        if callbackIndex in self.callbacks:
            threading.Thread(target=self._runCallbacks, args=(callbackIndex, packet), name="secsgem_secsHandler_callback_{}".format(callbackIndex)).start()
        else:
            self._queuePacket(packet)

    def disableCEIDs(self):
        """Disable all Collection Events.
        """
        if not self.connection:
            return None

        return self.sendAndWaitForResponse(self.streamFunction(2, 37)({"CEED": False, "CEID": []}))

    def disableCEIDReports(self):
        """Disable all Collection Event Reports.
        """
        if not self.connection:
            return None

        return self.sendAndWaitForResponse(self.streamFunction(2, 33)({"DATAID": 0, "DATA": []}))

    def listSVs(self):
        """Get list of available Service Variables.

        :returns: available Service Variables
        :rtype: list
        """
        if not self.connection:
            return None

        packet = self.sendAndWaitForResponse(self.streamFunction(1, 11)([]))

        return self.secsDecode(packet)

    def requestSVs(self, SVs):
        """Request contents of supplied Service Variables.

        :param SVs: Service Variables to request
        :type SVs: list
        :returns: values of requested Service Variables
        :rtype: list
        """
        if not self.connection:
            return None

        packet = self.sendAndWaitForResponse(self.streamFunction(1, 3)(SVs))

        return self.secsDecode(packet)

    def requestSV(self, SV):
        """Request contents of one Service Variable.

        :param SV: id of Service Variable
        :type SV: int
        :returns: value of requested Service Variable
        :rtype: various
        """
        return self.requestSVs([SV])[0]

    def listECs(self):
        """Get list of available Equipment Constants.

        :returns: available Equipment Constants
        :rtype: list
        """
        if not self.connection:
            return None

        packet = self.sendAndWaitForResponse(self.streamFunction(2, 29)([]))

        return self.secsDecode(packet)

    def requestECs(self, ECs):
        """Request contents of supplied Equipment Constants.

        :param ECs: Equipment Constants to request
        :type ECs: list
        :returns: values of requested Equipment Constants
        :rtype: list
        """
        if not self.connection:
            return None

        packet = self.sendAndWaitForResponse(self.streamFunction(2, 13)(ECs))

        return self.secsDecode(packet)

    def requestEC(self, EC):
        """Request contents of one Equipment Constant.

        :param EC: id of Equipment Constant
        :type EC: int
        :returns: value of requested Equipment Constant
        :rtype: various
        """
        return self.requestECs([EC])

    def setECs(self, ECs):
        """Set contents of supplied Equipment Constants.

        :param ECs: list containing list of id / value pairs
        :type ECs: list
        """
        if not self.connection:
            return None

        packet = self.sendAndWaitForResponse(self.streamFunction(2, 15)(ECs))

        return self.secsDecode(packet).get()

    def setEC(self, EC, value):
        """Set contents of one Equipment Constant.

        :param EC: id of Equipment Constant
        :type EC: int
        :param value: new content of Equipment Constant
        :type value: various
        """
        return self.setECs([[EC, value]])

    def sendEquipmentTerminal(self, terminalID, text):
        """Set text to equipment terminal

        :param terminalID: ID of terminal
        :type terminalID: int
        :param value: text to send
        :type value: string
        """
        if not self.connection:
            return None

        return self.sendAndWaitForResponse(self.streamFunction(10, 3)({"TID": terminalID, "TEXT": text}))

    def getCEIDName(self, ceid):
        """Get the name of a collection event

        :param ceid: ID of collection event
        :type ceid: integer
        :returns: Name of the event or empty string if not found
        :rtype: string
        """
        if ceid in self.ceids:
            if "name" in self.ceids[ceid]:
                return self.ceids[ceid]["name"]

        return ""

    def getDVIDName(self, dvid):
        """Get the name of a data value

        :param ceid: ID of data value
        :type ceid: integer
        :returns: Name of the event or empty string if not found
        :rtype: string
        """
        if dvid in self.dvs:
            if "name" in self.dvs[dvid]:
                return self.dvs[dvid]["name"]

        return ""

    def areYouThere(self):
        """Check if remote is still replying"""
        if not self.connection:
            return None

        self.sendAndWaitForResponse(self.streamFunction(1, 1)())

    def streamFunction(self, stream, function):
        """Get class for stream and function

        :param stream: stream to get function for
        :type stream: int
        :param function: function to get
        :type function: int
        :return: matching stream and function class
        :rtype: secsSxFx class
        """
        if self.isHost:
            secsStreamsFunctions = self.secsStreamsFunctionsHost
        else:
            secsStreamsFunctions = self.secsStreamsFunctionsEquipment

        if stream not in secsStreamsFunctions:
            logging.warning("unknown function S%02dF%02d", stream, function)
            return None
        else:
            if function not in secsStreamsFunctions[stream]:
                logging.warning("unknown function S%02dF%02d", stream, function)
                return None
            else:
                return secsStreamsFunctions[stream][function]

    def secsDecode(self, packet):
        """Get object of decoded stream and function class, or None if no class is available.

        :param packet: packet to get object for
        :type packet: :class:`secsgem.hsmsPackets.hsmsPacket`
        :return: matching stream and function object
        :rtype: secsSxFx object
        """
        if self.isHost:
            secsStreamsFunctions = self.secsStreamsFunctionsEquipment
        else:
            secsStreamsFunctions = self.secsStreamsFunctionsHost

        if packet.header.stream not in secsStreamsFunctions:
            logging.warning("unknown function S%02dF%02d", packet.header.stream, packet.header.function)
            return None

        if packet.header.function not in secsStreamsFunctions[packet.header.stream]:
            logging.warning("unknown function S%02dF%02d", packet.header.stream, packet.header.function)
            return None

        logging.debug("decoding function S{}F{} using {}".format(packet.header.stream, packet.header.function, secsStreamsFunctions[packet.header.stream][packet.header.function].__name__))
        function = secsStreamsFunctions[packet.header.stream][packet.header.function]()
        function.decode(packet.data)
        logging.debug("decoded {}".format(function))
        return function
