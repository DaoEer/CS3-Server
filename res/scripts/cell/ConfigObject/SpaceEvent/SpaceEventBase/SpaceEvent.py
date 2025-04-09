# -*- coding: utf-8 -*-

# 副本事件

from ConfigObject.SpaceEvent.SpaceEventConditionsLoader import g_SEConditionsLoader
from ConfigObject.SpaceEvent.SpaceEventActionsLoader import g_SEActionsLoader
from KBEDebug import *

class SpaceEvent:
	def __init__( self ):
		self.id = 0
		self.eventType = 0
		self.actions = []
		self.triggerConditions = []
		self.spaceConditions = []
		self.canLoop = True		#可重复执行

	def init( self, fileName,id, eventType, sect ):
		"""
		初始化事件配置
		"""
		self.id = sect[ "id" ]
		self.eventType = eventType
		self.canLoop = sect[ "canLoop" ]
		
		for actSec in sect[ "actions" ]:
			action = g_SEActionsLoader[ actSec[ "id" ] ]()
			try:
				action.init( actSec )
			except:
				ERROR_MSG("space event file(%s) error!!! eventType:%s, ID:%i,actions id=%i is error( info:%s )"%(fileName,eventType,self.id, actSec["id"], actSec))
			self.actions.append( action )
		
		for condSec in sect.get( "triggerConditions", [] ):
			condition = g_SEConditionsLoader[ condSec[ "id" ] ]()
			try:
				condition.init( condSec )
			except:
				ERROR_MSG("space event file(%s) error!!! eventType:%s, ID:%i,triggerConditions id=%i is error"%(fileName,eventType,self.id, condSec["id"]))
			self.triggerConditions.append( condition )
		
		for condSec in sect.get( "spaceConditions", [] ):
			condition = g_SEConditionsLoader[ condSec[ "id" ] ]()
			try:
				condition.init( condSec )
			except:
				ERROR_MSG("space event file(%s) error!!! eventType:%s, ID:%i,spaceConditions id=%i is error"%(fileName,eventType,self.id, condSec["id"]))
			self.spaceConditions.append( condition )

	def checkBind( self, entity ):
		"""
		"""
		return True

	def bindForTrigger( self, spaceScriptID, entity ):
		"""
		"""
		if self.checkBind( entity ):
			entity.addListenSpaceEvents( spaceScriptID, self.eventType, self.id, self.triggerConditions )

	def checkSpaceCon( self, spaceEntity, eventParams ):
		"""
		"""
		for cond in self.spaceConditions:
			if not cond.check( spaceEntity, eventParams ):
				DEBUG_MSG_FOR_SPACECOPY_PLOT(spaceEntity, 0, "事件检测未通过：%s, params:%s" %(cond.__class__.__name__, cond.getParams()))
				return False
			DEBUG_MSG_FOR_SPACECOPY_PLOT(spaceEntity, 0, "事件检测通过：%s, params:%s" %(cond.__class__.__name__, cond.getParams()))
		return True

	def checkTriggerCon( self, triggerEntity, eventParams ):
		"""
		"""
		for cond in self.triggerConditions:
			if not cond.check( triggerEntity, eventParams ):
				DEBUG_MSG_FOR_SPACECOPY_PLOT(triggerEntity, 0, "事件检测未通过：%s, params:%s" %(cond.__class__.__name__, cond.getParams()))
				return False
			DEBUG_MSG_FOR_SPACECOPY_PLOT(triggerEntity, 0, "事件检测通过：%s, params:%s" %(cond.__class__.__name__, cond.getParams()))
		return True
	
	def do( self, spaceEntity, triggerID, eventParams ):
		"""
		"""
		for index, action in enumerate( self.actions ):
			if action.delayTime > 0:
				spaceEntity.addTimerCallBackForScript( action.delayTime, "doGivenSpaceEventAction", ( self.eventType, self.id, index, triggerID, eventParams ) )
			else:
				action.do( spaceEntity, triggerID, eventParams )
				DEBUG_MSG_FOR_SPACECOPY_PLOT(spaceEntity, triggerID, "事件已执行：%s, params:%s" %(action.__class__.__name__, action.getParams()))
	
	def doGivenAction( self, spaceEntity, actionIndex, triggerID, eventParams ):
		"""
		"""
		action = self.actions[ actionIndex ]
		action.do( spaceEntity, triggerID, eventParams )
		DEBUG_MSG_FOR_SPACECOPY_PLOT(spaceEntity, triggerID, "事件已执行：%s, params:%s" %(action.__class__.__name__, action.getParams()))
	
	def doOnRoleLoginDiffSpace( self, roleEntity, eventParams ):
		"""
		玩家登陆其他地图时执行
		不支持延时功能
		"""
		for index, action in enumerate( self.actions ):
			action.do( None, roleEntity.id, eventParams )	#此流程不能配副本相关的行为, spaceEntity传个None，配错则报错