# -*- coding: utf-8 -*-


import KBEngine
import KBEDebug
#script
import MonsterOptimize
import time
import csarithmetic
import csdefine
import Const
import CoreInterface.MonsterCombatInterface as MonsterCombatInterface
import CoreInterface.MonsterAIInterface as MonsterAIInterface
import KBEMath
import Math
import math


class MonsterSoldier( MonsterOptimize.MonsterOptimize ):
	"""
	士兵小怪
	"""
	def __init__( self ):
		MonsterOptimize.MonsterOptimize.__init__( self )
		self.aiStatus = csdefine.MONSTER_SOLDIER_AI_STATUS_PEND 
		self.onCreate()
		self.isCmdMoving = False #当前是否正在执行指令移动
		

	def onCreate(self):
		"""
		"""
		cmder = self.getCmder()
		if cmder:
			cmder.onSoldierCreate(self.id)
			self.cmdMoveArgs = (cmder.position, cmder.direction, 3.0, 2.0, 5, self.getSpeed()) #(startDist, spacing, columnMax)

		#self.moveToFollowTargetPos(3.0, 2.0, 5, False)

	def setSelfEntityFlagExt(self):
		"""
		virtual method
		"""
		self.setEntityFlagExt(csdefine.ENTITY_FLAG_EXT_MONSTER_SOLDIER)

	def getCmder(self):
		"""
		"""
		return KBEngine.entities.get(self.cmderID)

	def onEnterDead( self ):
		"""
		士兵死亡
		"""
		MonsterOptimize.MonsterOptimize.onEnterDead( self )
		cmder = self.getCmder()
		if cmder:
			cmder.removeMember( self.id )

	def getAIStatus(self):
		"""
		"""
		return self.aiStatus

	def changeAIStatus(self, newStatus):
		"""
		"""
		if self.aiStatus== newStatus:
			return
		self.aiStatus = newStatus


	def doCmdFollow(self, centerPos, direction, startDist, spacing, columnMax, moveSpeed):
		"""
		"""
		self.cmdMoveArgs = (centerPos, direction, startDist, spacing, columnMax, moveSpeed)
		self.resetEnemyList()
		self.changeAIStatus(csdefine.MONSTER_SOLDIER_AI_STATUS_FOLLOW)
		self.triggerEvent(csdefine.ENTITY_EVENT_SPECIAL_ATTRIBUTES_CHANGE, ["aiStatus",self.aiStatus])
		
	
	def doCmdRectFormation(self, centerPos, direction, startDist, spacing, columnMax, moveSpeed):
		"""
		"""
		self.cmdMoveArgs = (centerPos, direction, startDist, spacing, columnMax, moveSpeed)
		self.resetEnemyList()
		self.changeAIStatus(csdefine.MONSTER_SOLDIER_AI_STATUS_RECTFORM)
		self.triggerEvent(csdefine.ENTITY_EVENT_SPECIAL_ATTRIBUTES_CHANGE, ["aiStatus",self.aiStatus])


	def doCmdCircleFormation(self, centerPos, direction, startDist, spacing, columnMax, moveSpeed):
		"""
		"""
		self.cmdMoveArgs = (centerPos, direction, startDist, spacing, columnMax, moveSpeed)
		self.resetEnemyList()
		self.changeAIStatus(csdefine.MONSTER_SOLDIER_AI_STATUS_CIRCLEFORM)
		self.triggerEvent(csdefine.ENTITY_EVENT_SPECIAL_ATTRIBUTES_CHANGE, ["aiStatus",self.aiStatus])


	def doCmdAttack(self):
		"""
		"""
		self.changeAIStatus(csdefine.MONSTER_SOLDIER_AI_STATUS_ATTACK)
		self.triggerEvent(csdefine.ENTITY_EVENT_SPECIAL_ATTRIBUTES_CHANGE, ["aiStatus",self.aiStatus])


	def doCmdUseSkill(self):
		"""
		"""
		pass


	def getFollowMoveData(self, centerPos, direction, startDist, spacing, columnMax, moveSpeed):
		"""
		"""
		centerPos2d = Math.Vector2(centerPos.x, centerPos.z)
		selfIndex = self.memberIndex
		targetPos2d = self.getFollowTargetPos2d(centerPos2d, direction.z, startDist, spacing, columnMax, selfIndex)
		targetPos = Math.Vector3(targetPos2d.x, centerPos.y, targetPos2d.y)
	
		return (targetPos, direction, moveSpeed)


	def getRectMoveData(self, centerPos, direction, startDist, spacing, columnMax, moveSpeed):
		"""
		"""
		cmder = self.getCmder()
		if not cmder:
			return
		amount = len(cmder.memberDict)
		centerPos2d = Math.Vector2(centerPos.x, centerPos.z)
		selfIndex = self.memberIndex
		targetPos2d = self.getRectFormationTargetPos2d(centerPos2d, direction.z, startDist, spacing, columnMax, selfIndex, amount)
		targetPos = Math.Vector3(targetPos2d.x, centerPos.y, targetPos2d.y)

		return (targetPos, direction, moveSpeed)


	def getCircleMoveData(self, centerPos, direction, startDist, spacing, columnMax, moveSpeed):
		"""
		"""
		cmder = self.getCmder()
		if not cmder:
			return
		amount = len(cmder.memberDict)
		centerPos2d = Math.Vector2(centerPos.x, centerPos.z)
		selfIndex = self.memberIndex
		targetPos2d = self.getCircleFormationTargetPos2d(centerPos2d, direction.z, startDist, spacing, columnMax, selfIndex, amount)
		targetPos = Math.Vector3(targetPos2d.x, centerPos.y, targetPos2d.y)
		vdir = Math.Vector2(targetPos2d - centerPos2d)
		vdir.normalise()
		
		return (targetPos, direction, moveSpeed)


	def moveFollow(self, isCmdMove):
		"""
		跟随移动
		"""
		if isCmdMove:
			self.isCmdMoving = True
		targetPos, targetDir, moveSpeed = self.getFollowMoveData(*self.cmdMoveArgs)
		if self.position.flatDistTo(targetPos)<0.5:
			return
		self.spawnPos = targetPos
		self.moveStart(csdefine.MOVE_TYPE_SOLDIER_FOLLOW, moveSpeed, True, (isCmdMove, targetPos, targetDir, 0.5 ))


	def moveRectFormation(self, isCmdMove):
		"""
		矩形列阵移动
		"""
		if isCmdMove:
			self.isCmdMoving = True
		targetPos, targetDir, moveSpeed = self.getRectMoveData(*self.cmdMoveArgs)
		if self.position.flatDistTo(targetPos)<0.5:
			return
		self.spawnPos = targetPos
		self.moveStart(csdefine.MOVE_TYPE_SOLDIER_RECT, moveSpeed, True, ( isCmdMove, targetPos, targetDir, 0.5 ))		


	def moveCircleFormation(self, isCmdMove):
		"""
		圆形列阵移动
		"""
		if isCmdMove:
			self.isCmdMoving = True
		targetPos, targetDir, moveSpeed = self.getCircleMoveData(*self.cmdMoveArgs)
		if self.position.flatDistTo(targetPos)<0.5:
			return
		self.spawnPos = targetPos
		self.moveStart(csdefine.MOVE_TYPE_SOLDIER_CIRCLE, moveSpeed, True, (isCmdMove, targetPos, targetDir, 0.5 ))


	def getFollowTargetPos2d(self, centerPos2d, yaw, startDist, spacing, columnMax, selfIndex):
		"""
		"""
		index = selfIndex
		if index%columnMax==0:	
			line = index/columnMax
			column = columnMax
		else:
			line = index//columnMax+1
			column = index%columnMax

		leftDist = columnMax//2*spacing
		vDir = Math.Vector2(math.sin(yaw), math.cos(yaw))
		vForward = KBEMath.v2dRotate(vDir, 180)
		vLeft = KBEMath.v2dRotate(vDir, 90)
		vBase = vForward*startDist + vLeft*leftDist
		vRelative = vBase + vForward*(line-1)*spacing + (vLeft*-1)*(column-1)*spacing
		targetPos = vRelative + centerPos2d
		
		return targetPos

	def getRectFormationTargetPos2d(self, centerPos2d, yaw, startDist, spacing, columnMax, selfIndex, amount):
		"""
		"""
		startIndex = columnMax - amount%columnMax
		index = selfIndex+startIndex
		if index%columnMax==0:	
			line = index/columnMax
			column = columnMax
		else:
			line = index//columnMax+1
			column = index%columnMax

		leftDist = columnMax//2*spacing

		vDir = Math.Vector2(math.sin(yaw), math.cos(yaw))
		vForward = vDir
		vLeft = KBEMath.v2dRotate(vDir, 90)
		vBase = vForward*startDist + vLeft*leftDist
		vRelative = vBase + vForward*(line-1)*spacing + (vLeft*-1)*(column-1)*spacing
		targetPos = centerPos2d + vRelative

		return targetPos

	def getCircleFormationTargetPos2d(self, centerPos2d, yaw, startDist, spacing, columnMax, selfIndex, amount):
		"""
		"""
		startIndex = columnMax - amount%columnMax
		index = selfIndex+startIndex
		if index%columnMax==0:	
			line = index/columnMax
			column = columnMax
		else:
			line = index//columnMax+1
			column = index%columnMax

		vDir = Math.Vector2(math.sin(yaw), math.cos(yaw))
		average = 360/columnMax
		degrees = math.degrees(yaw)+average*column
		length = startDist+(line-1)*spacing
		vRelative = KBEMath.v2dRotate(vDir*length, degrees)
		targetPos = centerPos2d + vRelative

		return targetPos

#-------------------------重写接口------------------------------------------

	def onMonsterAIQuitPeadCB( self ):
		"""
		退出准备状态回调
		"""
		self.isInPending = 0
		#战斗列表为空切换到自由状态,战斗列表不为空切换到战斗状态
		if self.getState()!=csdefine.ENTITY_STATE_PEAD:
			return
			
		if len(self.enemyList):
			self.changeState( csdefine.ENTITY_STATE_FIGHT )
		else:
			self.changeState( csdefine.ENTITY_STATE_FREE )

		self.changeAIStatus(csdefine.MONSTER_SOLDIER_AI_STATUS_FOLLOW)
		self.triggerEvent(csdefine.ENTITY_EVENT_SPECIAL_ATTRIBUTES_CHANGE, ["aiStatus",self.aiStatus])


	def addDamageList( self, entityID, damage ):
		"""
		添加伤害列表 如果当前正在做指令移动则不反击
		@param entityID  : entityID
		@param damage	 : 伤害值
		"""
		if self.isCmdMoving:
			return

		MonsterCombatInterface.MonsterCombatInterface.addDamageList( self, entityID, damage )


	def monsterAIOnEnterAIAttackTrap(self, entity, rangeXZ, rangeY, proximityID ):
		"""
		触发主动攻击陷阱
		"""
		#如果当前在做指令移动 屏蔽掉主动攻击陷阱
		if self.isCmdMoving:
			return

		MonsterAIInterface.MonsterAIInterface.monsterAIOnEnterAIAttackTrap(self, entity, rangeXZ, rangeY, proximityID)

	def onCmdMoveOver(self, args):
		"""
		当指令移动结束的时候需要做一些处理 比如重新触发一下主动攻击陷阱，因为指令移动的过程会屏蔽陷阱
		"""
		#触发指令完成事件
		self.monsterAITriggerEvent(csdefine.ENTITY_EVENT_ACTION_COMPLETED, args)
		#重新触发陷阱
		self.monsterAIReTriggerNearTrap()

