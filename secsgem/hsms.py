#####################################################################
# hsms.py
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

import socket
import struct

import thread
import threading
import traceback

import time

from common import *

import logging

hsmsSTypes = {
	1: "Select.req",
	2: "Select.rsp",
	3: "Deselect.req",
	4: "Deselect.rsp",
	5: "Linktest.req",
	6: "Linktest.rsp",
	9: "Separate.req"
}

class hsmsHeader:
	def __init__(self, system, sessionID):
		self.sessionID = sessionID
		self.requireResponse = False
		self.stream = 0x00
		self.function = 0x00
		self.pType = 0x00
		self.sType = 0x01
		self.system = system
	
	def __str__(self):
		return '{sessionID:0x%04x, stream:%02d, function:%02d, pType:0x%02x, sType:0x%02x, system:0x%08x, requireResponse:%01d}' % \
			(self.sessionID, self.stream, self.function, self.pType, self.sType, self.system, self.requireResponse)

	def __repr__(self):
		return "%s(%r)" % (self.__class__, self.__dict__)

class hsmsSelectReqHeader(hsmsHeader):
	def __init__(self, system):
		self.sessionID = 0xFFFF
		self.requireResponse = False
		self.stream = 0x00
		self.function = 0x00
		self.pType = 0x00
		self.sType = 0x01
		self.system = system

class hsmsSelectRspHeader(hsmsHeader):
	def __init__(self, system):
		self.sessionID = 0xFFFF
		self.requireResponse = False
		self.stream = 0x00
		self.function = 0x00
		self.pType = 0x00
		self.sType = 0x02
		self.system = system

class hsmsDeselectReqHeader(hsmsHeader):
	def __init__(self, system):
		self.sessionID = 0xFFFF
		self.requireResponse = False
		self.stream = 0x00
		self.function = 0x00
		self.pType = 0x00
		self.sType = 0x03
		self.system = system

class hsmsDeselectRspHeader(hsmsHeader):
	def __init__(self, system):
		self.sessionID = 0xFFFF
		self.requireResponse = False
		self.stream = 0x00
		self.function = 0x00
		self.pType = 0x00
		self.sType = 0x04
		self.system = system

class hsmsLinktestReqHeader(hsmsHeader):
	def __init__(self, system):
		self.sessionID = 0xFFFF
		self.requireResponse = False
		self.stream = 0x00
		self.function = 0x00
		self.pType = 0x00
		self.sType = 0x05
		self.system = system

class hsmsLinktestRspHeader(hsmsHeader):
	def __init__(self, system):
		self.sessionID = 0xFFFF
		self.requireResponse = False
		self.stream = 0x00
		self.function = 0x00
		self.pType = 0x00
		self.sType = 0x06
		self.system = system

class hsmsSeparateReqHeader(hsmsHeader):
	def __init__(self, system):
		self.sessionID = 0x0FFFF
		self.requireResponse = False
		self.stream = 0x00
		self.function = 0x00
		self.pType = 0x00
		self.sType = 0x09
		self.system = system

class hsmsStreamFunctionHeader(hsmsHeader):
	def __init__(self, system, stream, function, requireResponse, sessionID):
		self.sessionID = sessionID
		self.requireResponse = requireResponse
		self.stream = stream
		self.function = function
		self.pType = 0x00
		self.sType = 0x00
		self.system = system

class hsmsPacket:
	def __init__(self, header=None, data = ""):
		if header==None:
			self.header = hsmsHeader()
		else:
			self.header = header
			
		self.data = data
	
	def __str__(self):
		data = "header: " + self.header.__str__()
		return data

	def __repr__(self):
		return "%s(%r)" % (self.__class__, self.__dict__)
		
	def encode(self):
		length = 10 + len(self.data)
		dataLengthText = str(len(self.data))+"s"

		headerStream = 	self.header.stream
		if self.header.requireResponse == True:
			headerStream |= 0b10000000

		return struct.pack(">LHBBBBL"+dataLengthText, length, self.header.sessionID, headerStream, self.header.function, self.header.pType, self.header.sType, self.header.system, self.data)
		
	@staticmethod	
	def decode(text):
		dataLength = len(text) - 14
		dataLengthText = str(dataLength)+"s"

		res = struct.unpack(">LHBBBBL"+dataLengthText, text)
		
		result = hsmsPacket(hsmsHeader(res[6], res[1]))
		result.header.requireResponse = (((res[2] & 0b10000000) >> 7) == 1)
		result.header.stream = res[2] & 0b01111111
		result.header.function = res[3]
		result.header.pType = res[4]
		result.header.sType = res[5]
		result.data = res[7]
		
		return result

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
	def __init__(self, port = 5000, connectionCallback = None, sessionID = 0):
		_callbackHandler.__init__(self)

		self.port = port
		self.connectionCallback = connectionCallback
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

			connection = _hsmsConnection(sock, self.callbacks, False, sourceIP, sourcePort, self.sessionID)

			if not self.connectionCallback == None:
				self.connectionCallback(connection)

			connection.startReceiver()

			return connection

		sock.close()

#start server accepting all connections
class hsmsMultiServer(_callbackHandler):
	def __init__(self, port = 5000, connectionCallback = None, sessionID = 0):
		_callbackHandler.__init__(self)

		self.listenSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		self.sessionID = sessionID
		self.port = port

		self.threadRunning = False
		self.stopThread = False

		self.connections = []
		self.connectionsLock = threading.Lock()

		self.connectionCallback = connectionCallback

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

				connection = _hsmsConnection(sock, self.callbacks, False, sourceIP, sourcePort, self.sessionID)

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
	def __init__(self, address, port = 5000, connectionCallback = None, sessionID = 0):
		_callbackHandler.__init__(self)

		self.address = address
		self.port = port
		self.connectionCallback = connectionCallback
		self.sessionID = sessionID
		
	def connect(self):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((self.address, self.port)) 
		
		connection = _hsmsConnection(sock, self.callbacks, True, self.address, self.port, self.sessionID)

		if not self.connectionCallback == None:
			self.connectionCallback(connection)

		connection.startReceiver()

		return connection

class hsmsConnectionState:
    NOT_CONNECTED, CONNECTED, NOT_SELECTED, SELECTED = range(4)

class _hsmsConnection(_callbackHandler):
	def __init__(self, sock, callbacks, active, address, port, sessionID = 0):
		_callbackHandler.__init__(self)

		self.sock = sock
		self.callbacks = dict(callbacks)
		self.active = active
		self.remoteIP = address
		self.remotePort = port
		self.sessionID = sessionID

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
		logging.debug("> %s", packet)
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
		logging.debug("> %s\n  %s", packet, hsmsSTypes[1])

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

		logging.debug("> %s\n  %s", packet, hsmsSTypes[2])

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
		logging.debug("> %s\n  %s", packet, hsmsSTypes[5])

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
		logging.debug("> %s\n  %s", packet, hsmsSTypes[6])

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
		logging.debug("> %s\n  %s", packet, hsmsSTypes[3])

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
		logging.debug("> %s\n  %s", packet, hsmsSTypes[4])

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
		logging.debug("> %s\n  %s", packet, hsmsSTypes[9])

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
					logging.debug("< %s\n  %s", response, hsmsSTypes[response.header.sType])
				else:
					if response.data == None:
						logging.debug("< %s", response)
					else:
						logging.debug("< %s", response)
				
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
			logging.debug("> %s\n  %s", responsePacket, hsmsSTypes[6])

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

	def _postInit(self):
		pass

class hsmsConnectionManager:
	def __init__(self):
		self.pendingPeers = {}
		self.peers = {}

	def connectionCallback(self, connection):
		connectionID = "%s:%05d:%05d" % (connection.remoteIP, connection.remotePort, connection.sessionID)

		peer = self.pendingPeers[connectionID]
		del self.pendingPeers[connectionID]

		peer._setConnection(connection)

		self.peers[peer.name] = peer

	def addPeer(self, name, address, port, active, sessionID, connectionHandler = hsmsDefaultHandler):
		peer = connectionHandler(address, port, active, sessionID, name)

		connectionID = "%s:%05d:%05d" % (address, port, sessionID)
		self.pendingPeers[connectionID] = peer

		if active:
			client = hsmsClient(address, port, self.connectionCallback, sessionID)

			client.connect()

			peer._postInit()

	def stop(self):
		for peerID in self.peers:
			peer = self.peers[peerID]
			peer.connection.disconnect()


		
#	def defaultS1F13Handler(self, connection, data, header):
#		s1f14 = secsS1F14(chr(0x00), "pysecs", "prototype")
#
#		packet = hsmsPacket(hsmsStreamFunctionHeader(1,14, False, header.system), s1f14)
#
#		print "packet:", packet
#		print "s1f14:", s1f14
#
#		self.sock.send(packet.encode())

		
		
	
