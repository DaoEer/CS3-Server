# -*- coding: utf-8 -*-

import KBEDebug
from SpacePlane import SpacePlane
import math
import Math
import KBEMath
import time

class SpacePlaneJSZZ( SpacePlane ):
	"""
	CST-7419 金树种子位面
	"""
	def __init__( self ):
		SpacePlane.__init__( self )
		self.wallPosList = []
		self.stageStartTime = 0.0 #当前阶段开始时间 根据怪物金树来的 金树开启某阶段 就会给副本发通知
		self.stageLongTime = 0.0 #当前阶段的时长
		self.nextRefreshMonsterTime = 0.0 # 下次刷怪的时间
		self.curStage = 0
		self.curStageRewardMoney = 0

	def calculateWallPosList( self, centerPos, radius ):
		"""
		计算光墙的坐标
		"""
		for i in range(9):
			radian = 2*math.pi / 9 * i
			pos = ( centerPos.x + radius * math.sin(radian), centerPos.y, centerPos.z + radius*math.cos(radian))
			self.wallPosList.append( Math.Vector3(KBEMath.KBEngine2UnrealPosition( pos )))

	def getPositionByRadian( self, pos, radius, radian ):
		"""
		"""
		return Math.Vector3( pos.x + radius*math.sin(radian), pos.y, pos.z + radius*math.cos(radian) )

	def setCurrentStageData( self, curStage,stageLongTime, curStageRewardMoney ):
		"""
		设置当前阶段的时长
		"""
		self.curStage = curStage
		self.stageLongTime = stageLongTime
		self.stageStartTime = time.time()
		self.curStageRewardMoney = curStageRewardMoney
		for playerRole in self._spaceRoles:
			self.showStageRemainTime( playerRole )

	def getCurStageRemainTime( self ):
		"""
		获得当前阶段的剩余时间
		"""
		if self.stageStartTime + self.stageLongTime > time.time():
			return int(self.stageStartTime + self.stageLongTime - time.time())
		else:
			return 0

	def showStageRemainTime(self, player ):
		"""
		通知显示阶段剩余时间
		"""
		remainTime = self.getCurStageRemainTime()
		if remainTime >0 and player.getClient():
			player.client.CLIENT_ShowJSZZCurStageRemainTime( self.curStage,remainTime )

	def setNextRefreshMonsterTime( self, refreshLongTime ):
		"""
		设置下次刷新怪时间
		"""
		self.nextRefreshMonsterTime = time.time() + refreshLongTime
		for playerRole in self._spaceRoles:
			self.showNextRefreshMonsterTime(playerRole)

	def getRemainNextRefreshMonsterTime( self ):
		"""
		获得刷怪的剩余时间
		"""
		if time.time() < self.nextRefreshMonsterTime:
			return int( self.nextRefreshMonsterTime - time.time() )
		else:
			return 0

	def showNextRefreshMonsterTime( self, player ):
		"""
		通知显示刷怪时间
		"""
		remainTime = self.getRemainNextRefreshMonsterTime()
		if remainTime >0 and player.getClient():
			player.client.CLIENT_ShowNextRefreshMonsterTime( remainTime )

	def onTeleportCompleted( self, playerRole ):
		"""
		传送结束，场景已加载完毕
		"""
		self.showStageRemainTime( playerRole )
		self.showNextRefreshMonsterTime( playerRole )
