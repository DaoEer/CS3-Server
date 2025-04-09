# -*- coding: utf-8 -*-

"""
cell/base部份的ItemTypeImpl实现模块.
"""
import KBEDebug
import json

class BattlefieldMember( object ):
	"""
	对战 成员数据
	"""
	def __init__( self, roleID = 0,roleName = "", roleDBID =0,roleMB = None,integral = 0,money = 0, kill = 0, beKill = 0 ):
		self.roleID = roleID
		self.roleName = roleName
		self.roleMB = roleMB
		self.roleDBID = roleDBID
		self.integral = integral
		self.money = money
		self.kill = 0
		self.beKill = 0
		self.killNum = 0  #连续击杀
		self.beKillNum = 0#连续被击杀次数
	
	def initData( self, dict ):
		self.roleID = dict[ "roleID" ]
		self.roleMB = dict[ "roleMB" ]
		self.roleDBID = dict["roleDBID"]
		self.money = dict["money"]
		self.integral = dict[ "integral" ]
		self.kill = dict["kill"]
		self.beKill = dict["beKill"]
		self.roleName = dict["roleName"]

	def addMoney( self, money ):
		self.money += money
	
	def addIntegral( self, integral ):
		self.integral += integral
	
	def decIntegral( self, integral ):
		if self.integral > 0:
			self.integral -= integral

	def onKill( self ):
		self.kill += 1
		self.killNum += 1
		self.beKillNum = 0

	def onDie( self ):
		self.beKill += 1
		self.beKillNum += 1
		self.killNum = 0

	def getKillNum( self ):
		return self.killNum

	def getBeKillNum( self ):
		return self.beKillNum
	
	def getDictFromObj( self, obj ):
		dict = {
			"roleID" 	: obj.roleID,
			"roleMB"	: obj.roleMB,
			"integral" 	: obj.integral,
			"money"		: obj.money,
			"kill"		: obj.kill,
			"beKill"	: obj.beKill,
			"roleDBID"  : obj.roleDBID,
			"roleName"  : obj.roleName,
		}
		return dict
	
	def createObjFromDict( self, dict ):
		obj = self.__class__()
		obj.initData( dict )
		return obj
		
	def isSameType( self, obj ):
		return isinstance( obj, BattlefieldMember )

g_battlefieldMemberInf = BattlefieldMember()
