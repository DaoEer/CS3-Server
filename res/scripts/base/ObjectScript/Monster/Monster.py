# -*- coding: utf-8 -*-

import csdefine
import Math
from ObjectScript.Monster import MonsterBase
import KBEDebug

MIN_DISTANCE_SPAWN_POS = 2.0

class Monster( MonsterBase.MonsterBase ):
	def __init__( self ):
		MonsterBase.MonsterBase.__init__( self )
		self.admType = 0
		self.admPoint = ""
		self.admSpeed = 0.0
		self.admAction = ""
		self._callRange = 0
		self._callList = []

	def initData( self, configData ):
		"""
		初始化数据
		@param configData: dict
		"""
		if configData is not None:
			MonsterBase.MonsterBase.initData( self, configData )
			if 'MinLevel' in configData:
				self.minLevel = configData["MinLevel"]
			
			if 'MaxLevel' in configData:
				self.maxLevel = configData["MaxLevel"]

			if "AdmType" in configData:
				self.admType = configData["AdmType"]		#登场类型
			if "AdmPoint" in configData:
				self.admPoint = configData["AdmPoint"]		#登场目标点
			if "AdmSpeed" in configData:
				self.admSpeed = configData["AdmSpeed"]		#登场速度
			if "AdmAction" in configData:
				self.admAction = configData["AdmAction"]	#登场动作
				
			if "WalkSpeed" in configData:		#走路速度
				self.walkSpeed = float(configData["WalkSpeed"])
			if "RunSpeed" in configData:		#跑步速度
				self.runSpeed = float(configData["RunSpeed"])

			if "callRange" in configData:
				self._callRange = int(configData[ "callRange" ])
			
			if "callList" in configData:
				self._callList = configData["callList"]

	def getCallRange( self ):
		return self._callRange

	def getCallList( self ):
		return self._callList

