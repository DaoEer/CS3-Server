# -*- coding: utf-8 -*-

# 各种评分项

import time
import csdefine

class SettlementBase:
	"""
	基类
	"""
	def __init__( self ):
		self.title = ""
		self.dataKey = ""
	
	def init( self, index, title, params ):
		self.title = title
	
	def getEventType( self ):
		return 0
	
	def addRecord( self, spaceEntity, value = 0, param = "" ):
		"""
		增加记录
		"""
		pass
	
	def getRecord( self, spaceEntity ):
		"""
		获取记录
		"""
		return 0
	
	def getScore( self, spaceEntity ):
		"""
		计算得分
		"""
		pass
	
	def getTitle( self ):
		"""
		获取标题
		"""
		return self.title

class Settlement_PassTime( SettlementBase ):
	"""
	通关时间
	"""
	def __init__( self ):
		SettlementBase.__init__( self )
		self.baseTime = 0.0			#标准时间
		self.baseScore = 0			#标准分
	
	def init( self, index, title, params ):		# params格式："标准时间|标准分"
		SettlementBase.init( self, index, title, params )
		self.dataKey = "%i_passTime"%index
		paramList = params.strip().split("|")
		self.baseTime = int( paramList[0] )
		self.baseScore = int( paramList[1] )
	
	def getEventType( self ):
		return csdefine.SPACE_STMT_SPACE_SUCCESS
	
	def addRecord( self, spaceEntity, value = 0, param = "" ):
		"""
		增加记录
		"""
		if spaceEntity.lifeStartTime != 0:
			_time = time.time() - spaceEntity.lifeStartTime
		else:
			_time = time.time() - spaceEntity.createTime
		
		if self.dataKey not in spaceEntity.settlementDatas:
			spaceEntity.settlementDatas[self.dataKey] = int( _time )	#单位为秒
	
	def getRecord( self, spaceEntity ):
		"""
		获取记录
		"""
		return spaceEntity.settlementDatas.get(self.dataKey, 0)
	
	def getScore( self, spaceEntity ):
		"""
		计算得分
		"""
		record = self.getRecord( spaceEntity )
		if not record:
			return 0
		return self.baseTime / record * self.baseScore

class Settlement_ReceiveDamage( SettlementBase ):
	"""
	接受伤害
	"""
	def __init__( self ):
		SettlementBase.__init__( self )
		self.baseDamage = 0			#标准伤害
		self.baseScore = 0			#标准分
	
	def init( self, index, title, params ):		# params格式："标准伤害|标准分"
		SettlementBase.init( self, index, title, params )
		self.dataKey = "%i_receiveDamage"%index
		paramList = params.strip().split("|")
		self.baseDamage = int( paramList[0] )
		self.baseScore = int( paramList[1] )
	
	def getEventType( self ):
		return csdefine.SPACE_STMT_RECEIVE_DAMAGE
	
	def addRecord( self, spaceEntity, value = 0, param = "" ):
		"""
		增加记录
		"""
		if self.dataKey not in spaceEntity.settlementDatas:
			spaceEntity.settlementDatas[self.dataKey] = 0
		
		spaceEntity.settlementDatas[self.dataKey] += value
	
	def getRecord( self, spaceEntity ):
		"""
		获取记录
		"""
		return spaceEntity.settlementDatas.get(self.dataKey, 0)
	
	def getScore( self, spaceEntity ):
		"""
		计算得分
		"""
		record = self.getRecord( spaceEntity )
		if not record:
			return 0
		return self.baseDamage / record * self.baseScore

class Settlement_DieAmount( SettlementBase ):
	"""
	死亡次数
	"""
	def __init__( self ):
		SettlementBase.__init__( self )
		self.baseScore = 0			#标准分
	
	def init( self, index, title, params ):		# params格式："标准分"
		SettlementBase.init( self, index, title, params )
		self.dataKey = "%i_dieAmount"%index
		self.baseScore = int( params.strip() )
	
	def getEventType( self ):
		return csdefine.SPACE_STMT_ROLE_DIE
	
	def addRecord( self, spaceEntity, value = 0, param = "" ):
		"""
		增加记录
		"""
		if self.dataKey not in spaceEntity.settlementDatas:
			spaceEntity.settlementDatas[self.dataKey] = 0
		
		spaceEntity.settlementDatas[self.dataKey] += 1
	
	def getRecord( self, spaceEntity ):
		"""
		获取记录
		"""
		return spaceEntity.settlementDatas.get(self.dataKey, 0)
	
	def getScore( self, spaceEntity ):
		"""
		计算得分
		"""
		record = self.getRecord( spaceEntity )
		if not record:
			return 0
		return self.baseScore - record * 200

class Settlement_BoxAmount( SettlementBase ):
	"""
	触发箱子数
	"""
	def __init__( self ):
		SettlementBase.__init__( self )
		self.amountAndScore = []		#[(数量,分数)]
		self.scriptIDs = []				#箱子ID
	
	def init( self, index, title, params ):		# params格式："数量1:分数1;数量2:分数2;...|scriptID1;scriptID2;scriptID3;..."
		SettlementBase.init( self, index, title, params )
		self.dataKey = "%i_boxAmount"%index
		
		paramList = params.strip().split("|")
		for i in paramList[0].split(";"):
			amount, score = i.split(":")
			self.amountAndScore.append( ( int(amount), int(score) ) )
		self.amountAndScore = sorted( self.amountAndScore, key=lambda x:x[0], reverse=True )	# 按数量降序排列
		
		if len(paramList) > 1:
			self.scriptIDs = paramList[1].strip().split(";")
	
	def getEventType( self ):
		return csdefine.SPACE_STMT_TRIGGER_BOX
	
	def addRecord( self, spaceEntity, value = 0, param = "" ):
		"""
		增加记录
		"""
		if len(self.scriptIDs) != 0 and param not in self.scriptIDs:
			return
		
		if self.dataKey not in spaceEntity.settlementDatas:
			spaceEntity.settlementDatas[self.dataKey] = 0
		
		spaceEntity.settlementDatas[self.dataKey] += 1
	
	def getRecord( self, spaceEntity ):
		"""
		获取记录
		"""
		return spaceEntity.settlementDatas.get(self.dataKey, 0)
	
	def getScore( self, spaceEntity ):
		"""
		计算得分
		"""
		record = self.getRecord( spaceEntity )
		if not record:
			return 0
		
		for amount, score in self.amountAndScore:
			if record >= amount:
				return score
		return 0

class Settlement_JDDBBigBox( SettlementBase ):
	"""
	金殿夺宝大宝箱获取时间
	"""
	def __init__( self ):
		SettlementBase.__init__( self )
		self.timeAndScore = []		#[(时间,分数)]
		self.scriptIDs = []			#箱子ID
	
	def init( self, index, title, params ):		# params格式："时间1:分数1;时间2:分数2;...|scriptID1;scriptID2;scriptID3;..."
		SettlementBase.init( self, index, title, params )
		self.dataKey = "%i_JDDBBigBox"%index
		
		paramList = params.strip().split("|")
		for i in paramList[0].split(";"):
			time, score = i.split(":")
			self.timeAndScore.append( ( int(time), int(score) ) )
		self.timeAndScore = sorted( self.timeAndScore, key=lambda x:x[0] )	# 按时间升序排列
		
		if len(paramList) > 1:
			self.scriptIDs = paramList[1].strip().split(";")
	
	def getEventType( self ):
		return csdefine.SPACE_STMT_TRIGGER_BOX
	
	def addRecord( self, spaceEntity, value = 0, param = "" ):
		"""
		增加记录
		"""
		if len(self.scriptIDs) != 0 and param not in self.scriptIDs:
			return
		
		if self.dataKey in spaceEntity.settlementDatas:
			return
		
		if spaceEntity.lifeStartTime != 0:
			_time = time.time() - spaceEntity.lifeStartTime
		else:
			_time = time.time() - spaceEntity.createTime
		
		spaceEntity.settlementDatas[self.dataKey] = int( _time )
	
	def getRecord( self, spaceEntity ):
		"""
		获取记录
		"""
		return spaceEntity.settlementDatas.get(self.dataKey, 0)
	
	def getScore( self, spaceEntity ):
		"""
		计算得分
		"""
		record = self.getRecord( spaceEntity )
		if not record:
			return 0
		
		for _time, score in self.timeAndScore:
			if record <= _time:
				return score
		return 0
		

class Settlement_childSpaceFailure(SettlementBase):
	"""
	子副本通关失败
	"""
	def __init__( self ):
		SettlementBase.__init__( self )
		self.baseScore = 0			#标准分
	
	def init( self, index, title, params ):		# params格式："标准分"
		SettlementBase.init( self, index, title, params )
		self.dataKey = "%i_childSpaceFailure"%index
		self.baseScore = int( params.strip() )
	
	def getEventType( self ):
		return csdefine.SPACE_STMT_CHILD_SPACE_FAILURE
	
	def addRecord( self, spaceEntity, value = 0, param = "" ):
		"""
		增加记录
		"""
		if self.dataKey not in spaceEntity.settlementDatas:
			spaceEntity.settlementDatas[self.dataKey] = 0
		
		spaceEntity.settlementDatas[self.dataKey] += 1
	
	def getRecord( self, spaceEntity ):
		"""
		获取记录
		"""
		return spaceEntity.settlementDatas.get(self.dataKey, 0)
	
	def getScore( self, spaceEntity ):
		"""
		计算得分
		"""
		record = self.getRecord( spaceEntity )
		if not record:
			return 0
		return self.baseScore - record * 200

	