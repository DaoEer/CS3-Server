# -*- coding- : utf-8 -*-

"""
掉落目标，怪物死亡后奖励目标的分配处理
"""

from ConfigObject.Drop.DropBase.DropOwnerBase import DOwnerBase

import csdefine
import KBEngine
import Define

class DOwnerPerson( DOwnerBase ):
	"""
	个人
	"""
	def __init__( self, attacker, monsterEntity ):
		DOwnerBase.__init__( self, attacker, monsterEntity )
		self._type = csdefine.DROP_OWNER_TYPE_PERSON
		self.ownnerID = attacker.id
		self.ownnerDBID = attacker.playerDBID

	@staticmethod
	def isUseOwnerType( monsterEntity, firstAttacker ):
		"""
		是否使用此目标作为掉落目标
		"""
		if firstAttacker and not firstAttacker.isInTeam():
			return True
		else:
			return False
	
	def getOwnerIDs( self, monsterEntity ):
		"""
		目标entity
		"""
		dct = {}
		role = KBEngine.entities.get( self.ownnerID, None )
		if role:
			dct[self.ownnerID] = self.ownnerDBID
		return dct

class DOwnerTeam( DOwnerBase ):
	"""
	队伍
	"""
	def __init__( self, attacker, monsterEntity ):
		DOwnerBase.__init__( self, attacker, monsterEntity )
		self._type = csdefine.DROP_OWNER_TYPE_TEAM
		self.ownnerID = attacker.teamMailbox.id
		self.allocation = attacker.getOwnerAllocation()
		self.allocationQuality = attacker.getOwnerQuality()
		
		self.teamCaptainDBID = 0
		captain = KBEngine.entities.get( attacker.captainID, None )
		if captain:self.teamCaptainDBID = captain.playerDBID
		
	@staticmethod
	def isUseOwnerType( monsterEntity, firstAttacker ):
		"""
		是否使用此目标作为掉落目标
		"""
		if firstAttacker.isInTeam():
			return True
		else:
			return False

	def getOwnerIDs( self, monsterEntity ):
		"""
		目标entity
		"""
		dct = {}
		roleList = monsterEntity.entitiesInRangeExt( Define.TEAM_ITEM_PICKUP_RANGE, "Role" )
		for role in roleList:
			if role.isInTeam() and role.teamMailbox.id == self.ownnerID:
				dct[role.id] = role.playerDBID
		return dct

class DOwnerTong( DOwnerBase ):
	"""
	帮会
	"""
	def __init__( self, attacker, monsterEntity ):
		DOwnerBase.__init__( self, attacker, monsterEntity )
		self._type = csdefine.DROP_OWNER_TYPE_TEAM
		self.ownnerID = attacker.id

	@staticmethod
	def isUseOwnerType( monsterEntity, firstAttacker ):
		"""
		是否使用此目标作为掉落目标
		"""
		return False
	
	def getOwnerIDs( self, monsterEntity ):
		"""
		目标entity
		"""
		return {}

DOwnerBase.registerOjbect( csdefine.DROP_OWNER_TYPE_PERSON, DOwnerPerson )
DOwnerBase.registerOjbect( csdefine.DROP_OWNER_TYPE_TEAM, DOwnerTeam )
DOwnerBase.registerOjbect( csdefine.DROP_OWNER_TYPE_TONG, DOwnerPerson )

