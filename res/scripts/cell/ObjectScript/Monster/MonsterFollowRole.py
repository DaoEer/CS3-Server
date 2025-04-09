# -*- coding: utf-8 -*-
import ObjectScript.Monster.Monster as Monster
import csdefine


class MonsterFollowRole( Monster.Monster ):
	"""
	客户端AI测试怪(跟随玩家)
	"""
	def __init__( self ):
		Monster.Monster.__init__( self )

	def initData( self, configData ):
		"""
		初始化数据
		@param configData: dict
		"""
		Monster.Monster.initData( self, configData )



