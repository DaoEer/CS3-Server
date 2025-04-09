# -*- coding: utf-8 -*-

from django.http import HttpResponse


from CrossService.Common import Define
from CrossService.Common.Results import CROSSSERVICERESULT, CROSSSERVICECODE, CheckResult, DATABASEACTIONRESULT
from CrossService.Common import Utils
from CrossService.Scripts.CrossServiceData import g_CSDataInst
from cs3_web_services import settings


class CrossServiceManager:
	_instance = None
	def __init__(self):
		self._serverInfos = {}
		self.initData()
		
	def initData(self):
		self._serverInfos = Utils.loadJsonDataByFile(Define.SERVER_CONFIG_PATH)
		
	def updateServerInfos(self):
		self._serverInfos = {}
		self._serverInfos = Utils.loadJsonDataByFile(Define.SERVER_CONFIG_PATH)
		
	@staticmethod
	def instance():
		"""
		"""
		if CrossServiceManager._instance == None:
			CrossServiceManager._instance = CrossServiceManager()
		return CrossServiceManager._instance
		
	"""
	def updateServerRecord(self, serverkey):
		dbInfo = {
			'ENGINE' : 'mysql.connector.django',
			'NAME' : self._serverInfos[serverkey]["dbInfo"]["database"],
			'USER' : self._serverInfos[serverkey]["dbInfo"]["user"],
			'PASSWORD' : self._serverInfos[serverkey]["dbInfo"]["password"],
			'HOST' : self._serverInfos[serverkey]["dbInfo"]["host"],
			'PORT' : self._serverInfos[serverkey]["dbInfo"]["port"],
			'OPTIONS'  : {
				'autocommit': True,
			}
		}
		settings.DATABASES.update({serverkey: dbInfo})
	"""
		
	def checkServerkey(self, serverkey):
		if serverkey not in self._serverInfos:
			return False
			
		#self.updateServerRecord(serverkey)
		
		return True
		
	def checkAccount(self, serverkey, accountName):
		result = g_CSDataInst.queryAccount(serverkey, accountName)
		if result.getResult() == DATABASEACTIONRESULT.FAIL or len(result.getData()) == 0:
			return False
		return True
		
	def checkRole(self, serverkey, accountName, roleName):
		result = g_CSDataInst.queryRole(serverkey, accountName, roleName)
		if result.getResult() == DATABASEACTIONRESULT.FAIL or len(result.getData()) == 0:
			return False
		return True
		
	def check(self, request, checkKeyTypes):
		"""
		检查
		"""
		checkResult = CheckResult()
		checkResult.setCheckResult(CROSSSERVICERESULT.SUCCESS, CROSSSERVICECODE.CROSS_SERVICE_SUCCESS)
		datas = request.GET
		accountName = datas.get("AccountName", None)
		roleName = datas.get("RoleName", None)
		prevServerkey = datas.get("PrevServerkey", None)
		followedServerkey = datas.get("FollowedServerkey", None)
		sign = datas.get("Sign", "")
		#检查参数
		if not accountName or not roleName or not prevServerkey or not followedServerkey or not sign:
			checkResult.setCheckResult(CROSSSERVICERESULT.FAIL, CROSSSERVICECODE.CROSS_SERVICE_ARGS_ERROR)
		elif sign != Utils.SecretMD5Sign(Define.CS3_GAME_SECRET, ("PrevServerkey", prevServerkey), ("FollowedServerkey",followedServerkey), ("AccountName", accountName), ("RoleName", roleName)):
				checkResult.setCheckResult(CROSSSERVICERESULT.FAIL, CROSSSERVICECODE.CROSS_SERVICE_SIGN_ERROR)
		elif Define.CHECK_SERVER_KEY_TYPE_PREV in checkKeyTypes:
			if not self.checkServerkey(prevServerkey):
				checkResult.setCheckResult(CROSSSERVICERESULT.FAIL, CROSSSERVICECODE.CROSS_SERVICE_SERVER_KEY_ERROR)
			elif not self.checkAccount(prevServerkey, accountName):
				checkResult.setCheckResult(CROSSSERVICERESULT.FAIL, CROSSSERVICECODE.CROSS_SERVICE_ACCOUNT_NOT_EXISTS)
			elif not self.checkRole(prevServerkey, accountName, roleName):
				checkResult.setCheckResult(CROSSSERVICERESULT.FAIL, CROSSSERVICECODE.CROSS_SERVICE_ROLE_NOT_EXISTS)
		elif Define.CHECK_SERVER_KEY_TYPE_FOLLOWED in checkKeyTypes:
			if not self.checkServerkey(followedServerkey):
				checkResult.setCheckResult(CROSSSERVICERESULT.FAIL, CROSSSERVICECODE.CROSS_SERVICE_SERVER_KEY_ERROR)
			elif not self.checkAccount(followedServerkey, accountName):
				checkResult.setCheckResult(CROSSSERVICERESULT.FAIL, CROSSSERVICECODE.CROSS_SERVICE_ACCOUNT_NOT_EXISTS)
			elif not self.checkRole(followedServerkey, accountName, roleName):
				checkResult.setCheckResult(CROSSSERVICERESULT.FAIL, CROSSSERVICECODE.CROSS_SERVICE_ROLE_NOT_EXISTS)
				
		return checkResult


class CrossServiceInterface:
	_instance = None
	def __init__(self):
		pass
		
	@staticmethod
	def instance():
		"""
		"""
		if CrossServiceInterface._instance == None:
			CrossServiceInterface._instance = CrossServiceInterface()
		return CrossServiceInterface._instance
		
	def requestCrossService(self, request):
		"""
		请求跨服
		"""
		#先更新服务器配置信息
		#self.updateServerInfos()
		
		checkResult = CrossServiceManager.instance().check(request, [Define.CHECK_SERVER_KEY_TYPE_PREV])
		if checkResult.getResult() != CROSSSERVICERESULT.SUCCESS:
			return Utils.HttpResponseJson({ "result" : checkResult.getResult(), "result_code" : checkResult.getCode() })
			
		accountName = request.GET.get("AccountName", None)
		roleName = request.GET.get("RoleName", None)
		prevServerkey = request.GET.get("PrevServerkey", None)
		followedServerkey = request.GET.get("FollowedServerkey", None)
		
		excuteResult = g_CSDataInst.updateCrossServiceData(prevServerkey, followedServerkey, accountName, roleName)
		if excuteResult.getResult() == DATABASEACTIONRESULT.FAIL:
			return Utils.HttpResponseJson({ "result" : CROSSSERVICERESULT.FAIL, "result_code" : CROSSSERVICECODE.CROSS_SERVICE_UNKNOW_ERROR })
			
		return Utils.HttpResponseJson({ "result" : CROSSSERVICERESULT.SUCCESS, "result_code" : CROSSSERVICECODE.CROSS_SERVICE_SUCCESS })
		
	def requestReturnServer(self, request):
		"""
		请求返回原服务器
		"""
		checkResult = CrossServiceManager.instance().check(request, [Define.CHECK_SERVER_KEY_TYPE_PREV, Define.CHECK_SERVER_KEY_TYPE_FOLLOWED])
		if checkResult.getResult() != CROSSSERVICERESULT.SUCCESS:
			return Utils.HttpResponseJson({ "result" : checkResult.getResult(), "result_code" : checkResult.getCode() })
			
		accountName = request.GET.get("AccountName", None)
		roleName = request.GET.get("RoleName", None)
		prevServerkey = request.GET.get("PrevServerkey", None)
		followedServerkey = request.GET.get("FollowedServerkey", None)
		
		excuteResult = g_CSDataInst.updateReturnServerData(prevServerkey, followedServerkey, accountName, roleName)
		if excuteResult.getResult() == DATABASEACTIONRESULT.FAIL:
			if excuteResult.getCode() == CROSSSERVICECODE.CROSS_SERVICE_OLD_PLAYER_INFO_ERROR:
				return Utils.HttpResponseJson({ "result" : CROSSSERVICERESULT.FAIL, "result_code" : CROSSSERVICECODE.CROSS_SERVICE_OLD_PLAYER_INFO_ERROR })
			else:
				return Utils.HttpResponseJson({ "result" : CROSSSERVICERESULT.FAIL, "result_code" : CROSSSERVICECODE.CROSS_SERVICE_UNKNOW_ERROR })
			
		return Utils.HttpResponseJson({ "result" : CROSSSERVICERESULT.SUCCESS, "result_code" : CROSSSERVICECODE.CROSS_SERVICE_SUCCESS })
		
	def returnServerFinished(self, request):
		"""
		请求返回原服务器完成
		"""
		
		checkResult = CrossServiceManager.instance().check(request, [Define.CHECK_SERVER_KEY_TYPE_PREV])
		if checkResult.getResult() != CROSSSERVICERESULT.SUCCESS:
			return Utils.HttpResponseJson({ "result" : checkResult.getResult(), "result_code" : checkResult.getCode() })
		
		accountName = request.GET.get("AccountName", None)
		roleName = request.GET.get("RoleName", None)
		prevServerkey = request.GET.get("PrevServerkey", None)
		followedServerkey = request.GET.get("FollowedServerkey", None)
		
		excuteResult = g_CSDataInst.onReturnServerFinished(prevServerkey, followedServerkey, accountName, roleName)
		if excuteResult.getResult() == DATABASEACTIONRESULT.FAIL:
			return Utils.HttpResponseJson({ "result" : CROSSSERVICERESULT.FAIL, "result_code" : CROSSSERVICECODE.CROSS_SERVICE_UNKNOW_ERROR })
		return Utils.HttpResponseJson({ "result" : CROSSSERVICERESULT.SUCCESS, "result_code" : CROSSSERVICECODE.CROSS_SERVICE_SUCCESS })
		
		
g_CSInterfaceInst = CrossServiceInterface.instance()