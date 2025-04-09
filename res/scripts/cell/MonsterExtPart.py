# -*- coding: utf-8 -*-


#python
#engine
import KBEngine
#script
import KBEDebug
import Monster
import csdefine
import Const

class MonsterExtPart( Monster.Monster ):
	"""
	联合怪物：副怪
	"""
	def __init__( self ):
		Monster.Monster.__init__( self )

	def setOwner(self, ownerID):
		"""
		设置拥有者
		"""
		self.ownerID = ownerID

	def getOwnerEntity(self):
		"""
		获得拥有者
		"""
		owner = KBEngine.entities.get( self.ownerID,None )
		if owner and  self.spaceID == owner.spaceID: #不在一个地图，默认为找不到
			return owner
		return None

	def receiveDamage( self, casterID, skillID, damageType, damage, isCritical, isParry, deadEffect, actForbid ):
		"""
		接受伤害
		"""
		Monster.Monster.receiveDamage( self, casterID, skillID, damageType, damage, isCritical, isParry, deadEffect, actForbid )
		owner = self.getOwnerEntity()
		if owner:
			owner.receiveDamage( casterID, skillID, damageType, damage, isCritical, isParry, deadEffect, actForbid )

	def hasParent(self):
		return False