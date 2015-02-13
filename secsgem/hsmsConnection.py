#####################################################################
# hsmsConnection.py
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

import logging

import socket
import struct

import thread
import threading
import traceback

import time

from hsmsPackets import *

from common import *

hsmsSTypes = {
	1: "Select.req",
	2: "Select.rsp",
	3: "Deselect.req",
	4: "Deselect.rsp",
	5: "Linktest.req",
	6: "Linktest.rsp",
	9: "Separate.req"
}

class _callbackHandler:
	def __init__(self):
		self.callbacks = {}

	def registerCallback(self, stream, function, callback):
		name = "s"+str(stream)+"f"+str(function)

		if not name in self.callbacks:
			self.callbacks[name] = []

		self.callbacks[name].append(callback)

	def unregisterCallback(self, stream, function, callback):
		name = "s"+str(stream)+"f"+str(function)

		if callback in self.callbacks[name]:
			self.callbacks[name].remove(callback)

#wait for one single client connection and terminate
class hsmsSingleServer(_callbackHandler):
	def __init__(self, port = 5000, sessionID = 0, connectionCallback = None, disconnectionCallback = None):
		_callbackHandler.__init__(self)

		self.port = port
		self.connectionCallback = connectionCallback
		self.disconnectionCallback = disconnectionCallback
		self.sessionID = sessionID

	def waitForConnection(self):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.bind(('', self.port))
		sock.listen(1)

		while True:
			accept_result = sock.accept()
			if accept_result == None:
				continue

			(sock,(sourceIP, sourcePort)) = accept_result

			connection = _hsmsConnection(sock, self.callbacks, False, sourceIP, sourcePort, self.sessionID, disconnectionCallback = self.disconnectionCallback)

			if not self.connectionCallback == None:
				self.connectionCallback(connection)

			connection.startReceiver()

			return connection

		sock.close()

#start server accepting all connections
class hsmsMultiServer(_callbackHandler):
	def __init__(self, port = 5000, sessionID = 0, connectionCallback = None, disconnectionCallback = None):
		_callbackHandler.__init__(self)

		self.listenSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		self.sessionID = sessionID
		self.port = port

		self.threadRunning = False
		self.stopThread = False

		self.connections = []
		self.connectionsLock = threading.Lock()

		self.connectionCallback = connectionCallback
		self.disconnectionCallback = disconnectionCallback

		self.listenThreadIdentifier = None

	def start(self):
		self.listenSock.bind(('', self.port))
		self.listenSock.listen(1)

		self.listenThreadIdentifier = threading.Thread(target=self._listen_thread, args=())
		self.listenThreadIdentifier.start()

	def stop(self):
		self.stopThread = True

		#this is evil madness
		socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("localhost", self.port))

		self.listenSock.close()

		if self.listenThreadIdentifier.isAlive:
			while self.threadRunning:
				pass

		self.connectionsLock.acquire()

		for connection in self.connections:
			connection.disconnect()

		self.connectionsLock.release()

	def _listen_thread(self):
		self.threadRunning = True
		try:
			while not self.stopThread:
				accept_result = self.listenSock.accept()
				if accept_result == None:
					continue

				if self.stopThread:
					continue

				self.connectionsLock.acquire()
				(sock,(sourceIP, sourcePort)) = accept_result

				connection = _hsmsConnection(sock, self.callbacks, False, sourceIP, sourcePort, self.sessionID, disconnectionCallback = self.disconnectionCallback)

				self.connections.append(connection)
				self.connectionsLock.release()

				if not self.connectionCallback == None:
					self.connectionCallback(connection)

				connection.startReceiver()

		except Exception, e:
			print "hsmsServer._listen_thread : exception", e
			traceback.print_exc()

		self.threadRunning = False

#single client connection
class hsmsClient(_callbackHandler):
	def __init__(self, address, port = 5000, sessionID = 0, connectionCallback = None, disconnectionCallback = None):
		_callbackHandler.__init__(self)

		self.address = address
		self.port = port
		self.connectionCallback = connectionCallback
		self.disconnectionCallback = disconnectionCallback
		self.sessionID = sessionID
		
	def connect(self):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		logging.debug("hsmsClient.connect: connecting to %s:%d", self.address, self.port)

		try:
			sock.connect((self.address, self.port)) 
		except socket.error, v:
			logging.debug("hsmsClient.connect: connecting to %s:%d failed", self.address, self.port)
			return None

		connection = _hsmsConnection(sock, self.callbacks, True, self.address, self.port, self.sessionID, disconnectionCallback = self.disconnectionCallback)

		if not self.connectionCallback == None:
			self.connectionCallback(connection)

		connection.startReceiver()

		return connection

class hsmsConnectionState:
    NOT_CONNECTED, CONNECTED, NOT_SELECTED, SELECTED = range(4)

class _hsmsConnection(_callbackHandler):
	def __init__(self, sock, callbacks, active, address, port, sessionID = 0, disconnectionCallback = None):
		_callbackHandler.__init__(self)

		self.sock = sock
		self.callbacks = dict(callbacks)
		self.active = active
		self.remoteIP = address
		self.remotePort = port
		self.sessionID = sessionID
		self.disconnectionCallback = disconnectionCallback

		self.systemCounter = 1

		self.threadRunning = False
		self.stopThread = False
		
		self.eventQueue = []
		self.packetQueue = []

		self.connected = True

		self.connectionState = hsmsConnectionState.NOT_SELECTED


	def startReceiver(self):
		thread.start_new_thread(self._receiver_thread, ())

		while not self.threadRunning:
			pass
		
		if self.active:			
			self.sendSelectReq()
			self.waitforSelectRsp()
			self.sendLinktestReq()
			self.waitforLinktestRsp()
		else:
			system = self.waitforSelectReq()
			self.sendSelectRsp(system)
			self.sendLinktestReq()
			self.waitforLinktestRsp()

	def disconnect(self, separate = False):
		if separate:
			self.sendSeparateReq()
		else:
			self.sendDeselectReq()
			self.waitforDeselectRsp()

		time.sleep(0.5)

		self.stopThread = True
		self.sock.shutdown(socket.SHUT_RDWR)
		self.sock.close()
		self.connected = False

		self.connectionState = hsmsConnectionState.NOT_CONNECTED
		
		while self.threadRunning:
			pass

	def sendPacket(self, packet):
		logging.info("> %s", packet)
		self.sock.send(packet.encode())
				
	def waitforStreamFunction(self, stream, function):
		event = threading.Event()
		self.eventQueue.append(event)

		foundPacket = None
		
		while foundPacket == None:
			for packet in self.packetQueue:
				if (packet.header.stream == stream) and (packet.header.function == function):
					self.packetQueue.remove(packet)
					foundPacket = packet
					break

			if foundPacket == None:
				if event.wait(1) == True:
					event.clear()
					
		self.eventQueue.remove(event)
		
		return packet

	def sendSelectReq(self):
		packet = hsmsPacket(hsmsSelectReqHeader(self.getNextSystemCounter()))
		logging.info("> %s\n  %s", packet, hsmsSTypes[1])

		self.sock.send(packet.encode())

	def waitforSelectReq(self):
		result = None

		event = threading.Event()
		self.eventQueue.append(event)

		eventReceived = False
		
		while not eventReceived:
			if event.wait(1) == True:
				event.clear()
				for packet in self.packetQueue:
					if (packet.header.sessionID == 0xFFFF) and (packet.header.stream == 0x00) and (packet.header.sType == 0x01):
						self.packetQueue.remove(packet)
						eventReceived = True
						result = packet.header.system
						break
		
		self.eventQueue.remove(event)

		return result

	def sendSelectRsp(self, system = None):
		packet = hsmsPacket(hsmsSelectRspHeader(system))

		logging.info("> %s\n  %s", packet, hsmsSTypes[2])

		self.sock.send(packet.encode())

	def waitforSelectRsp(self):
		event = threading.Event()
		self.eventQueue.append(event)

		eventReceived = False
		result = -1

		while not eventReceived:
			if event.wait(1) == True:
				event.clear()
				for packet in self.packetQueue:
					if (packet.header.sessionID == 0xFFFF) and (packet.header.stream == 0x00) and (packet.header.sType == 0x02):
						self.packetQueue.remove(packet)
						eventReceived = True
						result = packet.header.function
						break
		
		self.eventQueue.remove(event)

		self.connectionState = hsmsConnectionState.SELECTED

		return result

	def sendLinktestReq(self):
		packet = hsmsPacket(hsmsLinktestReqHeader(self.getNextSystemCounter()))
		logging.info("> %s\n  %s", packet, hsmsSTypes[5])

		self.sock.send(packet.encode())

	def waitforLinktestReq(self):
		event = threading.Event()
		self.eventQueue.append(event)

		eventReceived = False
		
		while not eventReceived:
			if event.wait(1) == True:
				event.clear()
				for packet in self.packetQueue:
					if (packet.header.sessionID == 0xFFFF) and (packet.header.stream == 0x00) and (packet.header.sType == 0x05):
						self.packetQueue.remove(packet)
						eventReceived = True
						break
		
		self.eventQueue.remove(event)

	def sendLinktestRsp(self, system):
		packet = hsmsPacket(hsmsLinktestReqHeader(system))
		logging.info("> %s\n  %s", packet, hsmsSTypes[6])

		self.sock.send(packet.encode())

	def waitforLinktestRsp(self):
		event = threading.Event()
		self.eventQueue.append(event)

		eventReceived = False
		
		while not eventReceived:
			if event.wait(1) == True:
				event.clear()
				for packet in self.packetQueue:
					if (packet.header.sessionID == 0xFFFF) and (packet.header.stream == 0x00) and (packet.header.sType == 0x06):
						self.packetQueue.remove(packet)
						eventReceived = True
						break
		
		self.eventQueue.remove(event)

	def sendDeselectReq(self):
		packet = hsmsPacket(hsmsDeselectReqHeader(self.getNextSystemCounter()))
		logging.info("> %s\n  %s", packet, hsmsSTypes[3])

		self.sock.send(packet.encode())

	def waitforDeselectReq(self):
		event = threading.Event()
		self.eventQueue.append(event)

		eventReceived = False
		
		while not eventReceived:
			if event.wait(1) == True:
				event.clear()
				for packet in self.packetQueue:
					if (packet.header.sessionID == 0xFFFF) and (packet.header.stream == 0x00) and (packet.header.sType == 0x03):
						self.packetQueue.remove(packet)
						eventReceived = True
						break

		self.eventQueue.remove(event)

	def sendDeselectRsp(self, system):
		packet = hsmsPacket(hsmsDeselectRspHeader(system))
		logging.info("> %s\n  %s", packet, hsmsSTypes[4])

		self.sock.send(packet.encode())

	def waitforDeselectRsp(self):
		event = threading.Event()
		self.eventQueue.append(event)

		eventReceived = False
		result = -1
		
		while not eventReceived:
			if event.wait(1) == True:
				event.clear()
				for packet in self.packetQueue:
					if (packet.header.sessionID == 0xFFFF) and (packet.header.stream == 0x00) and (packet.header.sType == 0x04):
						self.packetQueue.remove(packet)
						eventReceived = True
						result = packet.header.function
						break
		
		self.eventQueue.remove(event)

		self.connectionState = hsmsConnectionState.NOT_SELECTED

		return result

	def sendSeparateReq(self):
		packet = hsmsPacket(hsmsSeparateReqHeader(self.getNextSystemCounter()))
		logging.info("> %s\n  %s", packet, hsmsSTypes[9])

		self.sock.send(packet.encode())

		self.connectionState = hsmsConnectionState.NOT_SELECTED

	def _receiver_thread(self):
		self.threadRunning = True
		try:
			while not self.stopThread:
				data = self.sock.recv(4) 
				if len(data) == 0:
					self.connected = False
					self.stopThread = True
					continue

				length = struct.unpack(">L", data)[0]

				while len(data) < length + 4:
					data += self.sock.recv(length) 
					if len(data) == 4:
						self.connected = False
						self.stopThread = True
						continue
					
				response = hsmsPacket.decode(data)
				if response.header.sessionID == 0xffff:
					logging.info("< %s\n  %s", response, hsmsSTypes[response.header.sType])
				else:
					if response.data == None:
						logging.info("< %s", response)
					else:
						logging.info("< %s", response)
				
				data = ""

				unhandeled = True
				
				callbackIndex = "s"+str(response.header.stream)+"f"+str(response.header.function)
				if callbackIndex in self.callbacks:
					unhandeled = False
					for callback in self.callbacks[callbackIndex]:
						thread.start_new_thread(callback, (self, response))
				else:
					self.packetQueue.append(response)
					for event in self.eventQueue:
						event.set()
		except Exception, e:
			print "hsmsClient.ReceiverThread : exception", e
			print traceback.format_exc()

		if not self.disconnectionCallback == None:
			self.disconnectionCallback(self)

		self.threadRunning = False

	def getNextSystemCounter(self):
		self.systemCounter += 1
		return self.systemCounter

	def defaultS0F0Handler(self, connection, packet):
		if packet.header.sessionID != 0xffff:
			logging.error("S00F00: invalid sessionID")
			return
		
		if packet.header.sType == 0x05:
			responsePacket = hsmsPacket(hsmsLinktestRspHeader(packet.header.system))
			logging.info("> %s\n  %s", responsePacket, hsmsSTypes[6])

			self.sock.send(responsePacket.encode())
		else:
			logging.error("S00F00: unexpected sType (%s)", packet.header)

class hsmsDefaultHandler:
	def __init__(self, address, port, active, sessionID, name):
		self.address = address
		self.port = port
		self.active = active
		self.sessionID = sessionID
		self.name = name
		self.connection = None

	def _setConnection(self, connection):
		self.connection = connection

	def _clearConnection(self):
		self.connection = None

	def _postInit(self):
		pass

class hsmsConnectionManager:
	def __init__(self):
		self.unconnectedPeers = {}
		self.peers = {}

		self.stopping = False

		self.reconnectTimeout = 10.0

	def __getitem__(self, index):
		for peer in self.peers:
			if peer.name == index:
				return peer

		return None

	def getConnectionID(self, address, port, sessionID):
		return "%s:%05d:%05d" % (address, port, sessionID)

	def startActiveConnect(self, peer):
		if not self.stopping:
			threading.Thread(target=self._activeConnectThread, args=(peer,)).start()

	def _activeConnectThread(self, peer):
		client = hsmsClient(peer.address, peer.port, sessionID = peer.sessionID, connectionCallback = self.connectionCallback, disconnectionCallback = self.disconnectionCallback)

		if client.connect() == None:
			time.sleep(self.reconnectTimeout)
			self.startActiveConnect(peer)
		else:
			peer._postInit()

	def connectionCallback(self, connection):
		connectionID = self.getConnectionID(connection.remoteIP, connection.remotePort, connection.sessionID)

		peer = self.unconnectedPeers[connectionID]
		del self.unconnectedPeers[connectionID]

		peer._setConnection(connection)

		self.peers[connectionID] = peer

	def disconnectionCallback(self, connection):
		connectionID = self.getConnectionID(connection.remoteIP, connection.remotePort, connection.sessionID)

		peer = self.peers[connectionID]
		del self.peers[connectionID]

		peer._clearConnection()

		self.unconnectedPeers[connectionID] = peer

		if peer.active:
			self.startActiveConnect(peer)

	def addPeer(self, name, address, port, active, sessionID, connectionHandler = hsmsDefaultHandler):
		logging.debug("hsmsConnectionManager.addPeer: connecting to %s at %s:%d", name, address, port)

		peer = connectionHandler(address, port, active, sessionID, name)

		connectionID = self.getConnectionID(address, port, sessionID)
		self.unconnectedPeers[connectionID] = peer

		if peer.active:
			self.startActiveConnect(peer)

	def removePeer(self, name, address, port, sessionID):
		connectionID = self.getConnectionID(address, port, sessionID)

		if connectionID in self.peers:
			peer = self.peers[connectionID]
			del self.peers[connectionID]

			peer.connection.disconnect()

		if connectionID in self.unconnectedPeers:
			peer = self.unconnectedPeers[connectionID]
			del self.unconnectedPeers[connectionID]

	def stop(self):
		self.stopping = True

		for peerID in self.peers.keys():
			peer = self.peers[peerID]
			peer.connection.disconnect()
