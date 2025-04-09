# -*- coding: utf-8 -*-


#python
#engine
import KBEngine
#script
import Monster
import csdefine

SHARE_HP_MAX_RANGE = 100 # 共享血量最大范围

class MonsterExtShareHP( Monster.Monster ):
	"""
	血量共享Monster
	"""
	def __init__( self ):
		Monster.Monster.__init__( self )

	def setHP( self, value ):
		"""
		设置HP
		"""
		Monster.Monster.setHP( self, value )
		for e in self.entitiesInRangeExt( SHARE_HP_MAX_RANGE, "MonsterExtShareHP" ):
			if e.HP_Max != self.HP_Max:
				# 最大血量一样的才共享血量
				continue
			difValue = e.HP - self.HP
			if difValue > 0:
				e.receiveDamageFromShareHP( difValue )
			elif difValue < 0:
				e.addHPFromShareHP( - difValue )

	def receiveDamageFromShareHP( self, damage ):
		"""
		接受共享血量的伤害。
		"""
		Monster.Monster.setHP( self, self.HP - damage )
		
		if self.state == csdefine.ENTITY_STATE_DEAD:
			return
		if self.HP == 0:
			self.setMP( 0 )

	def addHPFromShareHP( self, value ):
		"""
		<Define method>
		血量共享增加HP
		"""
		Monster.Monster.setHP( self, self.HP + value )