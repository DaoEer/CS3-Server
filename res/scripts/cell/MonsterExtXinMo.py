# -*- coding: utf-8 -*-


#python
#engine
import KBEngine
#script
import Monster
import csstatus
import csdefine

class MonsterExtXinMo( Monster.Monster ):
	"""
	心魔怪物类
	"""
	def __init__( self ):
		Monster.Monster.__init__( self )

	def behDoSpell(self, spellID, spellTargetID, isGroupSkill=False, isOptimize=False):
		"""
		执行施法行为
		:param spellID:
		:param spellTargetID:
		:param isOptimize: 是否使用优化方案
		:return:
		"""
		skill = self.getSkill( skillID )
		targetEntity = KBEngine.entities[targetID]
		castRangeMax = float( skill.getRangeMax( self, targetEntity ) )
		distance = self.position.flatDistTo(targetEntity.position)
		if castRangeMax<distance:
			if not self.isMovingType(csdefine.MOVE_TYPE_CHASE):
				self.chaseEntity( targetEntity , castRangeMax*2/3 )
		else:
			Monster.Monster.behDoSpell( self, spellID, spellTargetID, isGroupSkill, isOptimize )

