# -*- coding- : utf-8 -*-
import csdefine

class CMonsterAIInterface( object ):
	def __init__( self ):
		object.__init__( self )
		self.cMonsterAIState = csdefine.CMONSTER_AI_STATE_NORMAL
		
	def changeCMonsterAIState(self, newState):
		"""
		"""
		self.cMonsterAIState = newState

	def CAI_AddEnemy( self, exposed, enemyID ):
		"""
		exposed method
		添加敌对目标
		"""
		if not  self.IsValidMsg( exposed, enemyID ):
			return 
			
		self.addEnemy( enemyID )

	def CAI_RemoveEnemy(self, exposed, enemyID):
		"""
		exposed method
		移除敌对目标
		"""
		if not self.IsValidMsg(exposed, enemyID):
			return

		self.removeEnemy(enemyID)





	
	