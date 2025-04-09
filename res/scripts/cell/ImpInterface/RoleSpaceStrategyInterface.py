# -*- coding: utf-8 -*-

class RoleSpaceStrategyInterface:
	"""
	玩家副本策略点接口
	"""
	def spaceStrategy_onAddBuff( self, buffID ):
		"""
		增加Buff
		"""
		if not self.isInSpaceCopy():
			return
		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			spaceEntity.getScript().spaceStrategy_onRoleAddBuff( spaceEntity, self, buffID )

	def spaceStrategy_onTriggerBox( self, boxScriptID ):
		"""
		触发箱子
		"""
		if not self.isInSpaceCopy():
			return
		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			spaceEntity.getScript().spaceStrategy_onRoleTriggerBox( spaceEntity, self, boxScriptID )


	def spaceStrategy_onReceiveDamage( self, casterID ):
		"""
		接收伤害
		"""
		if not self.isInSpaceCopy():
			return
		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			spaceEntity.getScript().spaceStrategy_onRoleReceiveDamage( spaceEntity, self, casterID )

