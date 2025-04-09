# -*- coding: utf-8 -*-
import Const
import Math
import KBEMath
from ObjectScript import Space
from ObjectScript.Space.SpaceCopyMagicMazeChild import SpaceCopyMagicMazeChild


class SpaceCopyMagicMazeChildDropBox( SpaceCopyMagicMazeChild ):
	"""
	幻阵迷宫 宝箱玩法
	"""
	def __init__( self ):
		SpaceCopyMagicMazeChild.__init__( self )
		
	def initData( self, configData ):
		"""
		virtual method
		"""
		SpaceCopyMagicMazeChild.initData( self, configData )
		self.needXiuWei = configData["SpaceData"].get("needXiuWei", 0)
		
