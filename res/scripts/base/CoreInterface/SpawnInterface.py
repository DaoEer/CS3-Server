# -*- coding: utf-8 -*-
import KBEngine

import KST

class SpawnInterface:
	def __init__( self ):
		pass
		
	def startLoaderSpawnFile( self, componentid ):
		"""
		<define method>
		"""
		KBEngine.globalData[ "SpawnManager" ].registerSpace( componentid, self )
	
	def createSpawnPoint( self ):
		"""
		define method
		开始刷怪
		"""
		if self.isDestroyed:
			return
			
		if hasattr(self, "cell") and self.cell:								# 会有一定的概率出现 cell 为None，打印消息便于查找问题。
			self.cell.createSpawnPoint()
		else:
			self.addTimerCallBack( 1.0, "createSpawnPoint", () ) #如果没有cell，则添加一个定时器去检查
		