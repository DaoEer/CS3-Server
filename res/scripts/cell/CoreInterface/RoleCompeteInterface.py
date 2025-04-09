# -*- coding: utf-8 -*-

import KBEngine
import KBEDebug
import csconst
import FightRuleMgr
import csdefine
import csstatus
import random
import Math
import csarithmetic




class RoleCompeteInterface:
	"""
	玩家切磋 类
	"""
	def __init__(self):
		self.competeState =  csdefine.COMPETE_NONE  #初始切磋状态
		self.competeTargetID= 0 		#切磋对手
		self.competeFlagID = 0 			#旗子ID
		self.readyStartCountDownTimerID = 0
		self.lastCountDownTimerID = 0
		self.roleCompeteTimeOutTimerID = 0
		self.competeInviterID = 0
		self.competeCenterPos = self.position
		self.competeCheckTimerID = 0
		self.leaveCompeteAreaTimerID = 0
		self.speekMsgID = 0
		self.tempInviterID = 0 #邀请邀请者ID 未同意切磋
		

	def isCanCompete(self, targetID):
		"""
		检测是否能进行切磋
		"""
		competeTarget = KBEngine.entities.get(targetID, None)
		if not competeTarget:
			self.statusMessage(csstatus.COMPETE_INVALID_SO_FAR)
			return False
		#地图是否允许切磋
		if not self.getCurrentSpace().getScript().getRoleIsCanCompete():
			self.statusMessage(csstatus.COMPETE_SPACE_CAN_NOT)
			return False

		#如果自身切磋状态不为COMPETE_NONE 返回false
		if self.competeState != csdefine.COMPETE_NONE:
			self.statusMessage(csstatus.COMPETE_SELF_IN_COMPETING)
			return False

		#如果目标切磋状态不为COMPETE_NONE 返回false
		if competeTarget.competeState != csdefine.COMPETE_NONE:
			self.statusMessage(csstatus.COMPETE_TARGET_IN_COMPETING)
			return False

		#判断是否在同一地图
		if competeTarget.spaceID != self.spaceID:
			self.statusMessage(csstatus.COMPETE_INVALID_SO_FAR)
			return False

		#判断自身是否在自由状态下
		if self.getState() != csdefine.ENTITY_STATE_FREE:
			self.statusMessage(csstatus.COMPETE_SELF_NOT_IN_FREE)
			return False

		#判断目标是否在自由状态下
		if competeTarget.getState() != csdefine.ENTITY_STATE_FREE:
			self.statusMessage(csstatus.COMPETE_TARGET_NOT_IN_FREE)
			return False

		#判断等级是否符合要求
		if self.getLevel()<csconst.COMPETE_MIN_LEVEL or competeTarget.getLevel()< csconst.COMPETE_MIN_LEVEL:	
			return False
		
		#判断是否超过距离
		if self.position.flatDistTo(competeTarget.position) >csconst.COMPETE_MAX_DIST:
			self.statusMessage(csstatus.COMPETE_INVALID_SO_FAR)
			return False

		return True


	def CELL_requestRoleCompete(self, callEntityID, competeTargetID):
		"""
		<exposed method>
		请求切磋
		"""
		if not self.validateClientCall( callEntityID ):
			return

		competeTarget = KBEngine.entities.get(competeTargetID, None)
		if  not competeTarget:
			return

		if not self.isCanCompete(competeTarget.id):
			return

		#发送邀请前讲骚话
		self.speekMsgID = random.sample(csconst.COMPETE_RAND_MSG, 1)[0]
		competeTarget.speekMsgID = self.speekMsgID +1
		self.statusMessageAllClients(self.speekMsgID, self.getName(), competeTarget.getName())

		#通知对手客户端接收邀请信息
		competeTarget.client.CLIENT_RoleCompeteBeInvited(self.id)
		#记录一下临时邀请者ID，玩家如果传送走了需要通知一下临时邀请者
		competeTarget.tempInviterID = self.id

	def CELL_requestAgreeRoleCompete(self, callEntityID, inviterID):
		"""
		<exposed method>
		同意切磋
		"""
		self.tempInviterID = 0
		if not self.validateClientCall( callEntityID ):
			return
		if not self.isCanCompete(inviterID):
			return		
		inviter = KBEngine.entities.get(inviterID, None)
		#接受邀请后 回应骚话
		self.statusMessageAllClients(self.speekMsgID, self.getName())
		inviter.statusMessage(csstatus.COMPETE_TARGET_ACCEPT, self.getName())

		#朝向对方 播放作揖动作
		self.playCompeteAction(self, csconst.COMPETE_ACTION_START, inviter, csconst.COMPETE_ACTION_START)

		self.setCompeteTargetID(inviterID)
		inviter.setCompeteTargetID(self.id)
		self.competeInviterID = inviterID
		inviter.competeInviterID = inviterID

		self.changeCompeteState(csdefine.COMPETE_READY)
		inviter.changeCompeteState(csdefine.COMPETE_READY)

		self.changeCompeteState(csdefine.COMPETE_READY)
		inviter.changeCompeteState(csdefine.COMPETE_READY)

		inviter.competeCheckTimerID = inviter.addTimerRepeat(0.5, "competeCheck",())
		self.competeCheckTimerID = self.addTimerRepeat(0.5, "competeCheck",())

		#开始倒计时
		inviter.roleCompeteStartCountdown(csconst.COMPETE_PREP_COUNTDOWN)


	def CELL_requestRefuseRoleCompete(self, callEntityID, inviterID):
		"""
		<exposed method>
		拒绝切磋
		"""
		self.tempInviterID=0
		inviter = KBEngine.entities.get(inviterID, None)
		if not inviter:
			return
		
		inviter.statusMessage(csstatus.COMPETE_TARGET_REFUSE, self.getName())
		inviter.changeCompeteState(csdefine.COMPETE_NONE)
		self.changeCompeteState(csdefine.COMPETE_NONE)


	def roleCompeteStartCountdown(self, time):
		"""
		开始切磋倒计时
		"""
		self.client.CLIENT_ShowCompeteCountDown(1, csconst.COMPETE_PREP_COUNTDOWN)
		competeTarget = KBEngine.entities.get(self.competeTargetID, None)
		if not competeTarget:
			return
		competeTarget.client.CLIENT_ShowCompeteCountDown(1, csconst.COMPETE_PREP_COUNTDOWN)

		self.placeCompeteFlag()
		#由于客户端的倒计时图片显示时间不准 导致定时器启动的时候数字还没播完 铜锣声会提前出现 加上一个延时
		delay = 1.0
		self.readyStartCountDownTimerID =  self.addTimerCallBack(time+delay, "roleCompeteStart", ())


	def roleCompeteStart(self):
		"""
		开始切磋
		"""
		competeTarget = KBEngine.entities.get(self.competeTargetID, None)
		if not competeTarget:
			return

		competeTarget.showMessagePlaySound(csconst.COMPETE_VOICEID)
		competeTarget.client.CLIENT_RoleCompeteStart(self.id)
		self.showMessagePlaySound(csconst.COMPETE_VOICEID)
		self.client.CLIENT_RoleCompeteStart(self.competeTargetID)

		self.changeCompeteState(csdefine.COMPETE_FIRE)
		competeTarget.changeCompeteState(csdefine.COMPETE_FIRE)
		FightRuleMgr.g_fightMgr.buildEnemyRelation( self, competeTarget)
		#加一个最后10s倒计时提示
		self.lastCountDownTimerID =  self.addTimerCallBack(csconst.COMPETE_TIME-csconst.COMPETE_LAST_COUNTDOWN, "onRoleCompeteLastCountDown", ())

	
	def onRoleCompeteLastCountDown(self):
		"""
		时间结束前10s倒计时提示
		"""
		self.lastCountDownTimerID = 0
		self.statusMessage(csstatus.COMPETE_COUNTDOWN_END, csconst.COMPETE_LAST_COUNTDOWN)
		# self.statusMessage(csstatus.COMPETE_COUNTDOWN, csconst.COMPETE_LAST_COUNTDOWN)
		self.client.CLIENT_ShowCompeteCountDown(2, csconst.COMPETE_LAST_COUNTDOWN)
		
		competeTarget = KBEngine.entities.get(self.getCompeteTargetID(), None)
		if competeTarget:
			competeTarget.statusMessage(csstatus.COMPETE_COUNTDOWN_END, csconst.COMPETE_LAST_COUNTDOWN)
			# competeTarget.statusMessage(csstatus.COMPETE_COUNTDOWN, csconst.COMPETE_LAST_COUNTDOWN)
			competeTarget.client.CLIENT_ShowCompeteCountDown(2, csconst.COMPETE_LAST_COUNTDOWN)

		#加个时间用完切磋结束回调
		self.roleCompeteTimeOutTimerID = self.addTimerCallBack(csconst.COMPETE_LAST_COUNTDOWN, "onRoleCompeteTimeOut", ())


	def onRoleCompeteTimeOut(self):
		"""
		时间耗尽
		"""
		competeTarget = KBEngine.entities.get(self.getCompeteTargetID(), None)
		if competeTarget:
			if competeTarget.HP / competeTarget.HP_Max > self.HP / self.HP_Max:
				self.loseCompete()
			else:
				competeTarget.loseCompete()


	def roleCompeteEnd(self):
		"""
		切磋结束
		"""
		inviter = KBEngine.entities.get(self.competeInviterID, None)
		if  inviter:		
			#准备倒计时中切磋结束
			if inviter.readyStartCountDownTimerID:
				inviter.popTimer(inviter.readyStartCountDownTimerID)
				inviter.readyStartCountDownTimerID = 0
				inviter.client.CLIENT_CloseCompeteCountDown()
			#过程中切磋结束 移除最后10s倒计时定时器
			if inviter.lastCountDownTimerID != 0:
				inviter.popTimer(inviter.lastCountDownTimerID)
				inviter.lastCountDownTimerID = 0


			#最后的倒计时过程中切磋结束 关闭倒计时界面 移除时间耗尽的定时器
			if inviter.roleCompeteTimeOutTimerID != 0:
				inviter.popTimer(inviter.roleCompeteTimeOutTimerID)
				inviter.roleCompeteTimeOutTimerID = 0
				inviter.client.CLIENT_CloseCompeteCountDown()

			if 	inviter.leaveCompeteAreaTimerID!=0:
				inviter.popTimer(inviter.leaveCompeteAreaTimerID)
				inviter.leaveCompeteAreaTimerID = 0
				inviter.client.CLIENT_CloseCompeteCountDown()

			if 	self.leaveCompeteAreaTimerID!=0:
				self.popTimer(self.leaveCompeteAreaTimerID)
				self.leaveCompeteAreaTimerID = 0

		eflag = KBEngine.entities.get(self.competeFlagID, None)

		competeTarget = KBEngine.entities.get(self.getCompeteTargetID(), None)
		if competeTarget:
			competeTarget.popTimer(competeTarget.competeCheckTimerID)
			competeTarget.competeCheckTimerID = 0
			self.competeRemoveEnemy(competeTarget)
			competeTarget.setCompeteTargetID(0)
			competeTarget.competeFlagID = 0
			competeTarget.changeCompeteState(csdefine.COMPETE_NONE)
			competeTarget.client.CLIENT_OnRoleCompeteEnd()
			competeTarget.tempInviterID = 0

		self.popTimer(self.competeCheckTimerID)
		self.competeCheckTimerID = 0
		self.setCompeteTargetID(0)
		self.competeFlagID = 0
		self.changeCompeteState(csdefine.COMPETE_NONE)
		if eflag:
			eflag.destroySelf()
		

		self.client.CLIENT_OnRoleCompeteEnd()


	def placeCompeteFlag(self):
		"""
		#插旗子
		"""
		competeTarget = KBEngine.entities.get(self.getCompeteTargetID(), None)
		if not competeTarget:
			return
		pos = (self.position + competeTarget.position)*0.5
		dir = (0.0, 0.0, 0.0)
		eflag = self.createEntityByScriptID(csconst.COMPETE_FLAG_SCRIPTID, pos, dir, {})
		if not eflag:
			return
		eflag.setTemp("competeTargetID1", self.id)
		eflag.setTemp("competeTargetID2", competeTarget.id)
		self.competeFlagID = eflag.id
		competeTarget.competeFlagID = eflag.id

		self.competeCenterPos = eflag.position
		competeTarget.competeCenterPos = eflag.position


	def leaveCompeteArea(self):
		"""
		离开切磋区域
		"""
		competeTarget = KBEngine.entities.get(self.getCompeteTargetID(), None)
		if competeTarget:
			competeTarget.statusMessage(csstatus.COMPETE_TARGET_LEAVE_AREA, self.getName())
		self.statusMessage(csstatus.COMPETE_SELF_LEAVE_AREA)
		self.leaveCompeteAreaTimerID = 0
		self.roleCompeteEnd()


	def onReceiveDamage(self):
		"""
		"""
		if self.competeState == csdefine.COMPETE_NONE:
			return
		if self.getState() == csdefine.ENTITY_STATE_DEAD:
			competeTarget = KBEngine.entities.get(self.getCompeteTargetID(), None)
			if competeTarget:
				competeTarget.statusMessage(csstatus.COMPETE_TARGET_DEAD)
			self.roleCompeteEnd()
			return



	def loseCompete(self):
		"""
		战败
		"""
		winner = KBEngine.entities.get(self.getCompeteTargetID(), None)
		if winner:
			winner.statusMessage(csstatus.COMPETE_WIN, self.getName())
			winner.allClients.statusMessage(csstatus.COMPETE_END,str(winner.getName())+"|"+ str(self.getName()))
			self.statusMessage(csstatus.COMPETE_LOSE, winner.getName())
			self.playCompeteAction(winner, csconst.COMPETE_ACTION_WIN, self, csconst.COMPETE_ACTION_LOSE)
		self.roleCompeteEnd()


	def changeCompeteState(self, state):
		"""
		改变切磋状态
		"""
		if self.competeState == state:	return
		oldState = self.competeState
		self.competeState = state
		self.onChangeCompeteState(oldState, self.competeState)


	def onChangeCompeteState(self, oldState, newState):
		"""
		"""
		pass


	def setCompeteTargetID(self, targetID):
		"""
		设置切磋对手ID
		"""
		self.competeTargetID =  targetID


	def getCompeteTargetID(self):
		"""
		获取切磋对手ID
		"""
		return self.competeTargetID


	def onLeaveSpaceNotify(self):
		"""
		"""
		if self.competeState != csdefine.COMPETE_NONE:
			self.leaveCompeteArea()
		#通知邀请者 距离过远无法切磋
		if self.tempInviterID!=0:
			inviter = KBEngine.entities.get(self.tempInviterID, None)
			if inviter:
				inviter.statusMessage(csstatus.COMPETE_INVALID_SO_FAR)
			self.tempInviterID = 0

	def competeCheck(self):
		"""
		切磋检测
		"""
		competeTarget = KBEngine.entities.get(self.competeTargetID, None)
		if not competeTarget:
			self.roleCompeteEnd()

		if self.position.flatDistTo(self.competeCenterPos) > csconst.COMPETE_AREA_DIST:
			if self.leaveCompeteAreaTimerID == 0:
				self.statusMessage(csstatus.COMPETE_SELF_LEAVE_AREA_WARNING, csconst.COMPETE_COME_BACK_AREA_TIME)
				self.client.CLIENT_ShowCompeteCountDown(3, csconst.COMPETE_COME_BACK_AREA_TIME)
				#KBEDebug.ERROR_MSG("please come back compete area in %f secends"%csconst.COMPETE_COME_BACK_AREA_TIME)
				self.leaveCompeteAreaTimerID = self.addTimerCallBack(csconst.COMPETE_COME_BACK_AREA_TIME,"leaveCompeteArea",())
		else:
			if self.leaveCompeteAreaTimerID !=0:
				self.popTimer(self.leaveCompeteAreaTimerID)
				self.leaveCompeteAreaTimerID = 0
				#KBEDebug.ERROR_MSG("you are come back in time")


	def competeRemoveEnemy(self, enemy):
		"""
		切磋结束 移除敌人列表
		"""
		selfPet = self.getActivePetCell()
		enemyPet = enemy.getActivePetCell()

		FightRuleMgr.g_fightMgr.breakEnemyRelation( self, enemy)
		if selfPet:
			FightRuleMgr.g_fightMgr.breakEnemyRelation( selfPet, enemy)
		if enemyPet:
			FightRuleMgr.g_fightMgr.breakEnemyRelation( self, enemyPet)
		if selfPet and enemyPet:
			FightRuleMgr.g_fightMgr.breakEnemyRelation( selfPet, enemyPet)


	def getCompeteActionBuffID(self, type):
		"""
		"""
		return csconst.COMPETE_ACTIONS_BUFF[type][self.getProfession()]

	def turnToCompeteTarget(self, target):
		"""
		"""
		yaw = csarithmetic.getYawByVector3(target.position-self.position)
		direction = (0.0, 0.0, yaw)
		self.changeDirection(direction, csdefine.REASON_CHANGE_DIR_FORCE)

	def playCompeteAction(self, player1, type1, player2, type2):
		"""
		播放切磋动作
		"""
		buffID1 = player1.getCompeteActionBuffID(type1)
		player1.turnToCompeteTarget(player2)
		player1.addBuff(player1, buffID1)

		buffID2 = player2.getCompeteActionBuffID(type2)
		player2.turnToCompeteTarget(player1)
		player2.addBuff(player2, buffID2)