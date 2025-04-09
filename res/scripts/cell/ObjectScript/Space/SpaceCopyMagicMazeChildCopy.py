# -*- coding: utf-8 -*-
import Const
import Math
import KBEMath
from ObjectScript import Space
from ObjectScript.Space.SpaceCopyMagicMazeChild import SpaceCopyMagicMazeChild


class SpaceCopyMagicMazeChildCopy( SpaceCopyMagicMazeChild ):
	"""
	幻阵迷宫 副本玩法
	"""
	def __init__( self ):
		SpaceCopyMagicMazeChild.__init__( self )
