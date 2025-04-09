# -*- coding: utf-8 -*-
"""
处理结果
"""


#请求跨服结果
class CROSSSERVICERESULT:
	DEFAULT = "DEFAULT"
	FAIL = "FAIL"
	SUCCESS = "SUCCESS"

#请求跨服结果码
class CROSSSERVICECODE:
	"""
	"""
	CROSS_SERVICE_DEFAULT 				= -1	#默认 未知
	CROSS_SERVICE_SUCCESS 				= 0		#成功
	CROSS_SERVICE_ARGS_ERROR 			= 1		#参数错误
	CROSS_SERVICE_SIGN_ERROR			= 2		#签名错误
	CROSS_SERVICE_UNKNOW_ERROR		= 3		#系统错误
	CROSS_SERVICE_ACCOUNT_NOT_EXISTS 	= 4		#账号不存在或未激活
	CROSS_SERVICE_ROLE_NOT_EXISTS 		= 5		#角色不存在
	CROSS_SERVICE_SERVER_KEY_ERROR 	= 6		#服务器配置错误
	CROSS_SERVICE_OLD_PLAYER_INFO_ERROR 	= 7	#原服务器玩家不存在
	CROSS_SERVICE_NOT_CROSS_SERVER_PLAY = 8	#非跨服玩家，不能删除


class CheckResult:
	def __init__(self):
		self._result = CROSSSERVICERESULT.DEFAULT
		self._code = CROSSSERVICECODE.CROSS_SERVICE_DEFAULT
		
	def setCheckResult(self, result, code):
		self._result = result
		self._code = code
	
	def getResult(self):
		return self._result
		
	def getCode(self):
		return self._code
	
#数据操作结果
class DATABASEACTIONRESULT:
	FAIL = "FAIL"
	SUCCESS = "SUCCESS"

class DBActionResult:
	def __init__(self, result = DATABASEACTIONRESULT.FAIL, code = CROSSSERVICECODE.CROSS_SERVICE_DEFAULT, data = [] ):
		self._result = result
		self_code = code
		self._data = data #该数据可能不是列表类型的
		
	def setResult(self, result):
		self._result = result
	
	def setCode(self, code):
		self._code = code
	
	def setData(self, data):
		self._data = data
	
	def getResult(self):
		return self._result
		
	def getCode(self):
		return self._code
		
	def getData(self):
		return self._data
		