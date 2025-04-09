# -*- coding: utf-8 -*-
#############
# 上古密阵BOSS
#############

import ObjectScript.Monster.Monster as Monster


class MonsterExtSGMZ( Monster.Monster ):
	def __init__( self ):
		Monster.Monster.__init__( self )

	def onEnterFree( self, selfEntity ):
		"""
		virtual method
		进入自由状态
		"""
		selfEntity.setBootyOwner( None )
		selfEntity.changeDefaultMove()