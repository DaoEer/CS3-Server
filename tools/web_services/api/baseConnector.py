# -*- coding: utf-8 -*-

#---------------------------
# 连接baseapp模块
#---------------------------


import logging
import socket, json, struct, time

logger = logging.getLogger("default")


CONNECT_TRY_COUNT = 1		#尝试连接次数
CONNECT_TRY_MAX = 3		#尝试连接最大叠加


class BaseappConnector:
	"""
	连接器
	"""
	_instance = None
	
	def __init__(self):
		"""
		"""
		self._hostList = []
		self._port = 0
		self._socket = None
		self.blocking = False
		
	def init(self, hostList, port):
		"""
		"""
		self._hostList = hostList
		self._port = port
	
	@staticmethod
	def instance():
		if not BaseappConnector._instance:
			BaseappConnector._instance = BaseappConnector()
		return BaseappConnector._instance
		
	def make_commend(self, msg):
		"""
		数据格式处理
		:param msg: 数据
		:return: 处理后的数据
		"""
		msg = json.dumps(msg)
		if isinstance(msg, str):
			msg = msg.encode("utf-8")
		return struct.pack("!H", len(msg)) + msg

	def unmake_commend(self, msg):
		"""
		:param msg:
		:return:
		"""

	def connect(self):
		"""
		连接socket
		:return:
		"""
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self._socket = sock
		success = False
		for host in self._hostList:
			conut = 0
			while conut != CONNECT_TRY_COUNT:
				conut += 1
				for i in range(CONNECT_TRY_MAX):
					try:
						sock.connect((host, self._port + i))
						success = True
					except Exception as err:
						logger.warning('connent to baseapp "%s:%s" fault, error: "%s"' % (host, self._port + i, err))
					else:
						logger.debug('connent to baseapp "%s:%s" success' % (host, self._port + i))
						return True
		if not success:
			logger.error('connent to baseapp "%s:%s" fault, maxConnect: "%s-%s"' % (self._hostList, self._port, CONNECT_TRY_COUNT, CONNECT_TRY_MAX))
			return False
		return True
		
	def reconnect(self, attempts = CONNECT_TRY_COUNT, delay = 0):
		"""
		尝试重连
		:param attempts: 重连次数
		:param delay: 每次重连相隔时间
		:return: 成功True, 失败False
		"""
		success = False
		for host in self._hostList:
			conut = 0
			while conut != attempts:
				conut += 1
				self.disconnect()
				self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				for i in range(CONNECT_TRY_MAX):
					try:
						self._socket.connect((host, self._port + i))
						success = True
					except Exception as err:
						logger.warning('reconnent to baseapp "%s:%s" fault, error: "%s"' % (host, self._port + i, err))
					else:
						logger.debug('reconnent to baseapp "%s:%s" success' % (host, self._port + i))
						return True
				if delay > 0:
					time.sleep(delay)
		if not success:
			logger.error('reconnent to baseapp "%s:%s" fault, maxConnect: "%s-%s"' % (self._hostList, self._port, CONNECT_TRY_COUNT, CONNECT_TRY_MAX))
			return False
		return True

	def close(self):
		"""
		断开连接
		:return:
		"""
		if not self._socket:
			return
		#self._host = None
		#self._port = None
		self._socket.close()

	disconnect = close

	def send_msg(self, msg):
		"""
		发送消息
		:param msg: 要发送的数据
		:return: 接收到的数据
		"""
		#socket发送数据需要bytes类型
		socketMsg = self.make_commend(msg)
		try:
			if self.blocking:
				self.reconnect()
			self._socket.send(socketMsg)
		except:
			if self.reconnect():
				self._socket.send(socketMsg)
			else:
				return False
		return self.recv_msg(msg)

	def recv_msg(self, msg):
		"""
		接受消息
		:return:
		"""
		total_len = 0
		total_data = []
		size = 524288
		sock_data = b""
		recvData = b""
		recv_size = 8192
		while total_len < size:
			self.blocking = True
			try:
				sock_data = self._socket.recv(recv_size)
			#下一次接收的时候，发现上一次没有正常结束，可能会出现ConnectionAbortedError [WinError 10053]的错误
			except ConnectionAbortedError as err:
				logger.error("recv ConnectionAbortedError Error: [%s], msg :[%s]", err, msg)
				self.blocking = False
				return False
			#如果连接中的baseapp服务器关闭了，可能会出现[WinError 10054]的错误，所以需要在这里处理一下
			except Exception as err:
				logger.error('recv msg "%s:%s" fault, error: "%s"' % (self._hostList, self._port, err))
				self.close()
				self.blocking = False
				return False
			if not recvData:
				if len(sock_data) > 4:		#协议头的长度为4个字节
					size = struct.unpack("!I",sock_data[:4])[0]
					recv_size = size
					if recv_size > 524288:
						recv_size = 524288
					recvData += sock_data[4:]
				else:
					self.blocking = False
					return False
			else:
				recvData += sock_data
			total_len = len(recvData)
			
		self.blocking = False	
		try:
			msgDatas = json.loads(recvData.decode("utf-8"))
		except:
			return False
			
		if "state" in msgDatas and msgDatas["state"] == "fault":
			try:
				logger.error("recv msg error: %s" % msgDatas["message"])
				return False
			except:
				return False
		elif "state" in msgDatas and msgDatas["state"] == "success":
			return True
		
		return False

g_baseappConnector = BaseappConnector.instance()