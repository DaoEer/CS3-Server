# -*- coding: utf-8 -*-
import KBEngine
import Monster
import csdefine
import Const
import KBEDebug
import csdefine
import csconst
import FightRuleMgr

CLIENT_MOVING_TYPE_POINT 	= 1
CLIENT_MOVING_TYPE_ENTITY 	= 2

class MonsterOptimize( Monster.Monster ):
	"""
	性能优化怪物
	@ 使用服务器去做逻辑支持，使用客户端去执行行为
	"""
	def __init__( self ):
		Monster.Monster.__init__( self )
		#当前累加ID下标，用于新ID生成，为了避免和使用服务器移动的ID冲突，这里使用32位到64位的ID
		self._clientMovingIDIdx = csdefine.INT_32_MAX
		#当前移动ID
		self.clientMovingID = 0
		self.clientMovingPos= (0.0, 0.0, 0.0 )
		#客户端移动路径
		self.clientMovingPathPoints = []
		#当前已经移动到点的下标
		self.clientMovingPathIdx = 0
		#跟随指定entity, 在没有切换移动方式前，这个值一直起作用
		self.clientMovingToEntityID = 0
		
		self._clientUseMovingType = 0
		
		#配置param1为rvoRadius 
		if self.getScript().param1:
			self.rvoRadius = float(self.getScript().param1) 

	def clientMoveReset(self):
		# 当前移动ID
		self.clientMovingID = 0
		self.clientMovingPos = (0.0, 0.0, 0.0)
		# 客户端移动路径
		self.clientMovingPathPoints = []
		# 当前已经移动到点的下标
		self.clientMovingPathIdx = 0
		# 跟随指定entity, 在没有切换移动方式前，这个值一直起作用
		self.clientMovingToEntityID = 0
		self._clientUseMovingType = 0

	def setSelfEntityFlagExt(self):
		"""
		virtual method
		"""
		self.setEntityFlagExt(csdefine.ENTITY_FLAG_EXT_MONSTER_OPTIMIZE)

	def behIsOptimize(self, bedType, behDescribe ):
		"""
		virtual method
		是否采用优化的方案
		:return: bool
		"""
		if bedType == csdefine.BEHAVIOUR_TYPE_MOVING and behDescribe != csdefine.MOVE_TYPE_CHASE:
			return False
			
		return True

	def __newClientMovingID(self):
		"""
		获取客户端移动ID
		:return:clientMovingID
		"""
		if self._clientMovingIDIdx == csdefine.INT_64_MAX:
			self._clientMovingIDIdx = csdefine.INT_32_MAX

		self._clientMovingIDIdx = self._clientMovingIDIdx + 1
		return self._clientMovingIDIdx

	def stopMoving( self, moveScriptID ):
		"""
		停止移动，使用移动类型，若当前移动类型不一样，则无效
		"""
		if self.moveScriptID == moveScriptID:
			if self.moveScriptID != csdefine.MOVE_TYPE_STOP:
				self.clientMoveReset()
			self.moveStart( csdefine.MOVE_TYPE_STOP, 0.0, False, (),  )#切换成停止移动
		return self.moveScriptID == csdefine.MOVE_TYPE_STOP

	def stopMovingForType( self, moveType ):
		"""
		停止移动，使用移动等级
		"""
		if moveType > csconst.MOVE_TYPE_DICT[ self.moveScriptID ]:
			return False

		if self.moveScriptID != csdefine.MOVE_TYPE_STOP:
			self.clientMoveReset()
		self.moveStart( csdefine.MOVE_TYPE_STOP, 0.0, False, () )#切换成停止移动
		return self.moveScriptID == csdefine.MOVE_TYPE_STOP
		
	def clientMovingSuccess(self, clientMovingID ):
		#当前移动ID
		#self.doMoveOver(self.clientMovingID, self.moveScriptID)
		pass
		
	def clientMovingFailure(self, clientMovingID ):
		"""
		移动失败
		:param self:
		:return:
		"""
		self.doMoveOver(self.clientMovingID, self.moveScriptID)

	def clientMovingAheadOver(self, exposed, clientMovingID, curPosition):
		target = KBEngine.entities.get(self.clientMovingToEntityID, None)
		if exposed != 0 and self.clientMovingToEntityID != 0 and target == None:#追击目标死亡或者消失，也接受一次同步，避免客户端和服务器位置不同步
			self.position = curPosition
		self.clientMoveReset()
		#这里要将onMoveOver放到后面，先处理自身的一些数据，因为onMoveOver之后可能会开启一次新的移动，比如巡逻移动的过程中就会出现此情况
		#上面的数据是移动过程中需要实时更新的， 如果发生了自身调用的情况，不实时更新数据会导致后面的逻辑出bug 在clientMovingPointReady方法中更新了的数据
		#会在方法退出后被旧值覆盖，此类问题的处理，必须要保证数据的有效性！
		self.onMoveOver(self.clientMovingID, self.moveScriptID)

	def clientMovingOver(self, exposed, clientMovingID ):
		"""
		移动到指定目标完成
		:param targetPos:
		:return:
		"""
		self.clientMoveReset()
		#这里要将onMoveOver放到后面，先处理自身的一些数据，因为onMoveOver之后可能会开启一次新的移动，比如巡逻移动的过程中就会出现此情况
		#上面的数据是移动过程中需要实时更新的， 如果发生了自身调用的情况，不实时更新数据会导致后面的逻辑出bug 在clientMovingPointReady方法中更新了的数据
		#会在方法退出后被旧值覆盖，此类问题的处理，必须要保证数据的有效性！
		self.onMoveOver(self.clientMovingID, self.moveScriptID)
	
	def doMoveOver( self, controllerID, moveScriptID ):
		"""
		移动完成
		"""
		self.clientMoveReset()
		Monster.Monster.doMoveOver( self, controllerID, moveScriptID )

#---------------------------------------------------move to point -------------------------------------------------------
	def clientMovingPointReady(self, targetPos ):
		"""
		先计算好移动到目的地的路径
		:param targetPos:
		:return:
		"""
		spaceEntity = self.getCurrentSpace()
		if not spaceEntity:
			return False
		
		if self.clientMovingPos == targetPos and len( self.clientMovingPathPoints ) != 0: #防止做同样的移动，消耗过高
			return False

		roleList = spaceEntity.getSpaceRoles()
		for r in roleList:
			#if r.isReal() and r.isEntityInView(self) and r.clientEntity(self.id) and not r.inDestroying() and self.position.flatDistTo(r.position)<=50.0:
			if r.isReal() and r.isEntityInView(self) and r.clientEntity(self.id) and not r.inDestroying():
				self.clientMoveReset()
				# 客户端移动路径
				self.clientMovingPathPoints = []
				# 当前已经移动到点的下标
				self.clientMovingPathIdx = 0

				self.clientMovingID = self.__newClientMovingID() #生成移动ID
				self.clientMovingPos = targetPos #设置移动目标
				self._clientUseMovingType = CLIENT_MOVING_TYPE_POINT
				try:
					r.clientEntity(self.id).movingToPointReady(self.clientMovingID, targetPos, 2.0)  # 点的最大间距暂时定为1米
				except:
					KBEDebug.DEBUG_MSG("clientMovingPointReady: monster client not exist!",self.id)
				return True

		return False

	def clientMovingPointReadyCB(self, exposed, clientMovingID,  nodePosList ):
		"""
		客户端返回移动路径
		:param exposed:
		:param targetPos:
		:param nodePosList:
		:return:
		"""
		if self.clientMovingID == clientMovingID:
			if len( nodePosList ):
				#设置后客户端会触发移动
				self.clientMovingPathPoints = nodePosList
				self.clientMovingPathIdx=0
				self.clientMovingSuccess( self.clientMovingID )
			else:
				self.clientMovingFailure( self.clientMovingID )

	def clientMovingPointUpNodeIdx(self, exposed, overStepIdx ):
		"""
		某客户端完成一个节点, 通知服务器
		:param exposed:
		:param stepIdx:
		:return:
		"""
		if not len(self.clientMovingPathPoints):
			return

		if self.clientMovingPathIdx == overStepIdx:
			if len(self.clientMovingPathPoints)-1 == overStepIdx:
				self.position = self.clientMovingPathPoints[overStepIdx]
				self.clientMovingOver( 0,  self.clientMovingID)
			else:
				self.clientMovingPathIdx = overStepIdx + 1
				# 更新位置
				self.position = self.clientMovingPathPoints[ overStepIdx ]

	def clientMovingPointUpWait(self, exposed, pos ):
		"""
		由于移动有一定原因被卡住在两个点的中间，为了防止位置出现异常，进行一次位置同步
		:param exposed:
		:param pos:
		:return:
		"""
		if len( self.clientMovingPathPoints ) == 0:
			return
			
		disToPrev = pos.distTo( self.clientMovingPathPoints[ self.clientMovingPathIdx - 1 ] )
		distToTwoPoint = self.clientMovingPathPoints[ self.clientMovingPathIdx - 1 ].distTo( self.clientMovingPathPoints[ self.clientMovingPathIdx ] )
		if self.clientMovingPathIdx != 0 and distToTwoPoint > disToPrev:
			self.position = pos

#---------------------------------------------------move to entity -------------------------------------------------------

	def moveToEntityExt(self, entityID,  distance ):
		"""
		优化型怪物持续移动到指定entity
		:param entityID:
		:param distance:
		:return:
		"""
		if self.clientMovingToEntityID == entityID:
			return self.clientMovingID
		
		self.clientMoveReset()
		self._clientUseMovingType = CLIENT_MOVING_TYPE_ENTITY
		self.clientMovingToEntityID = entityID
		self.clientMovingToEntityDis = distance
		self.clientMovingID = self.__newClientMovingID()  # 生成移动ID
		return self.clientMovingID

	def clientMovingToEntityTickUp(self, exposed, curPosition  ):
		"""
		客户端跟随移动反馈
		:param exposed:
		:param curPosition:
		:param nextPosition:
		:return:
		"""
		if (self.getMovingToEntityClientID(exposed) ==  exposed):#仅接受追击目标的同步
			self.position = curPosition

	def getMovingToEntityClientID(self, targetID):
		"""
		"""
		target = KBEngine.entities.get(targetID, None)
		if target:
			if target.getEntityFlagExt() == csdefine.ENTITY_FLAG_EXT_ROLE:
				return targetID

			if target.getEntityFlagExt() == csdefine.ENTITY_FLAG_MONSTER_CTRL_BY_CLIENT:
				return target.getControlEntity().id if target.getControlEntity() else  0
		return 0

#--------------------------------------------------method override -------------------------------------------------------
	def navigatePointExt(self, targetPosition, speedVal, distance=0.0, faceMovement=True, flag=0xFFFF, layer=0, maxMoveDistance=0xFFFF, maxSearchDistance=0xFFFF):
		"""
		优化类型怪物，重写移动方式
		@param	targetPosition:    目标坐标点
		@param	faceMovement:	 是否面向目标移动
		@param	distance:	  	 距离目标点多远停止移动
		@param	flag: 			 移动区域标志
		@param	layer: 			 使用某层导航层来进行导航
		@param	userData:        传递给回调函数的参数
		@param	maxMoveDistance: 最大移动距离，目前引擎底层预留该参数，但未起作用，0xFFFF默认值
		@param	maxSearchDistance: 最大搜索距离，目前引擎底层预留该参数，但未起作用，0xFFFF默认值
		"""
		if self.behIsOptimize(csdefine.BEHAVIOUR_TYPE_MOVING, self.moveScriptID ) == False: #不采取优化方案
			return Monster.Monster.navigatePointExt(self, targetPosition, speedVal, distance, faceMovement, flag, layer, maxMoveDistance, maxSearchDistance)
		else:
			if self.clientMovingPointReady( targetPosition ):
				return self.clientMovingID
			return 0

	def moveToPointExt(self, targetPosition, speedVal, distance, faceMovement = True , moveVertically = True ):
		"""
		优化类型怪物，重写移动方式
		@param	targetPosition:  	目标坐标
		@param	distance:	  	距离目标点多远停止移动
		@param	userData:	  	传给回调函数参数
		@param	faceMovement: 	是否面向目标移动
		@param	moveVertically: 是否贴着地面移动，bool，设为true指移动为直线移动，设为false指贴着地面移动。
		@Returns:  				移动控制器ID
		"""
		if self.behIsOptimize(csdefine.BEHAVIOUR_TYPE_MOVING, self.moveScriptID ) == False:  # 不采取优化方案
			return Monster.Monster.moveToPointExt(self, targetPosition, speedVal, distance, faceMovement , moveVertically )
		else:
			if self.clientMovingPointReady(targetPosition):
				return self.clientMovingID
			return 0
			
	def onEnterFight(self):
		"""
		"""
		Monster.Monster.onEnterFight(self)
		self.setUseRVOAvoidance(True)

	def onLeaveFight(self):
		"""
		"""
		Monster.Monster.onLeaveFight(self)
		self.setUseRVOAvoidance(False)
		
	def onViewRange( self ):
		"""
		视野范围
		清理已经不在视野内的所有敌人 只有在战斗状态时才进行检测
		return :None
		"""
		for id in list(self.enemyList):
			if not self.monsterAICheckInViewRange( id ):
				enemyEntity = KBEngine.entities.get( id, None )
				if enemyEntity:
					FightRuleMgr.g_fightMgr.breakEnemyRelation( self, enemyEntity )
				else:
					self.removeEnemy(id)
			if self.clientRoleID == id:
				self.behRoleClientLostOver()

#---------------------------RVO begin-----------------------------
	def setUseRVOAvoidance(self, boolValue):
		"""
		"""
		self.useRVOAvoidance = boolValue

	def setRVORadius(self, radius):
		"""
		"""
		self.rvoRadius = radius
		
#---------------------------RVO end-----------------------------


	