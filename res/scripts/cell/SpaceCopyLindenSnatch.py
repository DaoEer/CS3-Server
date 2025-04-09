# -*- coding: utf-8 -*-

from SpaceCopy import SpaceCopy
import KBEDebug
import Math
import KBEngine
import random
import Functions
import KBEMath

class SpaceCopyLindenSnatch( SpaceCopy ):
	"""
	送宝任务(菩提子送予燃灯道人)
	"""
	def __init__( self ):
		SpaceCopy.__init__( self )
		self.direction = Math.Vector3(0, 0, 0)

	def initSpaceData( self, coordinates, XTDLScriptIDList ):
		"""
		初始化数据
		"""
		self.coordinates = coordinates
		self.XTDLScriptIDList = XTDLScriptIDList

	def initRandomCreateXTDL( self ):
		"""
		初始化随机创建燃灯道人
		"""
		i = 0
		random.shuffle( self.coordinates )  #随机重新排列坐标点
		for coord in self.coordinates:
			posStr = Functions.vector3TypeConvert( coord )
			self.createEntityByScriptID( self.XTDLScriptIDList[i], KBEMath.Unreal2KBEnginePosition( posStr ), self.direction, {} )
			i += 1