# -*- coding: utf-8 -*-
import hashlib, time, json, threading, urllib

import KBEngine
from KBEDebug import *

import Utils
import Settings
import MysqlUtility

import DBConnect
from Functions import Functor
from DBConnector import DBConnector
from tornado.simple_httpclient import SimpleAsyncHTTPClient


class LoginData:
	"""
	"""
	def __init__(self, loginType, accountName, password, userDatas):
		"""
		"""
		self.loginType = loginType
		self.accountName = accountName
		self.password = password
		self.userDatas = userDatas


#登录线程数目
MAX_LOGIN_PROCESSER = 20
#连接超时时间
CONNECT_TIMEOUT = 3
#请求超时时间
REQUEST_TIMEOUT = 5
#二维码有效登录时间
QCODE_TIMEOUT = 1 * 60
class LoginProcesserManager:
	"""
	"""
	_instance = None
	
	def __init__(self):
		"""
		"""
		self.processers = {}
		self.freeProcesser = []
		self.busyProcesser = []
		self.loginQueue = []
		self.checkTimerID = 0
		
	@staticmethod
	def instance():
		if not LoginProcesserManager._instance:
			LoginProcesserManager._instance = LoginProcesserManager()
		return LoginProcesserManager._instance
		
	def start(self):
		"""
		启动线程
		"""
		for i in range(MAX_LOGIN_PROCESSER):
			self.processers[i] = LoginProcesser()
			self.freeProcesser.append(i)
		
	def onRequestAccountLogin( self, accountName, password, userDatas ):
		"""
		请求登录账号
		"""
		#0:账号密码登录  1：扫码登录
		loginType = 0
		#扫码登录的二维码信息
		qCode = ""
		#登录私钥（扫码时随机生成）
		qSecret = ""
		
		#如果有额外参数，那么有可能是扫码登录，或者是机器人登录
		if len(userDatas) > 0:
			try:
				userDatasStr = userDatas.decode("utf-8")
				if userDatasStr != "bots":
					userData = json.loads(userDatasStr)
					loginType = userData.get("LoginType", 0)
					qCode = userData.get("QCode", "")
					qSecret = userData.get("QSecret", "")
					userDatas = userData
			except:
				status = KBEngine.SERVER_ERR_USER4
				DEBUG_MSG( "accountName = '{}', userDatas = '{}', status = '{}'".format(accountName, userDatas, status) )
				KBEngine.accountLoginResponse( accountName, accountName, b"", status )
				return
		
		#如果是扫码登录
		if loginType:
			#没有二维码信息，没有随机私钥
			if not qCode or not qSecret:
				status = KBEngine.SERVER_ERR_USER4
				DEBUG_MSG( "accountName = '{}', userDatas = '{}', status = '{}'".format(accountName, userDatas, status) )
				KBEngine.accountLoginResponse( accountName, accountName, b"", status )
				return
		
		#加入队列
		data = LoginData(loginType, accountName, password, userDatas)
		self.loginQueue.append(data)
		self.stRun()
		
	def stRun(self):
		"""
		"""	
		#如果没有空闲的线程处理登录
		if not len(self.freeProcesser):
			return
			
		for index in list(self.freeProcesser):
			#没有人等待登录
			if len(self.loginQueue) <= 0:
				break
				
			#取出空闲线程
			index = self.freeProcesser.pop(0)
			self.busyProcesser.append(index)
			processer = self.processers[index]
			
			data = self.loginQueue.pop(0)
			processer.onLoginAccount(data)
		
		#加入定时器
		if len(self.busyProcesser) and not self.checkTimerID: 
			self.checkTimerID = KBEngine.addTimer( 0.1, 0.1, self.mtOnTimeToCheck )
		
	def mtOnTimeToCheck(self, timerID):
		"""
		"""
		for index in list(self.busyProcesser):
			processer = self.processers[index]
			
			#线程处理完了，加入到空闲队列中
			if not processer.isBusy():
				self.busyProcesser.remove(index)
				self.freeProcesser.append(index)
		
		#这里执行一下
		self.stRun()
		
		#没有工作的线程了，移除定时器
		if len(self.busyProcesser) <= 0:
			KBEngine.delTimer(self.checkTimerID)
			self.checkTimerID = 0
	
	
class LoginProcesser:
	"""
	"""
	def __init__(self):
		"""
		@param manager: 管理器实例
		"""
		dbConfig = DBConnect.getCsol3DBConfig()
		self.dbc = DBConnector( **dbConfig )
		
		#是否启动中
		self.thread = None
		#登录数据
		self.loginData = None
	
	def isBusy( self ):
		"""
		"""
		#没有线程运行,并且没有登录数据
		return self.thread is not None or self.loginData is not None
		
	def onLoginAccount(self, data):
		"""
		"""
		if self.isBusy():
			ERROR_MSG("Processer is Busy")
			status = KBEngine.SERVER_ERR_USER5	#系统错误
			self.onLoginResponse( self.loginData.accountName, b"", status )
			return
			
		self.loginData = data

		#创建线程
		self.thread = threading.Thread( target = self.stRun )
		self.thread.start()
			
	def stRun( self ):
		"""
		线程运行函数
		"""
		sql = "select sm_password, sm_trusteeshipTime, sm_trusteeshipPasswd, sm_lockEndTime from tbl_GameSeccion where sm_accountName = %s"
		sql = MysqlUtility.makeSafeSql(sql, (self.loginData.accountName,))

		try:
			results = self.dbc.select( sql )
		except:
			status = KBEngine.SERVER_ERR_USER5	#系统错误
			self.onLoginResponse( self.loginData.accountName, b"", status )
			return
		
		if self.loginData.loginType:	#扫码登录
			try:
				self.LoginByQcode(results)
			except Exception:
				ERROR_MSG("Account:{}, {}".format(self.loginData.accountName, Exception))
				status = KBEngine.SERVER_ERR_USER5	#系统错误
				self.onLoginResponse( self.loginData.accountName, b"", status )
				return
		else:
			try:
				self.LoginByPasswd(results)
			except Exception:
				ERROR_MSG("Account:{}, {}".format(self.loginData.accountName, Exception))
				status = KBEngine.SERVER_ERR_USER5	#系统错误
				self.onLoginResponse( self.loginData.accountName, b"", status )
				return
		
	def LoginByQcode(self, results):
		"""
		扫码登录
		"""
		accountName = self.loginData.accountName
		qCode = self.loginData.userDatas.get("QCode", "")
		qSecret = self.loginData.userDatas.get("QSecret", "")
		
		#如果是扫码登录，但二维码信息为空,这里理论上不会进来了，前面已经有过一次验证
		if not qCode or not qSecret:
			status = KBEngine.SERVER_ERR_USER4
			self.onLoginResponse( accountName, b"", status )
			return

		if len(results) <= 0:	#账号不存在或未激活
			status = KBEngine.SERVER_ERR_USER2
			self.onLoginResponse( accountName, b"", status )
			return

		#验证托管
		if self.isBeTrusteeship(results):
			status = KBEngine.SERVER_ERR_USER1
			self.onLoginResponse( accountName, b"", status )
			return

		#验证账号是否被冻结
		if not self.validateFreeze(results, accountName):
			return
		
		params = {
			"QCode"		: qCode,
		}
		
		#计算签名
		sign = Utils.SecretMD5Sign(Settings.cs_qcode_login_secret_key, ("QCode",params["QCode"]))
		params["sign"] = sign
		
		postdata = urllib.parse.urlencode(params)
		full_uri = "%s?%s" % (Settings.cs_qcode_login_addr, postdata)
		#ERROR_MSG(full_uri)
		
		# 向服务器发送数据
		client = SimpleAsyncHTTPClient()
		client.fetch(full_uri, self.accountLoginResponseHandler, True, method="POST", allow_nonstandard_methods=True, connect_timeout = CONNECT_TIMEOUT, request_timeout = REQUEST_TIMEOUT)
		
	def accountLoginResponseHandler( self, response ):
		"""
		@param response: see also: httpclient::HTTPResponse
		"""	
		accountName = self.loginData.accountName
		qCode = self.loginData.userDatas.get("QCode")
		qSecret = self.loginData.userDatas.get("QSecret")
		result = rQCode = rQSecret = rQTime = None
		
		if response.error: 
			ERROR_MSG(response.error)
			status = KBEngine.SERVER_ERR_USER5	#系统错误
			self.onLoginResponse( accountName, b"", status )
			return
			
		try:
			body = response.body.decode( "utf-8" )
			body = json.loads( body )
			
			#取出数据
			result = body.get("result", False)
			rQCode = body.get("QCode", "")
			rQSecret = body.get("QSecret", "")
			rQTime = int(body.get("QTime", "0"))
		except:
			status = KBEngine.SERVER_ERR_USER5	#系统错误
			self.onLoginResponse( accountName, b"", status )
			return
		
		if not result or not rQCode or not rQSecret or not rQTime:
			status = KBEngine.SERVER_ERR_USER6	#扫码失败
			self.onLoginResponse( accountName, b"", status )
			return
		
		#二维码、随机私钥不一致
		if qCode != rQCode or qSecret != rQSecret:
			status = KBEngine.SERVER_ERR_USER6	#扫码失败
			self.onLoginResponse( accountName, b"", status )
			return
		
		#扫码超时
		if rQTime + QCODE_TIMEOUT < int(time.time()):
			status = KBEngine.SERVER_ERR_USER7	#超时
			self.onLoginResponse( accountName, b"", status )
			return
		
		status = KBEngine.SERVER_SUCCESS
		self.onLoginResponse( accountName, b"", status )
		
	def LoginByPasswd(self, results):
		"""
		密码登录
		"""
		accountName = self.loginData.accountName
		password = self.loginData.password
		
		if len(results) <= 0:
			#如果关闭了测试标记/打开了账号激活验证
			if not Settings.test_flag or Settings.open_account_activation:
				status = KBEngine.SERVER_ERR_USER2	#账号未激活
				self.onLoginResponse( accountName, b"", status )
				return
			
			#从kbe_accountinfos中取密码来进行验证
			if not self.validateTestPassWd(accountName, password):
				return
			
			#否则的话，就让他直接创建账号好了
			status = KBEngine.SERVER_SUCCESS
			self.onLoginResponse( accountName, b"", status )
			return
		
		#验证托管
		if self.isBeTrusteeship(results):
			if not self.validateTrusteeship(results, accountName, password):
				return
		else:
			#如果关闭了测试标记/打开了账号激活验证，直接验证账号密码
			if not Settings.test_flag or Settings.open_account_activation:
				if not self.validatePassWd(results, accountName, password):
					return
			else:
				#从kbe_accountinfos中取密码来进行验证
				if not self.validateTestPassWd(accountName, password):
					return

		#验证账号是否被冻结
		if not self.validateFreeze(results, accountName):
			return
		
		status = KBEngine.SERVER_SUCCESS
		self.onLoginResponse( accountName, b"", status )
		
	def isBeTrusteeship(self, results):
		"""
		是否已经被托管
		"""
		trusteeshipTime = float(results[0][1])
		if trusteeshipTime > time.time():
			return True
			
		return False
		
	def validateTrusteeship(self, results, accountName, password):
		"""
		验证账号托管
		"""
		#托管的话，验证托管密码对不对
		trusteeshipPasswd = (results[0][2]).decode('utf-8')
		if Utils.str_make_md5(password) != trusteeshipPasswd:
			status = KBEngine.SERVER_ERR_USER1
			self.onLoginResponse( accountName, b"", status )
			return False
			
		return True
	
	def validatePassWd(self, results, accountName, password):
		"""
		验证账号密码
		"""	
		passwd = (results[0][0]).decode('utf-8')
		#密码错误
		if Utils.str_make_md5(password) != passwd:
			status = KBEngine.SERVER_ERR_NAME_PASSWORD
			self.onLoginResponse( accountName, b"", status )
			return False
		
		return True
		
	def validateFreeze(self, results, accountName):
		"""
		验证账号是否被冻结
		"""
		lockEndTime = float(results[0][3])
		if lockEndTime > time.time():
			timeArray = time.localtime(lockEndTime)
			styleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
			status = KBEngine.SERVER_ERR_USER3
			userDatas = styleTime.encode()
			self.onLoginResponse( accountName, userDatas, status )
			return False
			
		return True
			
	def validateTestPassWd( self, accountName, password ):
		"""
		验证测试密码(通过查询kbe_accountinfos表格)
		"""
		sql = "select password from kbe_accountinfos where accountName = %s;"
		sql = MysqlUtility.makeSafeSql(sql, (accountName,))
		results = self.dbc.select( sql )
		
		if len(results) <= 0:
			#账号不存在就创建新的,所以这里返回
			return True
		else:
			password = Utils.str_make_md5(password)
			if results[0][0].decode('utf-8') == password:
				return True
			
			#密码错误
			status = KBEngine.SERVER_ERR_NAME_PASSWORD
			self.onLoginResponse( accountName, b"", status )
			return False
	
	def onLoginResponse(self, accountName, userDatas, status):
		"""
		"""
		DEBUG_MSG( "accountName = '{}', userDatas = '{}', status = '{}'".format(accountName, userDatas, status) )
		KBEngine.accountLoginResponse( accountName, accountName, userDatas, status )
		
		self.loginData = None
		self.thread = None
		
g_loginProcesser = LoginProcesserManager.instance()