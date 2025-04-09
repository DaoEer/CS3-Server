# -*- coding: utf-8 -*-

# 副本事件行为
import random
import Math
import KBEMath
import KBEDebug
import KBEngine
import Functions
import csarithmetic
import time, operator
import Reward.RewardBasicValueData as RewardBase
import ConfigObject.Reward.RewardBase.RewardMgr as RewardMgr
from ConfigObject.SpaceEvent.SpaceEventBase.SEActions.SEActionBase import SEActionBase

class SEAction191( SEActionBase ):
	"""
	梦魇画卷：副本初始化随机刷出number个光效模型,其中不能出现连续3个同样的相邻且相连的光效模型。
	"""
	def init ( self, section ):
		SEActionBase.init( self, section )
		
	def do( self, spaceEntity, triggerID, eventParams ):
		if spaceEntity:
			spaceEntity.isComplete = False
			spaceEntity.initPlantModel()

class SEAction217( SEActionBase ):
	"""
	梦魇画卷：通知副本显示界面
	"""
	def init ( self, section ):
		SEActionBase.init( self, section )
		
	def do( self, spaceEntity, triggerID, eventParams ):
		if spaceEntity:
			for player in spaceEntity._spaceRoles:
				player.client.CLIENT_NotifyHealthDisplayScreen()
		
class SEAction257( SEActionBase ):
	"""
	梦魇画卷：不再进行刷新
	"""
	def init ( self, section ):
		SEActionBase.init( self, section )
		
	def do( self, spaceEntity, triggerID, eventParams ):
		if spaceEntity:
			spaceEntity.destroyAllPieces()
			spaceEntity.isComplete = True

class SEAction261( SEActionBase ):
	"""
	梦魇画卷：新增奖励获得
	"""
	def init ( self, section ):
		SEActionBase.init( self, section )
		self.ratio = float(section["param1"])
		self.intervalTime = float(section["param2"])
		
	def do( self, spaceEntity, triggerID, eventParams ):
		if spaceEntity:
			if spaceEntity.startTime > 0 and spaceEntity.startTime + self.intervalTime > time.time():
				potentialBase = RewardBase.datas[spaceEntity.spaceLevel]["potential"]
				potential = int( potentialBase * self.ratio )
				for player in spaceEntity._spaceRoles:
					player.addPotential( potential )

class SEAction262( SEActionBase ):
	"""
	梦魇画卷：开始倒计时
	"""
	def init ( self, section ):
		SEActionBase.init( self, section )
		
	def do( self, spaceEntity, triggerID, eventParams ):
		if spaceEntity:
			for player in spaceEntity._spaceRoles:
				player.client.CLIENT_NotifyStartCountdown()
			spaceEntity.startTime = time.time()

class SEAction263( SEActionBase ):
	"""
	梦魇画卷：停止倒计时
	"""
	def init ( self, section ):
		SEActionBase.init( self, section )
		
	def do( self, spaceEntity, triggerID, eventParams ):
		if spaceEntity:
			for player in spaceEntity._spaceRoles:
				player.client.CLIENT_NotifyStopCountdown()

SEActionBase.setActionClass( "SEAction191",SEAction191 )
SEActionBase.setActionClass( "SEAction217",SEAction217 )
SEActionBase.setActionClass( "SEAction257",SEAction257 )
SEActionBase.setActionClass( "SEAction261",SEAction261 )
SEActionBase.setActionClass( "SEAction262",SEAction262 )
SEActionBase.setActionClass( "SEAction263",SEAction263 )