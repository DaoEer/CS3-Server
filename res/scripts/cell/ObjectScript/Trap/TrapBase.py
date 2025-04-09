# -*- coding: utf-8 -*-

import KBEngine
import KBEDebug
from ObjectScript.ObjectScriptBase.NPCBaseScript import NPCBaseScript
from ObjectScript.Trap.TrapPropertyLoader import TrapPropertyLoader
from ObjectScript.Trap.Condition.TrapCondition import g_trapConditionMgr
from ObjectScript.Trap.Action.TrapActionMgr import g_trapActionMgr

class TrapBase( NPCBaseScript, TrapPropertyLoader ):
	"""
	陷阱对象script基础类
	"""
	def __init__( self ):
		NPCBaseScript.__init__( self )
		TrapPropertyLoader.__init__( self )
		self.initAction = {}						# 初始行为
		self.condition = {}
		self.enterAction = {}						# 普通行为
		self.leaveAction = {}
		self.cycleAction = {}						# 周期行为
		self.holdAction = {}						# 持有行为
		
		self.moveSpeed = 0
		self.maxMoveSpeed = 0
		self.vortexSpeed = 0.0
	
	def initData( self, data ):
		"""
		初始化数据
		@param data: dict
		"""
		NPCBaseScript.initData( self, data )
		TrapPropertyLoader.initData( self, data )
		if "MoveSpeed" in data:		#走路速度
			self.moveSpeed = float(data["MoveSpeed"])
		if "MaxMoveSpeed" in data:	#最大行走速度
			self.maxMoveSpeed = float(data["MaxMoveSpeed"])
		if "vortexSpeed" in data:	#最大行走速度
			self.vortexSpeed = float(data["vortexSpeed"])
		try:
			if "initAction" in data:
				for value in data["initAction"]:
					parms = []
					for num in range( 1, 4 ):
						v = value["param" + str(num)]
						if v != None and v != "":
							parms.append( v )
					self.initAction[value["scriptKey"]] = parms
		except KeyError as e :
			KBEDebug.CRITICAL_MSG( "Trap ( %s ) Config Error:  initAction( %s ) ErrorKey:%s"%( self.scriptID, str( data["initAction"] ), e ) )
		
		try:
			for value in data["condition"]:
				parms = []
				for num in range( 1, 4 ):
					v = value["param" + str(num)]
					if v != None and v != "":
						parms.append( v )
				self.condition[value["scriptKey"]] = parms
		except KeyError as e :
			KBEDebug.CRITICAL_MSG( "Trap ( %s ) Config Error:  condition( %s ) ErrorKey:%s"%( self.scriptID, str( data["condition"] ), e ) )
		
		try:
			for index, value in enumerate(data["onEnterAction"]):
				parms = []
				for num in range( 1, 4 ):
					v = value["param" + str(num)]
					if v != None and v != "":
						parms.append( v )
				
				doOnce = False
				if "doOnce" in value:
					doOnce = bool(value["doOnce"])
				self.enterAction[ index ] = ( value["scriptKey"], parms, doOnce )
		except KeyError as e :
			KBEDebug.CRITICAL_MSG( "Trap ( %s ) Config Error:  onEnterAction( %s ) ErrorKey:%s"%( self.scriptID, str( data["onEnterAction"] ), e ) )
		
		try:
			for index, value in enumerate(data["onLeaveAction"]):
				parms = []
				for num in range( 1, 4 ):
					v = value["param" + str(num)]
					if v != None and v != "":
						parms.append( v )
				
				doOnce = False
				if "doOnce" in value:
					doOnce = bool(value["doOnce"])
				self.leaveAction[ index ] = ( value["scriptKey"], parms, doOnce )
		except KeyError as e :
			KBEDebug.CRITICAL_MSG( "Trap ( %s ) Config Error:  onLeaveAction( %s ) ErrorKey:%s"%( self.scriptID, str( data["onLeaveAction"] ), e ) )
		
		try:
			if "cycleAction" in data:
				for value in data["cycleAction"]:
					self.cycleAction[value["scriptKey"]] = value
		except KeyError as e :
			KBEDebug.CRITICAL_MSG( "Trap ( %s ) Config Error:  cycleAction( %s ) ErrorKey:%s"%( self.scriptID, str( data["cycleAction"] ), e ) )
		
		try:
			if "holdAction" in data:
				for value in data["holdAction"]:
					parms = []
					for num in range( 1, 4 ):
						v = value["param" + str(num)]
						if v != None and v != "":
							parms.append( v )
					self.holdAction[value["scriptKey"]] = parms
		except KeyError as e :
			KBEDebug.CRITICAL_MSG( "Trap ( %s ) Config Error:  holdAction( %s ) ErrorKey:%s"%( self.scriptID, str( data["holdAction"] ), e ) )
			
	def getEntityProperties( self, params ):
		return TrapPropertyLoader.getEntityProperties( self, params )
	
	def getRunSpeed( self, selfEntity ):
		""""""
		return self.runSpeed
		
	def getWalkSpeed( self, selfEntity ):
		""""""
		return self.walkSpeed

	def initEntity( self, selfEntity ):
		"""
		virtual method.
		陷阱初始化
		"""
		for key, value in self.initAction.items():
			g_trapActionMgr.init( selfEntity, key, value )

	def triggerValidate( self, selfEntity, enterEntity ):
		"""
		virtual method.
		陷阱是否触发验证
		"""
		return True

	def onEnterTrap( self, selfEntity, enterID ):
		"""
		virtual method.
		进入陷阱
		"""
		if enterID == selfEntity.id:
			return
		
		enterEntity = KBEngine.entities.get( enterID , None )
		if enterEntity == None:
			return
		
		for key, value in self.holdAction.items():
			g_trapActionMgr.holdBegin( selfEntity, enterEntity, key, value )

		for key, value in self.condition.items():
			if not g_trapConditionMgr.validate( selfEntity, enterEntity, key, value ):
				return

		for index, info in self.enterAction.items():
			doOnce = info[2]
			if doOnce and ( index in selfEntity.enterActionRecd ):		#只执行一次
				continue
			
			g_trapActionMgr.action( selfEntity, enterEntity, info[0], info[1] )
			
			if doOnce:
				selfEntity.enterActionRecd.append( index )
	
	def onLeaveTrap( self, selfEntity, enterID ):
		"""
		virtual method.
		离开陷阱
		"""
		if enterID == selfEntity.id:
			return

		enterEntity = KBEngine.entities.get( enterID , None )
		if enterEntity == None:
			return
			
		for key, value in self.holdAction.items():
			g_trapActionMgr.holdEnd( selfEntity, enterEntity, key, value )

		for key, value in self.condition.items():
			if not g_trapConditionMgr.validate( selfEntity, enterEntity, key, value ):
				return

		for index, info in self.leaveAction.items():
			doOnce = info[2]
			if doOnce and ( index in selfEntity.leaveActionRecd ):		#只执行一次
				continue
			
			g_trapActionMgr.action( selfEntity, enterEntity, info[0], info[1] )
			
			if doOnce:
				selfEntity.leaveActionRecd.append( index )
	
	def onEnterClientTrap( self, selfEntity, enterID ):
		"""
		virtual method.
		进入客户端陷阱
		"""
		pass
		
	def onLeaveClientTrap( self, selfEntity, enterID ):
		"""
		virtual method.
		离开客户端陷阱
		"""
		pass

	#---------------------------------陷阱周期行为-------------------------------------------------------------------------
	def onWitnessed( self, selfEntity, isWitnessed ):
		"""
		玩家视野范围内才开始执行
		"""
		# if isWitnessed:
		# 	for index, value in self.cycleAction.items():
		# 		g_trapActionMgr.cycleBegin( selfEntity, index, value )
		# else:
		# 	for index, value in self.cycleAction.items():
		# 		g_trapActionMgr.cycleEnd( selfEntity, index, value )
		
		#CST-3704 按策划需求 周期性行为需要延迟触发
		pass


	def cycleBegin(self, selfEntity):
		"""
		延时开启周期行为
		"""
		for index, value in self.cycleAction.items():
			g_trapActionMgr.cycleBegin( selfEntity, index, value )
	
	
	def cycleDo( self, selfEntity, type, value ):
		"""执行周期行为"""
		g_trapActionMgr.cycleDo( selfEntity, type, value )
		
	def onEnterDead( self, selfEntity ):
		"""进入死亡状态"""
		for index, value in self.cycleAction.items():
			g_trapActionMgr.cycleEnd( selfEntity, index, value )

