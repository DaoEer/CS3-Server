# -*- coding: utf-8 -*-
#
import csdefine
import KBEngine
from KBEDebug import *

class RoleTalkInterface:
	"""
	角色对话接口
	"""
	def __init__(self):
		pass

	def setGossipText(self, NPCID, text):
		"""
		将对话内容发送到客户端
		@param 		text: 设置任务窗口文本
		@type 		 text: str
		@return: 	None
		"""
		self.client.onSetGossipText(NPCID, text)
		isalnums = True
		voiceIDList = text.split("|")
		for voiceID in voiceIDList:
			if not voiceID.isalnum():
				isalnums = False
		if isalnums:
			self.showMessagePlaySound(text)

	def addGossipOption(self, key, title, type = csdefine.GOSSIP_TYPE_NORMAL_TALKING):
		"""
		普通对话
		@type 		 key: string
		@type 		 title: string
		@return:	 None

		type : 默认是普通对话才用 csdefine.GOSSIP_TYPE_NORMAL_TALKING
		"""
		self.client.onAddGossipOption(key, title, type)

	def sendGossipComplete( self ,targetID ):
		"""
		@param 		 player: ROLE 实例
		@type 		 targetID: OBJECT_ID
		@return: None
		"""
		self.client.onGossipComplete( targetID )

	#----------------------------------------------
	# 与MonsterExtClick\MonsterExtClickAndModel交互相关
	#----------------------------------------------
	def setMonsterGossipText(self, MonsterID, text):
		"""
		将对话内容发送到客户端
		@param 		text: 设置任务窗口文本
		@type 		 text: str
		@return: 	None
		"""
		self.client.onSetMonsterGossipText(MonsterID, text)
		
	def addMonsterGossipOption(self, key, title, type = csdefine.GOSSIP_TYPE_NORMAL_TALKING):
		"""
		普通对话
		@type 		 key: string
		@type 		 title: string
		@return:	 None

		type : 默认是普通对话才用 csdefine.GOSSIP_TYPE_NORMAL_TALKING
		"""
		self.client.onAddMonsterGossipOption(key, title, type)

	def sendMonsterGossipComplete( self ,targetID ):
		"""
		@param 		 player: ROLE 实例
		@type 		 targetID: OBJECT_ID
		@return: None
		"""
		self.client.onMonsterGossipComplete( targetID )
		
	def talkWithMonster(self, srcEntityID, MonsterID, key):
		"""
		<Exposed method>
		Monster和客户端对话
		@param dlgKey: 对话关键字
		@param args: 对话参数(暂定为字符串型 后面需修改为自定义数据类型)
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		self.triggerSkillEvent(csdefine.SKILL_EVENT_REQUEST_ACTION, self.id, {"requestType" : csdefine.SKILL_EVENT_ACTION_TYPE_TALK})
		monster = KBEngine.entities.get( int(MonsterID), None )
		if monster:
			monster.monsterAITriggerEvent( csdefine.ENTITY_EVENT_ON_GOSSIP_WITH_MONSTER, [key], self )
	#----------------------------------------------
	# 与SpellBox交互相关
	#----------------------------------------------
	def requestRefreshBoxStatus( self, srcEntityID, entityID ):
		"""
		<exposed method>
		请求刷新某个箱子的状态
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		entity = KBEngine.entities.get( entityID )
		if entity:
			entity.requestRefreshCondition( entity, self )

	#----------------------------------------------
	# 与MultiAreaSpellBox多区域触发相关
	#----------------------------------------------
	def CELL_RequestRefreshAreaStatus( self, srcEntityID, entityID ):
		"""
		<exposed method>
		请求刷新某个区域的状态
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		entity = KBEngine.entities.get( entityID )
		if entity:
			entity.getScript().requestRefreshAreaStatus( entity, self )
