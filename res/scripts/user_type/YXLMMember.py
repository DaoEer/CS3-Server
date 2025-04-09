# -*- coding: utf-8 -*-

"""
cell/base部份的ItemTypeImpl实现模块.
"""
import KBEDebug
import json
import csdefine

class YXLMMember( object ):
	"""
	英雄联盟 成员数据
	"""
	def __init__( self, roleID = 0,roleName = "", roleDBID =0,roleMB = None ):
		self.roleID = roleID
		self.roleName = roleName
		self.roleMB = roleMB
		self.roleDBID = roleDBID
		self.kill = 0
		self.beKill = 0
		self.killNum = 0  #连续击杀
		self.beKillNum = 0#连续被击杀次数
		self.nextYXLMToReviveTime = 0 #下次复活时间
		self.reviveYXLMNumber = 0 #复活次数
		self.totalAddExpValue = 0 #击杀总获得经验值
		self.roleJade = 0 #玩家的魂玉 主要掉线存下
	
	def initData( self, dict ):
		self.roleID = dict[ "roleID" ]
		self.roleMB = dict[ "roleMB" ]
		self.roleDBID = dict["roleDBID"]
		self.kill = dict["kill"]
		self.beKill = dict["beKill"]
		self.roleName = dict["roleName"]
		self.nextYXLMToReviveTime = dict["nextYXLMToReviveTime"]
		self.reviveYXLMNumber = dict[ "reviveYXLMNumber" ]
		self.totalAddExpValue = dict["totalAddExpValue"]
		self.roleJade = dict["roleJade"]

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

	def addTotalAddExpValue( self, value ):
		"""
		"""
		self.totalAddExpValue += value
		if self.roleMB and self.roleMB.getClient():
			self.roleMB.addExp( value, csdefine.EXP_ADD_REASON_YXLM_KILL_REWARD )

	def getTotalAddExpValue( self ):
		return self.totalAddExpValue
	
	def getDictFromObj( self, obj ):
		dict = {
			"roleID" 	: obj.roleID,
			"roleMB"	: obj.roleMB,
			"nextYXLMToReviveTime" 	: obj.nextYXLMToReviveTime,
			"reviveYXLMNumber"		: obj.reviveYXLMNumber,
			"kill"		: obj.kill,
			"beKill"	: obj.beKill,
			"roleDBID"  : obj.roleDBID,
			"roleName"  : obj.roleName,
			"totalAddExpValue":obj.totalAddExpValue,
			"roleJade" : obj.roleJade
		}
		return dict
	
	def createObjFromDict( self, dict ):
		obj = self.__class__()
		obj.initData( dict )
		return obj
		
	def isSameType( self, obj ):
		return isinstance( obj, YXLMMember )

g_YXLMMemberInf = YXLMMember()
