# -*- coding: utf-8 -*-


#python
#engine
import KBEngine
#script
import Monster
import KBEDebug

class MonsterExtFirstTongStarcraftBoss( Monster.Monster ):
	"""
	CST-7904 帮会争霸第一场 Boss怪
	"""
	def __init__( self ):
		Monster.Monster.__init__( self )
		
	def removeEnemyDmgList( self, entityID ):
		"""
		将这个敌人从伤害列表中删除
		"""
		pass

	def onEnterDead( self ):
		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			spaceEntity.addBossDamageData( self.id, self.damageList )
		Monster.Monster.onEnterDead( self )


	def onFirstBruise( self, caster, damage, skillID ):
		"""
		第一次受击事件

		@param 		 caster: 对你产生伤害的人
		@type  		 caster: Entity
		@param       damage: 伤害
		@type        damage: int
		@param      skillID: 法术ID
		@type       skillID: INT
		@return:             无
		"""
		Monster.Monster.onFirstBruise( self, caster, damage, skillID )
		if self.firstDamageEntityID == 0:
			self.firstDamageEntityID = caster.id

	def getFirstDamageEntityID( self ):
		"""
		获得第一个伤害Boss 的ID
		"""
		return self.firstDamageEntityID