# -*- coding: utf-8 -*-

# 副本事件行为
import KBEDebug
import KBEngine
import Const
from ConfigObject.SpaceEvent.SpaceEventBase.SEActions.SEActionBase import SEActionBase

class SEAction294( SEActionBase ):
	"""
	CST-6526 冥域缉凶 显示能量条
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.maxEnergy = int( section["param1"] )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		trapEntity = spaceEntity.getEntityMailBoxRecord( Const.MYJX_MACHINE_TRAP_SCRIPTID )
		if trapEntity:
			trapEntity[0].setMaxEnergy( self.maxEnergy )
			trapEntity[0].updateEnergyToClient()

SEActionBase.setActionClass("SEAction294", SEAction294)

