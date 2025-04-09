# -*- coding: utf-8 -*-


"""
用于所有游戏对象派生出来的基类
"""

#python
import random
#engine
import KBEngine
import Math
#cell
import CoreObject.EntityObject as EntityObject
from KBEDebug import *
from ObjectScript.ObjectScriptFactory import g_objFactory
from ConfigObject.SpaceEntityRelation.SpaceEntityRelationLoader import g_spaceEntityRelationLoader
import CoreInterface.EntityEventInterface as EntityEventInterface

import KST
import Const
import csdefine
import csconst

import KBEDebug

class GameObject( EntityObject.EntityObject, EntityEventInterface.EntityEventInterface ):
	"""
	游戏对象基类
	"""
	def __init__( self ):
		EntityObject.EntityObject.__init__( self )
		EntityEventInterface.EntityEventInterface.__init__(self)
		self.keepChangeModelScaleTimerID = 0 #模型持续改变定时器
		self._scriptObject = None
		KST.calculateCreateEntity(self.getEntityFlag())

	def onEnterSpace( self ):
		"""
		KBEngine callback
		进入一个空间调用
		"""
		self.doEnterSpace()

	
	def doEnterSpace( self ):
		"""
		进入空间前要做的事，例如一些与客户相关的临时变量声明或者赋值
		:return: None
		"""
		self._scriptObject = None

	def onLeaveSpace( self ):
		"""
		KBEngine callback
		离开一个空间调用（在doEnterSpace之后）
		"""
		self.doLeaveSpace()

	def doLeaveSpace( self ):
		"""
		离开空间前要做的事，例如一些与客户相关的临时变量声明或者赋值
		:return: None
		"""
		pass


	def onTeleportSuccess( self, nearbyEntity ):
		"""
		传送成功
		KBEngine callback
		:param nearbyEntity:teleport对象
		:return:None
		"""
		self.doTeleportSuccess( nearbyEntity )

	def doTeleportSuccess( self, nearbyEntity ):
		"""
		传送完成要处理的内容
		:param nearbyEntity:
		:return:
		"""
		pass

	def onTeleportFailure(self):
		"""
		传送失败
		KBEngine callback
		:return:
		"""
		self.doTeleportFailure()

	def doTeleportFailure( self ):
		"""
		传送失败要处理的内容
		:param nearbyEntity:
		:return:
		"""
		pass

	def CELL_onClientReady(self, srcEntityID):
		"""
		<Expose method>
		客户端Character Actor已经准备好
		"""
		pass

	def isCombatEntity( self ):
		"""
		是不是战斗entity
		"""
		return self.entityFlag in csdefine.COMBAT_ENTITY_FLAG_LIST

	def isReady( self ):
		"""
		判断entity是否准备好了，在某些情况下（玩家传送界面还没加载好）不让该entity进行触发陷阱，关系建立，不被AI搜索等等
		"""
		if self.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE or  self.getEntityFlag() == csdefine.ENTITY_FLAG_MONSTER:
			if self.state == csdefine.ENTITY_STATE_PEAD:
				return False
				
		return True

	def destroySelf( self, hasDestroy = False ):
		"""
		销毁entity唯一入口，用于脚本层功能扩展，比如销毁之前做一些什么事
		"""
		if self.isDestroyed or self.isDestroySelf:
			return
			
		self.isDestroySelf = True
		self.beforeDestroy()
		if not hasDestroy:
			self.destroy()

	def beforeDestroy( self ):
		"""
		virtual method
		销毁前做一些事
		"""
		#取消所有entity事件订阅
		self.entityEventUnsubscribeAllEvents()
		self.resetArmyModelList()

		
	def onDestroy( self ):
		"""
		"""
		self.timerCellExt.clearReference()
		if not self.isDestroySelf:	#被动销毁（掉线）的情况下，不会走destroySelf流程，这里要另外调用一下
			self.destroySelf( True )
		KST.calculateDestroyEntity(self.getEntityFlag())

	def inDestroying( self ):
		"""
		正在销毁或已经销毁
		"""
		return self.isDestroyed or self.isDestroySelf

	def destroyCellByBase( self ):
		"""
		<define method>
		base请求销毁cell
		"""
		self.destroySelf()
	
	def delayDestroy( self, delayTime ):
		"""
		延时销毁
		"""
		self.addTimerCallBack( delayTime, "destroySelf", () )
#----------------------基础属性--------------------------------------------------------------
	def getScript( self ):
		return None
	
	def getScriptID( self ):
		return self.getScriptProperty( "scriptID", "" )
	
	def getScriptProperty( self, name, defaultValue = None ):
		if self.getScript():
			return self.getScript().getEntityProperty( name, defaultValue )
		else:
			return defaultValue
	
	def getName( self ):
		"""
		virtual method
		获取名称
		"""
		return ""

#----------------临时数据---------------------------------------
	def setTemp( self, key, value ):
		"""
		"""
		self.tempMapping[key] = value

	def queryTemp( self, key, default = None ):
		"""
		"""
		try:
			return self.tempMapping[key]
		except KeyError:
			return default

	def removeTemp( self, key ):
		"""
		"""
		if key in self.tempMapping:
			return self.tempMapping.pop(key,None)

#----------------------space--------------------------------------------------------------	
	def getCurrentSpaceData( self, key ):
		return KBEngine.getSpaceData( self.spaceID, key )
	
	def setCurrentSpaceData( self, key, value ):
		KBEngine.setSpaceData( self.spaceID, key, value )
	
	def getCurrentSpaceBase( self ):
		return KBEngine.cellAppData.get( Const.GET_SPACE_CELLAPP_KEY( self.spaceID ), None )
	
	def getCurrentSpace( self ):
		spaceBase = self.getCurrentSpaceBase()
		if spaceBase:
			return KBEngine.entities.get( spaceBase.id, None )
		else:
			return None
	
	def getCurrentSpaceObject( self ):
		return g_objFactory.getSpaceObject( self.getCurrentSpaceScriptID() )
	
	def getCurrentSpaceScriptID( self ):
		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			return spaceEntity.scriptID
		return None
	
	def isInSpaceCopy( self ):
		"""
		是否在副本中
		"""
		from SpaceCopy import SpaceCopy
		spaceEntity = self.getCurrentSpace()
		if isinstance( spaceEntity, SpaceCopy ):
			return True
		return False
	
	def isInSpacePlane( self ):
		"""
		是否在位面中
		"""
		from SpacePlane import SpacePlane
		spaceEntity = self.getCurrentSpace()
		if isinstance( spaceEntity, SpacePlane ):
			return True
		return False

#----------------------create entity------------------------------------------------------

	def createNPC( self, scriptID, position, direction, params  ):
		"""
		创建一个NPC
		"""
		sciprtObj = KST.g_objFactory.getNPCObject( scriptID )
		newEntity = None
		if sciprtObj:
			newEntity = sciprtObj.createEntity( self.getCurrentSpace(), tuple(Math.Vector3(position)), direction, params  )
		return newEntity
	
	def createMonster( self, scriptID, position, direction, params  ):
		"""
		创建一个怪物
		"""
		sciprtObj = KST.g_objFactory.getMonsterObject( scriptID )
		newEntity = None
		if sciprtObj:
			newEntity = sciprtObj.createEntity( self.getCurrentSpace(), tuple(Math.Vector3(position)), direction, params  )
		return newEntity

	def hasParent(self):
		"""
		是否在移动平台上
		"""
		return self.parent
	
	def getParentNavigatePoint( self, targetPos, layer = 0,  flags = 0xFFFF ):
		"""
		注：targetPos是相对于移动平台的坐标，非世界坐标
		"""
		distance = 1.0
		newX = targetPos.x + random.randint( 0,  distance )
		newZ = targetPos.z + random.randint( 0,  distance )
		newY = targetPos.y
		newPosition = Math.Vector3( ( newX, newY, newY ) )
		if self.parent:
			parentNavPaths = KBEngine.navigatePathPoints( self.parent.getNavmeshPath(), targetPos, newPosition, 0xFFFF, layer, flags )
			if parentNavPaths:
				return parentNavPaths[0]
		
		return self.parent.positionLocalToWorld( targetPos )
	
	def createMonsterOnParent( self, targetPos, targetDir, scriptID, params ):
		"""
		注：targetPos是相对于移动平台的坐标，非世界坐标
		"""
		targetParentPos = self.parent.positionWorldToLocal( targetPos ) #转换坐标为相对坐标
		#targetParentDir = self.parent.directionWorldToLocal( targetDir ) #转换面向为相对面向
		pos = self.getParentNavigatePoint( targetParentPos )
		params[ "parent" ] = self.parent
		entity = self.createMonster( scriptID, pos, targetDir, params )
		entity.parent = self.parent
		return entity
	
	def createSpellBox( self, scriptID, position, direction, params  ):
		"""
		创建一个spellbox
		"""
		sciprtObj = KST.g_objFactory.getSpellBoxObject( scriptID )
		newEntity = None
		if sciprtObj:
			newEntity = sciprtObj.createEntity( self.getCurrentSpace(), tuple(Math.Vector3(position)), direction, params  )
		return newEntity

	def createTrap( self, scriptID, position, direction, params  ):
		"""
		创建一个spellbox
		"""
		sciprtObj = KST.g_objFactory.getTrapBoxObject( scriptID )
		newEntity = None
		if sciprtObj:
			newEntity = sciprtObj.createEntity( self.getCurrentSpace(), tuple(Math.Vector3(position)), direction, params  )
		return newEntity
	
	def createEntityNear( self, entityType, position, direction, params  ):
		"""
		virtual method.
		创建一个entity, 近距离
		@param npcID: STRING, 非玩家控制对象的唯一标识
		@param position: 创建的目标位置
		@param direction: 创建的目标方向
		@param state: see also: cell::KBEngine.createEntity()
		@return: new entity
		"""
		return KBEngine.createEntity( entityType, self.spaceID, tuple(Math.Vector3(position)), direction, params  )

	def createEntityByScriptID( self, scriptID, position, direction, params):
		"""
		根据scriptID自动选择创建entity
		"""
		return KST.g_objFactory.createEntity( scriptID, self.getCurrentSpace(), tuple(Math.Vector3(position)), direction, params  )
#----------------------函数调用--------------------------------
	def remoteCall( self, name, args ):
		"""
		<define method>
		远程方法调用，此方法用于让其它cellapp、baseapp调用未在.def中声明的方法；
		此方法在cellapp/baseapp调用clientapp的未声明方法最有价值，这样可以减少.def中client的声明方法，以其达到网络数据最少占用率。
		client top-level property Efficient to 61 (limit is 256)
		client method Efficient to 62 (limit is 15872)
		base method Efficient to 62 (limit is 15872)
		cell method Efficient to 62 (limit is 15872)

		@param name: STRING; 要调用的方法名称
		@param args: PY_ARGS; 被调用方法的参数列表，具体参数个数由各方法自行处理；
		"""
		try:
			method = getattr( self, name )
		except AttributeError as errstr:
			ERROR_MSG( "%s(%i): class %s has no method %s." % (self.getName(), self.id, self.__class__.__name__, name) )
			return
		method( *args )

	def remoteScriptCall( self, name, args ):
		"""
		<define method>
		远程脚本方法调用，以此接口所属的entity为realEntity，调用自己相关联的脚本上的某个方法；
		此方法主要用于简化使用次数不多的脚本中的特定功能代码。

		@param name: STRING; 要调用的方法名称
		@param args: PY_ARGS; 被调用方法的参数列表，具体参数个数由各方法自行处理；
		"""
		scriptClass = self.getScript()

		try:
			method = getattr( scriptClass, name )
		except AttributeError as errstr:
			ERROR_MSG( "%s(%i): class %s has no method %s." % (self.getName(), self.id, scriptClass.__class__.__name__, name) )
			return
		method( self, *args )

#---------------位置方向相关------------------------------------------------------------------
	def setDirection(self, direction):
		"""
		"""
		self.direction = direction
	
	def setPosition(self, position):
		"""
		"""
		self.position = position

	def distanceBB( self, destEntity ):
		"""
		计算与目标entity之间的3D坐标系的距离
		"""
		return self.position.distTo( destEntity.position )
	
	def getDistToEntityForSkill( self, destEntity ):
		if self.parent != None and self.parent == destEntity.parent:
			return Math.Vector3( ( self.localPosition.x, 0, self.localPosition.z ) ).distTo(  ( destEntity.localPosition.x, 0, destEntity.localPosition.z ) )
		
		return self.distanceBB( destEntity )

	def getYaw( self ):
		"""
		获取yaw值
		"""
		return self.direction.z

	def changeDirection(self, direction, reason= csdefine.REASON_CHANGE_DIR_FORCE):
		"""
		改变朝向 需要判断是主动设置还是被动设置 事务见:CST-7630 程序功能需求（0级）—— "禁止转向"设定优化
		"""
		#主动改变朝向
		if reason == csdefine.REASON_CHANGE_DIR_VOLUNTARY:
			if self.hasActFlag and self.actionForbidSign(csdefine.ACTION_FORBID_TRANSLATE_DIRECTION):
				return
				
		self.setDirection(direction)
#----------------------timer--------------------------------------------------------------
	def addTimerCallBack( self, delayTime, method, methodArgs ):
		"""
		添加一个计时回调
		@delayTime:执行时间 (秒)
		@method:回调方法
		@methodArgs:回调方法参数
		"""
		return self.timerCellExt.addTimerCallBack( self, delayTime, method, methodArgs )
	
	def executeTimer(self, timerID):
		"""
		立即执行一个定时器
		"""
		self.timerCellExt.executeTimer(self, timerID) 

	def addTimerRepeat( self, repeatTime, method, methodArgs ):
		"""
		添加一个循环计时器
		@repeatTime:重复执行时间 (秒)
		@method:回调方法
		@methodArgs:回调方法参数
		"""
		return self.timerCellExt.addTimerRepeat( self, repeatTime, method, methodArgs )

	def addTimerRepeatNoTickSpeedLimit( self, repeatTime, method, methodArgs ):
		"""
		添加一个循环计时器，帧率最低为0.1，addTimerRepeat的目前为0.5
		@repeatTime:重复执行时间 (秒)
		@method:回调方法
		@methodArgs:回调方法参数
		"""
		return self.timerCellExt.addTimerRepeatNoTickSpeedLimit( self, repeatTime, method, methodArgs )
		
	def addTimerRepeatExt(self, delayTime, repeatTime, method, methodArgs):
		"""
		添加一个循环计时器
		@delayTime:定时器从注册到第一次回调的时间间隔
		@repeatTime:重复执行时间 (秒)
		@method:回调方法
		@methodArgs:回调方法参数
		"""
		return self.timerCellExt.addTimerRepeatExt(self, delayTime, repeatTime, method, methodArgs)
	
	def popTimer( self, timerArg ):
		"""
		移除一个timer
		timerArg添加定时器时返回的参数
		"""
		self.timerCellExt.popTimer( self, timerArg )
	
	def hasTimer( self, timerArg ):
		"""
		是否存在一个timer
		timerArg添加定时器时返回的参数
		"""
		return self.timerCellExt.hasTimer( timerArg )
	
	def timerValeDelCB( self, timerArg ):
		"""
		取消一个timer arg的回调，也可能是执行完了
		这里主要是处理掉一些存起来的timerArg
		"""
		pass
	
	def onTimer( self, tid, userArg ):
		self.timerCellExt.onTimer( self, tid, userArg )
	
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
	
	def onTimerScript( self, method, args ):
		"""
		脚本层的回调
		"""
		newArgList = []
		newArgList.append( self )
		newArgList.extend( args )
		getattr( self.getScript(), method )( *newArgList )

#-----------标志位功能---------------------------
	def setFlag( self, flag ):
		"""
		重新设置标志

		@param flag: ENTITY_FLAG_* 左移后组合的值
		@type  flag: INT
		"""
		oldFlags = self.flags
		self.flags = flag
		self.onFlagChange( oldFlags, self.flags )

	def addFlag( self, flag ):
		"""
		增加设置标志
		@param flag: ENTITY_FLAG_*
		@type  flag: INT
		"""
		oldFlags = self.flags
		flag = 1 << flag
		self.flags |= flag
		self.onFlagChange( oldFlags, self.flags )

	def removeFlag( self, flag ):
		"""
		移出标志

		@param flag: ENTITY_FLAG_*
		@type  flag: INT
		"""
		oldFlags = self.flags
		# 第0位系统保留，64位整型
		flag = 1 << flag
		self.flags &= flag ^ 0x7FFFFFFFFFFFFFFF
		self.onFlagChange( oldFlags, self.flags )

	def onFlagChange( self, oldFlags, newFlags ):
		"""
		标志位改变
		"""
		pass

	def hasFlag( self, flag ):
		"""
		判断一个entity是否有指定的标志

		@param flag: ENTITY_FLAG_*
		@type  flag: INT
		@return: BOOL
		"""
		flag = 1 << flag
		return ( self.flags & flag ) == flag

#-----------entity调试标志位功能---------------------------
	def setDebugFlag( self, debugFlag ):
		"""
		直接设置调试标志

		@param flag: ENTITY_DEBUG_FLAG_* 左移后组合的值
		@type  flag: INT
		"""
		self.debugFlags = debugFlag

	def addDebugFlag( self, debugFlag ):
		"""
		添加调试标志

		@param flag: ENTITY_DEBUG_FLAG_*
		@type  flag: INT
		"""
		debugFlag = 1 << debugFlag
		self.debugFlags |= debugFlag

	def removeDebugFlag( self, debugFlag ):
		"""
		移除调试标志

		@param flag: ENTITY_DEBUG_FLAG_*
		@type  flag: INT
		"""
		# 第0位系统保留，32位整型
		debugFlag = 1 << debugFlag
		self.debugFlags &= debugFlag ^ 0x7FFFFFFF

	def hasDebugFlag( self, debugFlag ):
		"""
		判断一个entity是否有指定的标志

		@param flag: ENTITY_DEBUG_FLAG_*
		@type  flag: INT
		@return: BOOL
		"""
		debugFlag = 1 << debugFlag
		return ( self.debugFlags & debugFlag ) == debugFlag

#-----------entity状态标志位功能(程序内部使用)---------------------------
	def setStateFlag( self, stateFlag ):
		"""
		重新设置标志
		"""
		oldStateFlags = self.stateFlags
		self.stateFlags = stateFlag
		self.onFlagChange( oldStateFlags, self.stateFlags )

	def addStateFlag( self, stateFlag ):
		"""
		增加设置标志
		"""
		oldStateFlags = self.stateFlags
		stateFlag = 1 << stateFlag
		self.stateFlags |= stateFlag
		self.onFlagChange( oldStateFlags, self.stateFlags )

	def removeStateFlag( self, stateFlag ):
		"""
		移出标志
		"""
		oldStateFlags = self.stateFlags
		# 第0位系统保留，64位整型
		stateFlag = 1 << stateFlag
		self.stateFlags &= stateFlag ^ 0x7FFFFFFFFFFFFFFF
		self.onFlagChange( oldStateFlags, self.stateFlags )

	def isHasStateFlag( self, stateFlag ):
		"""
		判断一个entity是否有指定的标志
		"""
		stateFlag = 1 << stateFlag
		return ( self.stateFlags & stateFlag ) == stateFlag

#-------------客户端同步位置--------------------------------------------------------
	def setSyncPosClient( self, clientPlayerID ):
		self.SyncPosClient = clientPlayerID

	def getSyncPosClient( self ):
		return self.SyncPosClient

	def syncPosToServer( self, srcEntityID, clientPos ):
		"""
		<Exposed Method>
		发送位置到服务器
		"""
		if self.isMoving( True ): return
		self.position = clientPos

#-------------碰撞类型-------------------------------------------------------------
	def setCollisionType( self, collisionType ):
		self.CollisionType = collisionType

	def getCollisionType( self ):
		return self.CollisionType

#-------------关系--------------------------------------------------------
	def queryRelation( self, entity ):
		"""
		查询关系
		"""
		if not entity or self.inDestroying() or entity.inDestroying():
			return csdefine.COMBAT_RELATION_NORMAL
			
		if self.id == entity.id:
			return csdefine.COMBAT_RELATION_NORMAL
		
		relationIns = self.getEntityRelationIns()
		if not relationIns:
			return csdefine.COMBAT_RELATION_NORMAL
		
		return relationIns.getRelation( self, entity )
	
	def getEntityRelationIns( self ):
		"""
		virtual method
		获取关系判断实例
		"""
		try:
			relationMode = self.getCurrentSpaceData( Const.SPACE_DATA_RELATION_MODE )
		except:
			return None
		
		entityFlagExt = self.getEntityFlagExt()
		relationIns = g_spaceEntityRelationLoader.getRelationIns( relationMode, entityFlagExt )
		if not relationIns:
			ERROR_MSG( "Entity(%s) relation instance not find!(%s)"%( self.id, relationMode ) )
			return None
		
		return relationIns
	
	def updateRelation( self ):
		"""
		virtual method
		关系改变
		"""
		self.addTimerCallBack( 0.2, "updateRelationToClient", () )	#告诉所有客户端，你跟我的关系可能改变了（0.2秒后再通知，防止客户端数据还未更新，导致获取的关系错误）
	
	def updateRelationToClient( self ):
		"""
		"""
		self.allClients.UpdateRelation()

#-------------阵营关系----------------------------------------------------
	def getCampRelation( self, campA, campB ):
		"""
		获取阵营关系
		"""
		if campA == 0 or campB == 0:
			return csdefine.COMBAT_RELATION_DEFAULT
		
		if campA == campB:
			return csdefine.COMBAT_RELATION_NORMAL
		
		for key, relation in csconst.CAMP_RALETION.items():
			if set(key) == set( (campA, campB) ):
				return relation
		
		return csdefine.COMBAT_RELATION_DEFAULT

#-------模型相关-----------------------------------------------------
	def setModelNumber( self, modelNumber ):
		"""
		<define method>
		设置模型编号
		"""
		if self.modelNumber != modelNumber:
			self.modelNumber = modelNumber

	def setModelScale( self, modelScale ):
		"""
		<define method>
		设置模型尺寸
		"""
		if self.maxModelScale > 0:
			self.modelScale = min(modelScale, self.maxModelScale)
		else:
			self.modelScale = modelScale

	def addModelScale(self, modelScale):
		"""
		"""
		if self.maxModelScale > 0:
			self.modelScale = min(self.maxModelScale, self.modelScale+modelScale)
		else:
			self.modelScale += modelScale
			
	def keepChangeModelScale(self, modelScale):
		"""
		模型持续改变
		"""
		self.addModelScale(modelScale)
		if self.modelScale>=self.maxModelScale:
			if self.keepChangeModelScaleTimerID:
				self.popTimer(self.keepChangeModelScaleTimerID)
				self.keepChangeModelScaleTimerID = 0

	def getModelNumber( self ):
		"""
		获取模型编号
		"""
		return self.modelNumber

	def getModelScale( self ):
		"""
		获取模型尺寸
		"""
		return self.modelScale

	def getMaxModelScale(self):
		"""
		"""
		return self.maxModelScale 

	def setMaxModelScale(self, scale):
		"""
		"""
		if self.maxModelScale != scale:
			self.maxModelScale = scale

	
	def setExtraModelNumber( self, modelNumber ):
		"""
		<define method>
		设置额外模型编号
		"""
		if self.extraModelNumber != modelNumber:
			self.extraModelNumber = modelNumber

	def getExtraModelNumber( self ):
		"""
		获取额外模型编号
		"""
		return self.extraModelNumber
		
	def setInitActionId(self,initActionId):
		"""
		设置初始动作
		"""
		self.initActionId = initActionId
		
	def getInitActionId( self ):
		"""
		获取初始动作
		"""
		return self.initActionId	

	def setAppearanceColor(self, colorType):
		"""
		设置头顶，光圈，血条颜色
		colorString:  0:不改变颜色，1:绿色，2:红色
		"""
		if self.appearanceColor!= colorType:
			self.appearanceColor = colorType

	def resetApperanceColor(self):
		"""
		重置头顶，光圈，血条颜色
		"""
		self.appearanceColor = 0

	#-----------------------------
	# entityInRange重载
	#-----------------------------
	def entityInRangeForSkill( self, range, entityType=None, position=None ):
		"""
		用于技能范围
		"""
		return filter( lambda e: e.getEntityFlag() not in Const.SKILL_FILTER_ENTITYS , self.entitiesInRangeExt( range, entityType, position  ) )

	def isEntityInView( self, entity ):
		"""
		判断某个entity是否在自己视野范围内
		"""
		if entity.isDestroyed:
			return False
			
		if not (self.isReal() or entity.isReal()):
			return False
		viewRadius =  self.getViewRadius()
		disX = abs( entity.position.x - self.position.x )
		disZ = abs( entity.position.z - self.position.z )
		if viewRadius > disX  and viewRadius > disZ:
			return True
		return False


#---------------------领兵begin----------------------------------------

	def setArmyModelList(self, modelList):
		"""
		"""
		self.armyModelList = modelList

	def resetArmyModelList(self):
		"""
		"""
		if self.armyModelList:
			self.armyModelList = []



#---------------------领兵end----------------------------------------


#-------------------前缀名称-----------------------------------------
	def setPrefixName( self, prefixName ):
		"""
		设置玩家的前缀名称
		"""
		self.prefixName = prefixName

	def getPrefixName( self ):
		"""
		获得玩家的前缀名称
		"""
		return self.prefixName

	#---------------设置归属某一方-----------------------------
	def setBelongSide( self, belongSide ):
		"""
		"""
		self.belongSide = belongSide

	def getBelongSide( self ):
		"""
		"""
		return self.belongSide
	
	def isBelongSide( self, belongSide ):
		"""
		"""
		return self.belongSide == belongSide