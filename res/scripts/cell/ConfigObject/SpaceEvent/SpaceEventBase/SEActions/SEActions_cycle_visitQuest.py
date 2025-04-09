# -*- coding: utf-8 -*-

# 副本事件行为  拜访任务
import csdefine
import KBEDebug
import KBEngine
from ConfigObject.SpaceEvent.SpaceEventBase.SEActions.SEActionBase import SEActionBase
import Functions
import Math
import csstatus
import ItemTypeEnum
import random
import KBEMath

class SEAction374( SEActionBase ):
	"""
	灵兽圈  打开贴屏显示
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.taktTime = int( section["param1"] )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		for role in spaceEntity._spaceRoles:
			role.client.NotifyLXQDisplayScreen( taktTime )

class SEAction375( SEActionBase ):
	"""
	灵兽圈  关闭贴屏显示
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		for role in spaceEntity._spaceRoles:
			role.client.NotifyLXQCloseScreen( )

SEActionBase.setActionClass("SEAction374", SEAction374)
SEActionBase.setActionClass("SEAction375", SEAction375)