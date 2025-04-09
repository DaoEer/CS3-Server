# -*- coding: utf-8 -*-
import csdefine
import csconst
import Const

import KBEngine

from CoreInterface import AmbulantInterface
import ImpInterface.MoveJumpInterface as MoveJumpInterface
import NPCMoveScript
import Functions
import random
import Math
import math
import KBEMath
import time
import KBEDebug
import csarithmetic
import Settings
from NPCMoveScript.MoveTest import MOVE_FUN_DICT
from ConfigObject import PatrolRouteLoader
from ConfigObject.MonsterJumpPointLoader import g_MonsterJumpPoint

USER_DATA_PARENT_NAVIGATE = 1000

MAX_MOVE_SPEED = 25.0 #添加Entity的最大移动速度限制，防止不停循环移动，导致服务器崩溃

DISTANCE_MAX_RANGE = 5.0
DISTANCE_MIN_RANGE = 2.0
MOVE_FIGHT_DISPERSE_SPEED = 2.5
MOVING_FIGHT_DISPERSE_NEAR_OR_WANDER_ODDS = 50 #靠近或游走概率


class NPCAmbulantInterface( AmbulantInterface.AmbulantInterface , MoveJumpInterface.MoveJumpInterface):
	def __init__( self ):
		AmbulantInterface.AmbulantInterface.__init__( self )
		MoveJumpInterface.MoveJumpInterface.__init__(self)
		self.moveControlID = 0 #当前移动控制器的ID
		self.isUpdateSpeed = True     #移动过程中是否更新移动速度
		self.patrolRoute = self.patrolList

		self.moveScriptID = 0 #当前移动类型
		self.moveArgs = [] #当前移动参数
		
		self.moveTimerID = 0 #移动循环时间
		
		self.moveDormancyTimerID = 0#移动休眠
		
		#仅提供给在移动平台上移动的功能使用
		self._navigateParentArgs = []
		self._navigateParentPoints = []
		
		#提供巡逻加速度使用
		self.patrolAccSpeed = 0.0		#巡逻加速度
		self.lastPatrolAccTime =0	#巡逻加速时间点
		self.moveSpeedExtra = 0.0 	#额外速度值 （v = at）
		self.patrolMoveSpeedMax = 0.0 #加速移动最大数度值
		self.accelerateSpeedTimerID = 0
		
		#游荡
		self.wanderCallBackID = 0

		#回走
		self.gobackTimer = 0

		#设置导航层  暂时在初始化的时候设置，如果资源消耗过大，再在考虑移到其他地方
		self.setLayer()

		self.__temp_move_method = None

		self.circleChaseAngle = 0.0
		self.circleChaseDistance = 0.0

		#跨层移动
		self.isJumping = False

	def doEnterSpace( self ):
		"""
		进入一个空间调用
		"""
		self.__temp_move_method = None


	def beforeDestroy( self ):
		"""
		销毁之前
		"""
		self.stopMovingForType( csdefine.SYSTEM_MOVE )
	
	#-------------------------------------------
	# npc移动方法
	#-------------------------------------------
	def initSpeed( self ):
		"""
		override
		初始化移动速度
		"""
		AmbulantInterface.AmbulantInterface.initSpeed( self )
		self.updateMoveSpeed()
	
	def stopMoving( self, moveScriptID ):
		"""
		停止移动，使用移动类型，若当前移动类型不一样，则无效
		"""
		if self.moveScriptID == moveScriptID:
			self.moveStart( csdefine.MOVE_TYPE_STOP, 0.0, False, (),  )#切换成停止移动
		return self.moveScriptID == csdefine.MOVE_TYPE_STOP
	
	def stopMovingForType( self, moveType ):
		"""
		停止移动，使用移动等级
		"""
		if moveType > csconst.MOVE_TYPE_DICT[ self.moveScriptID ]:
			return False

		self.moveStart( csdefine.MOVE_TYPE_STOP, 0.0, False, () )#切换成停止移动
		return self.moveScriptID == csdefine.MOVE_TYPE_STOP
	
	def isMovingType( self, moveScriptID ):
		return moveScriptID == self.moveScriptID
	
	def isMoving( self, isNotChasePlayer = False ):
		"""
		是否移动中
		"""
		if isNotChasePlayer:
			return self.moveControlID != 0
		else:
			return self.moveControlID != 0 or self.getSyncPosClient() != 0
	
	def gotoPosition( self, targetPosition, distance = 1.0 ,   faceMovement = True, layer = 0, speed = 0.0 ):
		"""
		使用导航数据移动到目标点
		targetPosition:目标点
		distance:移动距离目标点多远停止
		faceMovement:是否面向目标点移动
		layer:使用导航层的第几层
		lineToPoint:是否是直线移动（直接移动则不使用导航进行移动）
		"""
		if speed == 0.0:
			speed = self.getSpeed()
		self.moveStart( csdefine.MOVE_TYPE_NAVIGATE_POINT, speed, True, ( targetPosition, distance, faceMovement, layer ) )
	
	def moveToPosition(self, targetPosition , faceMovement = True,  moveVertically = True, distance = 0.0, speed = 0.0):
		"""
		直接移动到目标点，不使用导航数据
		targetPosition:	目标点坐标
		faceMovement:	实体移动过程中是否面向移动方向
		moveVertically:	移动过程中是否贴着地面移动，False为贴着地面移动，True为直线移动
		distance:		移动到距离目标点多远时停止移动
		"""
		if speed == 0.0:
			speed = self.getSpeed()
		self.moveStart( csdefine.MOVE_TYPE_MOVE_POINT, speed, True, ( targetPosition, distance, faceMovement, moveVertically ) )

	def getCurrentSpacePatrolnfo(self, patrolRoute):
		"""
		获取当前地图的某条巡逻路线
		"""
		if patrolRoute:
			return PatrolRouteLoader.g_patrolRouteLoader.getPatrolRoute( self.getCurrentSpaceScriptID(), patrolRoute)

		return None

	def startPatrol( self, moveSpeed, isUpdateSpeed, args = None  ):
		"""
		按默认巡逻路线巡逻
		"""
		if args == None:
			if self.patrolRoute:
				patrolRouteInfo = self.getCurrentSpacePatrolnfo(self.patrolRoute)
				self.moveStart( csdefine.MOVE_TYPE_PATROL, moveSpeed, isUpdateSpeed, ( patrolRouteInfo, self.patrolPathNode, self.patrolMoveMode, self.patrolAccSpeed ) )
		else:
			self.moveStart( csdefine.MOVE_TYPE_PATROL, moveSpeed, isUpdateSpeed, args )

	def startReversePatrol( self, moveSpeed, isUpdateSpeed, args = None ):
		"""
		按巡逻路线的反向巡逻
		"""
		self.moveStart( csdefine.MOVE_TYPE_REVERSE_PATROL, moveSpeed, isUpdateSpeed, args )
		
	def startRandomWalk( self, moveSpeed, isUpdateSpeed):
		"""
		开始
		"""
		if self.isMovingType( csdefine.MOVE_TYPE_RANDOM ):
			return
			
		if self.randomWalkRange > 0:
			self.moveStart( csdefine.MOVE_TYPE_RANDOM, moveSpeed, isUpdateSpeed, () )

	def startRandomWalkFromList( self, moveSpeed, isUpdateSpeed ):
		"""
		开始随机从列表取点
		"""
		if self.isMovingType( csdefine.MOVE_TYPE_RANDOM_CHOICE_FORM_LIST ):
			return
		self.moveStart( csdefine.MOVE_TYPE_RANDOM_CHOICE_FORM_LIST, moveSpeed,isUpdateSpeed, () )

	def chargeToPosition( self, targetPosition, moveSpeed, distance ):
		"""
		怪物冲锋到目标位置
		"""
		self.moveStart( csdefine.MOVE_TYPE_CHARGE, moveSpeed, False, ( targetPosition,distance ))

	def moveNearToTarget( self, targetPosition, moveSpeed, isUpdateSpeed, moveDst = 0.0 ):
		newPos = self.getTargetNearPosition( targetPosition, moveDst )
		self.moveStart( csdefine.MOVE_TYPE_NAVIGATE_POINT, moveSpeed, isUpdateSpeed, ( newPos, 0.0 ) )

	def walkAroundTarget( self,  targetID, targetPosition, maxRadians, moveSpeed, isUpdateSpeed, distance = 0.0 ):
		newPos = self.getTargetAroundPosition(  targetPosition, maxRadians )
		self.moveStart( csdefine.MOVE_TYPE_WALK_AROUND, moveSpeed, isUpdateSpeed, ( newPos, distance, targetID ) )

	def moveAwayFromTarget( self, targetPosition, moveSpeed, isUpdateSpeed, moveDst = 0.0, distance = 0.0 ):
		newPos = self.getTargetAwayPosition( targetPosition, moveDst, distance )
		self.moveStart( csdefine.MOVE_TYPE_NAVIGATE_POINT, moveSpeed, isUpdateSpeed, ( newPos, 1.0 ) )

	def moveBack( self,  dstPosition, backSpeed ):
		"""
		受击击退移动
		"""
		return self.moveStart( csdefine.MOVE_TYPE_HIT_BACK, backSpeed, False, ( dstPosition, ) )
	
	def chaseEntity( self, entity, distance ):
		"""
		追击
		"""
		self.moveStart( csdefine.MOVE_TYPE_CHASE, self.getSpeed(), True, ( entity.id, distance ) )

	def skillChaseEntity( self, entity, distance, speedVal, skill ):
		"""
		技能追击
		"""
		self.moveStart( csdefine.MOVE_TYPE_SKILL_CHASE, speedVal, False, ( entity.id, distance, skill ) )

	def startLoopRotator( self, rotatorSpeed ):
		"""
		开始转圈
		"""
		self.moveStart( csdefine.MOVE_TYPE_LOOP_ROTATOR, self.getSpeed(), False, ( rotatorSpeed, ) )
		
	def navigateToPointTest( self, targetPosition, distance = 1.0):
		"""
		寻路到某一个点，将不能寻路的情况打印出来
		"""
		self.moveStart( csdefine.MOVE_TYPE_NAVIGATE_POINT_TEST, self.getSpeed(), True, (targetPosition, distance))

	def moveRandomInSphere( self, moveSpeed, isUpdateSpeed, centerPosition, radius, aiCmd1, aiCmd2, maxTime, minTime ):
		"""
		在球内随机移动
		"""
		self.moveStart( csdefine.MOVE_TYPE_RANDOM_IN_SPHERE, moveSpeed, isUpdateSpeed, ( centerPosition, radius, aiCmd1, aiCmd2, maxTime, minTime ) )

	def moveFlyToPoint(self, targetPosition , speed = 0.0, faceMovement = True,  moveVertically = True, distance = 0.0):
		"""
		飞行移动到某一点
		"""
		if speed == 0.0:
			speed = self.getSpeed()
		self.moveStart( csdefine.MOVE_TYPE_FLY_TO_POINT, speed, True, ( targetPosition, distance, faceMovement, moveVertically ) )

	def skillJumpPosition( self, targetPosition, moveSpeed, distance ):
		"""
		技能跳扑到目标位置
		"""
		self.moveStart( csdefine.MOVE_TYPE_SKILL_JUMP, moveSpeed, False, ( targetPosition,distance ))

	#------------------------------
	# 小怪物追击及散开表现
	#------------------------------
	def fightDisperseSelectPos( self, targetEntity ):
		"""
		选择
		"""
		distanToTarget = self.position.flatDistTo(targetEntity.position)
		selectMovePos = ( 0, 0, 0 )
		selectStyle = 0
		if distanToTarget > DISTANCE_MAX_RANGE:
			selectMovePos = Math.Vector3( targetEntity.position )
			selectStyle = csdefine.MOVING_FIGHT_DISPERSE_STYLE_CHASE
		else:
			if distanToTarget > DISTANCE_MIN_RANGE:
				selectMovePos = self.getNearOrWanderingPos( targetEntity.position )
				selectStyle = csdefine.MOVING_FIGHT_DISPERSE_STYLE_WANDER
			else:
				selectMovePos = self.getAroundOrAwayPos( targetEntity.position )
				selectStyle = csdefine.MOVING_FIGHT_DISPERSE_STYLE_AWAY

		return ( selectStyle, selectMovePos )

	def fightDisperseMove( self, targetEntity, styleSelect, moveSpeed ):
		"""
		小怪物追击及散开移动
		"""
		selectStyle, selectMovePos = self.fightDisperseSelectPos( targetEntity )
		if (selectMovePos, selectStyle) != self.moveArgs and styleSelect != selectMovePos:
			self.moveStart( csdefine.MOVE_TYPE_FIGHT_DISPERSE, moveSpeed, False, ( selectMovePos, selectStyle ) )

	def getNearOrWanderingPos( self, targetPosition ):
		"""
		"""
		newPos = None
		if random.randint(0, 100) < MOVING_FIGHT_DISPERSE_NEAR_OR_WANDER_ODDS:
			newPos = self.getTargetNearPosition( targetPosition, DISTANCE_MIN_RANGE )
		else:
			newPos = self.getTargetAroundPosition(  targetPosition, math.pi/2 )
		return newPos

	def getAroundOrAwayPos( self, targetPosition ):
		"""
		"""
		newPos = self.getTargetAwayPosition(  targetPosition, math.pi/2 )
		return newPos
	#-------------------------------游荡----------------------------------------------------------------------
	def startWander( self ):
		"""
		保持游荡
		"""
		if not self.canMoveCheck() or not self.hasFlag(csdefine.FLAG_WANDER) or self.wanderCallBackID:
			return
			
		if self.getSpeed() <= 0.0:
			return False
			
		self.wanderCallBackID = self.addTimerRepeat( Const.WANDER_TIMES, "doRepeatWander", () )
	
	def doRepeatWander( self ):
		"""
		执行保持游荡的检查循环
		"""
		if self.moveScriptID == csdefine.MOVE_TYPE_WANDER: #当前还在继续游荡，不做处理
			return
			
		target = KBEngine.entities.get( self.targetID )
		if not target or self.spaceID != target.spaceID:
			return
			
		if not self.isState( csdefine.ENTITY_STATE_FIGHT ) or entity.isCastingSkill() or not self.canMoveCheck():					#只有战斗状态下并且不再释放技能以及吟唱等行为进行游荡行为
			return
			
		self.moveStart( csdefine.MOVE_TYPE_WANDER, self.getSpeed(), False, target.position )
		
	def stopWander( self ):
		"""
		停止游荡
		"""
		if self.wanderCallBackID:
			self.popTimer( self.wanderCallBackID )
			self.wanderCallBackID = 0
			self.changeDefaultMove()
	
	#-------------------------------------------
	# npc移动机制
	#-------------------------------------------
	def changeDefaultMove( self ):
		"""
		vitual method
		切换成默认的移动方式， 不同怪物可以根据需求重载
		"""
		if self.moveScriptID == csdefine.MOVE_TYPE_STOP:
			return
			
		defaultScriptID = csdefine.MOVE_TYPE_STOP
		defaultScriptArgs = ()
		defaultSpeed = self.getSpeed()
		self.moveStart( defaultScriptID, defaultSpeed, False, defaultScriptArgs )  #切换成默认的移动方式


	def updateMoveSpeed(self):
		"""
		如果当前有移动则以新速度重新开启移动
		"""
		if not self.isUpdateSpeed:
			return
		moveSpeed = self.getSpeed()
		if self.moveControlID:
			self.moveStart(self.moveScriptID, moveSpeed, True, self.moveArgs)


	def getMoveScript( self ):
		"""
		获取当前的移动脚本
		"""
		if not self.__temp_move_method:
			UseMoveType = None
			if self.behIsOptimize( csdefine.BEHAVIOUR_TYPE_MOVING, self.moveScriptID ):
				UseMoveType = NPCMoveScript.g_moveDict_optimize
			else:
				UseMoveType = NPCMoveScript.g_moveDict

			try:
				if self.__temp_move_method == None:
					self.__temp_move_method = UseMoveType[ self.moveScriptID ]
			except:
				self.__temp_move_method = UseMoveType[ self.moveScriptID ]
					
		return self.__temp_move_method


	def getMoveScriptByType( self, moveScriptID ):
		"""
		获取当前的移动脚本
		"""
		if self.__temp_move_method and self.__temp_move_method.getScriptID() == moveScriptID:
			return self.__temp_move_method
		else:
			UseMoveType = None
			if self.behIsOptimize( csdefine.BEHAVIOUR_TYPE_MOVING, NPCMoveScript ):
				UseMoveType = NPCMoveScript.g_moveDict_optimize
			else:
				UseMoveType = NPCMoveScript.g_moveDict

			try:
				if self.__temp_move_method == None:
					self.__temp_move_method = UseMoveType[ moveScriptID ]
			except:
				self.__temp_move_method = UseMoveType[ moveScriptID ]
				
			return self.__temp_move_method

	
	def canMoveCheck( self, isForceMove = False ):
		"""
		@param isForceMove:	是否受迫移动
		能否移动检测
		"""
		if self.hasStateFlag:
			if self.isState(csdefine.ENTITY_STATE_DEAD):
				return False
			if self.isJumping:
				return False
			if not isForceMove and self.actionForbidSign( csdefine.ACTION_FORBID_MOVE ):
				return False
		return True


	def triggerEventChangeMoveType(self, oldMoveType, newMoveType):
		"""
		触发移动类型改变事件
		"""
		pass
	
	def moveStart( self, mScriptID, mSpeed, misUpdateSpeed, mArgs  = () ):
		"""
		开始移动
		mScriptID:移动脚本 , mSpeed:移动速度 , misUpdateSpeed:当前移动能否变速，mArgs:移动参数 , isForce:是否为强制执行，只有停止才使用这个参数
		"""
		if self.inDestroying() or self.isSpaceGone == True:
			return
		
		if self.isJumping:
			self.moveFailure( mScriptID, mArgs )
			return

		if not mScriptID in [csdefine.MOVE_TYPE_STOP] and not self.getMoveScript().isCanBreak( self, mScriptID ): #新的移动方式不能打断当前的移动，停止移动是会强制打断
			self.moveFailure( mScriptID, mArgs )
			return

		if self.moveScriptID != mScriptID:	
			if self.moveScriptID == csdefine.MOVE_TYPE_PATROL or self.moveScriptID == csdefine.MOVE_TYPE_FLY_TO_POINT \
			or mScriptID == csdefine.MOVE_TYPE_FLY_TO_POINT:
				self.triggerEventChangeMoveType(self.moveScriptID, mScriptID)

		self.__start( mScriptID, mSpeed, misUpdateSpeed, mArgs  )
	
	def __start( self, mScriptID, mSpeed, misUpdateSpeed, mArgs ):
		# 移动测试代码

		# if Settings.test_flag and Settings.move_test:
		# 	#停掉移动
		# 	if Settings.move_test not in MOVE_FUN_DICT:
		# 		return
		#
		# 	MOVE_FUN_DICT[Settings.move_test][csdefine.MOVE_TYPE_STOP](self)
		# 	self.moveScriptID = mScriptID
		# 	self.moveArgs = mArgs
		# 	self.moveSpeed = float( mSpeed )
		# 	self.isUpdateSpeed = misUpdateSpeed
		# 	moveType = csconst.MOVE_TYPE_DICT[ mScriptID ]
		# 	isForceMove = moveType in [ csdefine.PERFORMANCE_PASSIVITY_MOVE, csdefine.SYSTEM_MOVE ]
		# 	moveFunc = MOVE_FUN_DICT[Settings.move_test].get(self.moveScriptID, None)
		# 	if moveFunc is None:
		# 		#KBEDebug.ERROR_MSG("not found moveScriptID[%d]" %(mScriptID))
		# 		return
		#
		# 	if self.moveScriptID == csdefine.MOVE_TYPE_STOP or (self.moveSpeed > 0.0 and self.canMoveCheck( isForceMove )):
		# 		moveFunc(self, *self.moveArgs)
		# 	return
		
		if mScriptID == self.moveScriptID and self.moveControlID != 0 and mArgs == self.moveArgs and self.moveSpeed == mSpeed:
				return

		self.moveStopTick() #停止移动循环
		self.moveStopDormancy() #停止移动休眠
		self.cancelController( "Movement" )
		self.moveControlID = 0
		self.getMoveScript().stop( self, *(self.moveArgs if self.moveArgs!=None else ()) )
		self.__temp_move_method = None
		self.moveScriptID = mScriptID
		newMoveScript = self.getMoveScript()
		self.moveSpeed = float( mSpeed )
		self.isUpdateSpeed = misUpdateSpeed
		self.moveArgs = mArgs
		moveType = csconst.MOVE_TYPE_DICT[ mScriptID ]
		isForceMove = moveType in [ csdefine.PERFORMANCE_PASSIVITY_MOVE, csdefine.SYSTEM_MOVE ]
		isCanMove = self.canMoveCheck(isForceMove)
		if isCanMove: #是否可以进行移动
			self.moveControlID = newMoveScript.start( self,  *self.moveArgs )
						
		if newMoveScript.isStartTick( isCanMove ): #如果当前需要开启移动心跳
			self.moveStartTick( newMoveScript.getTickTime() )
	
		if  self.moveControlID == 0 and self.moveTimerID ==0: #没有移动，而且也没有启动心跳的移动，延迟调用onMoveOver，防止没有移动，又没有移动结束导致移动被中止
			self.addTimerCallBack( 1.0, "onMoveOver",  (0, self.moveScriptID) )

	def moveFailure( self, mScriptID, mArgs ):
		"""
		开启某个移动失败
		"""
		self.getMoveScript().failure( self, *mArgs )

	def moveUseSpeed( self, mScriptID, mArgs ) :
		"""
		使用当前怪物的移动速度进行移动
		"""
		self.moveStart( mScriptID, self.getSpeed(), True, mArgs )
		
	def doMoveOver( self, controllerID, moveScriptID ):
		"""
		移动结束，但似乎不管移动是否成功，都调用此函数
		@param controllerID		:	移动控制器ID
		@type  controllerID     :	int
		"""
		MoveJumpInterface.MoveJumpInterface.doMoveOver(self, controllerID, moveScriptID)		
		self.moveControlID = 0
		if USER_DATA_PARENT_NAVIGATE == moveScriptID: #特别处理，如果是在移动平台上用导航移动
			self.__navigateForParent( *self._navigateParentArgs )
	
		elif self.moveScriptID == moveScriptID: #如果当前是在循环/多次移动，则回调到移动的tick里面
			self.getMoveScript().over( self, *self.moveArgs )
		
	def doMoveFailure( self, controllerID, moveScriptID ):
		#即便寻路结束，没有移动到目标点，此处似乎也不会自动回调
		if USER_DATA_PARENT_NAVIGATE == moveScriptID: #特别处理，如果是在移动平台上用导航移动
			self.__navigateForParent( *self._navigateParentArgs )
			return
			
		if self.moveScriptID == moveScriptID: #如果当前是在循环/多次移动，则回调到移动的tick里面
			self.getMoveScript().over( self, *self.moveArgs )
				
	#------------------------------------------------------
	# move timer
	#------------------------------------------------------
	def moveStartTick( self, repeatTime ):
		"""
		移动循环
		"""
		self.moveStopTick()
		self.moveTimerID = self.addTimerRepeatNoTickSpeedLimit( repeatTime, "moveOnTick", () )
	
	def moveOnTick( self ):
		"""
		移动循环回调
		"""
		self.moveControlID = 0
		self.moveControlID = self.getMoveScript().tick( self, *self.moveArgs )
		#if self.moveControlID == 0: #表示移动失败，直接回调移动结束
		#	self.getMoveScript().over( self, *self.moveArgs )
	
	def moveStopTick( self ):
		"""
		停止移动循环
		"""
		if self.moveTimerID:
			self.popTimer(self.moveTimerID)
			self.moveTimerID = 0
	
	#移动休眠功能
	def moveStartDormancy( self, timeVal ):
		"""
		设置移动休眠, 当改变移动方式时，休眠被打断
		timeVal：休眠时间
		moveScriptID：移动脚本ID
		moveSpeed：移动速度
		moveArgs：移动参数
		"""
		if self.inDestroying():
			return
			
		self.moveStopDormancy()
		if timeVal < 0.1:
			self.moveOnDormancy( self.moveScriptID )
		else:
			self.moveDormancyTimerID = self.addTimerCallBack( timeVal, "moveOnDormancy", ( self.moveScriptID, ) )
	
	def moveOnDormancy( self, moveScriptID ):
		"""
		休眠回调
		"""
		if moveScriptID == self.moveScriptID: #如果当前移动方式没变，唤醒 移动
			self.getMoveScript().onDormancy( self, *self.moveArgs )
	
	def moveStopDormancy( self ):
		"""
		停止移动休眠
		"""
		if self.moveDormancyTimerID:
			self.popTimer(self.moveDormancyTimerID)
			self.moveDormancyTimerID = 0

	#回走移动 回走过程被打断 打断结束后继续回走
	def moveGoBack(self):
		"""
		"""
		self.gobackTimer = self.addTimerRepeat(0.2, "_moveGoback", ())

	def _moveGoback(self):
		"""
		"""
		self.moveStart(csdefine.MOVE_TYPE_GOBACK, self.getSpeed(), False)



	#------------------------------
	# 服务器控制移动函数
	#------------------------------
	def navigatePointExt( self,  targetPosition, speedVal, distance = 0.0, faceMovement = True, flag = 0xFFFF, layer = 0, maxMoveDistance = 0xFFFF, maxSearchDistance = 0xFFFF):
		"""
		protected method
		引擎方法navigatet封装
		此方法不允许重载
		@param	targetPosition:    目标坐标点
		@param	faceMovement:	 是否面向目标移动
		@param	distance:	  	 距离目标点多远停止移动
		@param	flag: 			 移动区域标志
		@param	layer: 			 使用某层导航层来进行导航
		@param	userData:        传递给回调函数的参数
		@param	maxMoveDistance: 最大移动距离，目前引擎底层预留该参数，但未起作用，0xFFFF默认值
		@param	maxSearchDistance: 最大搜索距离，目前引擎底层预留该参数，但未起作用，0xFFFF默认值
		"""
		moveControlID = 0
		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			flag = spaceEntity.getAreaFlags()
		

		#是否需要跨层移动
		if self.isCanJumpMove(targetPosition):
			moveControlID = self.startMoveJump(targetPosition)
			return moveControlID


		if not self.hasParent():
			moveControlID = self.navigate( targetPosition, min( speedVal, MAX_MOVE_SPEED ) , float( distance ), maxMoveDistance, maxSearchDistance, faceMovement, self.layer, flag, self.moveScriptID )
		else:
			moveControlID = self.navigateForParent( targetPosition, min( speedVal, MAX_MOVE_SPEED ), float( distance ), maxMoveDistance, maxSearchDistance, faceMovement, self.layer, flag, self.moveScriptID )
		
		return moveControlID

	def moveToPointExt(self, targetPosition, speedVal, distance, faceMovement = True , moveVertically = True ):
		"""
		protected method
		引擎方法moveToPoint封装
		此方法不允许重载
		@param	targetPosition:  	目标坐标
		@param	distance:	  	距离目标点多远停止移动
		@param	userData:	  	传给回调函数参数
		@param	faceMovement: 	是否面向目标移动
		@param	moveVertically: 是否贴着地面移动，bool，设为true指移动为直线移动，设为false指贴着地面移动。  		
		@Returns:  				移动控制器ID
		"""
		if self.parent:
			targetPosition = self.parent.positionWorldToLocal( targetPosition )
		moveControlID = self.moveToPoint( targetPosition, min( speedVal, MAX_MOVE_SPEED ), distance, self.moveScriptID, faceMovement, moveVertically)
		return moveControlID
	
	#---------------------------------------------------加速度移动---------------------------------------------------------------------------------------------------------------------

	def getPatrolMoveSpeedMax(self):
		"""
		获取最大巡逻速度
		"""
		return self.patrolMoveSpeedMax
	
	def getPatrolSpeed( self, speedVal ):
		"""
		如果有巡逻加速度，要重新获取初始速度
		"""
		if self.getPatrolMoveSpeedMax()>0:
			return min(speedVal + self.moveSpeedExtra, self.getPatrolMoveSpeedMax())
		else:
			return speedVal + self.moveSpeedExtra

	def setPatrolSpeed( self, accSpeed ):
		"""
		设置巡逻加速度
		"""
		self.patrolAccSpeed = float( accSpeed )		#巡逻加速度
		self.lastPatrolAccTime = KBEngine.time()	#巡逻加速时间点
	
	def navigateAccel( self,  targetPosition, speedVal, distance = 0.0, faceMovement = True, flag = 0xFFFF, layer = 0, maxMoveDistance = 0xFFFF, maxSearchDistance = 0xFFFF ):
		"""
		加速度的移动方式
		"""
		speedVal = self.getPatrolSpeed( speedVal )
		moveControlID = self.navigatePointExt(  targetPosition, speedVal, distance, faceMovement, flag, layer, maxMoveDistance, maxSearchDistance  )
		if not moveControlID:
			return 0
		if self.patrolAccSpeed != 0.0 and self.accelerateSpeedTimerID == 0:
			self.accelerateSpeedTimerID = self.addTimerRepeat(0.1, "accelerateSpeed", (self.patrolAccSpeed)) #加速移动
		return moveControlID
	
	def moveToPointAccel(self, targetPosition, speedVal, distance = 0.0, faceMovement = True , moveVertically = True ):
		"""
		加速度的移动方式(点到点)
		"""
		speedVal = self.getPatrolSpeed( speedVal )
		moveControlID = self.moveToPointExt( targetPosition, speedVal, distance, faceMovement , moveVertically )
		if self.patrolAccSpeed != 0.0:
			if self.accelerateSpeedTimerID == 0:
				self.accelerate( "Movement", self.patrolAccSpeed ) #加速移动
		return moveControlID

	def accelerateSpeed(self, velocity):
		"""
		加速巡逻速度
		"""
		#如果有最大速度限定
		if self.getPatrolMoveSpeedMax()>0:
			if self.getPatrolSpeed(self.moveSpeed) + velocity >= self.getPatrolMoveSpeedMax():
				self.accelerate( "Movement", self.getPatrolMoveSpeedMax() - self.getPatrolSpeed(self.moveSpeed))
				self.popTimer(self.accelerateSpeedTimerID)
				self.accelerateSpeedTimerID = 0
				self.moveSpeedExtra = 0.0
			else:
				self.accelerate( "Movement", velocity )
				self.moveSpeedExtra += velocity
		else:
			self.accelerate( "Movement", velocity )
			self.moveSpeedExtra += velocity
		

	#---------------------------------------------------------------移动平台的移动，理论上在引擎层的代码，现在暂时放这里---------------------------------------------------------
	
	def navigateForParent( self, targetPosition, speedVal, distance, maxMoveDistance, maxSearchDistance, faceMovement, layer, flag, moveScriptID ):
		"""
		移动平台上寻路
		"""
		if not self.parent:
			return False
			
		localDestPos = self.parent.positionWorldToLocal( targetPosition )
		localPaths = KBEngine.navigatePathPoints( self.parent.getNavmeshPath(), self.localPosition, localDestPos, 0xFFFF, layer, flag)
		self._navigateParentPoints = []
		if len( localPaths ) != 0:
			self._navigateParentPoints.extend( localPaths )
		else:
			#如果没有寻路点就直接移动失败
			return 0
		
		self._navigateParentArgs = ( speedVal, distance, maxMoveDistance, maxSearchDistance, faceMovement, layer, flag, moveScriptID )
		return self.__navigateForParent( speedVal, distance, maxMoveDistance, maxSearchDistance, faceMovement, layer, flag, USER_DATA_PARENT_NAVIGATE )
	
	def __navigateForParent( self, speedVal, distance, maxMoveDistance, maxSearchDistance, faceMovement, layer, flag, moveScriptID ):
		"""
		移动平台上根据导航上得出来的点逐个移动
		"""
		if len( self._navigateParentPoints ) == 0:
			self._navigateParentArgs = []
			self.onMoveOver( 0, moveScriptID ) #告诉移动脚本，移动完成
			return False
			
		dest = self._navigateParentPoints.pop(0)
		return self.moveToPoint( dest, speedVal, distance, USER_DATA_PARENT_NAVIGATE, faceMovement, False )


	def setLayer(self):
		"""
		设置导航层数
		"""
		layer = self.getCurrentSpace().getScript().getNavmeshLayers()
		self.layer = 0
		if not (layer - 1):
			#KBEDebug.ERROR_MSG("setLayer:layer is %s:"%layer)
			return
		for i in range(layer):
			PositionList = KBEngine.collideVertical(self.spaceID, i, self.position, 6, -6 )
			if PositionList and len(PositionList):
				self.layer = i
				#KBEDebug.ERROR_MSG("setLayer:self.layer is %s:"%self.layer)
				return


	def CELL_updateMoveTargetPosFromClient(self, srcEntityID, posStr):
		"""
		同步客户端移动目标位置
		"""
		#保存信息 服务器分析信息 选择最终移动位置 暂时处理追击目标玩家发过 来的数据	
		
		def getPos(srcEntityID, posStr):
			"""
			从数据中解析追击目标
			"""
			posList =  [float(i) for i in posStr.split("|")]

			return Math.Vector3(posList)

		pos = getPos(srcEntityID, posStr)
		if srcEntityID == self.targetID:
			self.getMoveScript().updateMoveTargetPosFromClient(self, pos)
		




