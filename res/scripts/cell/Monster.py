# -*- coding: utf-8 -*-


"""
usage:
	怪物基类

attribute:
	modelNumber

member function:
	getModelNumber
	setModelNumber

callback:
	pass

"""


#python
#engine
import KBEngine
import KBEDebug
#script
import CoreObject.MonsterObject as MonsterObject
import time
import csarithmetic
import csdefine
import Const


class Monster( MonsterObject.MonsterObject ):
	"""
	怪物基类
	"""
	def __init__( self ):
		MonsterObject.MonsterObject.__init__( self )
		#self.setMonsterType( csdefine.MONSTER_TYPE_MONSTER )
		self._isPlayAdmissionAction = False			#是否在播放出场动作
		self._isShowMove = False 					#是否在做出场动作的移动
		self.attackRange =	self.getScript().attackRange
		self.isServerAttackTrap = self.getScript().isServerAttackTrap						# 主动攻击陷阱类型：默认为客户端陷阱
		self.attackTrapShape = self.getScript().attackTrapShape							# 主动攻击陷阱形状：默认为方形（配为服务器端陷阱时可以减少消耗）

	def checkScoutHeight( self, entity ):
		"""
		override
		"""
		if self.getScript().getScoutHeight() >= Const.MIN_SCOUT_HEIGHT and abs( self.position.y - entity.position.y ) > self.getScript().getScoutHeight():
			return False
		else:
			return True
		
	def isPlayAdmissionAction( self ):
		"""
		是否正在播放出场动作
		"""
		return self._isPlayAdmissionAction
		
	def setIsPlayAdmissionAction( self, bValue ):
		"""
		设置_isPlayAdmissionAction
		"""
		self._isPlayAdmissionAction = bValue

	def playAdmissionAction( self, actionID ):
		"""
		怪物播放出场动作
		"""
		if actionID.strip() == "":
			KBEDebug.ERROR_MSG(" actionID is invalid! ")
			return
		self._isPlayAdmissionAction = True
		self.allClients.CLIENT_PlayAdmissionAction( actionID )

	def CELL_OnPlayAdmissionAction( self, exposed ):
		"""
		<Exposed method>
		怪物播放出场动作的回调
		"""
		pass


	def monsterShow( self, actionID, playTime, targetPosition, isChangeDir ):
		"""
		怪物特殊登场
		"""
		#加上浮空标志位
		self.addFlag(9)
		#先转向
		if isChangeDir:
			v = targetPosition - self.position
			direction = (0.0,0.0,csarithmetic.getYawByVector3( v ))
			self.changeDirection(direction, csdefine.REASON_CHANGE_DIR_FORCE)
		self._isPlayAdmissionAction = True
		self.addTimerCallBack( 0.2, 'monsterShowDelayCallBack', ( actionID, playTime, targetPosition, isChangeDir ))

	def monsterShowDelayCallBack( self, actionID, playTime, targetPosition, isChangeDir ):
		"""
		因为现在客户端动作衔接存在一个0.2秒融合的问题，需要延迟播放
		"""
		if isChangeDir:
			moveSpeed = self.position.flatDistTo( targetPosition ) / playTime
			self.chargeToPosition( targetPosition, moveSpeed, 0.1 )
		self.playAdmissionAction( actionID )
		self.addTimerCallBack( playTime, 'onMonsterShow', ( isChangeDir, ) )


	def onMonsterShow( self, isChangeDir ):
		"""
		登场结束时的回调
		"""
		self.removeFlag(9)
		AItargetEntity = self.monsterAIGetTargetEntity()
		if AItargetEntity:
			if isChangeDir:
				v = AItargetEntity.position - self.position
				direction = (0.0,0.0,csarithmetic.getYawByVector3( v ))	
				self.changeDirection(direction, csdefine.REASON_CHANGE_DIR_FORCE)	
		self._isPlayAdmissionAction = False

	def monsterShowEx( self, actionID, playTime, targetPosition, isChangeDir):
		"""
		怪物特殊登场
		"""
		#加上浮空标志位
		self.addFlag(9)
		#先转向
		if isChangeDir:
			v = targetPosition - self.position
			direction = (0.0,0.0,csarithmetic.getYawByVector3( v ))
			self.changeDirection(direction, csdefine.REASON_CHANGE_DIR_FORCE)

		self._isPlayAdmissionAction = True
		self.addTimerCallBack( 0.2, 'monsterShowDelayCallBackEx', ( actionID, playTime, targetPosition, isChangeDir ))

	def monsterShowDelayCallBackEx( self, actionID, playTime, targetPosition, isChangeDir ):
		"""
		因为现在客户端动作衔接存在一个0.2秒融合的问题，需要延迟播放
		"""
		moveSpeed = self.position.flatDistTo( targetPosition ) / playTime
		self.chargeToPosition( targetPosition, moveSpeed, 0.1 )
		self.playAdmissionAction( actionID )
		self.addTimerCallBack( playTime, 'onMonsterShowEx', ( isChangeDir, ) )

	def onMonsterShowEx( self, isChangeDir ):
		"""
		登场结束时的回调
		"""
		self.removeFlag(9)
		AItargetEntity = self.monsterAIGetTargetEntity()
		if AItargetEntity:
			if isChangeDir:
				v = AItargetEntity.position - self.position
				direction = (0.0,0.0,csarithmetic.getYawByVector3( v ))
				self.changeDirection(direction, csdefine.REASON_CHANGE_DIR_FORCE)		
		self._isPlayAdmissionAction = False
		
	def moveStart( self, mScriptID, mSpeed, isUpdateSpeed, mArgs  = () ):
		MonsterObject.MonsterObject.moveStart( self, mScriptID, mSpeed, isUpdateSpeed, mArgs )

	def onMoveOver( self, controllerID, userData ):
		"""
		virtual method
		移动结束，但似乎不管移动是否成功，都调用此函数
		@param controllerID		:	移动控制器ID
		@type  controllerID     :	int
		"""
		MonsterObject.MonsterObject.onMoveOver( self, controllerID, userData )

	def CELL_ChangeMonsterParent( self, exposed, destEntityID, parentID ):
		"""
		<Exposed method>
		当怪物从移动平台掉下时，更改怪物的parent
		"""
		parentEntity = None
		monsterEntity  = KBEngine.entities.get( destEntityID, None )
		if parentID:
			parentEntity  = KBEngine.entities.get( parentID, None )
		monsterEntity.parent = parentEntity

	
















