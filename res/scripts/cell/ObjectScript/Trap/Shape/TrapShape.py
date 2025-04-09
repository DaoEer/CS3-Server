# -*- coding: utf-8 -*-
#
import csdefine
import KBEngine
import KBEDebug
import Vector
import Math
import math
import Const
from Singleton import Singleton

# 验证客户端陷阱的有效性
# 因为玩家的坐标是客户端同步到服务器的，有可能玩家坐标服务器与客户端不一致！因此，验证只要在一个范围内有效，则该触发有效

class TrapShapeMgr( Singleton ):
	"""
	陷阱形状管理
	"""
	def __init__( self ):
		"""
		"""
		self.map = {
			csdefine.TRAP_SHAPE_RECTANGLE	:	TrapShapeRectangle(),
			csdefine.TRAP_SHAPE_CIRCULAR	:	TrapShapeCircular(),
			csdefine.TRAP_SHAPE_CYLINDER	:	TrapShapeCylinder(),
		}

	def getShape( self, type ):
		"""
		根据类型给予条件
		"""
		return self.map.get( type, None )

	def validate( self, selfEntity, avatar ):
		"""
		触发陷阱验证
		@param selfEntity: 陷阱本身
		@type  selfEntity: ENTITY
		@param avatar: 触发对象
		@type  avatar: ENTITY
		@return BOOL
		"""
		shapeClass = self.getShape( selfEntity.triggerShape )
		if shapeClass == None:
			return False
		
		if not shapeClass.validate( selfEntity, avatar ):
			KBEDebug.ERROR_MSG( "TrapShapeMgr::validate-->>>Client Trap(Shap:%i,Radius:%s) Can't pass validate!! " % (selfEntity.triggerShape, selfEntity.triggerRadius) )
			return False
		return True

class TrapShapeBase:
	"""
	陷阱触发范围基础类
	"""
	def __init__( self ):
		"""
		"""
		pass

	def validate( self, selfEntity, avatar ):
		"""
		"""
		return True

class TrapShapeRectangle( TrapShapeBase ):
	"""
	陷阱矩形体触发范围(正确的方式需要考虑到朝向的问题，这里只简单验证)
	"""
	def __init__( self ):
		"""
		"""
		pass

	def validate( self, selfEntity, avatar ):
		"""
		"""
		maxRadius = max( selfEntity.triggerDepth, selfEntity.triggerWidth )
		y = selfEntity.triggerHeight
		
		distX = abs( selfEntity.position.x - avatar.position.x )
		distY = abs( selfEntity.position.y - avatar.position.y )
		distZ = abs( selfEntity.position.z - avatar.position.z )
		
		return  distX <= maxRadius+Const.PERMISSIBLE_MAX_RANGE and distY <= y+Const.PERMISSIBLE_MAX_RANGE and distZ <= maxRadius+Const.PERMISSIBLE_MAX_RANGE

class TrapShapeCircular( TrapShapeBase ):
	"""
	陷阱球形触发范围
	"""
	def __init__( self ):
		"""
		"""
		pass

	def validate( self, selfEntity, avatar ):
		"""
		"""
		distRange = avatar.position.distTo( selfEntity.position )
		return  distRange <= selfEntity.triggerRadius + Const.PERMISSIBLE_MAX_RANGE

class TrapShapeCylinder( TrapShapeBase ):
	"""
	陷阱圆柱体触发范围
	"""
	def __init__( self ):
		"""
		"""
		pass

	def validate( self, selfEntity, avatar ):
		"""
		"""
		radiusXZ = selfEntity.triggerRadius
		radiusY = selfEntity.triggerHeight
		
		distRange = Math.Vector2( selfEntity.position.x, selfEntity.position.z ).distTo( Math.Vector2( avatar.position.x, avatar.position.z ))
		distY = abs( selfEntity.position.y - avatar.position.y )
		return  distRange <= radiusXZ+Const.PERMISSIBLE_MAX_RANGE and distY <= radiusY+Const.PERMISSIBLE_MAX_RANGE

g_trapShapeMgr = TrapShapeMgr()
