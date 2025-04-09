# -*- coding: utf-8 -*-

import copy
import KBEngine
import KBEDebug

class TimerExt( dict ):
	def __init__( self ):
		dict.__init__( self )
		self.timeIndex = 0
		self.timerCallCache = {}
		self.executing = set()

	def __getTimerArgValue( self ):
		self.timeIndex += 1
		if self.timeIndex > 4294967295: #防止超出uint64
			self.timeIndex = 1
		if self.timeIndex in self:
			return self.__getTimerArgValue() #这里只会存在理论上的死循环机会
		else:
			return self.timeIndex
		
	def addTimerRepeat( self, selfObject, repeatTime, method, methodArgs ):
		"""
		添加一个循环计时器
		"""
		if type(repeatTime) != int and type(repeatTime) != float:
			KBEDebug.ERROR_MSG("time type error!!!selfObject:%s repeatTime:%s method:%s methodArgs:%s"%(selfObject, repeatTime, method, methodArgs))
		if repeatTime < 0:
			KBEDebug.ERROR_MSG("timer interval < 0!!!selfObject:%s repeatTime:%s method:%s methodArgs:%s"%(selfObject, repeatTime, method, methodArgs))
		
		repeatTime = max(repeatTime, 0.5)
		argValue = self.__getTimerArgValue()
		self[ argValue ] = None
		timerID = selfObject.addTimer( repeatTime, 0.0, argValue )
		self[ argValue ] = ( method, copy.copy( methodArgs ), repeatTime, timerID )
		return argValue

	def addTimerRepeatNoTickSpeedLimit(self, selfObject, repeatTime, method, methodArgs):
		if type(repeatTime) != int and type(repeatTime) != float:
			KBEDebug.ERROR_MSG("time type error!!!selfObject:%s repeatTime:%s method:%s methodArgs:%s" % (
			selfObject, repeatTime, method, methodArgs))
		if repeatTime < 0:
			KBEDebug.ERROR_MSG("timer interval < 0!!!selfObject:%s repeatTime:%s method:%s methodArgs:%s" % (
			selfObject, repeatTime, method, methodArgs))

		repeatTime = max(repeatTime, 0.1)
		argValue = self.__getTimerArgValue()
		self[argValue] = None
		timerID = selfObject.addTimer(repeatTime, 0.0, argValue)
		self[argValue] = (method, copy.copy(methodArgs), repeatTime, timerID)
		return argValue

	def addTimerRepeatExt(self, selfObject, delayTime, repeatTime, method, methodArgs):
		"""
		"""
		if (type(delayTime) != int and type(delayTime) != float) or (type(repeatTime) != int and type(repeatTime)!= float):
			KBEDebug.ERROR_MSG("time type error!!!selfObject:%s delayTime:%s repeatTime:%s method:%s methodArgs:%s"%(selfObject, delayTime, repeatTime, method, methodArgs))
		if repeatTime < 0 or delayTime < 0:
			KBEDebug.ERROR_MSG("timer interval < 0!!!selfObject:%s delayTime:%s repeatTime:%s method:%s methodArgs:%s"%(selfObject, delayTime, repeatTime, method, methodArgs))
		
		delayTime = max(delayTime, 0.5)
		repeatTime = max(repeatTime, 0.5)
		argValue = self.__getTimerArgValue()
		self[ argValue ] = None
		timerID = selfObject.addTimer( delayTime, 0.0, argValue )
		self[ argValue ] = ( method, copy.copy( methodArgs ), repeatTime, timerID )
		return argValue

	def addTimerCallBack( self, selfObject, delayTime, method, methodArgs ):
		"""
		添加一个计时器回调
		"""
		argValue = self.__getTimerArgValue()
		if type(delayTime) != int and type(delayTime) != float:
			KBEDebug.ERROR_MSG("time type error!!!selfObject:%s delayTime:%s method:%s methodArgs:%s"%(selfObject, delayTime, method, methodArgs))
		if delayTime < 0:
			KBEDebug.ERROR_MSG("timer interval < 0!!!selfObject:%s delayTime:%s method:%s methodArgs:%s"%(selfObject, delayTime, method, methodArgs))
		
		delayTime = max(delayTime, 0.5)
		argValue = self.__getTimerArgValue()
		self[ argValue ] = None
		timerID = selfObject.addTimer( delayTime, 0.0, argValue )
		self[ argValue ] = ( method, copy.copy( methodArgs ), 0.0, timerID )
		return argValue
	
	def executeTimer(self, selfObject, argValue):
		"""
		立即执行一个定时器
		"""
		if not argValue in self:
			return
		
		self.executing.add(argValue)

		method, methodArgs, repeatTime, timerID = self[argValue]
		
		self.getObjectMethod( selfObject, method )( *methodArgs )
		if argValue in self:
			self.pop(argValue)
		selfObject.delTimer(timerID)

		if repeatTime>0:
			repeatTime = max(repeatTime, 0.5)
			timerID = selfObject.addTimer(repeatTime, 0.0, argValue)
			self[ argValue ] = ( method, methodArgs, repeatTime, timerID )
		else:
			selfObject.timerValeDelCB( argValue )

		self.executing.remove(argValue)


	def popTimer( self, selfObject, argValue ):
		"""
		删除一个计时器
		"""
		if argValue in self:
			timerID = self.pop( argValue )[3]
			selfObject.delTimer( timerID )
			selfObject.timerValeDelCB( argValue )
		#else:
		#	KBEDebug.WARNING_MSG( "popTimer Error!!entityID:%d, argValue: %s"%( selfObject.id, argValue) )
	
	def hasTimer( self, argValue ):
		"""
		是否存在一个计时器
		"""
		return argValue in self
	
	def onTimer( self, selfObject, timerID, argValue ):
		"""
		定时器回调
		"""
		if selfObject.isDestroyed:
			return
			
		if argValue not in self:
			KBEDebug.ERROR_MSG( "object's( %s ) timer argValue:%d is remove!!"%( str( selfObject.id ), argValue ) )
			return
			
		if argValue in self.executing:
			KBEDebug.ERROR_MSG("object's id:(%d) object's classname:%s timer argValue:%d is executing!"%(selfObject.id, selfObject.__class__.__name__, argValue))
			return

		method, methodArgs, repeatTime = self[ argValue ][:3]
		self.getObjectMethod( selfObject, method )( *methodArgs )
		if repeatTime == 0 and argValue in self: #后面一个判断是防止在回调方法里面做删除处理出错
			self.pop( argValue )
			selfObject.timerValeDelCB( argValue )
		elif repeatTime > 0 and argValue in self:
			selfObject.delTimer(timerID)
			timerID = selfObject.addTimer( repeatTime, 0, argValue )
			self[ argValue ] = ( method, methodArgs, repeatTime, timerID )
	
	def getObjectMethod( self, selfObject, methodName ):
		if methodName not in self.timerCallCache:
			self.timerCallCache[ methodName ] = getattr( selfObject, methodName )
		
		return self.timerCallCache[ methodName ]
	
	def clearReference( self ):
		"""
		清理引用，防止内存泄漏
		"""
		self.timerCallCache = {}

#-----------------------------------for KBEngine--------------------------------------------------------
	def getDictFromObj( self, obj ):
		"""
		"""
		dataList = []
		for argValue, record in obj.items():
			method, methodArgs, repeatTime, timerID = record
			tempDict = {}
			tempDict[ "argValue" ] = argValue
			tempDict[ "method" ] = method
			tempDict[ "methodArgs" ] = methodArgs
			tempDict[ "repeatTime" ] = repeatTime
			tempDict[ "timerID" ] = timerID
			dataList.append( tempDict )
		
		proDict = {}
		proDict[ "datas" ] = dataList
		proDict[ "timeIndex" ] = obj.timeIndex
		if KBEngine.component == "cellapp" and len( obj.timerCallCache ):
			obj.clearReference()
			
		return proDict
		
	def createObjFromDict( self, proDict ):
		"""
		"""
		obj = TimerExt()
		for tdata in proDict[ "datas" ]:
			obj[ tdata[ "argValue" ] ] = ( tdata[ "method" ], tdata[ "methodArgs" ], tdata[ "repeatTime" ], tdata[ "timerID" ] )
		
		obj.timeIndex = proDict[ "timeIndex" ]
		return obj
		
	def isSameType( self, obj ):
		"""
		"""
		return isinstance( obj, TimerExt )


instance = TimerExt()