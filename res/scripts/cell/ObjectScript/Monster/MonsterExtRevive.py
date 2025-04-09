# -*- coding: utf-8 -*-

#------------------
#复活怪物脚本
#------------------

import ObjectScript.Monster.Monster as Monster

class MonsterExtRevive( Monster.Monster ):
	def __init__( self ):
		Monster.Monster.__init__( self )
		self._scriptID = 0
		self.reviveTime = 0.0

	def initData( self, configData ):
		Monster.Monster.initData( self, configData )
		if "scriptID" in configData:
			self._scriptID = int(configData[ "scriptID" ])
		if configData[ "Param1" ]:
			self.reviveTime = float(configData[ "Param1" ])

	def onEnterDead( self, selfEntity ):
		"""
		死亡
		"""
		selfEntity.addTimerCallBack( self.reviveTime, 'hasOtherRevive', ())
