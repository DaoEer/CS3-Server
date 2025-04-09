# -*- coding- : utf-8 -*-
import csdefine
import ItemTypeEnum

class DOwnerBase( object ):
	_TYPES = {}
	def __init__( self, attacker, monsterEntity ):
		self._type = 0
		self.ownnerID = 0
		self.ownnerDBID = 0
		self.allocation = csdefine.TEAM_PICKUP_TYPE_FREEDOM	#分配类型
		self.allocationQuality = ItemTypeEnum.QUALITY_WHITE	#分配品质

	@classmethod
	def registerOjbect( SELF, type, classOjbect ):
		SELF._TYPES[ type ] = classOjbect

	@classmethod
	def getObject( SELF, type ):
		return SELF._TYPES.get( type, None )

	@classmethod
	def getAllTypes( SELF ):
		return SELF._TYPES.keys()

	@staticmethod
	def isUseOwnerType( monsterEntity, firstAttacker ):
		"""
		是否使用此目标作为掉落目标
		"""
		return True

	def getType( self ):
		return self._type

	def getOwnerID( self ):
		return self.ownnerID

	def getOwnerIDs( self, monsterEntity ):
		"""
		怪物所有者列表
		"""
		return {}
		
	def getOwnerType( self ):
		"""
		"""
		return self._type
		
	def getAllocation( self ):
		"""
		"""
		return (self.allocation, self.allocationQuality)
