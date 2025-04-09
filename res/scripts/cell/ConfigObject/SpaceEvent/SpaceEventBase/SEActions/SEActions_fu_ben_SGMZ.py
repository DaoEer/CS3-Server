# -*- coding: utf-8 -*-

# 副本事件行为  上古密阵
from ConfigObject.SpaceCopyYXLMMonsterDataLoader import g_spaceCopyYXLMMonsterDataLoader
from ConfigObject.SpaceEvent.SpaceEventBase.SEActions.SEActionBase import SEActionBase
from ConfigObject import PatrolRouteLoader

import KBEDebug
import KBEngine
import Functions
import Math
import csdefine
import csstatus
import cschannel_msgs
import ItemTypeEnum
import random
from Reward import RewardBasicValueData

CAMP_NAMES = {	csdefine.CAMP_TAOSIM : cschannel_msgs.CAMP_TAOSIM,		#仙道
					csdefine.CAMP_DEMON : cschannel_msgs.CAMP_DEMON		#魔道
				}
				
class SEAction354( SEActionBase ):
	"""
	上古密阵  (终极大Boss)怪物被击杀 奖励
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.rewardExpRate = float( section["param1"] )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		dieEntity = KBEngine.entities.get(triggerID,None)
		killEntity = KBEngine.entities.get( eventParams["killerID"], None )
		if not dieEntity.isReady() or dieEntity.inDestroying():
			return
		if not killEntity.isReady() or killEntity.inDestroying():
			return
		if dieEntity.getEntityFlag() != csdefine.ENTITY_FLAG_MONSTER:
			return
		if killEntity.getEntityFlag() == csdefine.ENTITY_FLAG_VEHICLEPET:
			killEntity = killEntity.getOwnerEntity()

		rewardExp = int(self.rewardExpRate * RewardBasicValueData.datas.get(dieEntity.getLevel(), {}).get("exp", 0))
		if killEntity.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
			for member in killEntity.getAllTeamMemberMB():
				entity = KBEngine.entities.get( member.id, None )
				if not entity:
					continue
				entity.addExp( rewardExp, csdefine.EXP_ADD_REASON_SPACE_SENTLEMENT )
		spaceEntity.onFinalBossBeKill( triggerID, rewardExp, killEntity )


class SEAction355( SEActionBase ):
	"""
	创建NPC队伍 废弃
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.scriptID = section["param1"].split("|")

	def do( self, spaceEntity, triggerID, eventParams ):
		return
		spaceEntity.getScript().onSpaceCreateEntity( spaceEntity, self.scriptID )

class SEAction366( SEActionBase ):
	"""
	上古密阵 怪物被击杀 计数 废弃
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		return
		if not spaceEntity:
			return
		killEntity = KBEngine.entities.get( eventParams["killerID"], None )
		if not killEntity.isReady() or killEntity.inDestroying():
			return
		if killEntity.getEntityFlag() == csdefine.ENTITY_FLAG_VEHICLEPET:
			killEntity = killEntity.getOwnerEntity()

		if killEntity.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
			spaceEntity.statisticsKillNum( killEntity )

class SEAction367( SEActionBase ):
	"""
	上古密阵  怪物被击杀完成阶段
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.monsterScriptID = section["param1"]
		self.rate = 1.0
		if section["param2"]:
			self.rate = float( section["param2"] )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		killEntity = KBEngine.entities.get( eventParams["killerID"], None )
		if not killEntity.isReady() or killEntity.inDestroying():
			return
		if killEntity.getEntityFlag() == csdefine.ENTITY_FLAG_VEHICLEPET:
			killEntity = killEntity.getOwnerEntity()

		if killEntity.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
			spaceEntity.onMonsterBeKill( triggerID, killEntity, self.rate )
			spaceEntity.getScript().spaceStage_onMonsterBeKill( spaceEntity, self.monsterScriptID, killEntity )
			
class SEAction402( SEActionBase ):
	"""
	上古密阵 队伍第一次抵达最终BOSS区域
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		"""
		队伍进入BOSS区域的提示。CST-10350 一
		"""
		if not spaceEntity:
			return
		entity = KBEngine.entities.get(triggerID)
		if entity and entity.getCamp() in spaceEntity.notArriveBossCamp:
			spaceEntity.notArriveBossCamp.remove(entity.getCamp())
			for roleCell in spaceEntity._spaceRoles:
				roleCell.statusMessage( csstatus.MI_ZHEN_LAST_BOSS_ENTER_BATTLE, CAMP_NAMES[entity.getCamp()] )
	
SEActionBase.setActionClass("SEAction354", SEAction354)
SEActionBase.setActionClass("SEAction355", SEAction355)
SEActionBase.setActionClass("SEAction366", SEAction366)
SEActionBase.setActionClass("SEAction367", SEAction367)
SEActionBase.setActionClass("SEAction402", SEAction402)