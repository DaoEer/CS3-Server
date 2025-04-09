# -*- coding: utf-8 -*-

"""
cell/base部份的ItemTypeImpl实现模块.
"""
import KBEDebug
import json
import csdefine
import KBEngine

class LBCPVPMember( object ):
	"""
	练兵场PVP 成员数据
	"""
	def __init__( self, roleID = 0,roleName = "", roleDBID =0,roleMB = None ):
		self.belongSide = csdefine.BELONG_SIDE_ATTACK
		self.roleID = roleID
		self.roleMB = roleMB
		self.roleName = roleName
		self.roleDBID = roleDBID
		self.playerKill = 0 #玩家击杀数
		self.beKill = 0 #被击杀数
		self.assists = 0 #助攻数
		self.soldierKill = 0 #小兵击杀数
		self.exploits = 0 #获得的军功
		self.roleJade = 0 #玩家的魂玉 主要掉线存下
	
	def initData( self, dict ):
		self.belongSide = dict["belongSide"]
		self.roleID = dict[ "roleID" ]
		self.roleMB = dict["roleMB"]
		self.roleName = dict["roleName"]
		self.roleDBID = dict["roleDBID"]
		self.playerKill = dict["playerKill"]
		self.beKill = dict["beKill"]
		self.assists = dict["assists"]
		self.soldierKill = dict["soldierKill"]
		self.exploits = dict["exploits"]
		self.roleJade = dict["roleJade"]

	
	def getDictFromObj( self, obj ):
		dict = {
			"belongSide": obj.belongSide,
			"roleID" 	: obj.roleID,
			"roleMB" 	: obj.roleMB,
			"roleName"  : obj.roleName,
			"roleDBID"  : obj.roleDBID,
			"playerKill"		: obj.playerKill,
			"beKill"	: obj.beKill,
			"assists"	: obj.assists,
			"soldierKill" : obj.soldierKill,
			"exploits"  : obj.exploits,
			"roleJade"  : obj.roleJade
		}
		return dict
	
	def createObjFromDict( self, dict ):
		obj = self.__class__()
		obj.initData( dict )
		return obj
		
	def isSameType( self, obj ):
		return isinstance( obj, LBCPVPMember )


class LBCPVPMemberMgr(dict):
	"""
	练兵场PVP 数据
	"""
	def __init__(self):
		pass

	def onEnterRole(self, player, belongSide):
		"""
		"""
		key = player.playerDBID
		#玩家第一次进入
		if key not in self:
			params={}
			params["belongSide"] = belongSide
			params["roleID"] = player.id 
			params["roleMB"] = player
			params["roleName"] = player.getName()
			params["roleDBID"] = key
			params["playerKill"] = 0
			params["beKill"] = 0
			params["assists"] = 0
			params["soldierKill"] = 0
			params["exploits"] = 0
			params["roleJade"] = 0
			obj = g_LBCPVPMember.createObjFromDict(params)
			self[key] = obj
		else:
			#重新进入 更新玩家部分数据
			obj = self[key]
			obj.roleID = player.id
			obj.roleMB = player
			obj.roleName = player.getName()


	def createObjFromDict( self, dict ):
		obj = LBCPVPMemberMgr()
		for member in dict["members"]:
			obj[member.roleDBID] = member
		return obj


	def getDictFromObj( self, obj ):
		dict = {"members":[]}
		for value in self.values():
			dict["members"].append(value)
		return dict

	def isSameType( self, obj ):
		return isinstance( obj, LBCPVPMemberMgr )
		
	def killPlayer(self, roleDBID):
		if roleDBID in self:
			self[roleDBID].playerKill+=1

	def killSoldier(self, roleDBID):
		if roleDBID in self:
			self[roleDBID].soldierKill+=1

	def beKill(self, roleDBID):
		if roleDBID in self:
			self[roleDBID].beKill+=1

	def assist(self, roleDBID):
		if roleDBID in self:
			self[roleDBID].assists+=1

	def addExploit(self, roleDBID, value):
		if roleDBID in self:
			self[roleDBID].exploits+=value

	def addJade(self, roleDBID, value):
		if roleDBID in self:
			self[roleDBID].roleJade+=value

#------------------updateDataToClient------------------------------

	def updateSingleDataforLBCPVP(self, dbid, name, newValue):
		"""
		更新playerDBID等于dbid的一个字段名为name数据给客户端 更新值为newValue
		"""
		data = self.get(dbid, None)
		if not data:
			return

		for v in self.values():
			rid = v["roleID"]
			r = KBEngine.entities.get(rid, None)
			if r:
				r.client.UpdateSingleDataForLBCPVP(dbid, name, newValue)



g_LBCPVPMember = LBCPVPMember()
g_LBCPVPMemberMgr = LBCPVPMemberMgr()
