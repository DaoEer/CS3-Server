# -*- coding: utf-8 -*-
import Const
import Math
import KBEMath
import KBEngine
from KBEDebug import *
import time
import csstatus
import csconst
import json
import random
import Functions
from ObjectScript import Space
from ObjectScript.Space.SpaceCopyMagicMazeChild import SpaceCopyMagicMazeChild

class SpaceCopyMagicMazeChildLYSL( SpaceCopyMagicMazeChild ):
	"""
	幻阵迷宫 临渊试炼
	"""
	def __init__( self ):
		SpaceCopyMagicMazeChild.__init__( self )
		self.herbKindList = []
		self.coordinates = []

	def initData( self, configData ):
		"""
		virtual method
		"""
		SpaceCopyMagicMazeChild.initData( self, configData )
		herbKindList = configData["SpaceData"].get("herbKindList", "")
		if herbKindList:
			self.herbKindList = [ int(i) for i in herbKindList.split("|") ]
		coordinates = configData["SpaceData"].get("coordinates", "")
		if coordinates:
			self.coordinates = coordinates.split("|")
		self.delayTime = float(configData["SpaceData"].get("delayTime",0.0))

	def initEntity( self, selfEntity ):
		"""
		virtual method
		初始化space entity要做的事情
		"""
		SpaceCopyMagicMazeChild.initEntity( self, selfEntity )
		selfEntity.initSpaceData( self.herbKindList, self.coordinates, self.delayTime )