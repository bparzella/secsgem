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


class HsmsConnection:  # pragma: no cover # pylint: disable=too-many-instance-attributes
    """Connection class used for active and passive hsms connections."""

    select_timeout = 0.5
    """ Timeout for select calls ."""

    send_block_size = 1024 * 1024
    """ Block size for outbound data ."""

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
        :type delegate: inherited from :class:`secsgem.hsms.protocol.HsmsProtocol`
        """
        self._logger = logging.getLogger(self.__module__ + "." + self.__class__.__name__)

        # set parameters
        self._active = active
        self._remote_address = address
        self._remote_port = port
        self._session_id = session_id
        self._delegate = delegate

        # connection socket
        self._sock = None

        # buffer for received data
        self._receive_buffer = b""

        # receiving thread flags
        self._thread_running = False
        self._stop_thread = False

        # connected flag
        self._connected = False

        # flag set during disconnection
        self._disconnecting = False

        self._timeouts = secsgem.common.Timeouts()

    @property
    def timeouts(self) -> secsgem.common.Timeouts:
        """Get connection timeouts."""
        return self._timeouts

    @property
    def disconnecting(self) -> bool:
        """Connection is disconnecting."""
        return self._disconnecting

    def _serialize_data(self):
        """
        Return data for serialization.

        :returns: data to serialize for this object
        :rtype: dict
        """
        return {
            'active': self._active,
            'remoteAddress': self._remote_address,
            'remotePort': self._remote_port,
            'session_id': self._session_id,
            'connected': self._connected}

    def __str__(self):
        """Get the contents of this object as a string."""
        return f"{('Active' if self._active else 'Passive')} connection to " \
               f"{self._remote_address}:{str(self._remote_port)}" \
               f" session_id={str(self._session_id)}"

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
        self._connected = True

        # start data receiving thread
        threading.Thread(target=self.__receiver_thread, args=(),
                         name=f"secsgem_hsmsConnection_receiver_{self._remote_address}:{self._remote_port}").start()

        # wait until thread is running
        while not self._thread_running:
            pass

        # send event
        if self._delegate and hasattr(self._delegate, 'on_connection_established') \
                and callable(getattr(self._delegate, 'on_connection_established')):
            try:
                self._delegate.on_connection_established(self)
            except Exception:  # pylint: disable=broad-except
                self._logger.exception('ignoring exception for on_connection_established handler')

    def _on_hsms_connection_close(self, data):
        pass

    def disconnect(self):
        """Close connection."""
        # return if thread isn't running
        if not self._thread_running:
            return

        # set disconnecting flag to avoid another select
        self._disconnecting = True

        # set flag to stop the thread
        self._stop_thread = True

        # wait until thread stopped
        while self._thread_running:
            pass

        # clear disconnecting flag, no selects coming any more
        self._disconnecting = False

    def send_packet(self, packet) -> bool:
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
                while not select.select([], [self._sock], [], self.select_timeout)[1]:
                    pass

                try:
                    # send packet
                    self._sock.send(block)

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
        if len(self._receive_buffer) < 4:
            return False

        # unpack length from input buffer
        length = struct.unpack(">L", self._receive_buffer[0:4])[0] + 4

        # check if enough data in input buffer
        if len(self._receive_buffer) < length:
            return False

        # extract and remove packet from input buffer
        data = self._receive_buffer[0:length]
        self._receive_buffer = self._receive_buffer[length:]

        # decode received packet
        response = HsmsPacket.decode(data)

        # redirect packet to hsms handler
        if self._delegate and hasattr(self._delegate, 'on_connection_packet_received') \
                and callable(getattr(self._delegate, 'on_connection_packet_received')):
            try:
                self._delegate.on_connection_packet_received(self, response)
            except Exception:  # pylint: disable=broad-except
                self._logger.exception('ignoring exception for on_connection_packet_received handler')

        # return True if more data is available
        if len(self._receive_buffer) > 0:
            return True

        return False

    def __receiver_thread_read_data(self):
        # check if shutdown requested
        while not self._stop_thread:
            # check if data available
            select_result = select.select([self._sock], [], [self._sock], self.select_timeout)

            # check if disconnection was started
            if self._disconnecting:
                time.sleep(0.2)
                continue

            if select_result[0]:
                try:
                    # get data from socket
                    recv_data = self._sock.recv(1024)

                    # check if socket was closed
                    if len(recv_data) == 0:
                        self._connected = False
                        self._stop_thread = True
                        continue

                    # add received data to input buffer
                    self._receive_buffer += recv_data
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
        self._thread_running = True

        try:
            self.__receiver_thread_read_data()
        except Exception:  # pylint: disable=broad-except
            self._logger.exception('exception')

        # notify listeners of disconnection
        if self._delegate and hasattr(self._delegate, 'on_connection_before_closed') \
                and callable(getattr(self._delegate, 'on_connection_before_closed')):
            try:
                self._delegate.on_connection_before_closed(self)
            except Exception:  # pylint: disable=broad-except
                self._logger.exception('ignoring exception for on_connection_before_closed handler')

        # close the socket
        self._sock.close()

        # notify listeners of disconnection
        if self._delegate and hasattr(self._delegate, 'on_connection_closed') \
                and callable(getattr(self._delegate, 'on_connection_closed')):
            try:
                self._delegate.on_connection_closed(self)
            except Exception:  # pylint: disable=broad-except
                self._logger.exception('ignoring exception for on_connection_closed handler')

        # reset all flags
        self._connected = False
        self._thread_running = False
        self._stop_thread = False

        # clear receive buffer
        self._receive_buffer = b""

        # notify inherited classes of disconnection
        self._on_hsms_connection_close({'connection': self})
