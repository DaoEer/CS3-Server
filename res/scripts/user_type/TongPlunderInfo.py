# -*- coding: utf-8 -*-

import KBEDebug
import csdefine
from WarMemberInfo import WarMemberInfo

class TongPlunderShopData( dict ):
	"""
	帮会掠夺战 商店数据
	"""
	def __init__( self ):
		self.id = ""
		self.itemID = 0
		self.amount = 0
		
	def initData(self, dict):
		self.id = dict["id"]
		self.itemID = dict["itemID"]
		self.amount = dict["amount"]
		
	def getDictFromObj(self, obj):
		data = {}
		data["id"] = obj.id
		data["itemID"] = obj.itemID
		data["amount"] = obj.amount
		return data
		
	def createObjFromDict(self, dict):
		obj = TongPlunderShopData()
		obj.initData(dict)
		return obj
		
	def isSameType(self, obj):
		return isinstance(obj, TongPlunderShopData)
		
class TongPlunderMgr( dict ):
	"""
	帮会掠夺战 数据管理
	"""
	def __init__( self ):
		self.isSignUpActive = False
		self.belongSide = -1
		self.members = [] #玩家dbid
		self.lockMoney = 0 #锁定帮会资金
		self.victory = False
		self.shopData = []
		self.isLockTongShop = False
		self.shopDataSell = False
		self.sellEndTime = 0

	def initData(self, dict):
		self.isSignUpActive = bool(dict["isSignUpActive"])
		self.belongSide = dict["belongSide"]
		self.members = list(dict["members"])
		self.lockMoney = int(dict["lockMoney"])
		self.victory = bool(dict["victory"])
		self.isLockTongShop = bool(dict["isLockTongShop"])
		self.shopDataSell = bool(dict["shopDataSell"])
		self.sellEndTime = int(dict["sellEndTime"])
		self.shopData = []
		for data in dict["shopData"]:
			tempShopData = TongPlunderShopData()
			tempData = {"id": data.id, "itemID": data.itemID, "amount": data.amount}
			tempShopData.initData(tempData)
			self.shopData.append(tempShopData)

	def resetSignUpData(self):
		self.isSignUpActive = False
		self.belongSide = -1
		self.lockMoney = 0
		self.members.clear()
		
	def resetResultData(self):
		self.victory = False
		self.shopData.clear()
		self.shopDataSell = False
		self.isLockTongShop = False
		self.sellEndTime = 0

	def resetData(self):
		self.resetSignUpData()
		self.resetResultData()

	def getDictFromObj(self, obj):
		data = {}
		data["isSignUpActive"] = bool(obj.isSignUpActive)
		data["belongSide"] = obj.belongSide
		data["members"] = obj.members
		data["lockMoney"] = obj.lockMoney
		data["victory"] = bool(obj.victory)
		data["isLockTongShop"] = bool(obj.isLockTongShop)
		data["shopDataSell"] = bool(obj.shopDataSell)
		data["sellEndTime"] = obj.sellEndTime
		data["shopData"] = []
		for d in obj.shopData:
			tempShopData = TongPlunderShopData()
			tempData = {"id": d.id, "itemID": d.itemID, "amount": d.amount}
			tempShopData.initData(tempData)
			data["shopData"].append(tempShopData)
		return data
	
	def createObjFromDict(self, dict):
		obj = TongPlunderMgr()
		obj.initData(dict)
		return obj

	def isSameType( self, obj ):
		return isinstance(obj, TongPlunderMgr)

	def addMember(self, member):
		if member not in self.members:
			self.members.append(member)

	def removeMember(self, member):
		if member in self.members:
			self.members.remove(member)

	def changeMember(self, oldMember, newMember):
		if oldMember in self.members:
			self.members.remove(oldMember)
			self.members.append(newMember)

	def onSignUpSuccess(self, belongSide, lockMoney):
		self.isSignUpActive = True
		self.members = []
		self.belongSide = belongSide
		self.lockMoney = lockMoney

	def checkShopData(self, id, itemID, amount):
		"""
		"""
		for data in self.shopData:
			if data.id == id and data.itemID == itemID:
				return data.amount >= amount
		return False

	def tongPlunderShopSell(self, tongEntity, id, itemID, amount):
		for data in self.shopData:
			if data.id == id and data.itemID == itemID:
				data.amount -= amount
				if data.amount < 0:
					data.amount = 0
				tongEntity.onTongPlunderShopDataChange(id, itemID, amount)
				break

	def hasSignUpActive(self):
		return self.isSignUpActive

	def getBelongSide(self):
		return self.belongSide

	def getMembers(self):
		return self.members
		
	def getLockMoney(self):
		return self.lockMoney
		
	def setLockTongShop(self, isLock):
		self.isLockTongShop = isLock
		
	def hasLockedTongShop(self):
		return self.isLockTongShop
		
	def setShopDataSell(self, startSell):
		self.shopDataSell = startSell
		
	def tongShopStartSell(self):
		return self.shopDataSell

	def setSellEndTime(self, endTime):
		self.sellEndTime = endTime
		
	def getSellEndTime(self):
		return self.sellEndTime

	def onActiveVictory(self, shopData):		
		self.shopData.clear()
		for data in shopData:
			tempShopData = TongPlunderShopData()
			tempShopData.initData(data)
			self.shopData.append(tempShopData)
		self.victory = True

	def onActiveFailed(self):
		#self.resetResultData()
		#self.resetSignUpData()
		self.lockMoney = 0 #先将绑定金钱值设置为0，否则扣除帮会金钱时会出错

	def getShopData(self):
		return self.shopData

	def isVictory(self):
		return self.victory

class TongPlunderMemberInfoMgr( dict ):
	"""
	掠夺战 成员数据管理器
	"""
	def __init__( self ):
		self.attackName = ""
		self.protectName = ""

	def setBothName(self, attackName, protectName):
		self.attackName = attackName
		self.protectName = protectName
	
	def initData( self, dict ):
		self.attackName = dict["attackName"]
		self.protectName = dict["protectName"]
		for m  in dict["members"]:
			self[m.roleDBID] = m

	def addMember(self, id, mailBox, name, belongSide):
		"""
		"""
		#只有玩家
		if id in self and mailBox != None and mailBox.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
			member = self[id]
			del self[id]
			srcMemberID = member.roleID
			member.roleID = mailBox.id
			member.roleMB = mailBox
			self[id] = member
			return
		
		if mailBox == None:
			m = WarMemberInfo(id, mailBox, id, name, belongSide)
		else:
			m = WarMemberInfo(mailBox.id, mailBox, id, name, belongSide)

		self[id] = m

	def addMemberKillEnemyNum( self, id):
		"""
		增加成员击杀数
		"""
		if id in self:
			self[id].addMemberKillEnemyNum()

	def addMemberDeadNum(self, id):
		"""
		增加成员死亡数
		"""
		if id in self:
			self[id].addMemberDeadNum()

	def addMemberKillSoldierNum(self, id):
		"""
		增加成员击杀士兵数
		"""
		if id in self:
			self[id].addMemberKillSoldierNum()

	def addMemberSoldierDeadNum(self, id):
		"""
		增加成员的士兵死亡数
		"""
		if id in self:
			self[id].addMemberSoldierDeadNum()
			
	def onSoldierDead(self, belongSide):
		"""
		士兵死亡
		"""
		for m in self.values():
			if m.roleMB:
				if m.roleMB.getBelongSide() != belongSide and m.roleMB.getClient():
					m.roleMB.client.CLIENT_TongPlunderSoldierDead(1)
				elif m.roleMB.getClient():
					m.roleMB.client.CLIENT_TongPlunderSoldierDead(2)
					
	def getIDByEntityID(self, entityID):
		"""
		通过entityID 获得ID
		"""
		for m in self.values():
			if m.roleID == entityID:
				return m.roleDBID
		return None

	def getMembers(self):
		"""
		获得所有成员
		"""
		return list(self.values())

	def getDictFromObj(self, obj):
		tempDict = {}
		tempDict["attackName"] = obj.attackName
		tempDict["protectName"] = obj.protectName

		tempDict[ "members" ] = []
		for mObj in obj.values():
			tempDict["members"].append(mObj)
			
		return tempDict

	def getClientData(self, obj):
		"""
		"""
		tempDict = {}
		tempDict["attackName"] = obj.attackName
		tempDict["protectName"] = obj.protectName

		tempDict[ "members" ] = []
		for mObj in obj.values():
			memberDict = {}
			memberDict["id"] = mObj.roleID
			memberDict["roleName"] = mObj.roleName
			memberDict["belongSide"] = mObj.belongSide
			memberDict["killEnemy"] = mObj.killEnemy
			memberDict["dead"] = mObj.dead
			memberDict["assists"] = mObj.assists
			memberDict["killSoldier"] = mObj.killSoldier
			memberDict["totalGetExploit"] = mObj.totalGetExploit
			memberDict["ownerSoldierDeadNum"] = mObj.ownerSoldierDeadNum			

			tempDict["members"].append(memberDict)
			
		return tempDict
	
	def createObjFromDict(self, dict):
		obj = TongPlunderMemberInfoMgr()
		obj.initData(dict)
		return obj
		
	def isSameType(self, obj):
		return isinstance(obj, TongPlunderMemberInfoMgr)

g_tongPlunderShopDataInst = TongPlunderShopData()
g_tongPlunderInst = TongPlunderMgr()
g_plunderMemberInfoMgr = TongPlunderMemberInfoMgr()
