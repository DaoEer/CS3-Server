# -*- coding: utf-8 -*-

from SpaceCopyMagicMaze import SpaceCopyMagicMaze
import KBEDebug
import Math
import KBEngine
import random
import Functions
import KBEMath

class SpaceCopyMagicMazeChildLYSL( SpaceCopyMagicMaze ):
	"""
	幻阵迷宫 临渊试炼
	"""
	def __init__( self ):
		SpaceCopyMagicMaze.__init__( self )
		self.direction = Math.Vector3(0, 0, 0)

	def initSpaceData( self, herbKindList, coordinates, delayTime ):
		"""
		初始化数据
		"""
		self.herbKindList = herbKindList
		self.coordinates = coordinates
		self.delayTime = delayTime

	def initRandomCreateSpellBox( self ):
		"""
		初始化随机创建灵草
		"""
		for coord in self.coordinates:
			posStr = Functions.vector3TypeConvert( coord )
			herbID = random.choice( self.herbKindList )
			entity = self.createSpellBox( str(herbID), KBEMath.Unreal2KBEnginePosition( posStr ), self.direction, {} )
			
	def randomRefrehMedicine( self, position, direction ):
		"""
		随机刷新出一种灵草
		"""
		self.addTimerCallBack( self.delayTime, "delayTimeRefrehMedicine", (position, direction,))

	def delayTimeRefrehMedicine( self, position, direction):
		"""
		延时刷新
		"""
		herbID = random.choice( self.herbKindList )
		self.createSpellBox( str(herbID), position, direction, {} )
