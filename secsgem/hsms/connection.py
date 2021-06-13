#####################################################################
# connection.py
#
# (c) Copyright 2013-2021, Benjamin Parzella. All rights reserved.
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
"""Contains objects and functions to create and handle hsms connection."""

import logging
import select
import struct
import time
import threading

import secsgem.common

from .packet import HsmsPacket

# TODO: timeouts (T7, T8)

HSMS_STYPES = {
    1: "Select.req",
    2: "Select.rsp",
    3: "Deselect.req",
    4: "Deselect.rsp",
    5: "Linktest.req",
    6: "Linktest.rsp",
    7: "Reject.req",
    9: "Separate.req"
}
"""Names for hsms header SType."""


class HsmsConnection:  # pragma: no cover
    """Connection class used for active and passive hsms connections."""

    select_timeout = 0.5
    """ Timeout for select calls ."""

    send_block_size = 1024 * 1024
    """ Block size for outbound data ."""

    T3 = 45.0
    """ Reply Timeout ."""

    T5 = 10.0
    """ Connect Separation Time ."""

    T6 = 5.0
    """ Control Transaction Timeout ."""

    def __init__(self, active, address, port, session_id=0, delegate=None):
        """
        Initialize a hsms connection.

        :param active: Is the connection active (*True*) or passive (*False*)
        :type active: boolean
        :param address: IP address of remote host
        :type address: string
        :param port: TCP port of remote host
        :type port: integer
        :param session_id: session / device ID to use for connection
        :type session_id: integer
        :param delegate: target for messages
        :type delegate: inherited from :class:`secsgem.hsms.handler.HsmsHandler`
        """
        self.logger = logging.getLogger(self.__module__ + "." + self.__class__.__name__)

        # set parameters
        self.active = active
        self.remoteAddress = address
        self.remotePort = port
        self.sessionID = session_id
        self.delegate = delegate

        # connection socket
        self.sock = None

        # buffer for received data
        self.receiveBuffer = b""

        # receiving thread flags
        self.threadRunning = False
        self.stopThread = False

        # connected flag
        self.connected = False

        # flag set during disconnection
        self.disconnecting = False

    def _serialize_data(self):
        """
        Return data for serialization.

        :returns: data to serialize for this object
        :rtype: dict
        """
        return {
            'active': self.active,
            'remoteAddress': self.remoteAddress,
            'remotePort': self.remotePort,
            'sessionID': self.sessionID,
            'connected': self.connected}

    def __str__(self):
        """Get the contents of this object as a string."""
        return "{} connection to {}:{} sessionID={}".format(("Active" if self.active else "Passive"),
                                                            self.remoteAddress, str(self.remotePort),
                                                            str(self.sessionID))

    def _start_receiver(self):
        """
        Start the thread for receiving and handling incoming messages.

        Will also do the initial Select and Linktest requests.

        .. warning:: Do not call this directly, will be called from HSMS client/server class.
        .. seealso:: :class:`secsgem.hsms.connections.HsmsActiveConnection`,
            :class:`secsgem.hsms.connections.HsmsPassiveConnection`,
            :class:`secsgem.hsms.connections.HsmsMultiPassiveConnection`
        """
        # mark connection as connected
        self.connected = True

        # start data receiving thread
        threading.Thread(target=self.__receiver_thread, args=(),
                         name="secsgem_hsmsConnection_receiver_{}:{}".format(self.remoteAddress,
                                                                             self.remotePort)).start()

        # wait until thread is running
        while not self.threadRunning:
            pass

        # send event
        if self.delegate and hasattr(self.delegate, 'on_connection_established') \
                and callable(getattr(self.delegate, 'on_connection_established')):
            try:
                self.delegate.on_connection_established(self)
            except Exception:  # pylint: disable=broad-except
                self.logger.exception('ignoring exception for on_connection_established handler')

    def _on_hsms_connection_close(self, data):
        pass

    def disconnect(self):
        """Close connection."""
        # return if thread isn't running
        if not self.threadRunning:
            return

        # set disconnecting flag to avoid another select
        self.disconnecting = True

        # set flag to stop the thread
        self.stopThread = True

        # wait until thread stopped
        while self.threadRunning:
            pass

        # clear disconnecting flag, no selects coming any more
        self.disconnecting = False

    def send_packet(self, packet):
        """
        Send the ASCII coded packet to the remote host.

        :param packet: encoded data to be transmitted
        :type packet: string / byte array
        """
        # encode the packet
        data = packet.encode()

        # split data into blocks
        blocks = [data[i: i + self.send_block_size] for i in range(0, len(data), self.send_block_size)]

        for block in blocks:
            retry = True

            # not sent yet, retry
            while retry:
                # wait until socket is writable
                while not select.select([], [self.sock], [], self.select_timeout)[1]:
                    pass

                try:
                    # send packet
                    self.sock.send(block)

                    # retry will be cleared if send succeeded
                    retry = False
                except OSError as exc:
                    if not secsgem.common.is_errorcode_ewouldblock(exc.errno):
                        # raise if not EWOULDBLOCK
                        return False
                    # it is EWOULDBLOCK, so retry sending

        return True

    def _process_receive_buffer(self):
        """
        Parse the receive buffer and dispatch callbacks.

        .. warning:: Do not call this directly, will be called from
        :func:`secsgem.hsmsConnections.hsmsConnection.__receiver_thread` method.
        """
        # check if enough data in input buffer
        if len(self.receiveBuffer) < 4:
            return False

        # unpack length from input buffer
        length = struct.unpack(">L", self.receiveBuffer[0:4])[0] + 4

        # check if enough data in input buffer
        if len(self.receiveBuffer) < length:
            return False

        # extract and remove packet from input buffer
        data = self.receiveBuffer[0:length]
        self.receiveBuffer = self.receiveBuffer[length:]

        # decode received packet
        response = HsmsPacket.decode(data)

        # redirect packet to hsms handler
        if self.delegate and hasattr(self.delegate, 'on_connection_packet_received') \
                and callable(getattr(self.delegate, 'on_connection_packet_received')):
            try:
                self.delegate.on_connection_packet_received(self, response)
            except Exception:  # pylint: disable=broad-except
                self.logger.exception('ignoring exception for on_connection_packet_received handler')

        # return True if more data is available
        if len(self.receiveBuffer) > 0:
            return True

        return False

    def __receiver_thread_read_data(self):
        # check if shutdown requested
        while not self.stopThread:
            # check if data available
            select_result = select.select([self.sock], [], [self.sock], self.select_timeout)

            # check if disconnection was started
            if self.disconnecting:
                time.sleep(0.2)
                continue

            if select_result[0]:
                try:
                    # get data from socket
                    recv_data = self.sock.recv(1024)

                    # check if socket was closed
                    if len(recv_data) == 0:
                        self.connected = False
                        self.stopThread = True
                        continue

                    # add received data to input buffer
                    self.receiveBuffer += recv_data
                except OSError as exc:
                    if not secsgem.common.is_errorcode_ewouldblock(exc.errno):
                        raise exc

                # handle data in input buffer
                while self._process_receive_buffer():
                    pass

    def __receiver_thread(self):
        """
        Thread for receiving incoming data and adding it to the receive buffer.

        .. warning:: Do not call this directly, will be called from
        :func:`secsgem.hsmsConnections.hsmsConnection._startReceiver` method.
        """
        self.threadRunning = True

        try:
            self.__receiver_thread_read_data()
        except Exception:  # pylint: disable=broad-except
            self.logger.exception('exception')

        # notify listeners of disconnection
        if self.delegate and hasattr(self.delegate, 'on_connection_before_closed') \
                and callable(getattr(self.delegate, 'on_connection_before_closed')):
            try:
                self.delegate.on_connection_before_closed(self)
            except Exception:  # pylint: disable=broad-except
                self.logger.exception('ignoring exception for on_connection_before_closed handler')

        # close the socket
        self.sock.close()

        # notify listeners of disconnection
        if self.delegate and hasattr(self.delegate, 'on_connection_closed') \
                and callable(getattr(self.delegate, 'on_connection_closed')):
            try:
                self.delegate.on_connection_closed(self)
            except Exception:  # pylint: disable=broad-except
                self.logger.exception('ignoring exception for on_connection_closed handler')

        # reset all flags
        self.connected = False
        self.threadRunning = False
        self.stopThread = False

        # clear receive buffer
        self.receiveBuffer = b""

        # notify inherited classes of disconnection
        self._on_hsms_connection_close({'connection': self})
