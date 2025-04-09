# -*- coding: utf-8 -*-
#############
# 上古密阵BOSS
#############

import ObjectScript.Monster.Monster as Monster


class MonsterExtSGMZ( Monster.Monster ):
	def __init__( self ):
		Monster.Monster.__init__( self )

	def initData( self, configData ):
		"""
		初始化数据
		@param configData: dict
		"""
		Monster.Monster.initData( self, configData )
