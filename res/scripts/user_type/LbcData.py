

import time

import csconst
import csdefine
import KBEDebug
import KST



class LbcItem():
	"""
	练兵场信息
	"""
	def __init__(self):
		self.index = 0
		self.level = 0
		self.line = 0
		self.lbcName = ''
		self.status = csconst.LBC_STATUS_NORMAL
		self.occupierDBID = 0
		self.occupierName = ''
		self.occupierProfession = csdefine.CLASS_UNKNOWN
		self.declarerDBID = 0
		self.declarerName = ''
		self.declarerProfession = csdefine.CLASS_UNKNOWN
		self.attackTime = 0

	@classmethod
	def getDictFromObj(self, obj):
		temp = {}
		temp['index'] = obj.index
		temp['level'] = obj.level
		temp['line'] = obj.line
		temp['lbcName'] = obj.lbcName
		temp['status'] = obj.status
		temp['occupierDBID'] = obj.occupierDBID
		temp['occupierName'] = obj.occupierName
		temp['occupierProfession'] = obj.occupierProfession
		temp['declarerDBID'] = obj.declarerDBID
		temp['declarerName'] = obj.declarerName
		temp['declarerProfession'] = obj.declarerProfession
		temp['attackTime'] = obj.attackTime
		return temp

	@classmethod
	def createObjFromDict(self, dict):
		obj = LbcItem()
		obj.index = dict['index']
		obj.level = dict['level']
		obj.line = dict['line']
		obj.lbcName = dict['lbcName']
		obj.status = dict['status']
		obj.occupierDBID = dict['occupierDBID']
		obj.occupierName = dict['occupierName']
		obj.occupierProfession = dict['occupierProfession']
		obj.declarerDBID = dict['declarerDBID']
		obj.declarerName = dict['declarerName']
		obj.declarerProfession = dict['declarerProfession']
		obj.attackTime = dict['attackTime']
		return obj

	def isSameType(self, obj):
		return isinstance(obj, LbcItem)

	def init(self, data):
		"""
		"""
		self.index = data['index']
		self.level = data['level']
		self.line = data['line']
		self.lbcName = data['lbcName']
		self.status = csconst.LBC_STATUS_NORMAL
		self.occupierDBID = 0
		self.occupierName = ''
		self.occupierProfession = csdefine.CLASS_UNKNOWN
		self.declarerDBID = 0
		self.declarerName = ''
		self.declarerProfession = csdefine.CLASS_UNKNOWN
		self.attackTime = 0

	def clearData(self):
		"""
		清除数据
		"""
		self.index = 0
		self.level = 0
		self.line = 0
		self.lbcName = ''
		self.status = csconst.LBC_STATUS_NORMAL
		self.occupierDBID = 0
		self.occupierName = ''
		self.occupierProfession = csdefine.CLASS_UNKNOWN
		self.declarerDBID = 0
		self.declarerName = ''
		self.declarerProfession = csdefine.CLASS_UNKNOWN
		self.attackTime = 0

	def occupy(self, occupierDBID, occupierName, occupierProfession):
		"""
		练兵场被占领
		"""
		self.status = csconst.LBC_STATUS_OCCUPIED
		self.occupierDBID = occupierDBID
		self.occupierName = occupierName
		self.occupierProfession = occupierProfession
		KST.g_baseAppEntity.globalBroadcastLbcStatus(self.line, self.index, self.status)

	def abandon(self):
		"""
		放弃练兵场
		"""
		self.occupierDBID = 0
		self.occupierName = ''
		self.occupierProfession = csdefine.CLASS_UNKNOWN
		self.status = csconst.LBC_STATUS_NORMAL
		KST.g_baseAppEntity.globalBroadcastLbcStatus(self.line, self.index, self.status)

	def declare(self, declarerDBID, declarerName, declarerProfession, attackTime):
		"""
		宣战
		"""
		self.status = csconst.LBC_STATUS_DELCARED
		self.declarerDBID = declarerDBID
		self.declarerName = declarerName
		self.declarerProfession = declarerProfession
		self.attackTime = attackTime
		KST.g_baseAppEntity.globalBroadcastLbcStatus(self.line, self.index, self.status)


	def cancelDeclare(self):
		"""
		取消宣战
		"""
		if self.occupierDBID>0:
			self.status = csconst.LBC_STATUS_OCCUPIED
		else:
			self.status = csconst.LBC_STATUS_NORMAL
		self.declarerDBID = 0
		self.declarerName = ''
		self.declarerProfession = csdefine.CLASS_UNKNOWN
		self.attackTime = 0
		KST.g_baseAppEntity.globalBroadcastLbcStatus(self.line, self.index, self.status)


	def attackerWin(self, occupierDBID, occupierName, occupierProfession, declarerDBID, declarerName, declarerProfession, status, attackTime):
		"""
		进攻方获胜更新数据
		"""
		self.occupierDBID = occupierDBID
		self.occupierName =  occupierName
		self.occupierProfession = occupierProfession
		self.declarerDBID = declarerDBID
		self.declarerName = declarerName
		self.declarerProfession = declarerProfession
		self.status = status
		self.attackTime = attackTime
		KST.g_baseAppEntity.globalBroadcastLbcStatus(self.line, self.index, self.status)

	def attackerLose(self):
		"""
		进攻方失败更新数据
		"""
		self.declarerDBID = 0
		self.declarerName = ''
		self.declarerProfession = csdefine.CLASS_UNKNOWN
		self.attackTime = 0
		if self.occupierDBID>0:
			self.status = csconst.LBC_STATUS_OCCUPIED
		else:
			self.status = csconst.LBC_STATUS_NORMAL
		KST.g_baseAppEntity.globalBroadcastLbcStatus(self.line, self.index, self.status)


	def giveUpAttack(self):
		"""
		"""
		#宣战方放弃争夺
		self.declarerDBID == 0
		self.declarerName == ''
		self.declarerProfession = csdefine.CLASS_UNKNOWN
		self.attackTime = 0
		self.status = csconst.LBC_STATUS_OCCUPIED
		KST.g_baseAppEntity.globalBroadcastLbcStatus(self.line, self.index, self.status)


	def getClientDeclareInfo(self):
		"""
		获取玩家客户端宣战信息
		"""
		clientDeclareInfo ={}
		clientDeclareInfo['level'] = self.level
		clientDeclareInfo['line'] = self.line
		clientDeclareInfo['lbcName'] = self.lbcName
		clientDeclareInfo['status'] = self.status
		clientDeclareInfo['occupierName'] = self.occupierName
		clientDeclareInfo['occupierProfession'] = self.occupierProfession
		clientDeclareInfo['declarerName'] = self.declarerName
		clientDeclareInfo['declarerProfession'] = self.declarerProfession
		clientDeclareInfo['attackTime'] = self.attackTime
		return clientDeclareInfo

	def updateStatus(self, status):
		self.status = status
		KST.g_baseAppEntity.globalBroadcastLbcStatus(self.line, self.index, self.status)

class LbcData(dict):
	"""
	所有分线下的数据
	"""
	@classmethod
	def getDictFromObj( self, obj ):
		dctList = {'datas':[]}
		for line in obj.keys():
			for dct in obj[line].values():
				dctList['datas'].append(dct)
		return dctList

	@classmethod
	def createObjFromDict( self, dict ):
		obj = LbcData()
		for item in dict['datas']:
			line = item.line
			index = item.index
			if not line in obj:
				obj[line] ={}
			obj[line][index] = item
		return obj

	def isSameType( self, obj ):
		return isinstance(obj, LbcData)

	def init(self, configData):
		"""
		"""
		#剔除配置表中没有的数据
		for line in list(self.keys()):
			if not line in configData.keys():
				self.pop(line)
			else:
				for index in list(self[line].keys()):
					if not index in configData[line]:
						self[line].pop(index)
		#加载新配置
		for line in configData:
			if not line in self:
				self[line] = {}
			for index in configData[line]:
				if not index in self[line].keys():
					obj = LbcItem()
					obj.init(configData[line][index])
					self[line][index] = obj


	def getItem(self, line, index):
		"""
		"""
		if line in self and index in self[line]:
			return	self[line][index]
		return None

	def getStatusList(self):
		"""
		获取练兵场状态信息
		"""
		lst = []
		for line in self:
			for item in self[line].values():
				dct = {}
				dct['index'] = item.index
				dct['line'] = item.line
				dct['status'] = item.status
				lst.append(dct)
		return lst

	def getItemByOccupierDBID(self, occupierDBID):
		"""
		通过占领者的DBID获取练兵场
		"""
		for line in self:
			for item in self[line].values():
				if item.occupierDBID == occupierDBID:
					return item
		return LbcItem()

	def getItemByDeclarerDBID(self, declarerDBID):
		"""
		通过宣战者的DBID获取练兵场
		"""
		for line in self:
			for item in self[line].values():
				if item.declarerDBID == declarerDBID:
					return item
		return LbcItem()


class RoleLbcInfo():
	"""
	玩家练兵场信息
	"""
	def __init__(self, line =0, index=0, level=0, isNotified=0):
		self.line = line
		self.index = index
		self.level = level
		self.isNotified = isNotified

	@classmethod
	def getDictFromObj( self, obj ):
		dct = {}
		dct['line'] = obj.line
		dct['index'] = obj.index
		dct['level'] = obj.level
		dct['isNotified'] = obj.isNotified
		return dct

	@classmethod
	def createObjFromDict( self, dict ):
		obj = RoleLbcInfo()
		obj.line = dict['line']
		obj.index = dict['index']
		obj.level = dict['level']
		obj.isNotified = dict['isNotified']
		return obj

	def isSameType( self, obj ):
		return isinstance(obj, RoleLbcInfo)

	def updateInfo(self, line, index):
		self.line = line
		self.index = index
		self.isNotified = 0

	def resetInfo(self):
		"""
		"""
		self.line = 0
		self.index = 0
		self.level = 0
		self.isNotified = 0

g_lbcItem = LbcItem()
g_lbcData = LbcData()
g_roleLbcInfo = RoleLbcInfo()