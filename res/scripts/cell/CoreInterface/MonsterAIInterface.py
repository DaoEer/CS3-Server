# -*- coding- : utf-8 -*-
import time
import random
import KBEngine
import SkillTargetObjImpl
import FightRuleMgr
import ECBProximityDefine
import Const
from CoreInterface import  BehaviourInterface
from ConfigObject.MonsterAI.AIBase import AIMgr

import KBEDebug
import csdefine
import csconst
import csstatus


class MonsterAIInterface(  BehaviourInterface.BehaviourInterface ):
	def __init__( self ):
		BehaviourInterface.BehaviourInterface.__init__( self )
		self.monsterAIIsRunning = False
		self.monsterAICurGroupState = ""
		self.monsterAICurSubState = 0
		self.monsterAICurSubStateStartTime = 0.0	#当前状态开始时间
		self.monsterAITickSpeed = 1.0
		self.monsterAITickCallBackID = 0
		self.monsterAIQuitPeadDelayTime = 1.0       #退出未决状态的延迟时间
		self.monsterAIQuitPeadTimeID = 0 			
		self.monsterAIChangePeadToState = csdefine.ENTITY_STATE_FREE   #退出未决状态默认切换到自由状态
		self.monsterAIDoInstTimerID = {}
		self.aiIDLoops={} 							#AI实例执行次数

		self._monsterAITargetID = 0
		self.monsterAITimeTag = {}					#AI时间标签记录
		self.monsterAIIDToRoleData = {}				#记录AI目标玩家是否执行过当前AI
		self.timerID = 0							#停掉计时器
		
		self._isOpenInitiactiveTrapEffect = False	#当前是否已加主动反应陷阱预警光效

		self.__fsm.init( self.getScriptID() )

	#----------------------------------
	# AI逻辑
	#----------------------------------
	def monsterAIStart( self ):
		"""
		AI开始工作
		"""	
		if self.monsterAIIsStart():#避免再次启动
			return
			
		if self.__fsm.fsm:
			self.monsterAIIsRunning = True
			self.__fsm.fsm.start( self )
	
	def monsterAIReStart( self ):
		"""
		AI重新开始
		"""
		if self.monsterAIIsStart():#避免再次启动
			self.monsterAIStop()
			
		if self.__fsm.fsm:
			self.monsterAIIsRunning = True
			self.__fsm.fsm.start( self )

	def monsterAIStop( self ):
		"""
		停止AI
		"""
		BehaviourInterface.BehaviourInterface.behStop( self )
		if self.__fsm.fsm:
			self.monsterAIIsRunning = False
			self.__fsm.fsm.stop( self )
		
		self.__monsterAIStopTick()
	
	def monsterAIReset( self ):
		"""
		AI重置
		"""			
		self.monsterAISetTarget(0)
		self.monsterAIResetEAI()
		self.monsterAIResetTimeTag()
		self.resetAIIDLoops()

	def monsterAISetTickSpeed( self, tickSpeed ):
		"""
		设置tick的时间
		"""
		self.__monsterAIStopTick()

		self.monsterAITickSpeed = tickSpeed
		if self.monsterAIGetCurGroupStateIsStartTick():
			self.monsterAIStartTick()
		else:
			self.addTimerCallBack(self.monsterAITickSpeed, "monsterAITick", ())

	def monsterAIStartTick( self ):
		"""
		开始tick
		"""
		KBEDebug.DEBUG_MSG_FOR_AI(self, "entity( id:%d scriptID:%s AI组状态:%s, AI子状态:%s ) 启动AI心跳( AITickSpeed:%s )!"\
		%(self.id, self.scriptID, self.monsterAICurGroupState, self.monsterAICurSubState, self.monsterAITickSpeed ))

		self.monsterAITickCallBackID = self.addTimerRepeat( self.monsterAITickSpeed, "monsterAITick", () )

	def monsterAIIsStart( self ):
		"""
		AI是否在开始状态
		"""
		return self.monsterAIIsRunning

	def monsterAITick( self ):
		"""
		定时器心跳回调
		"""
		KBEDebug.DEBUG_MSG_FOR_AI(self, "entity( id:%d scriptID:%s AI组状态:%s, AI子状态:%s ) 开始本次AI心跳!"%(self.id, self.scriptID, self.monsterAICurGroupState, self.monsterAICurSubState ))
		self.__fsm.fsm.tick( self )
		KBEDebug.DEBUG_MSG_FOR_AI(self, "entity( id:%d scriptID:%s AI组状态:%s, AI子状态:%s ) 结束本次AI心跳!"%(self.id, self.scriptID, self.monsterAICurGroupState, self.monsterAICurSubState ))

	def __monsterAIStopTick( self ):
		"""
		停止AI循环
		"""
		if self.monsterAITickCallBackID:
			KBEDebug.DEBUG_MSG_FOR_AI(self, "entity( id:%d scriptID:%s AI组状态:%s, AI子状态:%s ) 停掉AI心跳( monsterAITickCallBackID:%d )!"\
			%(self.id, self.scriptID, self.monsterAICurGroupState, self.monsterAICurSubState, self.monsterAITickCallBackID ))
			self.popTimer( self.monsterAITickCallBackID )
			self.monsterAITickCallBackID = 0

	def monsterAIStopTick( self ):
		self.__monsterAIStopTick()
	
	def monsterAIDelayTick(self):
		"""
		此处延时是做个保护，防止当前tick执行过快而上个事件还没执行完因此造成问题
		"""
		if self.monsterAITickCallBackID:			#策划要求在AI状态发生改变时立刻执行一遍心跳检测
			self.__monsterAIStopTick()
			self.monsterAITick()	
			self.monsterAIStartTick()

	#----------------------------------
	# AI外部接口
	#----------------------------------
	def monsterAISetCurGroupState( self, newGroupState ):
		"""
		设置组状态
		"""
		KBEDebug.DEBUG_MSG_FOR_AI(self, "entity( id:%d scriptID:%s AI组状态:%s, AI子状态:%s ) 切换至新的AI组状态( %s )!" \
			% (self.id, self.scriptID, self.monsterAICurGroupState, self.monsterAICurSubState, newGroupState ))
		self.monsterAICurGroupState = newGroupState
	
	def monsterAISetCurSubState( self, newSubState ):
		KBEDebug.DEBUG_MSG_FOR_AI(self, "entity( id:%d scriptID:%s AI组状态:%s, AI子状态:%s ) 切换至新的AI子状态( %d )!" \
			% (self.id, self.scriptID, self.monsterAICurGroupState, self.monsterAICurSubState, newSubState ))
		self.behControlReset( 0 )
		self.monsterAICurSubState = newSubState
		self.monsterAICurSubStateStartTime = time.time()

	def monsterAIGetCurGroupState( self ):
		return self.monsterAICurGroupState

	def monsterAIGetCurSubState( self ):
		return self.monsterAICurSubState
	
	def monsterAIGetCurGroupStateObj( self ):
		"""
		获取当前组状态对象
		"""
		return self.__fsm.fsm.getCurrentGroupState( self )

	def monsterAIGetCurGroupStateIsStartTick( self ):
		"""
		获取当前组状态是否开启Tick
		"""
		return self.__fsm.fsm.getCurrentGroupStateIsStartTick( self )
	
	def monsterAIGetCurSubStateObj( self ):
		"""
		获取当前子状态对象
		"""
		result = None
		groupStateObj = self.monsterAIGetCurGroupStateObj()
		if groupStateObj:
			result = self.monsterAIGetCurGroupStateObj().getCurrentSubState( self )
			
		return result

	def monsterAIChangeGroupState( self, newGroupState ):
		"""
		改变AI的组状态
		"""
		if self.__fsm.fsm:
			self.__fsm.fsm.changeGroupState( self, self.monsterAIGetCurGroupState(), newGroupState )
		else:
			KBEDebug.DEBUG_MSG_FOR_AI(self, "entity( id:%d scriptID:%s AI组状态:%s, AI子状态:%s ) 没有AI配置数据！"\
				%(self.id, self.scriptID, self.monsterAICurGroupState, self.monsterAICurSubState ))
			
	def monsterAIChangeSubState( self, newState ):
		"""
		改变状态
		"""
		if self.__fsm.fsm:
			self.__fsm.fsm.changeSubState( self, self.monsterAICurSubState, newState )
		else:
			KBEDebug.DEBUG_MSG_FOR_AI(self, "entity( id:%d scriptID:%s AI组状态:%s, AI子状态:%s ) 没有AI配置数据！"\
			% (self.id, self.scriptID, self.monsterAICurGroupState, self.monsterAICurSubState ))

	def monsterAIGetSubStateStart( self ):
		"""
		获取当前子状态开始多少秒
		"""
		return time.time() - self.monsterAICurSubStateStartTime

	def monsterAITriggerEvent( self, eventType, args = [], triggerEntity = None ):
		"""
		triggerEntity: 当不是自身entity触发此事件时，传入该entity（比如陷阱触发）
		触发一个事件
		"""
		if self._monsterAITriggerEventCheck(eventType, args, triggerEntity):
			self._onMonsterAITriggerEvent(eventType, args, triggerEntity)

	def _monsterAITriggerEventCheck(self, eventType, args = [], triggerEntity = None):
		"""
		在这次AI事件还没有执行完的时候，由于该事件的AI行为会再次触发相同的事件，这样会出现死循环，
		不断自我调用。加入monsterAIExecuteEventArray的目的，是为了防止这种问题。在还没执行完本次事件之前，
		相同的事件不能够再次被触发。
		"""
		if not (self.__fsm.fsm and self.monsterAIIsStart()):
			return False

		if  self.isState(csdefine.ENTITY_STATE_RESET) and eventType != csdefine.ENTITY_EVENT_ENTITY_STATE_CHANGE:					# 重置状态下不接收事件，除了状态改变的事件，主要是状态改变会影响AI组状态的
			KBEDebug.DEBUG_MSG_FOR_AI(self, "entity( id:%d scriptID:%s AI组状态:%s, AI子状态:%s ) 重置状态下不能触发事件( %d )（除状态改变外的事件）！"\
				% (self.id, self.scriptID, self.monsterAICurGroupState, self.monsterAICurSubState, eventType ))
			return False

		if eventType in self.monsterAIExecuteEventArray:
			return False
		return True
		
	def _onMonsterAITriggerEvent(self, eventType, args = [], triggerEntity = None):
		"""
		"""
		KBEDebug.DEBUG_MSG_FOR_AI(self, "entity( id:%d scriptID:%s AI组状态:%s, AI子状态:%s ) 开始触发事件( %d )!"\
			% (self.id, self.scriptID, self.monsterAICurGroupState, self.monsterAICurSubState, eventType ))

		self.monsterAIExecuteEventArray.append( eventType )
		self.__fsm.fsm.trigger( self, eventType, args, triggerEntity )

		KBEDebug.DEBUG_MSG_FOR_AI(self, "entity( id:%d scriptID:%s AI组状态:%s, AI子状态:%s ) 结束触发事件( %d )！"\
			% (self.id, self.scriptID, self.monsterAICurGroupState, self.monsterAICurSubState, eventType ))

		self.monsterAIExecuteEventArray.remove( eventType )

	#------------------------------
	# 主动攻击陷阱
	#------------------------------
	def caculateTrapHeight( self ):
		"""
		获取主动攻击和主动反应陷阱高度
		"""
		return max( self.getScript().getScoutHeight(), Const.MIN_SCOUT_HEIGHT )

	def monsterAIAddAttackTrap( self ):
		"""
		添加主动攻击陷阱
		"""
		if self.hasAttackTrap:
			return
		
		if self.attackRange <= 0:
			return
			
		if self.clusterPosIndex != -1:		# 集群怪不加主动攻击陷阱
			return
		
		self.hasAttackTrap = 1
		
		( isServerTrap, shape, shapeParam ) = self.getScript().getAttackTrapParams(self)
		trapHeight = self.caculateTrapHeight()
		if isServerTrap:	#是服务器端陷阱
			self.addShapeProximityExt( shape, shapeParam, trapHeight, ECBProximityDefine.PROXIMITY_AI_ATTACK_1 )
		else:
			self.allClients.CLIENT_AddClientAttackTrap( shape, shapeParam, float(trapHeight) )

	def monsterAICancelAttackTrap( self ):
		"""
		取消主动攻击陷阱
		"""
		if not self.hasAttackTrap:
			return
		self.hasAttackTrap = 0
		if self.isServerAttackTrap:
			self.cancelProximityByUserArg( ECBProximityDefine.PROXIMITY_AI_ATTACK_1 )
		else:
			self.allClients.CLIENT_CancelClientAttackTrap()
	
	def monsterAIOnEnterAIAttackTrap(self, entity, rangeXZ, rangeY, proximityID ):
		"""
		触发主动攻击陷阱
		"""
		if self.canBuildEnemyRelation(entity) and self.monsterAICheckInViewRange(entity.id):
			FightRuleMgr.g_fightMgr.buildEnemyRelation( self, entity )
		self.monsterAITriggerEvent(csdefine.ENTITY_EVENT_ENTER_ATTACK_RANGE, [], entity )

	def monsterAIOnLeaveAttackTrap( self, entity, proximityID ):
		pass

	def CELL_onClientEnterAIAttackTrap( self, srcEntityID, enterID ):
		"""
		exposed method
		触发客户端主动攻击陷阱
		"""
		if not self.hasAttackTrap:
			return
		
		entity = KBEngine.entities.get( enterID )
		if not entity:
			return
		if not entity.isReady() or entity.inDestroying():
			return
		
		self.monsterAIOnEnterAIAttackTrap( entity, 0, 0, 0 )

	def CELL_onClientLeaveAIAttackTrap( self, srcEntity, leaveID ):
		"""
		exposed method
		离开客户端主动攻击陷阱
		"""
		if not self.hasAttackTrap:
			return
		
		entity = KBEngine.entities.get( leaveID )
		if not entity:
			return
		if not entity.isReady() or entity.inDestroying():
			return
		self.monsterAIOnLeaveAttackTrap( entity, 0 )

	#------------------------------
	# 主动反应陷阱
	#------------------------------
	def mosnterAIAddInitiativeTrap( self ):
		"""
		添加主动反应陷阱
		"""
		if self.hasInitiativeTrap:
			return

		self.hasInitiativeTrap = 1
		
		if self.monsterAIGetCurSubStateObj():
			( isServerTrap, shape, shapeParam ) = self.monsterAIGetCurSubStateObj().getInitiativeTrapParams()
			trapHeight = self.caculateTrapHeight()
			if isServerTrap:
				self.addShapeProximityExt( shape, shapeParam, trapHeight, ECBProximityDefine.PROXIMITY_AI_INITIATIVE_1 )
			else:
				try:
					self.allClients.CLIENT_AddClientInitiativeTrap( shape, shapeParam, float(trapHeight) )
					if self._isOpenInitiactiveTrapEffect:
						self.allClients.CLIENT_OpenInitiactiveTrapEffect( shape, shapeParam, float(trapHeight) )
				except:
					pass
					
	def monsterAICancelInitiativeTrap( self ):
		"""
		取消主动反应陷阱
		"""
		if not self.hasInitiativeTrap:
			return
			
		self.hasInitiativeTrap = 0
		self._isOpenInitiactiveTrapEffect = False
		
		if self.monsterAIGetCurSubStateObj().isServerInitiativeTrap:
			self.cancelProximityByUserArg( ECBProximityDefine.PROXIMITY_AI_INITIATIVE_1 )
		else:
			self.allClients.CLIENT_CancelClientInitiativeTrap()

	def monsterAIOnEnterInitiativeTrap( self, entity, rangeXZ, rangeY, proximityID ):
		"""
		触发主动反应陷阱
		"""
		self.monsterAITriggerEvent(csdefine.ENTITY_EVENT_TRIGGER_PROXIMITY, [], entity )

	def monsterAIOnLeaveInitiativeTrap( self, entity, proximityID ):
		"""
		离开主动反应陷阱
		"""
		self.monsterAITriggerEvent(csdefine.ENTITY_EVENT_OUT_OF_TERRITORY, [], entity )

	def CELL_onClientEnterInitiativeTrap( self, srcEntityID, enterID ):
		"""
		exposed method
		触发客户端主动反应陷阱
		"""
		if not self.hasInitiativeTrap:
			return
		
		entity = KBEngine.entities.get( enterID )
		if not entity:
			return
		if not entity.isReady() or entity.inDestroying():
			return
		if not self.monsterAIGetCurSubStateObj(): #目前看来，没有子状态的状态上，主动反应陷阱也没有作用
			return
		self.monsterAIOnEnterInitiativeTrap( entity, 0, 0, 0 )

	def CELL_onClientLeaveInitiativeTrap( self, srcEntityID, leaveID ):
		"""
		exposed method
		离开客户端主动反应陷阱
		"""
		if not self.hasInitiativeTrap:
			return
		
		entity = KBEngine.entities.get( leaveID )
		if not entity:
			return
		if not entity.isReady() or entity.inDestroying():
			return
		self.monsterAIOnLeaveInitiativeTrap( entity, 0 )


	def initAttackAndInitativeTrap( self, playerID ):
		"""
		客户端actor创建好了，添加主动攻击陷阱和主动反应陷阱
		"""
		player = KBEngine.entities.get( playerID )
		if not player or not player.getClient():
			return
		
		( isServerTrap, shape, shapeParam ) = self.getScript().getAttackTrapParams(self)
		trapHeight = self.caculateTrapHeight()
		if self.hasAttackTrap and not isServerTrap:
			try:
				player.clientEntity( self.id ).CLIENT_AddClientAttackTrap( shape, shapeParam, float(trapHeight) )
			except:
				KBEDebug.DEBUG_MSG("AddAttackTrap: monster client not exist!",self.id)
		
		if self.hasInitiativeTrap:
			( isServerTrap, shape, shapeParam ) = self.monsterAIGetCurSubStateObj().getInitiativeTrapParams()
			if not isServerTrap:
				try:
					player.clientEntity( self.id ).CLIENT_AddClientInitiativeTrap( shape, shapeParam, float(trapHeight) )
					if self._isOpenInitiactiveTrapEffect:
						player.clientEntity( self.id ).CLIENT_OpenInitiactiveTrapEffect( shape, shapeParam, float(trapHeight) )
				except:
					KBEDebug.DEBUG_MSG("AddInitiativeTrap: monster client not exist!",self.id)

	def monsterAIReTriggerNearTrap( self ):
		"""
		重新触发周围陷阱
		"""
		if not self.isReady() or self.inDestroying():
			return
		
		entityList = self.entitiesInRangeExt( csdefine.RE_TRIGGER_NEAR_TRAP_RANGE, "Monster" )
		for entity in entityList:
			if not entity.isReal() or entity.inDestroying() or not entity.monsterAIIsStart(): #被传送/被销毁/AI没启动 都不需要触发陷阱
				continue
			entity.beReTriggerTrap( self, ECBProximityDefine.PROXIMITY_AI_ATTACK_1 )
			entity.beReTriggerTrap( self, ECBProximityDefine.PROXIMITY_AI_INITIATIVE_1 )
		self.allClients.CLIENT_PlayerReTriggerTrap()
	
	def CELL_onClientLeaveAIBattleRegion( self, srcEntityID ):
		"""
		触发客户端BOSS离开光墙区域就自动脱战
		"""
		if self.isState(csdefine.ENTITY_STATE_FIGHT):
			self.monsterAITriggerEvent( csdefine.ENTITY_EVENT_ACTIVE_LEAVE_BATTLE )

	def openInitiativeTrapEffect( self ):
		"""
		开启预警范围的光效显示
		"""	
		if not self.monsterAIGetCurSubStateObj() or not self.hasInitiativeTrap:
			return
		
		( isServerTrap, shape, shapeParam ) = self.monsterAIGetCurSubStateObj().getInitiativeTrapParams()
		trapHeight = self.caculateTrapHeight()
		if not isServerTrap:
			try:
				self._isOpenInitiactiveTrapEffect = True
				self.allClients.CLIENT_OpenInitiactiveTrapEffect( shape, shapeParam, float(trapHeight) )
			except:
				pass
	
	def closeInitiativeTrapEffect( self ):
		"""
		关闭预警范围的光效显示
		"""
		if not self.monsterAIGetCurSubStateObj() or not self.hasInitiativeTrap:
			return
			
		( isServerTrap, shape, shapeParam ) = self.monsterAIGetCurSubStateObj().getInitiativeTrapParams()
		if not isServerTrap:
			try:
				self._isOpenInitiactiveTrapEffect = False
				self.allClients.CLIENT_CloseInitiactiveTrapEffect()
			except:
				pass
		
	#---------------------------------------
	# AI目标
	#---------------------------------------
	def monsterAISetTarget( self, targetID ):
		"""
		设置AI目标
		"""
		self._monsterAITargetID = targetID
	
	def monsterAIGetTarget( self ):
		"""
		获取AI目标
		"""
		return self._monsterAITargetID
	
	def monsterAIGetTargetEntity( self ):
		"""
		获取AI目标entity
		"""
		targetEntity = KBEngine.entities.get( self._monsterAITargetID, None )
		if targetEntity and self.monsterAIIsCanAttack( targetEntity ):
			return targetEntity
		else:
			return None
	
	def monsterAIIsCanAttack( self, entity ):
		"""
		判断当前目标是否可攻击
		"""
		if not entity.isCombatEntity():
			return False
		if entity.getState() in csconst.NOT_FIGHT_STATES:
			return False
		
		if not self.monsterAICheckInTerritory():
			return False
		
		return True
	
	def monsterAIIsCanAttackUseID( self, entityID ):
		"""
		判断当前目标是否可攻击,使用ID
		"""
		entity = KBEngine.entities.get( entityID )
		if not entity:
			return False
		
		return self.monsterAIIsCanAttack( entity )

	#---------------------------------------
	# AI命令
	#---------------------------------------
	def monsterAISendCommand(self, entityID, cmd):
		"""
		发送命令
		<Define Method>
		@param entityID	: 接受命令者ID
		@param cmd		: 命令 字符串
		"""
		entity = KBEngine.entities.get( entityID, None )
		if entity:
			KBEDebug.DEBUG_MSG_FOR_AI(self, "entity( id:%d scriptID:%s AI组状态:%s, AI子状态:%s ) AI发送指令成功！send AICommand( cmd:%s ) to entity( id:%d scriptID:%s )!"\
			% (self.id, self.scriptID, self.monsterAICurGroupState, self.monsterAICurSubState, cmd, entity.id, entity.scriptID ))

			entity.monsterAIOnCommand(self.id, self.scriptID, cmd)
		else:
			KBEDebug.DEBUG_MSG_FOR_AI(self, "entity( id:%d scriptID:%s AI组状态:%s, AI子状态:%s ) AI发送指令失败！send AICommand( cmd:%s ) to entity( id:%d is not found )!"\
			% (self.id, self.scriptID, self.monsterAICurGroupState, self.monsterAICurSubState, cmd, entityID ))

	def monsterAIOnCommand(self, entityID, scriptID, cmd):
		"""
		<Define Method>
		接受发过来的命令
		@param entityID	: 发送命令者ID
		@param type 	: int
		@param scriptID	: 发送命令者scriptID
		@param type 	: int
		@param cmd		: 指令ID
		@param type 	: string
		"""
		KBEDebug.DEBUG_MSG_FOR_AI(self, "entity( id:%d scriptID:%s AI组状态:%s, AI子状态:%s ) AI接收指令成功！get AICommand( cmd:%s ) from entity( id:%d scriptID:%s )!"\
			% (self.id, self.scriptID, self.monsterAICurGroupState, self.monsterAICurSubState, cmd, entityID, scriptID ))

		self.monsterAITriggerEvent(csdefine.ENTITY_EVENT_COMMAND, (entityID, scriptID, cmd) )

	#---------------------------------------
	# AI动作/条件支持接口
	#---------------------------------------
	def monsterAICheckInViewRange( self, id ):
		"""
		是否在视野范围
		"""
		entity = KBEngine.entities.get( id, None )
		if entity:
				if entity.position.flatDistTo( self.position ) <= self.viewRange and self.checkScoutHeight( entity ):
					return True
		return False
	
	def monsterAICheckInTerritory( self ):
		"""
		是否在领域范围
		"""
		return self.monsterAICheckInSpawnPosition( self.territoryRange )
	
	def monsterAICheckInSpawnPosition( self,radius ):
		return self.position.distTo( self.spawnPos ) <= radius or self.localPosition.distTo( self.spawnPos ) <= radius

	def monsterAIIsCanUseSkillToTarget(self, skillID ):
		"""
		判断当前技能ID能否对目标使用
		"""
		if skillID and self.getTargetID():
			state = self.skillTargetUseableCheckByAI(skillID, self.getTargetID())
			return state == csstatus.SKILL_GO_ON or state == csstatus.SKILL_TOO_FAR
		else:
			return False

	def monsterAIIsCanUseSkillToSelf(self, skillID):
		"""
		判断当前技能ID是否可对自身使用
		"""
		if skillID:
			state = self.skillTargetUseableCheckByAI(skillID, self.id)
			return state == csstatus.SKILL_GO_ON
		else:
			return False

	def skillTargetUseableCheckByAI( self, skillID, targetID):

		if self.behIsOptimize(None, None):
			return csstatus.SKILL_GO_ON
			
		state = self.skillTargetUseableCheck( skillID, targetID )
		if state != csstatus.SKILL_GO_ON:
			return state
		skill = self.getSkill( skillID )
		target = KBEngine.entities[targetID]
		state = skill.useableCheck( self, SkillTargetObjImpl.createTargetObjEntity( target ) )
		return state

	def playGroupActions( self, actionIDs, delayTimes ):
		"""
		播放一组动作
		"""
		delayTime = 0
		for index in list(range( 0,len( actionIDs ) )):
			self.timerID = self.addTimerCallBack( delayTime, 'playAdmissionAction', ( actionIDs[index], )  )
			delayTime += delayTimes[index]

		self.addTimerCallBack( delayTime, 'setIsPlayAdmissionAction', (False,) )

	def StopCurrentAction( self ):
		"""
		停止当前动作(后续动作也一并停止)
		"""
		self.allClients.CLIENT_StopAction()
		self.popTimer( self.timerID )

	#---------------------------------------
	# EAI
	#---------------------------------------
	def monsterAIAddEAI(self, eaiID):
		"""
		增加EAIID
		"""
		if not eaiID in self.monsterEAIList:
			KBEDebug.DEBUG_MSG_FOR_AI(self, "entity( id:%d scriptID:%s AI组状态:%s, AI子状态:%s ) 添加EAI( eaiID:%d )!"\
			%(self.id, self.scriptID, self.monsterAICurGroupState, self.monsterAICurSubState, eaiID ))
			self.monsterEAIList.append(eaiID)
	
	def monsterAIExtEAI(self, eaiList ):
		"""
		增加EAIID
		"""
		KBEDebug.DEBUG_MSG_FOR_AI(self, "entity( id:%d scriptID:%s AI组状态:%s, AI子状态:%s ) 添加EAI( eaiID:%s )!"\
			%(self.id, self.scriptID, self.monsterAICurGroupState, self.monsterAICurSubState, eaiList ))
		self.monsterEAIList = list(set(self.monsterEAIList+ eaiList ))

	def monsterAIHasEAI(self,eaiID):
		"""
		判断是否有某一个eai
		"""
		if eaiID in self.monsterEAIList:
			return True
		else:
			return False

	def monsterAIRemoveEAI(self, eaiID):
		"""
		删除某EAIID
		"""
		if eaiID in self.monsterEAIList:
			self.monsterEAIList.remove(eaiID)

	def monsterAIResetEAI(self):
		"""
		重置EAI
		"""
		KBEDebug.DEBUG_MSG_FOR_AI(self, "entity( id:%d scriptID:%s AI组状态:%s, AI子状态:%s ) 重置 EAI!"\
		%(self.id, self.scriptID, self.monsterAICurGroupState, self.monsterAICurSubState ))

		self.monsterEAIList = []

	def monsterAIResetTimeTag( self ):
		"""
		清除时间标签
		"""
		KBEDebug.DEBUG_MSG_FOR_AI(self, "entity( id:%d scriptID:%s AI组状态:%s, AI子状态:%s ) 重置 AITimeTag!"\
		%(self.id, self.scriptID, self.monsterAICurGroupState, self.monsterAICurSubState ))
		self.monsterAITimeTag = {}

	def monsterAIMarkRoleForAIID(self, aiid, playerDBID):
		"""
		某些AI行为只能对AI目标玩家执行一次，加数据进行记录保存
		"""
		if not aiid	in self.monsterAIIDToRoleData:
			self.monsterAIIDToRoleData[aiid] = [playerDBID]
		else:
			self.monsterAIIDToRoleData[aiid].append(playerDBID)

	def monsterAIIsMarkRoleForAIID(self,aiid, playerDBID):
		"""
		用于判断AI行为是否已经对AI目标玩家执行过
		"""
		if aiid in self.monsterAIIDToRoleData:
			if playerDBID in self.monsterAIIDToRoleData[aiid]:
				return True
			else:
				return False
		else:
			return False

	def monsterAIShowMessagePlaySound(self, player, voiceIDStr):
		"""
		播放语音并显示半身像
		"""
		if not player or player.getEntityFlag()!=csdefine.ENTITY_FLAG_ROLE:
			return
		voiceIDList = voiceIDStr.split("|")
		for voiceID in voiceIDList:
			param = {voiceID:self.id}
			player.playSoundRecords["AI"].update(param)
		player.showMessagePlaySound(voiceIDStr)

	def monsterAIGetFSM( self ):
		return  self.__fsm.fsm

	#-------------------------------------------
	# KBEngine calback
	#-------------------------------------------
	def onWitnessed( self, isWitnessed ):
		"""
		玩家视野范围内才开始执行AI
		"""
		if isWitnessed == True:
			spaceEntity = self.getCurrentSpace()
			if spaceEntity:
				if self.spawnIndex in spaceEntity.monsterAIWaitStart:
					return
					
			self.monsterAIStart()
			self.monsterAITriggerEvent( csdefine.ENTITY_EVENT_ON_WITNESSED )
		elif isWitnessed == False:
			if not self.hasFlag(csdefine.FLAG_AI_TICK):
				#因为不在玩家视野范围内，停掉怪物AI，需要考虑到怪物状态回到自由状态，清除EAI等问题，需要一个周全的考虑，所以暂时不停掉AI
				#self.AIStop()
				return
		elif isWitnessed == True and self.monsterAITickCallBackID:
			return

		
	#---------------------- timer --------------------------
	def timerValeDelCB( self, timerArg ):
		"""
		取消一个timer arg的回调，也可能是执行完了
		这里主要是处理掉一些存起来的timerArg
		"""
		pass


	#----------------------CallBack-------------------------
	
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
		

	def monsterAIDoInst(self, aiInst, *args):
		"""
		"""
		_id = aiInst._id
		_delayTime = aiInst._delayTime
		_repeatTime = aiInst._repeatTime

		if _repeatTime>0.0:
			self.monsterAIDoInstTimerID[_id] = self.addTimerRepeatExt(_delayTime, _repeatTime, "onMonsterAIDoInst", (aiInst, args))
		elif _delayTime>0.0:
			self.monsterAIDoInstTimerID[_id] = self.addTimerCallBack(_delayTime, "onMonsterAIDoInst", (aiInst, args))


	def onMonsterAIDoInst(self, aiInst, *args):
		"""
		"""
		aiInst.doAI(self)

	def stopMonsterAIInst(self, aiInstID):
		"""
		"""
		self.popTimer(self.monsterAIDoInstTimerID[aiInstID])
		self.monsterAIDoInstTimerID[aiInstID] = 0
		
	def setAIIDLoops(self, aiID, loops ):
		"""
		"""
		self.aiIDLoops[aiID] = loops

	def getAIIDLoops(self, aiID):
		"""
		"""
		if aiID in self.aiIDLoops:
			return self.aiIDLoops[aiID]
		else:
			return 0

	def resetAIIDLoops(self):
		"""
		"""
		self.aiIDLoops.clear()

		                                                                                                               