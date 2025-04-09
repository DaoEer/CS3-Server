# -*- coding: utf-8 -*-

# 副本事件行为
import KBEMath
import KBEDebug
import KBEngine
from ConfigObject.SpaceEvent.SpaceEventBase.SEActions.SEActionBase import SEActionBase
import csdefine
import cschannel_msgs
import csstatus

class SEAction362( SEActionBase ):
	"""
	烽火连天 击杀玩家
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		dieEntity = KBEngine.entities.get(triggerID,None)
		killEntity = KBEngine.entities.get( eventParams["killerID"],None )
		if dieEntity == None or killEntity == None:
			return
		if killEntity.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
			return
		spaceEntity.memberDatas.kill( dieEntity.id, killEntity.id )

class SEAction363( SEActionBase ):
	"""
	烽火连天 系统公告
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self._noticeNumber = int(section["param1"])

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		if self._noticeNumber == csstatus.ACTIVITY_CAMP_FHLT_CREATE_DROP:
			for role in spaceEntity._spaceRoles:
				if role.getClient():
					role.statusMessage( csstatus.ACTIVITY_CAMP_FHLT_CREATE_DROP, "" )
		else:
			killEntity = KBEngine.entities.get( eventParams["killerID"], None )
			if dieEntity == None or killEntity == None:
				return
			if killEntity.getEntityFlag() == csdefine.ENTITY_FLAG_VEHICLEPET:
				killEntity = killEntity.getOwnerEntity()
			if killEntity.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
				if killEntity.camp == csdefine.CAMP_TAOSIM:
					campStr = cschannel_msgs.CAMP_TAOSIM
				else:
					campStr = cschannel_msgs.CAMP_DEMON
				for role in spaceEntity._spaceRoles:
					if role.getClient():
						role.statusMessage( self._noticeNumber, campStr, killEntity.name )

class SEAction364( SEActionBase ):
	"""
	烽火连天 摧毁祭坛,转移积分
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self._integralRatio = float(section["param1"])
		self._camp = int(section["param2"])

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		spaceEntity.transferIntegral( self._camp, self._integralRatio )

class SEAction365( SEActionBase ):
	"""
	烽火连天 召唤先锋
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self._camp = int(section["param1"])

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		spaceEntity.onCallVanMonster( self._camp )

SEActionBase.setActionClass("SEAction362", SEAction362)
SEActionBase.setActionClass("SEAction363", SEAction363)
SEActionBase.setActionClass("SEAction364", SEAction364)
SEActionBase.setActionClass("SEAction365", SEAction365)