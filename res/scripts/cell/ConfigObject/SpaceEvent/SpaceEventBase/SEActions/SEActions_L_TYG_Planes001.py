# -*- coding: utf-8 -*-
# 副本事件行为
import KBEDebug
import KBEngine
from ConfigObject.SpaceEvent.SpaceEventBase.SEActions.SEActionBase import SEActionBase
import csstatus
class SEAction166( SEActionBase ):
	"""
	玩家向指定的Entity释放技能
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.appointScriptID = section["param1"]
		self.skillIDs = section["param2"].split("|")
		self.isHitTime = section["param3"].split("|")

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		isHit = bool(int(eventParams["extraValue"]))
		idList = spaceEntity.getEntityRecord( self.appointScriptID )
		for id in idList:
			entity = KBEngine.entities.get( id,None )
			if entity:
				for player in spaceEntity._spaceRoles:
					if isHit:
						statusID = player.useSkillToEntity( int(self.skillIDs[0]), entity.id )
						if statusID == csstatus.SKILL_GO_ON:
							player.addTimerCallBack( float(self.isHitTime[0]),"notifyContinueTorture",() )
					else:
						statusID = player.useSkillToEntity( int(self.skillIDs[1]), entity.id )
						if statusID == csstatus.SKILL_GO_ON:
							player.addTimerCallBack( float(self.isHitTime[1]),"notifyContinueTorture",() )

class SEAction167( SEActionBase ):
	"""
	通知客户端恢复玩家状态
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return		
		for player in spaceEntity._spaceRoles:
			player.client.CLIENT_NotifyClientRecoveryStatus()

class SEAction242( SEActionBase ):
	"""
	通知界面显示拷问结果
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return		
		for player in spaceEntity._spaceRoles:
			player.client.CLIENT_NotifyClientTortureResult()

SEActionBase.setActionClass("SEAction166", SEAction166)
SEActionBase.setActionClass("SEAction167", SEAction167)
SEActionBase.setActionClass("SEAction242", SEAction242)
