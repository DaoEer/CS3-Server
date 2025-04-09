# -*- coding: utf-8 -*-
#
import Math
import KST

import csstatus
import csdefine
import Functions
import Define
import KBEngine
import KBEDebug
from LoadJsonData import g_JsonData


class RoleTeleportInterface:
	"""
	传送石接口
	"""
	def __init__(self):
		self.initTeleportPoint()

	def initTeleportPoint( self ):
		"""
		初始化默认开启的传送点
		"""
		for data in g_JsonData.teleportStoneDatas:
			if data["IsOpen"]: self._addTeleportPoint(data["Name"])

	def CELL_TeleportPoint( self, srcEntityID, teleportType, point ):
		"""
		Exposed method
		请求传送到某个传送点
		"""
		if not self.validateClientCall(srcEntityID):
			return

		#判断当前所在的地图，是否允许传送
		spaceObj = KST.g_objFactory.getSpaceObject( self.spaceScriptID )
		if spaceObj.getForbidUseTeleportPoint():
			return
		
		#传送点是否已开启
		if not self.isOpenTeleportPoint(point):
			return

			
		data = self.getTeleportPointData(point)
		if not self.checkTeleportPointCondition(data):
			return
		
		scriptID = data["ScriptID"]
		position = self.str2Vector3(data["Position"])
		direction = self.str2Vector3(data["Direction"])
		
		#TODO(QRN):根据策划文档，后期可能会有两种传送方式，预留相应的处理方式
		if teleportType == Define.TELEPORT_BY_TELEPORTSTONE:	#0、通过神行石传送
			#当前为死亡状态，无法使用神行石进行寻路！
			if self.getState() == csdefine.ENTITY_STATE_DEAD:
				self.statusMessage(csstatus.CANT_TELEPORT_STONE_DEAD_STATE)
				return		
			#当前为战斗状态，无法使用神行石进行寻路！
			if self.getState() == csdefine.ENTITY_STATE_FIGHT:
				self.statusMessage(csstatus.CANT_TELEPORT_STONE_FIGHT_STATE)
				return
			self.teleportByItem( point )

		elif teleportType == Define.TELEPORT_BY_MONEY:			#1、通过消耗金钱传送
			money = int(data.get("MoneyCost", 0))
			if not self.subBindMoney( money, csdefine.MONEY_SUB_REASON_TELEPORT ):
				self.inquireMessage(csstatus.NPCSHOP_COST_MONEY_REPLACE_BIND_MONEY, [Functions.moneyToStr(money)], "replacePayTel", money, scriptID, position, direction)
				return
			self.gotoSpaceUE4( scriptID, position, direction )
		elif teleportType == Define.TELEPORT_BY_NONE:			#2、无条件传送
			self.gotoSpaceUE4( scriptID, position, direction )
		else:
			KBEDebug.ERROR_MSG("RoleTeleportInterface:CELL_TeleportPoint error, error teleportType(%d)" %(teleportType))
		
	def replacePayTel(self, reply, money, scriptID, position, direction):
		"""金币代付绑定金币传送"""
		if reply:
			if self.subMoney(money, csdefine.MONEY_SUB_REASON_TELEPORT):
				self.gotoSpaceUE4(scriptID, position, direction)
			else:
				self.statusMessage(csstatus.CANNOT_TELEPORT_WITHMONEYCOST)



	def getTeleportPointData(self, point):
		"""
		"""
		for data in g_JsonData.teleportStoneDatas:
			if data["Name"] == point:
				return data
		return None
	
	def checkTeleportPointCondition(self, data):
		"""
		条件检测(开启、传送)
		"""
		if not data:
			return False
		
		#阵营
		limitCamp = data["LimitCamp"]
		if limitCamp != csdefine.CMAP_NONE and limitCamp != self.camp:	
			#self.statusMessage(cssstatus.CANNOT_TELEPORT_WITHCAMPLIMIT, "")
			return False
		
		#等级		
		limitLv = data["LimitLevel"]
		if limitLv > self.level:
			#self.statusMessage(csstatus.CANNOT_OPEN_TELEPORTSTONE_WITHLIMITLV, str(limitLv))
			return False
		
		"""
		#金钱
		moneycost = data["MoneyCost"]
		if moneycost > self.money:
			#self.statusMessage(csstatus.CANNOT_TELEPORT_WITHMONEYCOST, "")
			return False
		"""
		return True	

	def str2Vector3(self, data):
		"""
		空格分割的vector3数据提取出来
		"""
		try:
			x = float(data["X"])
			y = float(data["Y"])
			z = float(data["Z"])
			return Math.Vector3( x, y, z )
		except:
			KBEDebug.ERROR_MSG("RoleTeleportInterface:str2Vector3, error")
			return Math.Vector3(0.0, 0.0, 0.0)
	
	def isOpenTeleportPoint(self, point):
		"""
		判断某传送点是否开启
		"""
		lst = self.teleportPointNPCs.split("|")
		return point in lst
		
	def _addTeleportPoint(self, point):
		"""
		"""
		data = self.getTeleportPointData(point)
		if not data: return
		
		#是否满足开启条件
		if not self.checkTeleportPointCondition(data):
			return
		
		if self.teleportPointNPCs == "":
			self.teleportPointNPCs += point
		elif self.isOpenTeleportPoint(point) == False:
			self.teleportPointNPCs += ("|" + point)

	def addTeleportPoint(self, point):
		"""
		传送点开启
		"""
		self._addTeleportPoint(point)
		data = self.getTeleportPointData(point)
		if not data: return
		self.statusMessage(csstatus.TELEPORT_STONE_HAS_ACTIVATE, data["DstName"])

	def removeTeleportPoint( self, point ):
		"""
		传送点关闭
		"""
		lst = self.teleportPointNPCs.split("|")
		if point in lst:
			replaceStr = "|" + point
			
			#如果字符串是第0个，那么应该是没有“|”字符的
			if lst[0] == point:
				replaceStr = point
				
			self.teleportPointNPCs = self.teleportPointNPCs.replace(replaceStr,"") 	
		
	def onOpenMapWin( self ):
		"""
		打开地图界面
		"""
		if hasattr(self, "client") and self.client:
			self.client.OnOpenMapWin()
			
	def setCurrentTeleportPoint( self, point ):
		"""
		"""
		self.currentTeleportPoint = point
			
	def teleportToNPCPos( self ):
		"""
		"""
		data = self.getTeleportPointData(self.currentTeleportPoint)
		if not data:
			KBEDebug.ERROR_MSG("RoleTeleportInterface:teleportToCurrentNPCPos, not found point's[%s] data" %(self.currentTeleportPoint))
			return
		
		scriptID = data["ScriptID"]
		position = self.str2Vector3(data["Position"])
		direction = self.str2Vector3(data["Direction"])
		self.gotoSpaceUE4( scriptID, position, direction )
	