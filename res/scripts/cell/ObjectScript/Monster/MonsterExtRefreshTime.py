# -*- coding: utf-8 -*-
import ObjectScript.Monster.Monster as Monster
import KBEDebug



import ObjectScript.Monster.Monster as Monster
import KBEDebug
import time
class MonsterExtRefreshTime( Monster.Monster ):
	def __init__( self ):
		Monster.Monster.__init__( self )
		self.reviveTime = 0.0

	def initData( self, configData ):
		Monster.Monster.initData( self, configData )
		if configData[ "Param1" ]:
			self.reviveTime = float(configData[ "Param1" ])
		
	def onEnterDead( self, selfEntity ):
		"""
		死亡
		"""
		selfEntity.endReviveTime = str(time.time() + self.reviveTime)
		selfEntity.addTimerCallBack( 5.0, "pretendModel",(selfEntity.endReviveTime,) )				#5秒后隐藏尸体
		selfEntity.addTimerCallBack( self.reviveTime, "onRevevie", ())
			
			
