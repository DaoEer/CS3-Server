#-*-coding:utf-8-*-

from urllib import request
from urllib.parse import quote
import string

import KST
import KBEDebug
import csdefine
import Functions
import Settings
from CoreObject.MgrPersistentObject import MgrPersistentObject


REQUEST_CROSS_SERVICE_URL = "RequestCrossService"
REQUEST_RETURN_SERVER_URL = "RequestReturnServer"
RETURN_SERVER_FINISHED_URL = "ReturnServerFinished"

class CrossServiceManager(MgrPersistentObject):
	def __init__(self):
		MgrPersistentObject.__init__(self)
		self._serverUrl = Settings.cross_service_addr
		self.onCompleteInit()
		
	def requestCrossService(self, prevServerkey, followedServerkey, accountName, roleName):
		"""
		define method
		请求跨服
		"""
		try:
			url = r"%s/%s/?PrevServerkey=%s&FollowedServerkey=%s&Account=%s&Role=%s" % (self._serverUrl, REQUEST_CROSS_SERVICE_URL, 
				prevServerkey, followedServerkey, accountName, roleName)
			url =quote(url, safe = string.printable)
			result = request.urlopen(url)
			resultData = result.read()
			print("-------------requestCrossService------------", resultData)
			KST.g_baseAppEntity.requestCrossServiceResult(roleName, Functions.toJsonString(eval(resultData)))
		except Exception as e:
			KBEDebug.ERROR_MSG("requestCrossService error: %s" % e)
			KST.g_baseAppEntity.requestCrossServiceResult(roleName, Functions.toJsonString({'result_code': csdefine.CROSS_SERVICE_UNKNOW_ERROR, 'result': 'FAIL'}))#3：系统错误
		
	def requestReturnServer(self, prevServerkey, followedServerkey, accountName, roleName):
		"""
		define method
		请求返回原服务器
		"""
		try:
			url = r"%s/%s/?PrevServerkey=%s&FollowedServerkey=%s&Account=%s&Role=%s" % (self._serverUrl, REQUEST_RETURN_SERVER_URL, 
				prevServerkey, followedServerkey, accountName, roleName)
			url =quote(url, safe = string.printable)
			result = request.urlopen(url)
			resultData = result.read()
			print("-------------requestReturnServer------------", resultData)
			KST.g_baseAppEntity.requestReturnServerResult(roleName, Functions.toJsonString(eval(resultData)))
		except Exception as e:
			KBEDebug.ERROR_MSG("requestReturnServer error: %s" % e)
			KST.g_baseAppEntity.requestReturnServerResult(roleName, Functions.toJsonString({'result_code': csdefine.CROSS_SERVICE_UNKNOW_ERROR, 'result': 'FAIL'}))#3：系统错误
	
	def onReturnServerFinished(self, prevServerkey, followedServerkey, accountName, roleName):
		"""
		define method
		返回原服务器完成
		"""
		#返回原服务器后再删除目标服务器的数据，不然会出现玩家还在游戏中数据却被删除了的情况
		try:
			url = r"%s/%s/?PrevServerkey=%s&FollowedServerkey=%s&Account=%s&Role=%s" % (self._serverUrl, RETURN_SERVER_FINISHED_URL, 
				prevServerkey, followedServerkey, accountName, roleName)
			url =quote(url, safe = string.printable)
			result = request.urlopen(url)
			#resultData = result.read()
		except Exception as e:
			KBEDebug.ERROR_MSG("onReturnServerFinished error: %s" % e)
			return
		