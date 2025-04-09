# -*- coding: utf-8 -*-

import KBEngine
from ObjectScript.Space.SpaceCopyRingTaskChild import SpaceCopyRingTaskChild
import KBEDebug
import csdefine
import Define

class SpaceCopyXuanTianBaoLu( SpaceCopyRingTaskChild ):
	"""
	玄天宝录副本
	"""
	def __init__( self ):
		SpaceCopyRingTaskChild.__init__( self )

	def initData( self, configData ):
		"""
		初始化数据
		"""
		SpaceCopyRingTaskChild.initData( self, configData )
		stoneScriptID = configData["SpaceData"].get( "stoneScriptID", "" )
		if stoneScriptID:
			self.stoneScriptID = stoneScriptID.split("|")							# 石像的scriptID
		self.stoneBurstNum = configData["SpaceData"].get( "stoneBurstNum", "" )		# 石像爆发的个数
		self.outBreakBuff = configData["SpaceData"].get( "outBreakBuff", "" )		# 爆发妖气Buff
		self.intervalTime = configData["SpaceData"].get( "intervalTime", 0.0 )		# 间隔时间
		self.mirrorId = configData["SpaceData"].get( "mirrorId", "" )				# 大日宝镜的SpellboxScriptID
		self.turnSpeed = float(configData["SpaceData"].get("turnSpeed", 0.0) )		# 旋转速度
		self.petrifyBuff = configData["SpaceData"].get( "petrifyBuff", "" )			# 石化Buff

	def initEntity( self, selfEntity ):
		"""
		virtual method
		初始化space entity要做的事情
		"""
		SpaceCopyRingTaskChild.initEntity( self, selfEntity )
		selfEntity.initSpaceData( self.stoneScriptID, self.stoneBurstNum, self.outBreakBuff, self.intervalTime, self.mirrorId, self.turnSpeed, self.petrifyBuff )