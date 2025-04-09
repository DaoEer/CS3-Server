# -*- coding: utf-8 -*-

import KBEngine
#common
import KBEDebug
import cschannel_msgs
import csstatus

class UnLockConditionBase:
	"""
	解锁兵种基类
	"""
	def __init__( self ):
		"""
		virtual method.
		"""
		pass

	def init( self, dictDat ):
		"""
		virtual method.
		"""
		pass

	def valid( self, role ):
		"""
		virtual method.
		条件检测
		"""
		return True

class UnLockConditionOccupyTrain( UnLockConditionBase ):
	"""
	是否有占领练兵场
	"""
	def __init__( self ):
		"""
		virtual method.
		"""
		self.occupyTrainType = 0 #占领练兵场类型 1代表低级 2 代表中级 3 高级
		self.targetLevel = 0 # 目标等级

	def init( self, dictDat ):
		"""
		virtual method.
		"""
		if dictDat["Param1"]:
			self.occupyTrainType = int(dictDat["Param1"])
		if dictDat["Param2"]:
			self.targetLevel = int( dictDat["Param2"] )

	def valid( self, role ):
		"""
		virtual method.
		条件检测
		"""
		line = role.occupyInfo.line
		index = role.occupyInfo.index
		level = role.occupyInfo.level
		if line>0 and index>0 and level>=self.occupyTrainType:
			isOccupy = True
		else:
			isOccupy = False
		if not isOccupy:
			role.statusMessage( csstatus.BARRACKS_UP_LEVEL_MSG,cschannel_msgs.LEVEL_TYPE_NAME.get( self.occupyTrainType ),self.targetLevel )
		return isOccupy

class BarracksObjectCondition:
	"""
	解锁条件
	"""
	def __init__( self ):
		"""
		virtual method.
		"""
		self._conditions = []

	def init( self, conditionList ):
		"""
		virtual method.
		"""
		if len( conditionList ) <= 0:
			return
		for cdata in conditionList:
			self.add( cdata )

	def add( self, conditionData ):
		"""
		增加一个条件
		"""
		instance = eval( conditionData["ConditionType"] )()
		instance.init( conditionData )
		self._conditions.append( instance )

	def valid( self, role ):
		"""
		virtual method.
		条件检测
		"""
		for cnd in self._conditions:
			if cnd.valid( role ) == False:
				return False
		return True
