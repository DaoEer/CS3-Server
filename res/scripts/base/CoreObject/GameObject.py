# -*- coding: utf-8 -*-

"""
用于所有服务器游戏对象  的基本类型
"""

import KBEngine

import KST
from CoreObject.EntityObject import EntityObject

class GameObject( EntityObject ):
	def __init__( self ):
		EntityObject.__init__( self )
		self.isDestroySelf = False
		
	def createBaseMonster( self, scriptID, spaceCell, position, direction, params ):
		"""
		<define method>
		"""
		self._createBaseMonster( scriptID, spaceCell, position, direction, params )
	
	def _createBaseMonster( self,  scriptID, spaceCell, position, direction, params ):
		"""
		"""
		return KST.g_objFactory.createMonster( scriptID, spaceCell, position, direction, params )

	def createBaseNPC( self, scriptID, spaceCell, position, direction, params ):
		"""
		<define method>
		"""
		self._createBaseNPC( scriptID, spaceCell, position, direction, params )
	
	def _createBaseNPC( self, scriptID, spaceCell, position, direction, params ):
		"""
		"""
		return  KST.g_objFactory.createNPC( scriptID, spaceCell, position, direction, params )

	def destroySelf( self, hasDestroy = False ):
		"""
		<Define method>
		virtual method
		销毁entity唯一入口，用于脚本层功能扩展，比如销毁之前做一些什么事
		"""
		if self.isDestroyed == True:
			return
			
		self.isDestroySelf = True
		if not hasDestroy:
			self.destroy()

	def onDestroy( self ):
		"""
		"""
		self.timerBaseExt.clearReference()
		if not self.isDestroySelf:	#被动销毁（掉线）的情况下，不会走destroySelf流程，这里要另外调用一下
			self.destroySelf( True )
	

    #----------------------timer--------------------------------------------------------------
	def addTimerCallBack( self, delayTime, method, methodArgs ):
		"""
		添加一个计时回调
		@delayTime:执行时间 (秒)
		@method:回调方法
		@methodArgs:回调方法参数
		"""
		return self.timerBaseExt.addTimerCallBack( self, delayTime, method, methodArgs )

	def executeTimer(self, timerID):
		"""
		立即执行一个定时器
		"""
		self.timerBaseExt.executeTimer(self, timerID) 
	
	def addTimerRepeat( self, repeatTime, method, methodArgs ):
		"""
		添加一个循环计时器
		@repeatTime:重复执行时间 (秒)
		@method:回调方法
		@methodArgs:回调方法参数
		"""
		return self.timerBaseExt.addTimerRepeat( self, repeatTime, method, methodArgs )

	def addTimerRepeatNoTickSpeedLimit( self, repeatTime, method, methodArgs ):
		"""
		添加一个循环计时器，帧率最低为0.1，addTimerRepeat的目前为0.5
		@repeatTime:重复执行时间 (秒)
		@method:回调方法
		@methodArgs:回调方法参数
		"""
		return self.timerBaseExt.addTimerRepeatNoTickSpeedLimit( self, repeatTime, method, methodArgs )

	def addTimerRepeatExt(self, delayTime, repeatTime, method, methodArgs):
		"""
		添加一个循环计时器
		@delayTime:定时器从注册到第一次回调的时间间隔
		@repeatTime:重复执行时间 (秒)
		@method:回调方法
		@methodArgs:回调方法参数
		"""
		return self.timerBaseExt.addTimerRepeatExt(self, delayTime, repeatTime, method, methodArgs)

	
	def popTimer( self, timerArg ):
		"""
		移除一个timer
		timerArg添加定时器时返回的参数
		"""
		self.timerBaseExt.popTimer( self, timerArg )
		
	def timerValeDelCB( self, timerArg ):
		"""
		取消一个timer arg的回调，也可能是执行完了
		这里主要是处理掉一些存起来的timerArg
		"""
		pass
	
	def onTimer( self, tid, userArg ):
		self.timerBaseExt.onTimer( self, tid, userArg )
	
	# timer for script
	def addTimerCallBackForScript( self, delayTime, method, methodArgs ):
		"""
		添加一个计时回调
		@delayTime:执行时间 (秒)
		@method:回调方法
		@methodArgs:回调方法参数
		"""
		return self.addTimerCallBack( delayTime, "onTimerScript", ( method, methodArgs ) )
	
	def addTimerRepeatForScript( self, repeatTime, method, methodArgs ):
		"""
		添加一个循环计时器
		@repeatTime:重复执行时间 (秒)
		@method:回调方法
		@methodArgs:回调方法参数
		"""
		return self.addTimerRepeat( repeatTime, "onTimerScript", ( method, methodArgs ) )

	def addTimerRepeatExtForScript( self, delayTime, repeatTime, method, methodArgs):
		"""
		添加一个循环计时器
		@delayTime:定时器从注册到第一次回调的时间间隔
		@repeatTime:重复执行时间 (秒)
		@method:回调方法
		@methodArgs:回调方法参数
		"""
		return self.addTimerRepeatExt(self, delayTime, repeatTime, method, methodArgs)
	
	def onTimerScript( self, method, args ):
		"""
		脚本层的回调
		"""
		newArgList = []
		newArgList.append( self )
		newArgList.extend( args )
		getattr( self.getScript(), method )( *newArgList )
    