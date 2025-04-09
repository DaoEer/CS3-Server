# -*- coding: utf-8 -*-

#---------------------------
# 连接baseapp模块
#---------------------------

from cs3_web_services import  settings
from common import csdefine, csstatus, tooldefine
from common import Functions
from common.DBConnectInterface import g_dbInterfaceInst
from collections import OrderedDict

import logging
import socket, json, struct, time

logger = logging.getLogger("KST")


CONNECT_TRY_COUNT = 1		#尝试连接次数
CONNECT_TRY_MAX = 3		#尝试连接最大叠加


class BaseappConnector:
	"""
	连接器
	"""
	def __init__(self, hostList, port):
		"""
		"""
		self._hostList = hostList
		self._port = port
		self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.blocking = False

	def update(self, hostList, port):
		"""
		更新socketIP和端口号
		:param hostList: IP列表
		:param port: 端口号
		:return:
		"""
		#如果settings 配置的IP或端口号有改变，则更新，并重新连接服务器
		if hostList != self._hostList or port != self._port:
			self._hostList = hostList
			self._port = port
			self.reconnect()

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
				if delay >0:
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
				return tooldefine._MSG_ERROR, csstatus.BASE_CONNECT_FAILED %( self._hostList, self._port )
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
				return ( tooldefine._MSG_ERROR, csstatus.MSG_MGR_RECV_CONNECT_BY_CLOSE_ERROR)
			#如果连接中的baseapp服务器关闭了，可能会出现[WinError 10054]的错误，所以需要在这里处理一下
			except Exception as err:
				logger.error('recv msg "%s:%s" fault, error: "%s"' % (self._hostList, self._port, err))
				self.close()
				self.blocking = False
				return ( tooldefine._MSG_ERROR, csstatus.MSG_MGR_RECV_EXCEPTION_ERROR)
			if not recvData:
				if len(sock_data) > 4:		#协议头的长度为4个字节
					size = struct.unpack("!I",sock_data[:4])[0]
					recv_size = size
					if recv_size > 524288:
						recv_size = 524288
					recvData += sock_data[4:]
				else:
					self.blocking = False
					return ( tooldefine._MSG_ERROR, csstatus.MSG_MGR_RECV_FORMAT_ERROR)
			else:
				recvData += sock_data
			total_len = len(recvData)
			
		self.blocking = False	
		try:
			msgDatas = json.loads(recvData.decode("utf-8"))
		except:
			return ( tooldefine._MSG_ERROR, csstatus.MSG_MGR_RECV_FORMAT_ERROR)
			
		if "state" in msgDatas and msgDatas["state"] == "fault":
			try:
				return (tooldefine._MSG_ERROR, msgDatas["message"])
			except:
				return (tooldefine._MSG_ERROR, csstatus.MSG_MGR_RECV_FORMAT_ERROR)
		elif "ping_state" in msgDatas and msgDatas["ping_state"] == "success":
			return (tooldefine._MSG_SUCCEED, csstatus.BASE_CONNECT_SUCCEED)
		elif "state" in msgDatas and msgDatas["state"] == "success":
			return (tooldefine._MSG_SUCCEED, csstatus.OPERATION_SUCCEED)
		
		return (tooldefine._MSG_SUCCEED, msgDatas)


class BaseappConnectionMgr:
	"""
	连接管理器
	"""
	_instance = None
	def __init__(self):
		self.configs = OrderedDict()
		self.connections = {}
	
	@staticmethod
	def instance():
		#configs = Functions.loadServerConfig()
		if not BaseappConnectionMgr._instance:
			BaseappConnectionMgr._instance = BaseappConnectionMgr()
		return BaseappConnectionMgr._instance
		
	def initConfig(self, configs):
		"""
		"""
		self.configs = configs
		self.connections = {}
		
	def getConfig(self):
		"""
		获取配置数据
		"""
		return self.configs
		
	def getCurrentConnection(self):
		"""
		获取当前的连接器
		"""
		return self._connection
		
	def getConnection(self, key):
		"""
		:param key:
		:return:
		"""
		if key in self.connections:
			return self.connections[key]
		else:
			connection = BaseappConnector(self.configs[key]["baseappHosts"], tooldefine.CS3GAME_SERVER_BASEAPP_GM_INTERFACE_PORT)
			self.connections.update({key: connection})
			return connection
			
	def onServerChange(self, key):
		"""
		修改服务器后，需要修改连接器
		"""
		connection = self.getConnection(key)
		if not g_dbInterfaceInst.onServerChange(key):
			return False
		if not connection.connect():
			return False
		return True
		
		
		

g_baseappConnector = BaseappConnectionMgr.instance()