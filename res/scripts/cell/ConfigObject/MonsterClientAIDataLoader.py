# -*- coding: utf-8 -*-

import KBEDebug
import Singleton

class MonsterClientAIDataLoader(Singleton.Singleton):
	"""
	怪物客户端AI数据
	"""
	def __init__( self ):
		Singleton.Singleton.__init__( self )
		self.monsterDatas = {}   #{ scriptID:{"enemyRange":"","distance":"",....}

	def init( self, configData ):
		"""
		读取配置
		"""
		self.monsterDatas.clear()
		for scriptID, monsterConfigData in configData.items():
			self.monsterDatas[scriptID] = monsterConfigData
			
	def getMonsterBaseData( self, monsterScriptID ):
		"""
		获取基本数据
		"""
		monsterDatas = self.monsterDatas.get( monsterScriptID, None )
		if not monsterDatas:
			return None
		return monsterDatas

g_monsterClientAIDataLoader = MonsterClientAIDataLoader()