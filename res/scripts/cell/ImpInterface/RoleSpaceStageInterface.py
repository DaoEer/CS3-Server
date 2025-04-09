# -*- coding: utf-8 -*-

# 副本阶段功能接口

class RoleSpaceStageInterface:
	"""
	"""
	def CELL_OnEnterSpaceStageArea( self, srcEntityID, stageIndex, taskIndex ):
		"""
		<exposed method>
		玩家进入某阶段目标区域
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		
		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			spaceEntity.getScript().onEnterSpaceStageArea( spaceEntity, stageIndex, taskIndex )