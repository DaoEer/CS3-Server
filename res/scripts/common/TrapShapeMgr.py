# -*- coding: utf-8 -*-

# --------------------------------------------------------------------
# 陷阱形状实现模块
# --------------------------------------------------------------------

import Math
import csdefine
import Singleton
import csarithmetic
import KBEDebug
import math

class ShapeBase:
	"""
	"""
	def __init__( self ):
		self.centrePos = Math.Vector3((0,0,0))		#中心点坐标
		self.height = 0.0								#高度
	
	def init( self, pos, height, paramStr):
		self.centrePos = pos
		self.height = height
	
	def getProximityXZ( self ):
		"""
		virtual method
		获取外接方形的半径（边长的一半）
		"""
		return 0.0
	
	def isPointIn( self, otherPos, direction = ( 0,0,0 ) ):
		"""
		virtual method
		某点是否在范围内
		"""
		return False

class ShapeCircular( ShapeBase ):
	"""
	以中心点为圆形的圆
	"""
	def __init__( self ):
		ShapeBase.__init__( self )
		self.radius = 0.0
	
	def init( self, pos, height, paramStr):
		ShapeBase.init( self, pos, height, paramStr)
		self.radius = float( paramStr )	#paramStr格式："0.0"
	
	def getProximityXZ( self ):
		"""
		virtual method
		获取外接方形的半径（边长的一半）
		"""
		return self.radius
	
	def isPointIn( self, otherPos, direction ):
		"""
		virtual method
		某点是否在范围内
		"""
		lenght = self.centrePos.flatDistTo( otherPos )
		yLenght = abs( self.centrePos.y - otherPos.y )
		return lenght <= self.radius and yLenght <= self.height

class ShapeSphere( ShapeBase ):
	"""
	球形
	"""
	def __init__( self ):
		ShapeBase.__init__( self )
		self.radius = 0.0
	
	def init( self, pos, height, paramStr ):
		ShapeBase.init( self, pos, height, paramStr )
		self.radius = float( paramStr )	#paramStr格式："0.0"
	
	def getProximityXZ( self ):
		"""
		virtual method
		获取外接方形的半径（边长的一半）
		"""
		return self.radius
	
	def isPointIn( self, otherPos, direction ):
		"""
		virtual method
		某点是否在范围内
		"""
		return self.centrePos.flatTo( otherPos ) <= self.radius

class ShapeSector( ShapeBase ):
	"""
	扇形
	"""
	def __init__( self ):
		ShapeBase.__init__( self )
		self.radius = 0.0
		self.angle = 0.0
	
	def init( self, pos, height, paramStr ):
		ShapeBase.init( self, pos, height, paramStr )
		params = paramStr.split("|")
		self.radius = float( params[0] )	#paramStr格式："半径|角度"
		self.angle = float( params[1] )

	def getProximityXZ( self ):
		"""
		virtual method
		获取外接方形的半径（边长的一半）
		"""
		return self.radius
	
	def isPointIn( self, otherPos, direction ):
		"""
		virtual method
		某点是否在范围内
		"""
		return csarithmetic.isInSector( otherPos, self.centrePos, csarithmetic.getYawByVector3(direction), self.radius, self.angle )


class ShapeRect( ShapeBase ):
	"""
	矩形
	"""
	def __init__( self ):
		ShapeBase.__init__( self )
		self.width = 0.0
		self.length = 0.0
	
	def init( self, pos, height, paramStr ):
		ShapeBase.init( self, pos, height, paramStr )
		params = paramStr.split("|")
		self.width = float( params[0] )	#paramStr格式："width|length"
		self.length = float( params[1] )

	def getProximityXZ( self ):
		"""
		virtual method
		获取外接方形的半径（边长的一半）
		"""
		return math.sqrt(self.width*self.width + self.length*self.length)/2.0
	
	def isPointIn( self, otherPos, direction ):
		"""
		virtual method
		某点是否在范围内
		"""
		return csarithmetic.isInRectangleExt( otherPos, self.centrePos, csarithmetic.getYawByVector3(direction), self.width, self.length )



SHAPE_TYPE_CLASS_MAP = { csdefine.TRAP_SHAPE_CIRCULAR: ShapeCircular,
						csdefine.TRAP_SHAPE_SQUARE: ShapeRect,
						csdefine.TRAP_SHAPE_SPHERE: ShapeSphere,
						csdefine.TRAP_SHAPE_SECTOR: ShapeSector,
		 }


class TrapShapeMgr( Singleton.Singleton ):
	"""
	"""
	def __init__( self ):
		pass
	
	def getShapeIns( self, shapeType, centrePos, rangeY, paramStr ):
		"""
		"""
		if shapeType not in SHAPE_TYPE_CLASS_MAP:
			return None
		ins = SHAPE_TYPE_CLASS_MAP[shapeType]()
		ins.init( centrePos, rangeY, paramStr )
		return ins


g_trapShapeMgr = TrapShapeMgr()