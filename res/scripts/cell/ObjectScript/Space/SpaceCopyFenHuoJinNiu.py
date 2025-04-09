# -*- coding: utf-8 -*-

import KBEngine
from ObjectScript.Space.SpaceCopyRingTaskChild import SpaceCopyRingTaskChild
import KBEDebug

class SpaceCopyFenHuoJinNiu( SpaceCopyRingTaskChild ):
	"""
	环任务副本 焚火金牛
	"""
	def __init__( self ):
		SpaceCopyRingTaskChild.__init__( self )
		self.destPos = []

	def initData( self, configData ):
		"""
		初始化数据
		"""
		SpaceCopyRingTaskChild.initData( self, configData )
		destPos = configData["SpaceData"].get("destPos", "")
		if destPos:
			self.destPos = destPos.split("|")										# 三个灵池的位置坐标
		self.centerPos = configData["SpaceData"].get("centerPos", "")				# 祭坛位置坐标	
		self.taurusScriptID = configData["SpaceData"].get("taurusScriptID", "")		# 金牛的ScriptID
		self.runSpeed = float(configData["SpaceData"].get("runSpeed", ""))			# 金牛的行走速度
		self.speedLimit = float(configData["SpaceData"].get("speedLimit", ""))		# 金牛的速度上限
		self.accSpeed = float(configData["SpaceData"].get("accSpeed", ""))			# 金牛的加速度
		self.buffID = float(configData["SpaceData"].get("buffID", ""))

	def initEntity( self, selfEntity ):
		"""
		virtual method
		初始化space entity要做的事情
		"""
		SpaceCopyRingTaskChild.initEntity( self, selfEntity )
		selfEntity.initSpaceData( self.taurusScriptID, self.destPos, self.centerPos, self.runSpeed, self.speedLimit, self.accSpeed, self.buffID )