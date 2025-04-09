# -*- coding: utf-8 -*-


import csdefine
import KBEMath
import Math
import math
import KBEDebug
import random
import csarithmetic
import Functions

YINBING_BUFFID = 12075714

class MonsterAppearInterface:
	"""
	怪物出场接口类
	"""
	def __init__( self ):
		self.isMonsterAppearJumping = False
		self.isMonsterAppearLineToPoint = False



	def monsterAppearJump(self, actions, effectID, targetPos, direction, jumpSpeed = csdefine.MONSTER_APPEAR_MOVE_SPEED,\
		gravity = csdefine.MONSTER_APPEAR_MOVE_GRAVITY, actionTime = csdefine.MONSTER_APPEAR_ACTION_TIME ):
		"""
		怪物出场的外部接口
		"""
		if len(actions)!=3:
			KBEDebug.ERROR_MSG("actionsID Less than three")
			return
		self.stopMovingForType(csdefine.SYSTEM_MOVE)
		callBackTime = self.monsterAppearJumpNeedTime( targetPos, jumpSpeed/100, gravity/100, actionTime/2 ) + csdefine.MONSTER_APPEAR_END_ACTION_TIME
		self.monsterAppearAddFlags()
		self.isMonsterAppearJumping = True
		targetPosition = Math.Vector3(KBEMath.KBEngine2UnrealPosition(targetPos))
		self.allClients.CLIENT_MonsterAppearJump( actions, effectID, gravity, 0.5 * actionTime, jumpSpeed, targetPosition )
		self.addTimerCallBack( callBackTime, 'onMonsterAppearJump', (Math.Vector3(targetPos),))
		
		if direction:
			self.changeDirection(direction, csdefine.REASON_CHANGE_DIR_FORCE)
		else:
			self.turnToPos( targetPos )

		
		self.spawnPos = Math.Vector3(targetPos)
		self.spawnDir = Math.Vector3(self.direction)


	def monsterAppearJumpNeedTime( self,targetPos, jumpSpeed, gravity, upTime ):
		"""
		计算怪物带位移出场落地时间
		"""
		targetPos = Math.Vector3(targetPos)
		horizontalDist = Math.Vector3(self.position.x,targetPos.y,self.position.z).flatDistTo(targetPos)
		yDist = targetPos.y - self.position.y
		if ( yDist > 0.0 ):	# 目标点高于起始点
			if ( 0.5*gravity*upTime*upTime > yDist ):
				needTime = math.sqrt( upTime*upTime - 2.0*yDist / gravity ) + upTime
			else:
				yGravity = (2.0*yDist) / (upTime*upTime) + 20.0
				needTime = math.sqrt( upTime*upTime - 2.0*yDist / yGravity ) + upTime
		else:
			needTime = horizontalDist/jumpSpeed
			if needTime <= 2.0 * upTime:
				needTime = math.sqrt( upTime*upTime + ( 2.0*abs(yDist)/gravity )) + upTime

		return needTime

	def monsterAppearJumpWithoutMove( self, actions, effectID, loopTime ):
		"""
		不带位移 原地出场 策划配置第二段跳的时间
		"""
		self.allClients.CLIENT_MonsterAppearJumpWithoutMove( actions, effectID, loopTime )
		

	def onMonsterAppearJump( self, targetPos ):
		"""
		出场动作结束的回调
		"""
		self.position =  targetPos 
		self.monsterAppearRemoveFlags()

		self.isMonsterAppearJumping = False


	def CELL_onMonsterAppearJumpEnd( self, exposed ):
		"""
		<Exposed method>
		出场动作结束的回调
		"""
		#self.position = Math.Vector3( self._targetPos )
		self.monsterAppearRemoveFlags()

		self.isMonsterAppearJumping = False


	def CELL_onMonsterAppearJumpWithoutMoveEnd( self ,exposed):
		"""
		<Exposed method>
		出场动作结束的回调
		"""
		self.isMonsterAppearJumping = False


	def isMonsterAppearJumpOver( self ):
		"""
		出场动作是否完毕
		"""
		return not self.isMonsterAppearJumping

	def monsterAppearAddFlags( self ):
		"""
		"""
		self.addFlag(csdefine.FLAG_CAN_FLY)
		self.addFlag(csdefine.FLAG_CANT_SELECTED)
		self.addFlag(csdefine.FLAG_HIDE_FLOAT_NAME)
		self.addFlag(csdefine.FLAG_HIDE_FLOAT_HPBAR)
		self.addFlag(csdefine.FLAG_HIDE_FLOAT_LEVEL)

	def monsterAppearRemoveFlags( self ):
		"""
		"""
		self.removeFlag(csdefine.FLAG_CAN_FLY)
		self.removeFlag(csdefine.FLAG_CANT_SELECTED)
		self.removeFlag(csdefine.FLAG_HIDE_FLOAT_NAME)
		self.removeFlag(csdefine.FLAG_HIDE_FLOAT_HPBAR)
		self.removeFlag(csdefine.FLAG_HIDE_FLOAT_LEVEL)		

	#-----------------------阴兵---------------------------------
	# def monsterAppearLineToPoint_chase(self, targetPos, posList, actionID, radius=10.0, speed=10.0):
	# 	"""
	# 	阴兵特殊移动--追击
	# 	"""
	# 	if self.isMonsterAppearLineToPoint:
	# 		return

	# 	times = 100
	# 	isCanMove = 0
	# 	while times and not isCanMove:
	# 		times -= 1
	# 		radian = random.uniform(-3.14,3.14)
	# 		x = radius * math.sin(radian) + targetPos.x
	# 		y = targetPos.y
	# 		z = radius * math.cos(radian) + targetPos.z
	# 		pos = Math.Vector3((x,y,z))
	# 		if self.isInRange(pos, posList):
	# 			isCanMove = 1
	# 			if self.getAllClients():
	# 				yaw = csarithmetic.getYawByVector3(pos-self.position)
	# 				self.direction = (0.0, 0.0, yaw)
	# 				self.isMonsterAppearLineToPoint = True
	# 				self.allClients.CLIENT_MonsterAppearLineToPoint(z*100, x*100, y*100, yaw*180/3.14, speed, actionID)
	# 				self.position = pos
	# 	if times == 0:
	# 		KBEDebug.ERROR_MSG("can't find a movePoint")


	def monsterAppearLineToPoint_chase(self, targetPos, posList, actionID, radius, moveTime):
		"""
		阴兵特殊移动--追击
		"""
		if self.isMonsterAppearLineToPoint:
			return

		times = 100
		isCanMove = 0
		while times and not isCanMove:
			times -= 1
			radian = random.uniform(-3.14,3.14)
			x = radius * math.sin(radian) + targetPos.x
			y = targetPos.y
			z = radius * math.cos(radian) + targetPos.z
			pos = Math.Vector3((x,y,z))
			if self.isInRange(pos, posList):
				isCanMove = 1
				if self.getAllClients():
					yaw = csarithmetic.getYawByVector3(pos-self.position)
					direction = (0.0, 0.0, yaw)
					self.changeDirection(direction, csdefine.REASON_CHANGE_DIR_FORCE)
					self.isMonsterAppearLineToPoint = True
					speed = self.position.distTo(pos)/moveTime
					self.onMonsterAppearLineToPointMove()
					self.addTimerCallBack(moveTime, "onMonsterAppearLineToPointMoveOver",())
					self.allClients.CLIENT_MonsterAppearLineToPoint(z*100, x*100, y*100, yaw*180/3.14, speed, actionID)
					self.position = pos
		if times == 0:
			KBEDebug.ERROR_MSG("can't find a movePoint")

	def monsterAppearLineToPoint_retreat(self, targetPos, posList, actionID, radius, moveTime):
		"""
		阴兵特殊移动--后撤
		"""
		if self.isMonsterAppearLineToPoint:
			return

		times = 100
		isCanMove = 0
		while times and not isCanMove:
			times -= 1
			radian = random.uniform(-3.14,3.14)
			x = radius * math.sin(radian) + targetPos.x
			y = targetPos.y
			z = radius * math.cos(radian) + targetPos.z
			pos = Math.Vector3((x,y,z))
			if self.isInRange(pos, posList):
				isCanMove = 1
				if self.getAllClients():
					yaw = csarithmetic.getYawByVector3(targetPos-pos)
					self.changeDirection(direction, csdefine.REASON_CHANGE_DIR_FORCE)
					self.isMonsterAppearLineToPoint = True
					speed = self.position.distTo(pos)/moveTime
					self.onMonsterAppearLineToPointMove()
					self.addTimerCallBack(moveTime, "onMonsterAppearLineToPointMoveOver",())
					self.allClients.CLIENT_MonsterAppearLineToPoint(z*100, x*100, y*100, yaw*180/3.14, speed, actionID)
					self.position = pos
		if times == 0:
			KBEDebug.ERROR_MSG("can't find a movePoint")

	def CELL_onMonsterAppearLineToPoint(self, exposed):
		"""
		"""
		pass

	def onMonsterAppearLineToPointMove(self):
		"""
		"""
		self.addBuff(self, YINBING_BUFFID)

	def onMonsterAppearLineToPointMoveOver(self):
		"""
		"""
		self.isMonsterAppearLineToPoint = False
		if self.getAllClients():
			#self.allClients.CLIENT_StopAction()
			self.allClients.MonsterAppearLineToPointOver()
		self.removeBuffByID(YINBING_BUFFID)	
		self.position = self.position

	def isInRange(self, pos, posList):
		"""
		判断是否在多边形范围内
		"""
		if len(posList)<3:
			return True

		return Functions.checkPositonIsInArea(pos, posList)


	def CELL_onMonsterJumpPointToPointEnd( self, exposed ):
		"""
		怪物跳跃点结束
		"""
		if self.moveJumpEndID:
			self.executeTimer( self.moveJumpEndID )



	def move_CST_9506(self ,yawBase, theta, moveTime = 0.5, radius=15, actionID="Show_04"):
		"""
		CST-9506 程序功能需求（22级）——副本勇闯绝命岛BOSS快速折线逃跑表现功能需求
		"""
		#以自身位置为起点 随机一个朝向  移动指定距离（radius） 
		#取多次 取到一个合适点就退出
		theta = int(theta/180*3.14/2 *100)
		radianList = list(x/100+yawBase for x in range(-theta, theta))
		restList = list(x/100+yawBase for x in range(-314, -314+theta)) + list(x/100+yawBase for x in range(314-theta, 314))
		random.shuffle(radianList)
		random.shuffle(restList)

		while radianList or restList:
			radian = radianList.pop() if len(radianList)  else restList.pop()
			#KBEDebug.ERROR_MSG("yawBase = %s, radian = %s, angle = %s"%(yawBase, radian, (radian-yawBase)*180/3.14))
			x = radius * math.sin(radian) + self.position.x
			z = radius * math.cos(radian) + self.position.z
			targetPos = Math.Vector3((x,self.position.y,z))
			raycastList = self.navmeshRaycast( self.position, targetPos )
			if len(raycastList):
				pos = Math.Vector3(raycastList[0])
				#距离大于radius的一半
				newRadius = pos.distTo(self.position)
				if newRadius>radius/2:
					moveSpeed = newRadius/moveTime
					yaw = csarithmetic.getYawByVector3(pos-self.position)
					direction = (0.0, 0.0, yaw)
					self.changeDirection(direction, csdefine.REASON_CHANGE_DIR_FORCE)
					self.onMonsterAppearLineToPointMove()
					self.addTimerCallBack(moveTime, "onMonsterAppearLineToPointMoveOver",())
					self.allClients.CLIENT_MonsterAppearLineToPoint(pos[2]*100, pos[0]*100, pos[1]*100, yaw*180/3.14, moveSpeed, actionID)
					self.position = pos
					return	



