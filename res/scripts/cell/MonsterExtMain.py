# -*- coding: utf-8 -*-


#python
#engine
import KBEngine
#script
import KBEDebug
import Monster
import csdefine
import Const

class MonsterExtMain( Monster.Monster ):
	"""
	联合怪物：主怪
	"""
	def __init__( self ):
		Monster.Monster.__init__( self )
		self.getScript().createMonterPart( self )
		

	def onEnterDead( self ):
		"""
		virtual method
		进入死亡状态
		"""
		Monster.Monster.onEnterDead( self )
		for i in self.partMonsterIDs:
			entity = KBEngine.entities.get( i, None )
			if entity:
				entity.setHP(0)