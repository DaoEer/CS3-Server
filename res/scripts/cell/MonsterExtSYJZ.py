# -*- coding: utf-8 -*-


import KBEngine
import KBEDebug
#script
import Monster
import time
import csarithmetic
import csdefine
import Const

class MonsterExtSYJZ( Monster.Monster ):
	"""
	三源镜柱 怪物（镜柱等）
	可点击怪物:左键单击
	"""
	def __init__( self ):
		Monster.Monster.__init__( self )

	def onClickCallBack( self, srcEntityID ):
		"""
		<exposed method>
		客户端左键单击回调
		"""
		spaceEntity = self.getCurrentSpace()
		if not spaceEntity:
			return
		spaceEntity.onStartRotatSource( spaceEntity, self.scriptID )