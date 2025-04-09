# -*- coding: utf-8 -*-
#############
# 灵脉战场Boss
#############

import ObjectScript.Monster.Monster as Monster


class MonsterExtLingMai( Monster.Monster ):
	def __init__( self ):
		Monster.Monster.__init__( self )

	def initData( self, configData ):
		"""
		初始化数据
		@param configData: dict
		"""
		Monster.Monster.initData( self, configData )
