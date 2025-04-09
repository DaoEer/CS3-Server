# -*- coding: utf-8 -*-

import KBEDebug

class WarMemberInfo( object ):
	"""
	成员数据
	"""
	def __init__( self, roleID = 0, roleMB = None, roleDBID = 0, roleName = "", belongSide = 0 ):
		self.roleID = roleID
		self.roleMB = roleMB
		self.roleDBID = roleDBID
		self.roleName = roleName
		self.belongSide = belongSide
		self.killEnemy = 0
		self.dead = 0
		self.assists = 0
		self.killSoldier = 0
		self.totalGetExploit = 0
		self.ownerSoldierDeadNum = 0

	def initData( self, dict ):
		self.roleID = dict[ "roleID" ]
		self.roleMB = dict[ "roleMB" ]
		self.roleDBID = dict["roleDBID"]
		self.roleName = dict["roleName"]
		self.belongSide = dict["belongSide"]
		self.killEnemy = dict["killEnemy"]
		self.dead = dict["dead"]
		self.assists = dict["assists"]
		self.killSoldier = dict["killSoldier"]
		self.totalGetExploit = dict["totalGetExploit"]
		self.ownerSoldierDeadNum = dict["ownerSoldierDeadNum"]

	def addMemberKillEnemyNum( self ):
		"""
		"""
		self.killEnemy += 1

	def addMemberDeadNum( self ):
		"""
		"""
		self.dead += 1

	def addMemberAssistsNum( self ):
		"""
		"""
		self.assists += 1

	def addMemberKillSoldierNum( self ):
		"""
		"""
		self.killSoldier += 1

	def addMemberSoldierDeadNum( self ):
		"""
		"""
		self.ownerSoldierDeadNum += 1

	def getDictFromObj( self, obj ):
		dict = {
			"roleID" 	: obj.roleID,
			"roleMB"	: obj.roleMB,
			"roleDBID"  : obj.roleDBID,
			"roleName" 	: obj.roleName,
			"belongSide": obj.belongSide,
			"killEnemy" : obj.killEnemy,
			"dead" 		: obj.dead,
			"assists" 	: obj.assists,
			"killSoldier":obj.killSoldier,
			"totalGetExploit":obj.totalGetExploit,
			"ownerSoldierDeadNum":obj.ownerSoldierDeadNum,
		}
		return dict
	
	def createObjFromDict( self, dict ):
		obj = self.__class__()
		obj.initData( dict )
		return obj
		
	def isSameType( self, obj ):
		return isinstance( obj, WarMemberInfo )

g_WarMemberInfo = WarMemberInfo()
