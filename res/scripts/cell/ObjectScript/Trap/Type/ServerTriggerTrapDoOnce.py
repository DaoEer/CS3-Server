# -*- coding: utf-8 -*-

import csdefine
import KBEDebug
import Math
import ECBProximityDefine
from ObjectScript.Trap.Type.ServerTriggerTrap import ServerTriggerTrap
from ObjectScript.Trap.Condition.TrapCondition import g_trapConditionMgr
from ObjectScript.Trap.Action.TrapActionMgr import g_trapActionMgr


class ServerTriggerTrapDoOnce( ServerTriggerTrap ):
	"""
	由服务器判定触发的陷阱
	"""
	def __init__( self ):
		ServerTriggerTrap.__init__( self )
	

	def initEntity( self, selfEntity ):
		"""
		virtual method.
		陷阱初始化
		"""
		ServerTriggerTrap.initEntity( self, selfEntity )

	def onEnterTrap( self, selfEntity, enterID ):
		"""
		virtual method.
		进入陷阱
		"""
		if enterID == selfEntity.id:
			return
		
		enterEntity = KBEngine.entities.get( enterID , None )
		if enterEntity == None:
			return
		
		for key, value in self.holdAction.items():
			g_trapActionMgr.holdBegin( selfEntity, enterEntity, key, value )

		for key, value in self.condition.items():
			if not g_trapConditionMgr.validate( selfEntity, enterEntity, key, value ):
				return

		#玩家下线再上线，只执行一次
		entityID = enterID
		if enterEntity.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
			entityID = -enterEntity.playerDBID #存玩家的DBID，为了防止与别的entityID冲突，加上个负号

		for index, info in self.enterAction.items():
			doOnce = info[2]
			if doOnce and  index in selfEntity.enterEntityRecd and  entityID in selfEntity.enterEntityRecd[index] :		#只执行一次
				continue
			
			g_trapActionMgr.action( selfEntity, enterEntity, info[0], info[1] )
			if index not in selfEntity.enterEntityRecd:
				selfEntity.enterEntityRecd[index] = []
			if entityID not in selfEntity.enterEntityRecd[index]:
				selfEntity.enterEntityRecd[index].append( entityID )

	def onLeaveTrap( self, selfEntity, enterID ):
		"""
		virtual method.
		离开陷阱
		"""
		if enterID == selfEntity.id:
			return

		enterEntity = KBEngine.entities.get( enterID , None )
		if enterEntity == None:
			return
			
		for key, value in self.holdAction.items():
			g_trapActionMgr.holdEnd( selfEntity, enterEntity, key, value )

		for key, value in self.condition.items():
			if not g_trapConditionMgr.validate( selfEntity, enterEntity, key, value ):
				return

		#玩家下线再上线，只执行一次
		entityID = enterID
		if enterEntity.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
			entityID = -enterEntity.playerDBID #存玩家的DBID，为了防止与别的entityID冲突，加上个负号

		for index, info in self.leaveAction.items():
			doOnce = info[2]
			if doOnce and  index in selfEntity.leaveEntityRecd and  entityID in selfEntity.leaveEntityRecd[index] :		#只执行一次
				continue
			
			g_trapActionMgr.action( selfEntity, enterEntity, info[0], info[1] )
			if index not in selfEntity.leaveEntityRecd:
				selfEntity.leaveEntityRecd[index] = []
			if entityID not in selfEntity.leaveEntityRecd[index]:
				selfEntity.enterEntityRecd[index].append( entityID )

