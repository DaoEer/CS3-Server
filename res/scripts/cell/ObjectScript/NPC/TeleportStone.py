#############
#传送石
#############

import KBEDebug
import KBEngine
import csdefine
import ObjectScript.NPC.NPC as NPC
from LoadJsonData import g_JsonData

class TeleportStone( NPC.NPC):
	"""
	"""
	def __init__( self ):
		"""
		"""
		NPC.NPC.__init__( self )
	
	def initData(self, configData):
		"""
		初始化数据
		@param data: dict
		"""
		NPC.NPC.initData( self, configData)
		
		#直接从这获取是解决配置重复的问题(因暂无配置，先用警告，配置好了之后应改回来，输出错误log)
		data = self.getTeleportPointData(self.scriptID)
		if not data:
			KBEDebug.WARNING_MSG("TeleportStone[%s]:initData error" %(self.scriptID))
			return

		self.triggerRadius = float(configData.get("Param1", "1"))
		#触发半径为0应该是不合理的(因暂无配置，先用警告，配置好了之后应改回来，输出错误log)
		if self.triggerRadius == 0:
			KBEDebug.WARNING_MSG("TeleportStone[%s]:initData error, triggerRadius is 0" %(self.scriptID))
			return
			
		#传送石默认开启
		self.setEntityProperty("isOpen", True)
		if "IsOpen" in data and int(data["IsOpen"]) == 0:
			self.setEntityProperty("isOpen", False)
		
		#传送石等级限制
		self.setEntityProperty("limitLv",1)
		if "LimitLevel" in data and data["LimitLevel"] != "":
			self.setEntityProperty("limitLv",int(data["LimitLevel"]))	
		
		#传送石阵营限制
		self.setEntityProperty("limitCamp",0)
		if "LimitCamp" in data and data["LimitCamp"] != "":
			self.setEntityProperty("limitCamp",int(data["LimitCamp"]))
	
	def getTeleportPointData(self, npcID):
		"""
		"""
		for data in g_JsonData.teleportStoneDatas:
			if data["DstNPCID"] == npcID:
				return data
		return None
		
	def onEnterTriggerRange( self, selfEntity, srcEntityID ):
		"""
		define method
		玩家进入触发范围内
		"""
		player = KBEngine.entities.get(srcEntityID, None)
		if not player:return
		
		flag = player.getEntityFlag()
		if flag != csdefine.ENTITY_FLAG_ROLE or selfEntity.spaceID != player.spaceID:
			return

		#传送点已经开启
		isOpen = self.getEntityProperty( "isOpen", True )
		if isOpen:return
		
		#大于触发距离
		#distance = selfEntity.position.flatDistTo(player.position)
		#if distance > self.triggerRadius:
		#	KBEDebug.ERROR_MSG(selfEntity.position, "#######", player.position)
		#	KBEDebug.ERROR_MSG("distance:%d radius:%d" %(distance, self.triggerRadius))
		#	return
			
		data = self.getTeleportPointData(self.scriptID)
		if not data: return
		
		player.addTeleportPoint(data["Name"])
			
	def onLeaveTriggerRange( self, selfEntity, srcEntityID ):
		"""
		define method
		玩家离开触发范围
		"""	
		pass