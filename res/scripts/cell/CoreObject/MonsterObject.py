# -*- coding: utf-8 -*-


#
# 用于普通怪物的类型派生对象
#

#engine
import KBEngine
import Math
import KBEMath
import KBEDebug
#interface
from CoreObject import NPCBaseObject
import CoreInterface.MonsterChatInterface as MonsterChatInterface
import CoreInterface.MonsterCombatInterface as MonsterCombatInterface
import CoreInterface.MonsterModelInterface as MonsterModelInterface
import CoreInterface.NPCAmbulantInterface as NPCAmbulantInterface
import ImpInterface.MonsterAppearInterface as MonsterAppearInterface

from ConfigObject import PatrolRouteLoader
import ItemTypeEnum
import csarithmetic
import Functions


import KST
import csdefine
import csconst

class MonsterObject(
	NPCBaseObject.NPCBaseObject,
	MonsterChatInterface.MonsterChatInterface,
	MonsterCombatInterface.MonsterCombatInterface,
	MonsterModelInterface.MonsterModelInterface,
	MonsterAppearInterface.MonsterAppearInterface,
	NPCAmbulantInterface.NPCAmbulantInterface,
	):
	"""
	怪物对象基类
	"""
	def __init__( self ):
		NPCBaseObject.NPCBaseObject.__init__( self )
		NPCAmbulantInterface.NPCAmbulantInterface.__init__( self )
		MonsterChatInterface.MonsterChatInterface.__init__( self )
		MonsterCombatInterface.MonsterCombatInterface.__init__( self )
		MonsterModelInterface.MonsterModelInterface.__init__( self )
		MonsterAppearInterface.MonsterAppearInterface.__init__( self )
		self.getScript().initEntity( self )
		self.initialPosition = Math.Vector3(self.position)
		self.initialDirection = Math.Vector3(self.direction)
		self.resetKeepBuffs = []					#回走不移除的buff
		self.signs = set()
		self.countDownID = 0
		self.ishasLightWall = False
		self.onInit()

	def doEnterSpace( self ):
		"""
		进入一个空间调用
		"""
		NPCBaseObject.NPCBaseObject.doEnterSpace( self )
		NPCAmbulantInterface.NPCAmbulantInterface.doEnterSpace( self )
		MonsterCombatInterface.MonsterCombatInterface.doEnterSpace( self )
		

	def doLeaveSpace( self ):
		"""
		离开一个空间调用（在doEnterSpace之后）
		"""
		NPCBaseObject.NPCBaseObject.doLeaveSpace( self )
		MonsterCombatInterface.MonsterCombatInterface.doLeaveSpace( self )
		
	def onInit(self):
		"""
		"""
		#通知space初始化完成
		spaceEntity = self.getCurrentSpace()
		if not spaceEntity:
			return
		if self.spawnIndex in spaceEntity.monsterSpawnIndexs:
			spaceEntity.monsterSpawnIndexs.remove(self.spawnIndex)
			spaceEntity.monsterAIWaitStart.append(self.id)
			if not len(spaceEntity.monsterSpawnIndexs):
				spaceEntity.startMonsterAI()


	def setSelfEntityFlag(self):
		"""
		virtual method
		"""
		self.setEntityFlag( csdefine.ENTITY_FLAG_MONSTER )

	def setSelfEntityFlagExt(self):
		"""
		virtual method
		"""
		self.setEntityFlagExt( csdefine.ENTITY_FLAG_EXT_MONSTER )
		
	def getScript( self ):
		if not self._scriptObject:
			self._scriptObject = KST.g_objFactory.getMonsterObject( self.scriptID )
			
		return self._scriptObject
		
	def CELL_onClientReady( self, srcEntityID ):
		"""
		<Expose method>
		客户端Character Actor已经准备好
		"""
		NPCBaseObject.NPCBaseObject.CELL_onClientReady( self, srcEntityID )
		self.initAttackAndInitativeTrap( srcEntityID )
		if self.ishasLightWall:
			self.allClients.CLIENT_CreateFightArea()
		self.getScript().onClientReady(self)
	
	def getSpeed( self ):
		if  self.state != csdefine.ENTITY_STATE_FREE:	#跑
			return self.calculateSpeed( self.getScript().getRunSpeed( self ) )
		else:
			return self.calculateSpeed( self.getScript().getWalkSpeed( self ) ) 		#走

	def calculateSpeed(self, speed):
		"""
		"""
		speed_percent = max(min(self.speed_percent, ItemTypeEnum.PRECENTPROPERTYRANGE[1]), ItemTypeEnum.PRECENTPROPERTYRANGE[0]) 
		speed_value = max(min(self.speed_value, ItemTypeEnum.VALUEPROPERTYRANGE[1]), ItemTypeEnum.VALUEPROPERTYRANGE[0]) 
		return  max(min(speed * (1+speed_percent / ItemTypeEnum.PRECENTRATIO) + speed_value, ItemTypeEnum.RESULTPROPERTYRANGE[1]), ItemTypeEnum.RESULTPROPERTYRANGE[0])

	def onHPChanged( self, oldValue ):
		self.spaceEvent_monsterChangeHP()
		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			spaceEntity.getScript().onMonsterHPChanged( spaceEntity, self )
		MonsterCombatInterface.MonsterCombatInterface.onHPChanged( self, oldValue )

	def onFlagChange( self, oldFlags, newFlags ):
		"""
		virtual method
		标志位改变
		"""
		NPCBaseObject.NPCBaseObject.onFlagChange( self, oldFlags, newFlags )
		self.updateRelation()

	def onTempCampChange(  self, oldCamp, newCamp ):
		"""
		virtual method
		临时阵营改变
		"""
		self.updateRelation()

	def onTempFactionChange( self ):
		"""
		virtual method
		临时势力改变
		"""
		self.updateRelation()

	def updateRelation( self ):
		"""
		virtual method
		更新关系
		"""
		NPCBaseObject.NPCBaseObject.updateRelation( self )
		MonsterCombatInterface.MonsterCombatInterface.updateRelation(self)


	def beforeDestroy( self ):
		"""
		virtual method
		销毁前做一些事
		"""
		if self.ishasLightWall:  #策划不想配置死亡状态下执行AIAction136 关闭光墙的行为，所以在这里进行默认执行下
			self.stopLightWallCountDown()
			self.allClients.CLIENT_OnLeaveFightArea()
		MonsterCombatInterface.MonsterCombatInterface.beforeDestroy( self )
		NPCAmbulantInterface.NPCAmbulantInterface.beforeDestroy( self )
		NPCBaseObject.NPCBaseObject.beforeDestroy( self )

	def getSpawnPos( self ):
		return self.spawnPos

	def setSpawnPos( self, pos ):
		pos = Math.Vector3( pos )
		if self.parent:
			self.spawnPos = self.parent.positionWorldToLocal(pos) 
		else:
			self.spawnPos = pos

	def setSpawnPosBySpawnRoute( self ):
		"""
		根据巡逻路线设置出生点
		"""
		if self.spawnRoute == csconst.SPAWN_ROUTE:
			return 
		if not len( PatrolRouteLoader.g_patrolRouteLoader.getPatrolRoute( self.getCurrentSpaceScriptID(),self.spawnRoute) ):
			return 
		nearestPoint = PatrolRouteLoader.g_patrolRouteLoader.getNearestRoutePoint( self.getCurrentSpaceScriptID(), self.spawnRoute,Math.Vector3(self.position))
		spawnPos = Math.Vector3( PatrolRouteLoader.g_patrolRouteLoader.getPatrolRoute( self.getCurrentSpaceScriptID(),self.spawnRoute)[nearestPoint]['position'])
		self.setSpawnPos( spawnPos )

	def setMinHPPercent( self, value ):
		"""
		设置怪物最低血量值
		"""
		self.minHPPercent = value

	def setOldMinHPPercent( self, value ):
		"""
		设置怪物最低血量值
		"""
		self.oldMinHPPercent = value

	def setMonsterType( self, mtype ):
		"""
		设置怪物类型
		"""
		self.monsterType  =  mtype

	def getMonsterType( self ):
		"""
		获取怪物类型
		"""
		return self.monsterType

	def onMoveOver( self, controllerID, userData ):
		"""
		virtual method
		移动结束，但似乎不管移动是否成功，都调用此函数
		@param controllerID		:	移动控制器ID
		@type  controllerID     :	int
		"""
		NPCAmbulantInterface.NPCAmbulantInterface.doMoveOver( self, controllerID, userData )
		MonsterCombatInterface.MonsterCombatInterface.doMoveOver( self, controllerID, userData )
	
	def onMoveFailure( self, controllerID, userData ):
		"""
		virtual method
		移动失败
		@param controllerID		:	移动控制器ID
		@type  controllerID     :	int
		"""
		NPCAmbulantInterface.NPCAmbulantInterface.doMoveFailure( self, controllerID, userData )
		MonsterCombatInterface.MonsterCombatInterface.doMoveFailure( self, controllerID, userData )

	def stopMoving( self, moveScriptID ):
		"""
		virtual method
		"""
		if not NPCAmbulantInterface.NPCAmbulantInterface.stopMoving( self, moveScriptID ):
			return False
		self.behControlReset(1)
		return True

	def stopMovingForType( self, moveType ):
		"""
		停止移动，使用移动等级
		"""
		if not NPCAmbulantInterface.NPCAmbulantInterface.stopMovingForType( self, moveType ):
			return False
		self.behControlReset(1)
		return True
#--------------------------光墙倒计时-------------------------
	def startLightWallCountDown( self ):
		"""
		开始光墙倒计时
		"""
		self.ishasLightWall = True
		self.countDownID = self.addTimerRepeat( 1,"onLightWallCountDown",() )

	def onLightWallCountDown( self ):
		"""
		"""
		if self.wallCountDownTime == 0:
			self.popTimer(self.countDownID)
			self.countDownID = 0
			return
		self.wallCountDownTime -= 1

	def stopLightWallCountDown( self ):
		"""
		停止光墙倒计时
		"""
		self.ishasLightWall = False
		if self.countDownID:
			self.popTimer(self.countDownID)
			self.countDownID = 0
		self.wallCountDownTime = -1

	def CELL_notifyChangeMonsterDirection( self, srcEntityID, yaw ):
		"""
		<Exposed method>
		客户端通知怪物改变朝向完成
		"""
		direction = KBEMath.Unreal2KBEngineDirection((0.0, 0.0, float(yaw)))
		self.changeDirection(direction, csdefine.REASON_CHANGE_DIR_FORCE)
		

	def onFaceToPlayer( self, state):
		"""
		通知客户端是否开启在战斗状态下始终面向玩家
		"""
		self.allClients.CLIENT_FaceToPlayer( state )

#---------------------- timer --------------------------
	def timerValeDelCB( self, timerArg ):
		"""
		取消一个timer arg的回调，也可能是执行完了
		这里主要是处理掉一些存起来的timerArg
		"""
		MonsterCombatInterface.MonsterCombatInterface.timerValeDelCB( self, timerArg )


	def changeState( self, newState ):
		"""
		改变状态。
			@param newState	:	新的状态
			@type newState	:	integer
		"""
		if self.state == newState:
			return
		MonsterCombatInterface.MonsterCombatInterface.changeState(self,newState)
		
		if newState == csdefine.ENTITY_STATE_FREE:
			self.startRandomWalk(self.getSpeed(), True)

		if newState == csdefine.ENTITY_STATE_FIGHT:
			self.startWander()			
		else:
			self.stopWander()
		
		if newState == csdefine.ENTITY_STATE_DEAD:
			if self.isPlayDeadEffect():
				self.allClients.CLIENT_PlayDeadEffect()
			if self.isPlayDeadMortuaryEffect():
				self.allClients.PlayDeadMortuaryEffect()

		#记录战斗状态开始时间
		if newState == csdefine.ENTITY_STATE_FIGHT:
			self.monsterAICombatTime = Functions.getTime()
			attackID = self.findFirstEnemyByTime()		#切换成战斗状态时自动将敌人列表中的第一个敌人作为攻击目标
			if attackID:
				self.setTargetID(attackID)
		else:
			self.monsterAICombatTime = 0	


		#重置状态后可以被再次呼叫
		if newState == csdefine.ENTITY_STATE_RESET:
			self.callSign = False

		#一段时间后选择敌人列表中最近的一个作为攻击目标
		self.addTimerCallBack(0.2, "selectMinDisTarget",())


	def selectMinDisTarget(self):
		"""
		选择敌人列表中最近的一个作为攻击目标
		"""
		if self.getState()!=csdefine.ENTITY_STATE_FIGHT:
			return 
		if not len(self.enemyList):
			return
		minDist = 10000
		targetID = 0
		for enemyID in self.enemyList.keys():
			entity = KBEngine.entities.get(enemyID, None)
			if not entity:
				continue
			dist = entity.position.flatDistTo(self.position)
			if dist<=minDist:
				targetID = enemyID
				minDist = dist
		self.setTargetID(targetID)


	def onStateChanged( self, new, old ):
		"""
		状态切换。
			@param new	:	更改以后的状态
			@type new	:	integer
			@param old	:	更改以前的状态
			@type old	:	integer
		"""
		self.triggerEvent(csdefine.ENTITY_EVENT_ENTITY_STATE_CHANGE, [ new, old ])
		MonsterCombatInterface.MonsterCombatInterface.onStateChanged(self, new, old)
		self.updateRelation()

	def onActWordChangedTrigger(self, params):
		"""
		"""
		MonsterCombatInterface.MonsterCombatInterface.onActWordChangedTrigger(self, params)
		act, disabled =  params
		self.triggerSkillEvent( csdefine.SKILL_EVENT_ACT_WORD_CHANGE, self.id, {"actWord":act, "disabled": disabled})

	def triggerEventChangeMoveType(self, oldMoveType, newMoveType):
		"""
		移动类型改变事件
		"""
		args = [oldMoveType, newMoveType]
		self.triggerEvent(csdefine.ENTITY_EVENT_ON_CHANGE_MOVE_TYPE, args)


	#--------------------------------------状态改变回调（此处不做实现）-----------------------------------------
	def onEnterFree( self ):
		"""
		virtual method
		进入自由状态
		"""
		self.triggerEvent(csdefine.ENTITY_EVENT_ON_ENTER_FREE,[])
		MonsterCombatInterface.MonsterCombatInterface.onEnterFree(self)
		self.getScript().onEnterFree( self )
		
	def onLeaveFree( self ):
		"""
		virtual method
		离开自由状态
		"""
		MonsterCombatInterface.MonsterCombatInterface.onLeaveFree(self)
		self.getScript().onLeaveFree( self )
	
	def onEnterFight( self ):
		"""
		virtual method
		进入战斗
		"""
		self.triggerEvent(csdefine.ENTITY_EVENT_ON_ENTER_FIGHT,[])
		MonsterCombatInterface.MonsterCombatInterface.onEnterFight(self)
		self.getScript().onEnterFight( self )
		
	def onLeaveFight( self ):
		"""
		virtual method
		离开战斗
		"""
		MonsterCombatInterface.MonsterCombatInterface.onLeaveFight(self)
		self.allClients.CLIENT_RemoveChasePosInfo()
		self.getScript().onLeaveFight( self )
	
	def onEnterDead( self ):
		MonsterCombatInterface.MonsterCombatInterface.onEnterDead( self )
		self.getScript().onEnterDead( self )
		
		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			spaceEntity.onMonsterDie( self.id, self.scriptID, self.group )
		self.spaceEvent_monsterDie()
		
		hasbuffhitback = False
		for index, buff in self.attrBuffs.items():
			buffname = self.getBuff(buff.buffID).__class__.__name__
			if buffname == "BuffHitBack":
				hasbuffhitback = True
		if not hasbuffhitback:
			self.stopMovingForType(csdefine.SYSTEM_MOVE)

	def onLeaveDead( self ):
		"""
		virtual method
		离开死亡状态
		"""
		MonsterCombatInterface.MonsterCombatInterface.onLeaveDead(self)
		self.getScript().onLeaveDead( self )
		
	def onEnterPead( self ):
		"""
		virtual method
		进入未决状态
		"""
		MonsterCombatInterface.MonsterCombatInterface.onEnterPead(self)
		self.getScript().onEnterPead( self )
		self.isInPending = 1
		
	def onLeavePead( self ):
		"""
		virtual method
		离开未决状态
		"""
		MonsterCombatInterface.MonsterCombatInterface.onLeavePead(self)
		self.getScript().onLeavePead( self )
		self.isInPending = 0
		
	def onEnterWarn( self ):
		"""
		virtual method
		进入警戒状态
		"""
		MonsterCombatInterface.MonsterCombatInterface.onEnterWarn(self)
		self.getScript().onEnterWarn( self )
		
	def onLeaveWarn( self ):
		"""
		virtual method
		离开警戒状态
		"""
		MonsterCombatInterface.MonsterCombatInterface.onLeaveWarn(self)
		self.getScript().onLeaveWarn( self )
		
	def onEnterReset( self ):
		"""
		virtual method
		进入重置状态
		"""
		MonsterCombatInterface.MonsterCombatInterface.onEnterReset(self)
		self.getScript().onEnterReset( self )
		
	def onLeaveReset( self ):
		"""
		virtual method
		离开重置状态
		"""
		MonsterCombatInterface.MonsterCombatInterface.onLeaveReset(self)
		self.getScript().onLeaveReset( self )

	def onEnterShow( self ):
		"""
		virtual method
		进入表演状态
		"""
		MonsterCombatInterface.MonsterCombatInterface.onEnterShow(self)
		self.getScript().onEnterShow( self )

	def onLeaveShow( self ):
		"""
		virtual method
		离开表演状态
		"""
		MonsterCombatInterface.MonsterCombatInterface.onLeaveShow(self)
		self.getScript().onLeaveShow( self )

	def onEnterStable( self ):
		"""
		virtual method
		进入稳定状态
		"""
		MonsterCombatInterface.MonsterCombatInterface.onEnterStable(self)
		self.getScript().onEnterStable( self )

	def onLeaveStable( self ):
		"""
		virtual method
		离开稳定状态
		"""
		MonsterCombatInterface.MonsterCombatInterface.onLeaveStable(self)
		self.getScript().onLeaveStable( self )
