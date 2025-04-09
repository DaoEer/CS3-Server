# -*- coding: utf-8 -*-

#engine
import KBEngine
#script
import Monster
import csdefine

class MonsterExtRevive( Monster.Monster ):
	"""
	自动复活类怪物
	"""
	def __init__( self ):
		Monster.Monster.__init__( self )

	def hasOtherRevive( self):
		_scriptID = self.getScript()._scriptID
		entityList = self.getCurrentSpace().getEntityRecord(_scriptID)
		flag = 0
		for _entity in entityList:
			monster = KBEngine.entities.get( _entity, None )
			if monster and monster.getState() != csdefine.ENTITY_STATE_DEAD:
				flag = 1
				break
				
		if flag:
			self.onRevevie()
		else:
			self.delayDestroy(1)

	def onRevevie(self):
		"""
		怪物复活
		"""
		self.changeState(csdefine.ENTITY_STATE_PEAD)
		self.monsterAIIsRunning = False
		self.monsterAIQuitPeadDelayTime = 0.0       #退出未决状态的延迟时间
		self.monsterAIQuitPeadTimeID = 0 			
		self.monsterAIChangePeadToState = csdefine.ENTITY_STATE_FREE   #退出未决状态默认切换到自由状态
		
		self.updateBornHPMP()
