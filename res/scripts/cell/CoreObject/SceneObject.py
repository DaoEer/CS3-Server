# -*- coding: utf-8 -*-

"""
用于场景物件类型的基本类型
"""

import KST
from CoreObject import GameObject

# 场景物件基类


class SceneObject( GameObject.GameObject):
	def __init__( self ):
		GameObject.GameObject.__init__( self )

	def getScript( self ):
		if not self._scriptObject:
			self._scriptObject = KST.g_objFactory.getSceneObject( self.scriptID )
		return self._scriptObject

	def CELL_onClientReady( self, srcEntityID ):
		"""
		<Expose method>
		客户端Character Actor已经准备好
		"""
		pass
	
	def behIsOptimize(self, bedType, behDescribe):
		"""
		是否采用优化的方案，用于客户端执行行为的判断
		:return: bool
		"""
		return False