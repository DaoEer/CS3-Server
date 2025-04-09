# -*- coding: utf-8 -*-

import csdefine
import KBEDebug
import Math
import Functions
import KBEMath


class SpellGossipConditionBase:
	"""
	交互条件基类
	"""
	def __init__( self ):
		pass
	
	def init( self, configDict ):
		"""
		virtual method
		"""
		pass
	
	def check( self, boxCell, playerEntity ):
		"""
		virtual method
		"""
		return True

class SpellGossipConditionQuest( SpellGossipConditionBase ):
	"""
	任务目标状态 可支持配置多个任务，但只需满足一个即可
	"""
	def __init__( self ):
		self.eventType = csdefine.SPELL_BOX_LISTEN_EVENT_QUEST_CHANGE
		self._questIDList = []
		self._taskIDList = []
		self._taskStatusList = []
	
	def init( self, configDict ):
		"""
		virtual method
		"""
		self._questIDList = [int(i) for i in configDict["param1"].split("|")]
		self._taskIDList = [int(i) for i in configDict["param2"].split("|")]
		self._taskStatusList = [int(i) for i in configDict["param3"].split("|")]
	
	def check( self, boxCell, playerEntity ):
		"""
		virtual method
		"""
		if len(self._questIDList) != len(self._taskIDList) or len( self._taskIDList ) != len(self._taskStatusList) or len(self._questIDList) != len(self._taskStatusList):
			KBEDebug.ERROR_MSG("spellBox scriptID(%s) config is error"%boxCell.scriptID)
			return
		for questID in self._questIDList:
			if playerEntity.hasQuest( questID ):
				index = self._questIDList.index(questID)
				if playerEntity.queryTaskStatus( questID, self._taskIDList[index] ) == self._taskStatusList[index]:
					return True
		return False

class SpellGossipConditionKillBoss( SpellGossipConditionBase ):
	"""
	是否击杀了Boss
	"""
	def __init__( self ):
		self.eventType = csdefine.SPELL_BOX_LISTEN_EVENT_KILL_BOSS
		self._bossID = 0
	
	def init( self, configDict ):
		"""
		virtual method
		"""
		self._bossID = configDict["param1"]
	
	def check( self, boxCell, playerEntity ):
		"""
		virtual method
		"""
		spaceEntity = playerEntity.getCurrentSpace()
		if spaceEntity and playerEntity.isInSpaceCopy():
			bossList = spaceEntity.getEntityRecord(self._bossID)
			if len(bossList) <= 0:
				return True
		return False

class SpellGossipConditionHasKey( SpellGossipConditionBase ):
	"""
	背包中是否有某个物品
	"""
	def __init__( self ):
		self.eventType = csdefine.SPELL_BOX_LISTEN_EVENT_ADD_ITEM
		self._itemID = 0
	
	def init( self, configDict ):
		"""
		virtual method
		"""
		self._itemID = int(configDict["param1"])
	
	def check( self, boxCell, playerEntity ):
		"""
		virtual method
		"""
		itemList = playerEntity.getItemInstsByID(self._itemID)
		for item in itemList:
			if item.amount >= 1:
				return True
		return False
		
class SpellGossipConditionHasKeys( SpellGossipConditionBase ):
	"""
	背包中是否有某些物品（只要有一个物品返回true）
	"""
	def __init__( self ):
		self.eventType = csdefine.SPELL_BOX_LISTEN_EVENT_ADD_ITEM
		self._itemIDList = []
		self.msgID = 0
	
	def init( self, configDict ):
		"""
		virtual method
		"""
		self._itemIDList = [ int(i) for i in configDict["param1"].split("|") ]
		if configDict["param2"]:
			self.msgID = int(configDict["param2"])
	
	def check( self, boxCell, playerEntity ):
		"""
		virtual method
		"""
		itemList = playerEntity.getItemInstsByIDList(self._itemIDList)
		for item in itemList:
			if item.amount >= 1:
				return True
		if self.msgID:
			playerEntity.statusMessage(self.msgID, "")
		return False

class SpellGossipConditionStageComplete( SpellGossipConditionBase ):
	"""
	副本某阶段已完成
	"""
	def __init__( self ):
		self.eventType = csdefine.SPELL_BOX_LISTEN_EVENT_SPACE_STAGE_COMPLETE
		self._stageIndex = 0
	
	def init( self, configDict ):
		"""
		virtual method
		"""
		self._stageIndex = int(configDict["param1"])
	
	def check( self, boxCell, playerEntity ):
		"""
		virtual method
		"""
		spaceEntity = playerEntity.getCurrentSpace()
		if spaceEntity:
			return self._stageIndex in spaceEntity.completeSpaceStages
		return False

class SpellGossipConditionIsTeamCaptain( SpellGossipConditionBase ):
	"""
	队长才能对话
	副本串传送门：组队副本队长才能交互，其他归属副本无此限制
	"""
	def __init__( self ):
		self.eventType = csdefine.SPELL_BOX_LISTEN_EVENT_IS_CAPTAIN
	
	def check( self, boxCell, playerEntity ):
		"""
		virtual method
		"""
		spaceEntity = playerEntity.getCurrentSpace()
		if spaceEntity:
			if spaceEntity.belongType == csdefine.SPACE_BELONG_TEAM and not playerEntity.isTeamCaptain():
				return False
		return True

class SpellGossipConditionHasAllBuffs( SpellGossipConditionBase ):
	"""
	有某些buff，buff可填1个，可填多个，多个buff之间“且”的关系。
	"""
	def __init__( self ):
		self.eventType = csdefine.SPELL_BOX_LISTEN_EVENT_HAS_BUFF
		self._buffIDList = []

	def init( self, configDict ):
		"""
		virtual method
		"""
		self._buffIDList = configDict["param1"].split("|")

	def check( self, boxCell, playerEntity ):
		"""
		virtual method
		"""
		for buffID in self._buffIDList:
			if not len(playerEntity.findBuffsByBuffID( int(buffID) )):
				return False
		return True

class SpellGossipConditionNotHasAllBuffs( SpellGossipConditionBase ):
	"""
	无某些buff，buff可填1个，可填多个，多个buff之间“且”的关系。
	"""
	def __init__( self ):
		self.eventType = csdefine.SPELL_BOX_LISTEN_EVENT_HAS_BUFF
		self._buffIDList = []

	def init( self, configDict ):
		"""
		virtual method
		"""
		self._buffIDList = configDict["param1"].split("|")

	def check( self, boxCell, playerEntity ):
		"""
		virtual method
		"""
		for buffID in self._buffIDList:
			if len(playerEntity.findBuffsByBuffID( int(buffID) )):
				return False
		return True

class SpellGossipConditionHasOneOfAllBuffs( SpellGossipConditionBase ):
	"""
	有某些buff其中一个，buff填多个，多个buff之间“或”的关系。
	"""
	def __init__( self ):
		self.eventType = csdefine.SPELL_BOX_LISTEN_EVENT_HAS_BUFF
		self._buffIDList = []

	def init( self, configDict ):
		"""
		virtual method
		"""
		self._buffIDList = configDict["param1"].split("|")

	def check( self, boxCell, playerEntity ):
		"""
		virtual method
		"""
		for buffID in self._buffIDList:
			if len(playerEntity.findBuffsByBuffID( int(buffID) )):
				return True
		return False

class SpellGossipConditionNoOneOfAllBuffs( SpellGossipConditionBase ):
	"""
	无某些buff其中一个，buff填多个，多个buff之间“或”的关系。
	"""
	def __init__( self ):
		self.eventType = csdefine.SPELL_BOX_LISTEN_EVENT_HAS_BUFF
		self._buffIDList = []

	def init( self, configDict ):
		"""
		virtual method
		"""
		self._buffIDList = configDict["param1"].split("|")

	def check( self, boxCell, playerEntity ):
		"""
		virtual method
		"""
		for buffID in self._buffIDList:
			if not len(playerEntity.findBuffsByBuffID( int(buffID) )):
				return True
		return False

class SpellGossipConditionCanInteractive( SpellGossipConditionBase ):
	"""
	"""
	def __init__( self ):
		self.eventType = csdefine.SPELL_BOX_LISTEN_EVENT_IS_INTERACT

	def check( self, boxCell, playerEntity ):
		"""
		virtual method
		"""
		if boxCell.IsCanInteract and boxCell.getScript().isInteractive == csdefine.SPELL_BOX_NOT_PLAYERS_INTERACTIVE:
			return True
		return False

class SpellGossipConditionHasEntity( SpellGossipConditionBase ):
	"""
	SpellBox某范围内某些entity是否不存在(销毁)
	"""
	def __init__( self ):
		self.eventType = csdefine.SPELL_BOX_LISTEN_EVENT_HAS_ENTITY
		self.entityType = ""
		self.radius = 0.0
		self.scriptIDList = []

	def init( self, configDict ):
		"""
		virtual method
		"""
		self.entityType = configDict["param1"]
		if configDict["param2"]:
			self.radius = float(configDict["param2"])
		self.scriptIDList = configDict["param3"].split("|")

	def check( self, boxCell, playerEntity ):
		"""
		virtual method
		"""
		if len(self.scriptIDList):
			entities = boxCell.entitiesInRangeExt(self.radius,self.entityType)
			for entity in entities:
				if entity.scriptID in self.scriptIDList:
					return False
			return True

class SpellGossipConditionHasCampGossip( SpellGossipConditionBase ):
	"""
	是否已与该阵营的玩家交互
	"""
	def __init__( self ):
		self.eventType = csdefine.SPELL_BOX_LISTEN_EVENT_HAS_CAMP_GOSSIP

	def check( self, boxCell, playerEntity ):
		"""
		virtual method
		"""
		rewardCamp = boxCell.queryTemp("rewardCamp")
		if rewardCamp != playerEntity.getCamp():
			return True
		return False

class SpellGossipConditionIsThisCamp( SpellGossipConditionBase ):
	"""
	是否为该阵营的玩家
	"""
	def __init__( self ):
		self.eventType = csdefine.SPELL_BOX_LISTEN_EVENT_IS_THIS_CAMP

	def init( self, configDict ):
		"""
		virtual method
		"""
		self._camp = int(configDict["param1"])

	def check( self, boxCell, playerEntity ):
		"""
		virtual method
		"""
		if playerEntity.getCamp() == self._camp:
			return True
		return False
		
class SpellGossipConditionIsInArea( SpellGossipConditionBase ):
	"""
	是否不在某个阵营对应的圆形区域
	"""
	def __init__( self ):
		self.eventType = csdefine.SPELL_BOX_LISTEN_EVENT_QUEST_CHANGE
		self._taosimPoint = Math.Vector3(0,0,0)
		self._demonPoint = Math.Vector3(0,0,0)
		self._distce = 0.0

	def init( self, configDict ):
		"""
		virtual method
		"""
		pos1 = Functions.vector3TypeConvert(configDict["param1"])
		self._taosimPoint = KBEMath.Unreal2KBEnginePosition( pos1 )
		
		pos2 = Functions.vector3TypeConvert(configDict["param2"])
		self._demonPoint = KBEMath.Unreal2KBEnginePosition( pos2 )
		
		self._distce = float( configDict["param3"] )

	def check( self, boxCell, playerEntity ):
		"""
		virtual method
		"""
		if playerEntity.getFinalCamp() == csdefine.CAMP_TAOSIM:
			return playerEntity.position.distTo( self._taosimPoint ) > self._distce
		else:
			return playerEntity.position.distTo( self._demonPoint ) > self._distce


class SpellGossipConditionIsTowerCanGossip( SpellGossipConditionBase ):
	"""
	哨塔是否可交互 CST-4056 冰雪之战
	"""
	def __init__( self ):
		self.eventType = csdefine.SPELL_BOX_LISTEN_EVENT_BXZZ


	def init( self, configDict ):
		"""
		virtual method
		"""

	def check( self, boxCell, playerEntity ):
		"""
		virtual method
		"""
		from SpaceCopyFrozenFight import SpaceCopyFrozenFight as SpaceCopyFrozenFight
		spaceEntity = playerEntity.getCurrentSpace()
		if not spaceEntity or not isinstance(spaceEntity, SpaceCopyFrozenFight):
			return

		return spaceEntity.isTowerCanGossip(boxCell.scriptID, playerEntity.getCamp())


class SpellGossipConditionIsRivivePosCanGossip( SpellGossipConditionBase ):
	"""
	复活点水晶是否可交互 CST-4056 冰雪之战
	"""
	def __init__( self ):
		self.eventType = csdefine.SPELL_BOX_LISTEN_EVENT_BXZZ

	def init( self, configDict ):
		"""
		virtual method
		"""

	def check( self, boxCell, playerEntity ):
		"""
		virtual method
		"""
		from SpaceCopyFrozenFight import SpaceCopyFrozenFight as SpaceCopyFrozenFight
		spaceEntity = playerEntity.getCurrentSpace()
		if not spaceEntity or not isinstance(spaceEntity, SpaceCopyFrozenFight):
			return

		return spaceEntity.isRevivePosCanGossip(boxCell.scriptID, playerEntity.getCamp())

class SpellGossipConditionSelfWithoutAllBuffs( SpellGossipConditionBase ):
	"""
	箱子自身没有这些buff,可填多个,"且"的关系
	"""
	def __init__( self ):
		self.eventType = csdefine.SPELL_BOX_LISTEN_EVENT_HAS_BUFF
		self._buffIDList = []

	def init( self, configDict ):
		"""
		virtual method
		"""
		self._buffIDList = configDict["param1"].split("|")

	def check( self, boxCell, playerEntity ):
		"""
		virtual method
		"""
		for buffID in self._buffIDList:
			if len(boxCell.findBuffsByBuffID( int(buffID) )):
				return False
		return True

class SpellGossipConditionReceiveCopyNotify( SpellGossipConditionBase ):
	"""
	是否接受过某副本通知
	"""
	def __init__( self ):
		self.eventType = csdefine.SPELL_BOX_LISTEN_EVENT_HAS_NOTIFY
		self._notifyID = ""

	def init( self, configDict ):
		"""
		virtual method
		"""
		self._notifyID = configDict["param1"]

	def check( self, boxCell, playerEntity ):
		"""
		virtual method
		"""
		if playerEntity.playerDBID in boxCell.spaceNotifyTempData:
			if self._notifyID == boxCell.spaceNotifyTempData[playerEntity.playerDBID]:
				return True
		return False

class SpellGossipConditionHasCreator ( SpellGossipConditionBase ):
	"""
	针对专属spellBox,创建者才可以交互 CST-5772
	"""
	def __init__( self ):
		self.eventType = csdefine.SPELL_BOX_LISTEN_EVENT_CREATOR

	def check( self, boxCell, playerEntity ):
		"""
		virtual method
		"""
		if boxCell.creatorDBID == playerEntity.playerDBID:
			return True
		return False

class SpellGossipConditionHasTongGossip( SpellGossipConditionBase ):
	"""
	是否没有与某个帮会玩家交互
	"""
	def __init__( self ):
		self.eventType = csdefine.SPELL_BOX_LISTEN_EVENT_HAS_TONG_GOSSIP

	def check( self, boxCell, playerEntity ):
		"""
		virtual method
		"""
		gossipTong = boxCell.queryTemp("gossipTong")
		if gossipTong != playerEntity.tongDBID:
			return True
		return False

class SpellGossipConditionRoleIsInterract( SpellGossipConditionBase ):
	"""
	判断玩家是否有正在交互的SpellBoxPickItem
	"""
	def __init__( self ):
		self.eventType = csdefine.SPELL_BOX_LISTEN_EVENT_ROLE_IS_INTERACT

	def check( self, boxCell, playerEntity ):
		"""
		virtual method
		"""
		if not boxCell.openEntityID and not playerEntity.getInteractiveSpellBox():
			return True
		if boxCell.id == playerEntity.getInteractiveSpellBox() and boxCell.openEntityID == playerEntity.id:
			return True
		return False

class SpellGossipConditionLingTianBelongRole( SpellGossipConditionBase ):
	"""
	判断灵田的所有权是否属于该玩家
	"""
	def __init__( self ):
		self.eventType = csdefine.SPELL_BOX_LISTEN_EVENT_LINGTIAN

	def check( self, boxCell, playerEntity ):
		"""
		virtual method
		"""
		if boxCell.belongDBID == playerEntity.playerDBID:
			return True
		return False