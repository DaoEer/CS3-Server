# -*- coding: utf-8 -*-

import KBEDebug
import csstatus

class SoldierSpecialSkillInfo( dict ):
	"""
	兵特殊技能数据
	"""
	def __init__( self,skillID = 0,  maxExp = 0, exp = 0 ):
		"""
		"""
		self.skillID = skillID
		self.exp = exp
		self.maxExp = maxExp

	def initData( self, dict ):
		"""
		"""
		self.skillID = dict["skillID"]
		self.exp = dict["exp"]
		self.maxExp = dict["maxExp"]

	def setCurExp( self, exp ):
		"""
		"""
		self.exp = exp

	def setMaxExp( self, maxExp ):
		"""
		"""
		self.maxExp = maxExp

	def setSkillID( self, skillID ):
		"""
		"""
		self.skillID = skillID

	def getCurExp( self ):
		"""
		获得当前的经验
		"""
		return self.exp

	def getMaxExp( self ):
		"""
		获得当前最大的经验
		"""
		return self.maxExp

	def getDictFromObj( self, obj ):
		dict = {
			"skillID" 	: obj.skillID,
			"exp"	: obj.exp,
			"maxExp"  : obj.maxExp
		}
		return dict

	def createObjFromDict( self, dict ):
		obj = self.__class__()
		obj.initData( dict )
		return obj

	def isSameType( self, obj ):
		return isinstance( obj, SoldierSpecialSkillInfo )


class BarracksSoldierInfo( object ):
	"""
	兵营兵数据
	"""
	def __init__( self, id = 0, scriptID = "", soldierType = 0, level = 0, maxExp =0, exp = 0, isInArmy = 0,skillIDDatas =[], isActive=1):
		self.id = id
		self.scriptID = scriptID
		self.soldierType = soldierType
		self.level = level
		self.exp = exp
		self.isInArmy = isInArmy
		self.maxExp = maxExp
		self.skillIDDatas = []
		for skillIDData in skillIDDatas:
			skillObj = SoldierSpecialSkillInfo(skillIDData[0],skillIDData[1])
			self.skillIDDatas.append(skillObj)
		self.isActive = isActive

	def initData( self, dict ):
		self.id = dict["id"]
		self.scriptID = dict["scriptID"]
		self.soldierType = dict["soldierType"]
		self.level = dict["level"]
		self.exp = dict["exp"]
		self.isInArmy = dict["isInArmy"]
		self.maxExp = dict["maxExp"]
		for skillIDDatas in dict["skillIDDatas"]:
			self.skillIDDatas.append( skillIDDatas )
		self.isActive = dict["isActive"]

	def getLevel( self ):
		"""
		"""
		return self.level

	def setLevel( self, level, role ):
		"""
		设置等级
		"""
		if self.level == level:
			return
		self.level = level
		if role.getClient():
			role.client.UpdateSoldierLevelData( self.scriptID, self.id,self.level )

	def getScriptID( self ):
		return self.scriptID

	def getSoldierType( self ):
		"""
		"""
		return self.soldierType

	def getMaxExp( self ):
		return self.maxExp

	def setMaxExp( self, maxExp ):
		self.maxExp = maxExp

	def getExp( self ):
		return self.exp

	def setExp( self, exp, role ): 
		"""
		设置经验
		"""
		self.exp = exp
		if role.getClient():
			role.client.UpdateSoldierExpData( self.scriptID, self.id, self.exp, self.maxExp )

	def setIsInArmy( self, isInArmy, role ):
		"""
		设置是否在部队
		"""
		self.isInArmy = isInArmy
		if role.getClient():
			role.client.UpdateSoldierIsInArmyData( self.scriptID, self.id,self.isInArmy )

	def setActive(self, isActive, role):
		"""
		"""
		self.isActive = isActive
		if role.getClient():
			role.client.UpdateSoldierIsActive(self.scriptID, self.id, self.isActive)

	def getDictFromObj( self, obj ):
		dict = {
			"id" 	: obj.id,
			"scriptID"	: obj.scriptID,
			"soldierType"  : obj.soldierType,
			"level" : obj.level,
			"exp": obj.exp,
			"isInArmy": obj.isInArmy,
			"maxExp":obj.maxExp,
			"skillIDDatas":obj.skillIDDatas,
			"isActive":obj.isActive
		}
		return dict
	
	def createObjFromDict( self, dict ):
		obj = self.__class__()
		obj.initData( dict )
		return obj
		
	def isSameType( self, obj ):
		return isinstance( obj, BarracksSoldierInfo )

class BarraceksSoldierInfoMgr( dict ):
	"""
	兵营兵管理器
	"""
	def __init__( self ):
		self.barracksSoldierType = 0
	
	def initData( self, dict ):
		self.barracksSoldierType = dict["barracksSoldierType"]
		for m  in dict[ "barracksSoldierDatas" ]:
			if m.scriptID not in self:
				self[m.scriptID] = {}

			self[ m.scriptID ][m.id] = m

	def initRoleBarracksDataToClient( self, role ):
		"""
		初始化 数据到客户端
		"""
		for barracksSoldierDatas in self.values():
			if role.getClient():
				role.client.InitRoleBarracksDatas( list(barracksSoldierDatas.values()) )

		return True

	def getSoldierID( self, scriptID ):
		"""
		"""
		newSoldierID = 0
		soldierIDs = list( self[scriptID].keys() )
		for i in range( 1,len( self[scriptID] ) + 1 ):
			if i not in soldierIDs:
				newSoldierID = i
				break
		if newSoldierID == 0:
			newSoldierID = len( self[scriptID] ) + 1
		return newSoldierID


	def addBarracksSoldier( self, soldierType,scriptID, maxExp,role,skillIDDatas, level = 1, name = "" ):
		"""
		增加兵
		"""
		if scriptID not in self:
			self[scriptID] = {}

		id = self.getSoldierID( scriptID )
		soldier = BarracksSoldierInfo( id, scriptID, soldierType, level,maxExp, 0,0,skillIDDatas)
		self[scriptID][soldier.id] = soldier
		#发送数据到客户端
		if role.getClient():
			role.client.AddRoleBarracksData(soldier)
		role.statusMessage(csstatus.BARRACKS_ADD_SUCCESS, str(level) + "|" + name)

	def removeBarracksSoldiersByScriptID( self, scriptID, id ):
		"""
		移除某个兵的数据
		"""
		if scriptID not in self:
			return
		if id in self[scriptID]:
			del self[scriptID][id]
		

	def getBarracksSoldiersByScriptID( self, scriptID):
		"""
		获得某种ScriptID兵
		"""
		if scriptID in self:
			return list(self[scriptID].values())
		return []

	def getBarracksSoldiersScriptIDsBySoldierType( self ):
		"""
		"""
		return list(self.keys())

	def getBarracksSoldiersBySoldierType( self ):
		"""
		"""
		tempList = []
		for scriptID, soldierDict in self.items():
			tempList.append( list(soldierDict.values()) )
		return tempList

	def getDictFromObj( self, obj ):
		tempDict = {}
		tempDict["barracksSoldierType"] = obj.barracksSoldierType
		tempDict[ "barracksSoldierDatas" ] = []
		
		for scriptID,soldierDict in obj.items():
			tempDict[ "barracksSoldierDatas" ].extend( list(soldierDict.values()) )

		return tempDict
	
	def createObjFromDict( self, dict ):
		obj = BarraceksSoldierInfoMgr()
		obj.initData( dict )
		return obj
		
	def isSameType( self, obj ):
		return isinstance( obj, BarraceksSoldierInfoMgr )
		
class RoleBarraceksMgr( dict ):
	"""
	玩家兵营管理器
	"""
	def __init__( self ):
		pass
	
	def initData( self, dict ):
		for m  in dict[ "datas" ]:
			self[ m.barracksSoldierType ] = m

	def addBarracksSoldier( self, soldierType, scriptID, maxExp,role, skillIDDatas, level = 1, name = "" ):
		"""
		增加兵
		"""
		if soldierType not in self:
			m = BarraceksSoldierInfoMgr()
			tempDict = {}
			tempDict["barracksSoldierType"] = soldierType
			tempDict["barracksSoldierDatas"] = []
			m.initData(tempDict)
			self[soldierType] = m
		self[soldierType].addBarracksSoldier( soldierType,scriptID, maxExp,role,skillIDDatas, level, name)

	def initRoleBarracksDataToClient( self, soldierType, role ):
		"""
		初始化 数据到客户端
		"""
		if soldierType in self:
			self[soldierType].initRoleBarracksDataToClient( role )
		return True

	def removeBarracksSoldiersByScriptID( self, soldierType, scriptID ,id ):
		"""
		移除某个兵的数据
		"""
		if soldierType in self:
			self[soldierType].removeBarracksSoldiersByScriptID( scriptID, id )

	def getBarracksSoldiersByScriptID( self, soldierType, scriptID ):
		"""
		获得某种ScriptID兵
		"""
		if soldierType in self:
			return self[soldierType].getBarracksSoldiersByScriptID( scriptID )
		return []

	def getBarracksSoldiersScriptIDsBySoldierType( self, soldierType ):
		"""
		获得某种类型兵的所有scriptID 
		"""
		if soldierType in self:
			return self[soldierType].getBarracksSoldiersScriptIDsBySoldierType()
		return []

	def getBarracksSoldiersBySoldierType( self, soldierType ):
		"""
		"""
		if soldierType in self:
			return self[soldierType].getBarracksSoldiersBySoldierType()
		return []

	def getDictFromObj( self, obj ):
		tempDict = {}
		tempDict[ "datas" ] = []
		
		for mObj in obj.values():
			tempDict[ "datas" ].append( mObj )
			
		return tempDict
	
	def createObjFromDict( self, dict ):
		obj = RoleBarraceksMgr()
		obj.initData( dict )
		return obj
		
	def isSameType( self, obj ):
		return isinstance( obj, RoleBarraceksMgr )

g_SoldierSpecialSkillInfo = SoldierSpecialSkillInfo()
g_BarraceksSoldierInfoMgr = BarraceksSoldierInfoMgr()
g_BarracksSoldierInfo = BarracksSoldierInfo()
g_RoleBarracksMgr = RoleBarraceksMgr()