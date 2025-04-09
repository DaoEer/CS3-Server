# -*- coding: utf-8 -*-


"""
用于所有非PC类型的基本类型

包括NPC、怪物、陷阱等各种类型
"""


#python
#engine
import KBEngine
from KBEDebug import *

#script
import CoreObject.GameObject as GameObject
import ImpInterface.EntitySpaceEventInterface as EntitySpaceEventInterface



class NPCBaseObject( GameObject.GameObject, EntitySpaceEventInterface.EntitySpaceEventInterface ):
	"""
	非玩家控制对象基类
	"""
	def __init__( self ):
		GameObject.GameObject.__init__( self )
		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			spaceEntity.addEntityRecord( self.scriptID, self.id )
			spaceEntity.addEntityMailBoxRecord( self.scriptID, self )
		self.spaceEvent_npcObjectCreate()

	def beforeDestroy( self ):
		"""
		virtual method
		销毁前做一些事
		"""
		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			spaceEntity.onNPCObjectDestroy( self.id, self.scriptID, self.group )
		self.spaceEvent_npcObjectDestroy()
		if spaceEntity:
			spaceEntity.delEntityRecord( self.scriptID, self.id )
			spaceEntity.delEntityMailBoxRecord( self.scriptID, self )
		GameObject.GameObject.beforeDestroy( self )

	def CELL_onClientReady( self, srcEntityID ):
		"""
		<Expose method>
		客户端Character Actor已经准备好
		"""
		pass
#----------------------基础属性--------------------------------------------------------------
	def behIsOptimize(self, bedType, behDescribe):
		"""
		是否采用优化的方案，用于客户端执行行为的判断
		:return: bool
		"""
		return False
		
	def getName( self ):
		"""
		virtual method
		获取名称
		"""
		return "NPCBaseObject"
	
	def getScriptID( self ):
		return self.scriptID

	def getUname( self ):
		"""
		获取当前Monster/NPC名字
		"""
		return self.uname
		
	def setUname( self, unameValue ):
		"""
		设置当前Monster/NPC名字
		"""
		self.uname = unameValue
	
	def getLevel( self ):
		"""获取等级"""
		return self.level
		
	def getProfession( self ):
		"""获取职业"""
		return self.profession
	
	def getCamp( self ):
		"""
		获取阵营
		"""
		return self.camp
	
	def clientsPlayAction( self, action, time ):
		"""
		"""
		self.allClients.CLIENT_OnPlayAction( action, time )

#----------------------临时阵营-------------------------
	def setTempCamp( self, newCamp ):
		"""
		设置临时阵营
		改变阵营玩法 CST-2129
		"""
		if self.tempCamp == newCamp:
			return
		oldCamp = self.tempCamp
		self.tempCamp = newCamp
		self.onTempCampChange( oldCamp, self.tempCamp )

	def onTempCampChange(  self, oldCamp, newCamp ):
		"""
		virtual method
		临时阵营改变
		"""
		pass
	
	def getFinalCamp( self ):
		"""
		获取最终阵营：有临时阵营则返回临时阵营，否则返回原阵营
		"""
		if self.tempCamp:
			return self.tempCamp
		return self.camp

#---------------------势力------------------------------
	def setTempFaction( self, newFaction ):
		"""
		设置临时势力
		"""
		if self.tempFaction == newFaction:
			return
		self.tempFaction = newFaction
		self.onTempFactionChange()
	
	def onTempFactionChange( self ):
		"""
		virtual method
		临时势力改变
		"""
		pass

	def getFinalfaction( self ):
		"""
		获取最终势力
		"""
		if self.tempFaction:
			return self.tempFaction
		return self.faction

#-------npc对话相关-----------------------------------------------------
	def CELL_gossipWith(self, srcEntityID):
		"""
		<exposed method>
		处理客户端点击NPC事件
		"""
		playerEntity = KBEngine.entities.get(srcEntityID)
		if playerEntity:
			playerEntity.triggerSkillEvent(csdefine.SKILL_EVENT_REQUEST_ACTION, self.id, {"requestType" : csdefine.SKILL_EVENT_ACTION_TYPE_TALK})
		self.getScript().gossipWith( self, srcEntityID )



