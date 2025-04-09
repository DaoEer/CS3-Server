# -*- coding: utf-8 -*-

from SpaceCopy import SpaceCopy
import KBEDebug
import Math
import KBEngine
import random
import Functions
import KBEMath

class SpaceCopyAndySnatch( SpaceCopy ):
	"""
	送宝任务(烈阳果送予莫何)
	"""
	def __init__( self ):
		SpaceCopy.__init__( self )
		self.direction = Math.Vector3(0, 0, 0)

	def initSpaceData( self, coordinates, moHeScriptID ):
		"""
		初始化数据
		"""
		self.coordinates = coordinates
		self.moHeScriptID = moHeScriptID

	def initRandomCreateMoHe( self ):
		"""
		初始化随机创建莫何
		"""
		coord = random.choice( self.coordinates )
		posStr = Functions.vector3TypeConvert( coord )
		self.createEntityByScriptID( self.moHeScriptID, KBEMath.Unreal2KBEnginePosition( posStr ), self.direction, {} )