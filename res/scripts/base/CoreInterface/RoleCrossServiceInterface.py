# -*- coding: utf-8 -*-
#KBEngine
import KBEngine

#common
import csdefine
import KBEDebug
import Functions


class RoleCrossServiceInterface:
	def __init__(self):
		self.isOnCrossService = False #是否处于跨服中
		
	def logon( self ):
		#isCrossServiceLogon属性在同步数据的后台赋值
		if not self.isCrossServiceLogon:
			self.resetCorssServiceInfo()
			
	def onLoseCell(self):
		if not self.isOnCrossService:
			self.resetCorssServiceInfo()
		
	def setCrossServiceInfo(self, prevServerkey, followedServerkey):
		self.prevServerkey = prevServerkey
		self.followedServerkey = followedServerkey
		
	def resetCorssServiceInfo(self):
		self.prevServerkey = ""
		self.followedServerkey = ""
		
	def canCrossService(self):
		"""
		检查能否跨服
		"""
		if self.isCrossServiceLogon:
			return False
		if self.isOnCrossService:
			return False
		return True
		
	def canReturnServer(self):
		"""
		检查能否返回原服
		"""
		if not self.isCrossServiceLogon:
			return False
		if self.prevServerkey == "" or self.followedServerkey == "":
			return False
		return True
		
	def requestCrossService(self, currServerkey, targetServerkey):
		"""
		Exposed method
		客户端请求跨服
		"""
		def onBeforeCrossServiceSaveCB(result, models):
			if result:
				CrossServiceMgr = KBEngine.globalData.get("CrossServiceManager", None)
				if CrossServiceMgr:
					CrossServiceMgr.requestCrossService(currServerkey, targetServerkey, self.accountEntity.playerName, self.playerName)
				else:
					KBEDebug.ERROR_MSG("requestCrossService: player(%s) before cross service error: can not find CrossServiceManager" % self.playerName)
					self.onRequestCrossServiceResult(Functions.toJsonString({'result_code': csdefine.CROSS_SERVICE_UNKNOW_ERROR, 'result': 'FAIL'}))
			else:
				KBEDebug.ERROR_MSG("requestCrossService: player(%s) before cross service write to db error" % self.playerName)
				self.onRequestCrossServiceResult(Functions.toJsonString({'result_code': csdefine.CROSS_SERVICE_UNKNOW_ERROR, 'result': 'FAIL'}))
			
		if not self.canCrossService():
			return
			
		self.setCrossServiceInfo(currServerkey, targetServerkey)
		self.writeToDB(onBeforeCrossServiceSaveCB)
	
	def onRequestCrossServiceResult(self, result):
		"""
		define method
		请求跨服结果
		"""
		data = eval(result)
		if data["ROOT"]["result_code"] != csdefine.CROSS_SERVICE_SUCCESS:
			self.resetCorssServiceInfo()
		
		self.client.CLIENT_OnRequestCrossServiceResult(result)
	
	def requestReturnServer(self):
		"""
		Exposed method
		客户端请求返回原服
		"""
		def onBeforeReturnServerSaveCB(result, models):
			if result:
				CrossServiceMgr = KBEngine.globalData.get("CrossServiceManager", None)
				if CrossServiceMgr:
					CrossServiceMgr.requestReturnServer(self.prevServerkey, self.followedServerkey, self.accountEntity.playerName, self.playerName)
				else:
					KBEDebug.ERROR_MSG("requestReturnServer: player(%s) before return server error: can not find CrossServiceManager" % self.playerName)
					self.onRequestReturnServerResult(Functions.toJsonString({'result_code': csdefine.CROSS_SERVICE_UNKNOW_ERROR, 'result': 'FAIL'}))
			else:
				KBEDebug.ERROR_MSG("requestReturnServer: player(%s) before return server write to db error" % self.playerName)
				self.onRequestReturnServerResult(Functions.toJsonString({'result_code': csdefine.CROSS_SERVICE_UNKNOW_ERROR, 'result': 'FAIL'}))
				
		if not self.canReturnServer():
			return
		self.writeToDB(onBeforeReturnServerSaveCB)
	
	def onRequestReturnServerResult(self, result):
		"""
		define method
		请求返回原服结果
		"""
		self.client.CLIENT_OnRequestReturnServerResult(result)
		
	def startCrossService(self):
		"""
		Exposed method
		开始跨服处理
		"""
		self.isOnCrossService = True
		
		#离开队伍
		self.leaveTeamFB(self.id)
		
		#self.writeToDB()
		
		self.destroyRoleCellEntity()
		
	def startReturnServer(self):
		"""
		Exposed method
		开始返回原服处理
		"""
		#self.clientOnCrossServiceOver()
		self.resetCorssServiceInfo()
		self.isOnCrossService = False
		
	def destroyRoleCellEntity(self):
		"""
		销毁原服务器玩家Cell部分
		"""
		self.destroyCellEntity()

	def clientOnCrossServiceOver(self):
		"""
		define method
		跨服结束返回原客户端
		"""
		self.logonSpace()
		self.client.OnRoleReEnterWorld()