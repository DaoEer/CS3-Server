


#阵营竞技副本奖励 

class ZyjjRewardDatas(dict):
	"""
	阵营竞技副本奖励 CST-13692
	"""
	def addExp(self, playerDBID, value):
		if playerDBID not in self:
			self[playerDBID] = ZyjjRewardData()
		self[playerDBID].addExp(value)

	def addFeats(self, playerDBID, value):
		if playerDBID not in self:
			self[playerDBID] = ZyjjRewardData()
		self[playerDBID].addFeats(value)

	def addExploit(self, playerDBID, value):
		if playerDBID not in self:
			self[playerDBID] = ZyjjRewardData()
		self[playerDBID].addExploit(value)

	def addContribution(self, playerDBID, value):
		if playerDBID not in self:
			self[playerDBID] = ZyjjRewardData()
		self[playerDBID].addContribution(value)


class ZyjjRewardData():
	"""
	阵营竞技奖励
	"""
	def __init__(self):
		self.exp = 0 #经验奖励
		self.feats = 0 #功勋奖励
		self.exploit = 0 #军功奖励
		self.contribution = 0 #帮贡奖励

	@classmethod
	def getDictFromObj( self, obj ):
		dct = {}
		dct['exp'] = obj.exp
		dct['feats'] = obj.feats
		dct['exploit'] = obj.exploit
		dct['contribution'] = obj.contribution
		return dct

	@classmethod
	def createObjFromDict( self, dict ):
		obj = ZyjjRewardData()
		obj.exp = dict['exp']
		obj.feats = dict['feats']
		obj.exploit = dict['exploit']
		obj.contribution = dict['contribution']
		return obj

	def isSameType( self, obj ):
		return isinstance(obj, ZyjjRewardData)

	def addExp(self, value):
		self.exp+=int(value)

	def addFeats(self, value):
		self.feats+=int(value)

	def addExploit(self, value):
		self.exploit+=int(value)
	
	def addContribution(self, value):
		self.contribution+=int(value)
				
g_zyjjRewardDatas = ZyjjRewardDatas()
g_zyjjRewardData = ZyjjRewardData()




