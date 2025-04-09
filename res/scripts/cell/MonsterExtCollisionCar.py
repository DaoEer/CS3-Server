# -*- coding: utf-8 -*-


#python
#engine
import KBEngine
#script
import MonsterExtAttackCityLadder
import KBEDebug
import csdefine

class MonsterExtCollisionCar( MonsterExtAttackCityLadder.MonsterExtAttackCityLadder ):
	"""
	撞车 
	"""
	def __init__( self ):
		MonsterExtAttackCityLadder.MonsterExtAttackCityLadder.__init__( self )

	def setSelfEntityFlagExt(self):
		"""
		virtual method
		"""
		self.setEntityFlagExt(csdefine.ENTITY_FLAG_EXT_MONSTER_EXT_COLLISION_CAR)

	def onMoveOver( self, controllerID, userData ):
		"""
		virtual method
		移动结束，但似乎不管移动是否成功，都调用此函数
		@param controllerID		:	移动控制器ID
		@type  controllerID     :	int
		"""
		self.addBuff( self, self.getScript().endAddBuffID )
		self.useSkillToEntity( self.getScript().skillID, self.id )
		try:
			space = self.getCurrentSpace()
			space.removeOpterationMachine(self.id)
		except:
			KBEDebug.INFO_MSG("This use in SpaceCopyAtackCityWar!")

	