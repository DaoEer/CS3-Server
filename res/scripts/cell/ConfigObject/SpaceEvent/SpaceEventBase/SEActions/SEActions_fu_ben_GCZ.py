# -*- coding: utf-8 -*-

# 副本事件行为
import csdefine
import KBEngine
from ConfigObject.SpaceEvent.SpaceEventBase.SEActions.SEActionBase import SEActionBase

class SEAction390( SEActionBase ):
	"""
	攻城战 小兵或者Boss被击杀
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.range = float(section["param1"])

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		dieEntity = KBEngine.entities.get(triggerID,None)
		killEntity = KBEngine.entities.get( eventParams["killerID"],None )
		if dieEntity == None or killEntity == None:
			return
		
		spaceEntity.onMonsterBeKill( killEntity, dieEntity, self.range )

class SEAction391( SEActionBase ):
	"""
	攻城战 玩家被击杀
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.range = float(section["param1"])

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return

		dieEntity = KBEngine.entities.get(triggerID,None)
		killEntity = KBEngine.entities.get( eventParams["killerID"],None )
		if dieEntity == None or killEntity == None:
			return

		spaceEntity.onRoleBeKill( killEntity, dieEntity, self.range )

class SEAction392( SEActionBase ):
	"""
	攻城战 玩家进入某范围增加操作提示Buff
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.buffID = int( section["param1"] )

	def do( self, spaceEntity, triggerID, eventParams ):
		entity = KBEngine.entities.get( triggerID,None )
		if entity and entity.queryTemp( "callAerialLadder" ) != None:
			entity.addBuff( entity, self.buffID )

class SEAction393( SEActionBase ):
	"""
	攻城战 设置攻城战副本成功
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		spaceEntity.setGCZIsWin(1)

class SEAction397( SEActionBase ):
	"""
	副本收到 兵营被占领的通知  从未被占领的兵营中移除
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		spaceEntity.removeRecordNotOccupyBarracks( int(eventParams["extraValue"]) )

SEActionBase.setActionClass("SEAction390", SEAction390)
SEActionBase.setActionClass("SEAction391", SEAction391)
SEActionBase.setActionClass("SEAction392", SEAction392)
SEActionBase.setActionClass("SEAction393", SEAction393)
SEActionBase.setActionClass("SEAction397", SEAction397)