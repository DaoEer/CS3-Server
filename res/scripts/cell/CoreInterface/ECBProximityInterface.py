# -*- coding: utf-8 -*-

"""
usage:
	陷阱封装类

attribute:
	objectType

member function:
	getObjectType
	getName

callback:
	pass

"""

#engine
import Math
import KBEngine
#script
import KBEDebug
import csdefine
import ECBProximityDefine
from TrapShapeMgr import g_trapShapeMgr


class ECBProximityInterface:
	"""
	陷阱封装类
	"""
	def __init__( self ):
		pass
	
	def checkScoutHeight( self, entity ):
		"""
		virtual method
		"""
		return True
	
	#-------------------------------------------
	# 添加底层方形陷阱
	#-------------------------------------------
	def addProximityExt( self, rangeXZ, rangeY, userArg = ECBProximityDefine.PROXIMITY_COMMON, isSquare = True ):
		"""
		添加陷阱
		"""
		proximityID = self.addProximity( rangeXZ, rangeY, userArg )
		if proximityID not in self.proximityInfo:
			self.proximityInfo[ proximityID ] = [ userArg, rangeXZ, rangeY, isSquare ]
		
		# 处理刚创建陷阱就进入的一批entity
		if proximityID in self.entersOnAddProximity:
			for eID in self.entersOnAddProximity[ proximityID ]:
				entity = KBEngine.entities.get( eID )
				if not entity:
					continue
				self.onEnterTrap( entity, rangeXZ, rangeY, proximityID, userArg )
		
		return proximityID
	
	def findProximityByUserArg( self, userArg ):
		for id, arg in self.proximityInfo.items():
			if arg[0] == userArg:
				return id
		return 0
	
	#-----------------------------------------------------------------------------------------------------------------
	"""
	添加其他形状陷阱：因为引擎只支持方形（且不带朝向）的陷阱，因此提供这些接口用于实现其他形状的陷阱，比如圆形
	处理机制：加一个覆盖整个形状的底层方形陷阱，进出陷阱时增减记录；额外加一个检测timer，检测记录中的entity是否进出形状。
	"""
	#-----------------------------------------------------------------------------------------------------------------
	def addShapeProximityExt( self, shapeType, shapeParams, rangeY, userArg = ECBProximityDefine.PROXIMITY_COMMON ):
		"""
		添加陷阱
		"""
		if shapeType == csdefine.TRAP_SHAPE_SQUARE and len(shapeParams.split("|"))==1:		#方形并且只有一个参数则按底层陷阱处理
			self.addProximityExt( float(shapeParams), rangeY, userArg, True )
		else:
			shapeIns = g_trapShapeMgr.getShapeIns( shapeType, Math.Vector3(self.position), rangeY, shapeParams )
			if not shapeIns:
				return
			rangeXZ = shapeIns.getProximityXZ()
			proximityID = self.addProximityExt( rangeXZ, rangeY, userArg, False )
			timerID = self.addTimerRepeat( 0.1, "onShapeProximityCheckTimer", (rangeXZ, rangeY, proximityID, userArg, shapeType, shapeParams) )
			self.shapeProximityTimers[ proximityID ] = timerID
	
	def onShapeProximityCheckTimer( self, rangeXZ, rangeY, proximityID, userArg, shapeType, shapeParams ):
		"""
		检测是否在形状内timer
		"""
		if proximityID not in self.shapeProximityEnters:
			return
		
		shapeIns = g_trapShapeMgr.getShapeIns( shapeType, Math.Vector3(self.position), rangeY, shapeParams )
		if not shapeIns:
			return
		
		#进陷阱检测
		for id in list( self.shapeProximityEnters[ proximityID ] ):
			entity = KBEngine.entities.get( id )
			if not entity:
				self.shapeProximityEnters[ proximityID ].remove( id )
				continue
			
			if shapeIns.isPointIn( Math.Vector3(entity.position), Math.Vector3(self.direction) ):	#当前在形状内
				if proximityID not in self.shapeProximityInners:	#之前没有在形状内
					self.callEnterTrapCB( entity, rangeXZ, rangeY, proximityID, userArg )
					self.shapeProximityInners[ proximityID ] = [ id ]
				
				elif id not in self.shapeProximityInners[proximityID]:
					self.callEnterTrapCB( entity, rangeXZ, rangeY, proximityID, userArg )
					self.shapeProximityInners[ proximityID ].append( id )
		
		#出陷阱检测
		if proximityID in self.shapeProximityInners:
			for id in list( self.shapeProximityInners[proximityID]):
				entity = KBEngine.entities.get( id )
				if not entity:
					self.shapeProximityInners[ proximityID ].remove( id )
					continue
				
				if not shapeIns.isPointIn( Math.Vector3(entity.position), Math.Vector3(self.direction) ):
					self.callLeaveTrapCB( entity, proximityID, userArg )
					self.shapeProximityInners[ proximityID ].remove( id )
	
	#-------------------------------------------
	# 取消陷阱
	#-------------------------------------------
	def cancelProximityByUserArg( self, userArg ):
		"""
		取消陷阱统一接口
		"""
		proximityID = self.findProximityByUserArg( userArg )
		if not proximityID:
			return
		
		isSquare = self.proximityInfo[ proximityID ][3]
		self.cancelController( proximityID )
		self.proximityInfo.pop( proximityID )
		self.entersOnAddProximity.pop( proximityID, {} )
		
		if not isSquare:	#是“其他形状”陷阱
			self.popTimer( self.shapeProximityTimers.pop( proximityID ) )
			self.shapeProximityEnters.pop( proximityID, [] )
			self.shapeProximityInners.pop( proximityID, [] )
	
	#-------------------------------------------
	# KBEngine calback
	#-------------------------------------------
	def onEnterTrap( self, entity, rangeXZ, rangeY, controllerID, userArg = 0 ):
		"""
		进入触发陷阱内
		"""
		if not entity.isReady() or entity.inDestroying():
			return
		
		if controllerID not in self.proximityInfo:	#是刚创建陷阱就触发的情况
			if controllerID in self.entersOnAddProximity:
				if entity.id not in self.entersOnAddProximity[ controllerID ]:
					self.entersOnAddProximity[ controllerID ].append( entity.id )
			else:
				self.entersOnAddProximity[ controllerID ] = [ entity.id ]
			return
		
		isSquare = self.proximityInfo[ controllerID ][3]
		if isSquare:	#方形
			if rangeY > 0 and abs( self.position.y - entity.position.y ) > rangeY:	#引擎的陷阱是一个高度无限延伸的“井”，因此加个高度验证避免在高空也能触发地面的陷阱
				return
			userArg = self.proximityInfo[ controllerID ][0]
			self.callEnterTrapCB( entity, rangeXZ, rangeY, controllerID, userArg )
		
		else:	#是“其他形状”陷阱：只添加到记录，不执行进陷阱回调
			if controllerID not in self.shapeProximityEnters:
				self.shapeProximityEnters[controllerID] = [ entity.id ]
			else:
				self.shapeProximityEnters[controllerID].append( entity.id )
	
	def onLeaveTrap( self, entity, rangeXZ, rangeY, controllerID, userArg = 0 ):
		"""
		离开触发陷阱内
		"""
		if not entity.isReady() or entity.inDestroying():
			return
		
		if controllerID not in self.proximityInfo:
			return
		
		isSquare = self.proximityInfo[ controllerID ][3]
		if isSquare:	#方形
			userArg = self.proximityInfo[ controllerID ][0]
			self.callLeaveTrapCB( entity, controllerID, userArg )
		else:				#是“其他形状”陷阱：只移除记录，不执行离开陷阱回调
			if controllerID in self.shapeProximityEnters and entity.id in self.shapeProximityEnters[controllerID]:
				self.shapeProximityEnters[controllerID].remove( entity.id )
	
	#-------------------------------------------
	# 陷阱被重新触发
	#-------------------------------------------
	def beReTriggerTrap( self, entity, userArg ):
		"""
		"""
		proximityID = self.findProximityByUserArg( userArg )
		if not proximityID:
			return
		
		[ userArg, rangeXZ, rangeY, isSquare ] = self.proximityInfo[ proximityID ]
		if self.position.flatDistTo( entity.position ) > rangeXZ:	#不在陷阱内
			return
		
		if not isSquare:	#是“其他形状”陷阱，清除“已进入”记录
			if proximityID in self.shapeProximityEnters and entity.id in self.shapeProximityEnters[ proximityID ]:
				self.shapeProximityEnters[ proximityID ].remove( entity.id )
			if proximityID in self.shapeProximityInners and entity.id in self.shapeProximityInners[ proximityID ]:
				self.shapeProximityInners[ proximityID ].remove( entity.id )
		
		self.onEnterTrap( entity, rangeXZ, rangeY, proximityID )
	
	#-------------------------------------------
	#基础接口
	#-------------------------------------------
	def callEnterTrapCB( self, entity, rangeXZ, rangeY, controllerID, userArg ):
		"""
		执行进入陷阱回调函数
		"""
		try:
			cbname = ECBProximityDefine.gcbs[ userArg ].split( "|" )[ 0 ]
			cb = getattr( self, cbname )
		except KeyError:
			# ECBExtend.gcbs不包含userArg
			KBEDebug.ERROR_MSG( "ECBCallback cant found call back for userArg ", userArg, self )
			return
		except AttributeError:
			# entity没有实现对应的回调函数
			KBEDebug.ERROR_MSG( "ECBCallback hasnt implement for ", cbname )
			return
		else:
			cb( entity, rangeXZ, rangeY, controllerID )
	
	def callLeaveTrapCB( self, entity, controllerID, userArg ):
		"""
		执行离开陷阱回调函数
		"""
		try:
			cbname = ECBProximityDefine.gcbs[ userArg ].split( "|" )[ 1 ]
			cb = getattr( self, cbname )
		except KeyError:
			# ECBExtend.gcbs不包含userArg
			KBEDebug.ERROR_MSG( "ECBCallback cant found call back for userArg ", userArg, self )
			return
		except AttributeError:
			# entity没有实现对应的回调函数
			KBEDebug.ERROR_MSG( "ECBCallback hasnt implement for ", cbname )
			return
		else:
			cb( entity, controllerID )