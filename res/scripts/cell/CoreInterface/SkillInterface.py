# -*- coding: utf-8 -*-


"""
usage:
	技能接口类

"""


#python
import math
import time
import copy
#engine
import KBEngine
import Math
#cell
import Const
import ConfigObject.Skill.SkillLoader as SkillLoader
import ConfigObject.Skill.BuffLoader as BuffLoader
import ConfigObject.Skill.EffectLoader as EffectLoader
import ConfigObject.Skill.SkillPostureLoader as SkillPostureLoader
#common
import KBEDebug
import csconst
import csdefine
import csarithmetic
import Functions
#data
import csstatus
#user_type
import SkillTargetObjImpl
#server_common
import KBEMath
import Settings
import KST


class SkillInterface:
	def __init__( self ):
		self.buffHoldTickTimerID = 0
		self.postureEffectIndex = -1
		
		self.__temp_skill_object = None
	
	def doEnterSpace( self ):
		"""
		KBEngine callback
		进入一个空间调用
		"""
		self.__temp_skill_object = None

	def doLeaveSpace( self ):
		"""
		KBEngine callback
		离开一个空间调用（在doEnterSpace之后）
		"""
		pass
		 
	def beforeDestroy( self ):
		"""
		销毁前做一些事
		"""
		if self.isEntityFlag(csdefine.ENTITY_FLAG_ROLE):
			self.roleCalculateBuffsOnDestroy()
		
		else:	#如果是其他entity，就简单的移除buff（以便结束buff光效）
			self.removeAllBuff()
		
		self.triggerSkillEvent( csdefine.SKILL_EVENT_DESTROY, self.id, {} )
	
#-----------玩家使用技能接口------------------------------------------------------------------------
	def useSkillToEntityFC( self, srcID, skillID, targetID ):
		"""
		<Exposed Method>
		客户端申请向entity施法
		"""
		userEntity = KBEngine.entities.get( self.id, None )
		#施法者为幻兽时需判断是否为玩家当前出战幻兽
		if userEntity.isEntityFlag(csdefine.ENTITY_FLAG_VEHICLEPET):
			srcEntity = KBEngine.entities.get( srcID, None )
			if srcEntity._activePetBase:
				srcID = srcEntity._activePetBase.id
			else:
				return
		if not self.validateClientCall( srcID ):
			return
		actForbid = None
		skill = self.getSkill( skillID )
		if skill is None:
			KBEDebug.CRITICAL_MSG( "%i: skill %i not exist." % ( self.id, skillID ) )
		else:
			actForbid = skill.getActForbid()
		self.triggerSkillEvent(csdefine.SKILL_EVENT_REQUEST_ACTION, self.id, {"requestType":csdefine.SKILL_EVENT_ACTION_TYPE_CAST, "id" : skillID, "actForbid" : actForbid})
		statusID = self.useSkillToEntity( skillID, targetID )
		if statusID != csstatus.SKILL_GO_ON and ( self.isEntityFlag(csdefine.ENTITY_FLAG_ROLE) or \
		self.isEntityFlag(csdefine.ENTITY_FLAG_VEHICLEPET) ):
			self.statusMessage( statusID, "" )
	
	def useSkillToPositionFC( self, srcID, skillID, pos ):
		"""
		<Exposed Method>
		客户端申请向位置施法
		"""
		userEntity = KBEngine.entities.get( self.id, None )
		#施法者为幻兽时需判断是否为玩家当前出战幻兽
		if userEntity.isEntityFlag(csdefine.ENTITY_FLAG_VEHICLEPET):
			srcEntity = KBEngine.entities.get( srcID, None )
			if srcEntity._activePetBase:
				srcID = srcEntity._activePetBase.id
			else:
				return
		if not self.validateClientCall( srcID ):
			return
		actForbid = None
		skill = self.getSkill( skillID )
		if skill is None:
			KBEDebug.CRITICAL_MSG( "%i: skill %i not exist." % ( self.id, skillID ) )
		else:
			actForbid = skill.getActForbid()
		self.triggerSkillEvent(csdefine.SKILL_EVENT_REQUEST_ACTION, self.id, {"requestType":csdefine.SKILL_EVENT_ACTION_TYPE_CAST, "id" : skillID, "actForbid" : actForbid})
		pos = KBEMath.Unreal2KBEnginePosition( pos )
		statusID = self.useSkillToPosition( skillID, pos )
		if statusID != csstatus.SKILL_GO_ON and ( self.isEntityFlag(csdefine.ENTITY_FLAG_ROLE) or \
		self.isEntityFlag(csdefine.ENTITY_FLAG_VEHICLEPET) ):
			self.statusMessage( statusID, "" )
	
	def useSkillToEntityForItem( self, skillID, targetID, itemUID ):
		"""
		对entity施法，用于物品施法
		"""
		self.setUsingItem( itemUID )
		statusID = self.useSkillToEntity( skillID, targetID )
		if statusID != csstatus.SKILL_GO_ON and self.isEntityFlag(csdefine.ENTITY_FLAG_ROLE):
			self.setUsingItem(0)
		return statusID

	def useSkillToEntityForItemPos( self, skillID, Pos, itemUID ):
		"""
		对entity施法，用于物品位置施法
		"""
		self.setUsingItem( itemUID )
		statusID = self.useSkillToPosition( skillID, Pos )
		if statusID != csstatus.SKILL_GO_ON and self.isEntityFlag(csdefine.ENTITY_FLAG_ROLE):
			self.setUsingItem(0)
		return statusID

#-----------技能使用基础接口------------------------------------------------------------------------
	def useSkillToEntity( self, skillID, targetID ):
		"""
		<Define method>
		向entity施法
		"""
		skill = self.getSkill( skillID )
		if skill is None:
			KBEDebug.CRITICAL_MSG( "%i: skill %i not exist." % ( self.id, skillID ) )
			return csstatus.SKILL_NOT_EXIST
		
		if skill.getTargetType() == csdefine.SKILL_CAST_OBJECT_TYPE_NONE:	#无施法目标，默认对自身释放
			targetID = self.id
		
		checkResult = self.skillTargetUseableCheck( skillID, targetID )
		if checkResult != csstatus.SKILL_GO_ON:
			return checkResult
		
		KST.calculateUseSkillTimes(self.getEntityFlag())
		target = KBEngine.entities[ targetID ]
		return skill.useSkill( self, SkillTargetObjImpl.createTargetObjEntity( target ) )

	def useSkillToPosition( self, skillID, pos ):
		"""
		<Define method>
		向位置施法
		"""
		skill = self.getSkill( skillID )
		if skill is None:
			KBEDebug.CRITICAL_MSG( "%i: skill %i not exist." % ( self.id, skillID ) )
			return csstatus.SKILL_NOT_EXIST
		
		pos = Math.Vector3( pos )
		checkResult = self.skillPosUseableCheck( skillID, pos )
		if checkResult != csstatus.SKILL_GO_ON:
			return checkResult
		
		KST.calculateUseSkillTimes(self.getEntityFlag())
		return skill.useSkill( self, SkillTargetObjImpl.createTargetObjPosition( pos ) )

	def useSkillToEntityGM( self, srcEntity, skillID, targetID ):
		"""
		GM指令 向某entity施法
		"""
		actForbid = None
		skill = self.getSkill( skillID )
		if skill is None:
			KBEDebug.CRITICAL_MSG( "%i: skill %i not exist." % ( self.id, skillID ) )
		else:
			actForbid = skill.getActForbid()
		self.triggerSkillEvent(csdefine.SKILL_EVENT_REQUEST_ACTION, self.id, {"requestType":csdefine.SKILL_EVENT_ACTION_TYPE_CAST, "id" : skillID, "actForbid" : actForbid})
		statusID = self.useSkillToEntity( skillID, targetID )
		if statusID != csstatus.SKILL_GO_ON:
			srcEntity.statusMessage( statusID, "" )

#-----------技能能否使用检测接口------------------------------------------------------------------------
	def skillTargetUseableCheck( self, skillID, targetID ):
		"""
		技能能否对目标entity使用
		"""
		if self.getEntityFlag()==csdefine.ENTITY_FLAG_MONSTER:
			if self.behIsOptimize(None,None):
				return csstatus.SKILL_GO_ON

		skill = self.getSkill( skillID )
		if skill is None:
			KBEDebug.CRITICAL_MSG( "%i: skill %i not exist." % ( self.id, skillID ) )
			return csstatus.SKILL_NOT_EXIST
		
		if skill.isPassiveSkill():
			KBEDebug.ERROR_MSG("passive skill(id:%i) cannot active use!!"%skillID )
			return csstatus.SKILL_CAST_FAILED
		
		if not KBEngine.entities.has_key( targetID ):
			KBEDebug.WARNING_MSG( "%s(%s) skill target not found. targetID:%s" %( self.getName(), self.id, targetID ) )
			return csstatus.SKILL_UNKNOWN
		
		target = KBEngine.entities.get(targetID, None)
		if skill.getTargetType() == csdefine.SKILL_CAST_OBJECT_TYPE_ENTITY and target == None:
			return csstatus.SKILL_CAST_ENTITY_ONLY

		if target.inDestroying():
			KBEDebug.WARNING_MSG( "%s(%s) skill target is destroying or destroyed. targetID:%s" %( self.getName(), self.id, targetID ) )
			return csstatus.SKILL_UNKNOWN
		
		if target.spaceID != self.spaceID:
			KBEDebug.WARNING_MSG( "%s(%s): skill target %s spaceID error." % ( self.getName(), self.id, targetID ) )
			return csstatus.SKILL_UNKNOWN
		
		return csstatus.SKILL_GO_ON

	def skillPosUseableCheck( self, skillID, pos ):
		"""
		技能能否对目标位置使用
		"""
		skill = self.getSkill( skillID )
		if skill is None:
			KBEDebug.CRITICAL_MSG( "%i: skill %i not exist." % ( self.id, skillID ) )
			return csstatus.SKILL_NOT_EXIST
		
		if skill.isPassiveSkill():
			KBEDebug.ERROR_MSG("passive skill(id:%i) cannot active use!!"%skillID )
			return csstatus.SKILL_CAST_FAILED
		
		return csstatus.SKILL_GO_ON
	
#------------------------------------------------------------------------
	def intonateSpell( self, intonateTime, skillID ):
		"""
		引导过程 吟唱（只是表现功能，非吟唱技能）
		"""
		if self.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ):
			self.client.intonateSpell( float( intonateTime ), skillID )
		
	def intonateSpellOver( self ):
		"""
		引导 吟唱结束
		"""
		if self.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ):
			self.client.intonateSpellOver()

#------------------------------------------------------------------------
	def setCooldown( self, cooldownDict ):
		"""
		设置冷却时间
		"""
		if not self.attrCooldowns:
			self.attrCooldowns = []
		
		currTime = Functions.getTime()
		validList = []
		#清理失效的冷却时间
		for dDict in self.attrCooldowns:
			if dDict["endTime"] > currTime:
				validList.append( dDict )
		self.attrCooldowns = validList
		
		#生成最新的冷却时间
		for id, cdTime in cooldownDict.items():
			newEndTime = Functions.getTime(cdTime)
			
			find = False
			for dDict in self.attrCooldowns:
				if dDict["id"] == id:
					if dDict["endTime"] < newEndTime:
						dDict["endTime"] = newEndTime
						dDict["persistTime"] = float( cdTime )
					find = True
			
			if not find:
				newDict = { "id":id, "endTime":newEndTime, "persistTime":float(cdTime) }
				self.attrCooldowns.append( newDict )

	def changeCooldown( self, paramDict ):
		"""
		增/减CD
		"""
		if not self.attrCooldowns:
			self.attrCooldowns = []
		
		currTime = Functions.getTime()
		validList = []
		#清理失效的冷却时间
		for dDict in self.attrCooldowns:
			if dDict["endTime"] > currTime:
				validList.append( dDict )
		self.attrCooldowns = validList
		
		for id, value in paramDict.items():
			#加CD
			if value > 0:
				hasCD = False
				for dDict in self.attrCooldowns:
					if dDict["id"] == id:
						hasCD = True
						dDict["endTime"] += int(value * csconst.TIME_ENLARGE_MULTIPLE)
						
						#添加后剩余时间大于持续时间，则重新赋值持续时间
						remainTime = float( Functions.convertTime( dDict["endTime"] - currTime ) )
						if remainTime > dDict["persistTime"]:
							dDict["persistTime"] = remainTime
				if not hasCD:
					newDict = { "id":id, "endTime":Functions.getTime(value), "persistTime":float(value) }
					self.attrCooldowns.append( newDict )
			#减CD
			else:
				for dDict in self.attrCooldowns:
					if dDict["id"] == id:
						dDict["endTime"] = max( currTime, ( dDict["endTime"] - int(abs(value)*csconst.TIME_ENLARGE_MULTIPLE) ) )	#剩余时间最多减少到0

	def getCooldown( self ):
		"""
		获取冷却时间
		"""
		if not self.attrCooldowns:
			self.attrCooldowns = []
		
		return self.attrCooldowns

	def clearCooldown( self, isClear = False ):
		"""
		清除CD
		"""
		if isClear:
			self.client.ClearCooldown( isClear )

#------------转向------------------------------------------------------------
	def turnToSkillTarget( self, target):
		"""
		旋转方向
		@param target: 施展对象
		@type  target: 一个包装过的对象entity 被包装对象可能是 (位置，entity, item)详细请看SkillTargetObjImpl.py
		"""
		# 转向处理, 需要精确的方向
		position = target.getObjectPosition()
		if self.position.flatDistTo(position) > 0.1:
			self.turnToPos(position)

	def turnToPos( self, position ):
		"""
		转向一个坐标
		"""
		if self.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
			yaw = csarithmetic.getYawByVector3(position-self.position)
			direction = (0.0, 0.0, yaw)
			self.changeDirection(direction, csdefine.REASON_CHANGE_DIR_FORCE)
		else:					# 玩家的转向需要配合客户端的施法辅助
			if self.client:
				self.client.SkillTurnToPos(KBEMath.KBEngine2UnrealPosition(position))

#-------------------------------------------------------------------------------
	def beforeUseSkill( self, skill, target ):
		"""
		在使用技能之前要做的事情
		"""
		pass

	def getSkill( self, skillID ):
		"""
		"""
		if not ( self.__temp_skill_object and self.__temp_skill_object.getID() == skillID ):
			self.__temp_skill_object = SkillLoader.g_skills[ skillID ]
		
		return self.__temp_skill_object

	def isCastingSkill( self ):
		"""
		是否正在释放引导技能
		"""
		return self.castingSkillID

	def interruptSkill( self, reason ):
		"""
		define method.
		中断法术的施放，并通知client。

		@param reason: 中断的原因
		"""
		if not self.isCastingSkill():
			return
		receiver = KBEngine.entities.get( self.receiverID, None )
		if receiver and receiver.getEntityFlag() == csdefine.ENTITY_FLAG_SPELL:
			receiver.notify_OtherClientCanInteractive(self.id)
		self.getSkill( self.castingSkillID ).interrupt( self, reason)

	def interruptInstantSkill( self,skillID, reason ):
		"""
		中断瞬发技能
		"""
		self.getSkill( skillID ).interrupt( self, reason )

	def onSkillInterrupted( self, skillID, reason ):
		"""
		virtual method
		当施法被打断时的通知
		"""
		KBEDebug.DEBUG_MSG( "skill %i interrupted. reason: %s" % (skillID, reason) )
		# 通知all client，结束当前的施法动作

	def triggerEventSkillBegin( self, skillInstance ):
		"""
		触发施法者“施展开始时”事件
		"""
		if self.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE and skillInstance.getActForbid() == csdefine.ACTION_FORBID_SPELL:
			self.applyEnterWarn(csdefine.ROLE_WARN_REASON_SKILL)
		if not skillInstance.isPassiveSkill():
			self.triggerSkillEvent( csdefine.SKILL_EVENT_PROCESS, self.id, { "actForbid": skillInstance.getActForbid(), "type":csdefine.SKILL_EVENT_SKILL_BEGIN, "skillID":skillInstance.getID() } )

	def triggerEventSkillEnd( self, skillInstance ):
		"""
		触发施法者“施展结束时”事件
		"""
		if not skillInstance.isPassiveSkill():
			self.triggerSkillEvent( csdefine.SKILL_EVENT_PROCESS, self.id, { "actForbid": skillInstance.getActForbid(), "type":csdefine.SKILL_EVENT_SKILL_END, "skillID":skillInstance.getID() } )

	def triggerEventSkillInterrupt( self, skillInstance ):
		"""
		触发施法者“施展中断时”事件
		"""
		if not skillInstance.isPassiveSkill():
			self.triggerSkillEvent( csdefine.SKILL_EVENT_PROCESS, self.id, { "actForbid": skillInstance.getActForbid(), "type":csdefine.SKILL_EVENT_SKILL_INTERRUPT, "skillID":skillInstance.getID() } )

	def triggerEventBuffAdd( self, buff ):
		"""
		触发施法者“Buff注册时”事件
		"""
		self.triggerSkillEvent( csdefine.BUFF_EVENT_PROCESS, self.id, { "actForbid": buff.getActForbid(), "type":csdefine.BUFF_EVENT_BUFF_ADD, "buffID":buff.getID() } )

	def triggerEventBuffRemove( self, buff ):
		"""
		触发施法者“Buff注销时事件”
		"""
		self.triggerSkillEvent( csdefine.BUFF_EVENT_PROCESS, self.id, { "actForbid": buff.getActForbid(), "type":csdefine.BUFF_EVENT_BUFF_REMOVE, "buffID":buff.getID() } )

	def triggerEventBuffBegin( self, buff ):
		"""
		触发施法者“Buff开始时”事件
		"""
		self.triggerSkillEvent( csdefine.BUFF_EVENT_PROCESS, self.id, { "actForbid": buff.getActForbid(), "type":csdefine.BUFF_EVENT_BUFF_BEGIN, "buffID":buff.getID() } )

	def triggerEventBuffInterrupt( self, buff ):
		"""
		触发施法者“Buff中断时”事件
		"""
		self.triggerSkillEvent( csdefine.BUFF_EVENT_PROCESS, self.id, { "actForbid": buff.getActForbid(), "type":csdefine.BUFF_EVENT_BUFF_INTERRUPT, "buffID":buff.getID() } )

	def triggerEventBuffEnd( self, buff ):
		"""
		触发施法者“Buff结束时”事件
		"""
		self.triggerSkillEvent( csdefine.BUFF_EVENT_PROCESS, self.id, { "actForbid": buff.getActForbid(), "type":csdefine.BUFF_EVENT_BUFF_END, "buffID":buff.getID() } )

	def onSkillBegin( self, skillInstance, target ):
		"""
		virtual method.
		技能开始

		@param  skillInstance: 技能实例
		@type   skillInstance: Skill
		"""
		self.skillHitTimerDelay = 0.0
		if not skillInstance.isInstantSkill():
			self.castingSkillID = skillInstance.getID()
			self.allClients.SetCastingSkill( self.castingSkillID, )
			self.checkSkillCastErrorTimer = self.addTimerCallBack( skillInstance.getSkillTotalTime() + 0.2, "checkSkillCastError", ( skillInstance.getID(), ) )

	def setReceiverID( self, id ):
		"""设置受术目标ID"""
		self.receiverID = id

	def onSkillEnd( self, skillInstance, castResult ):
		"""
		virtual method.
		技能结束

		@param  skillInstance: 技能实例
		@type   skillInstance: SPELL
		"""
		if castResult:
			self.triggerEventSkillEnd(skillInstance)
		self.skillHitTimerDelay = 0.0
		self.checkSkillError( skillInstance )
		self.casterSkillEnd( skillInstance)
		self.usingItemEnd(skillInstance, castResult )
		self.delSkillHitTimer(skillInstance.getID())
		# 如果是神通技能，则消耗神通技能使用次数
		if self.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
			self.onUseShenTongSkill(skillInstance.getID())
		if self.getEntityFlag() == csdefine.ENTITY_FLAG_VEHICLEPET and self.getOwnerEntity():
			self.getOwnerEntity().onUsePetShenTongSkill(skillInstance.getID())

		# 技能结束3秒后退出警戒状态
		if self.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE and skillInstance.getActForbid() == csdefine.ACTION_FORBID_SPELL:
			self.applyEnterWarn(csdefine.ROLE_WARN_REASON_SKILL, 3)

	def checkSkillError( self, skillInstance ):
		if not skillInstance.isInstantSkill():
			self.castingSkillID = 0
			self.allClients.SetCastingSkill( 0, )
			if self.checkSkillCastErrorTimer != 0:
				self.popTimer( self.checkSkillCastErrorTimer )
				self.checkSkillCastErrorTimer = 0

	def casterSkillEnd(self, skillInstance):
		if self.receiverID:
			receiver = KBEngine.entities.get( self.receiverID )
			self.receiverID = 0
			if receiver:
				receiver.onCasterSkillEnd( self.id, skillInstance.getID() )

	def usingItemEnd( self, skillInstance, castResult ):
		usingItemUid = self.getUsingItem()
		if usingItemUid:
			self.setUsingItem( 0 )
			item = self.getItemInstByUid( usingItemUid )
			if item != None:
				self.onUseItemResult( item, castResult )
			else:
				KBEDebug.CRITICAL_MSG( "Player(%s) cannot find the item form uid[%s]." %(self.playerName, usingItemUid ) )

	def onCasterSkillEnd( self, casterID, skillID ):
		"""
		Define Method
		施法者 技能结束
		"""
		self.unRegisterReceiverSkillEvent( casterID, skillID )

	def checkSkillCastError( self, lastCastingSkillID ):
		if self.castingSkillID == lastCastingSkillID:		# 上次施放的技能出错，未能成功结束调用 onSkillEnd
			self.interruptSkill( csstatus.SKILL_CAST_FAILED )

#--------------技能打击相关--------------------------------------------
	def addSkillHitTimer( self, delayTime, skillID, target, hitTime ):
		if delayTime <= Const.SKILL_MIN_HIT_TIME:
			self.onSkillHitTimer( skillID, target, hitTime )
		else:
			timerID = self.addTimerCallBack( delayTime, "onSkillHitTimer", ( skillID, target, hitTime ) )
			timerList = self.skillHitTimerList.get(skillID, [])
			timerList.append(timerID)
			self.skillHitTimerList[skillID] = timerList

	def delSkillHitTimer( self, skillID ):
		"""
		删除技能打击timer(目前先用技能ID为Key)
		"""
		timerList = self.skillHitTimerList.get(skillID, [])
		while( len( timerList ) != 0 ):
			timerID = timerList.pop(0)
			if self.hasTimer( timerID ):
				self.popTimer( timerID )

	def onSkillHitTimer( self, skillID, target, hitTime ):
		"""
		技能打击timer回调
		"""
		if self.skillHitTimerDelay > 0:
			self.addTimerCallBack( self.skillHitTimerDelay, "onSkillHitTimerDelay", ( skillID, target, hitTime ) )
		else:
			self.getSkill( skillID ).onSkillHit( self, target, hitTime )

	def startSkillHitSlow( self, actionSpeed, actionTime, hitTimerDelay ):
		"""
		开始打击迟缓
		"""
		self.skillHitTimerDelay += hitTimerDelay
		self.allClients.StartSkillHitSlow( actionSpeed, actionTime, hitTimerDelay )

	def stopSkillHitSlow( self ):
		self.allClients.StopSkillHitSlow()

	def onSkillHitTimerDelay( self, skillID, target, hitTime ):
		"""
		技能打击timer延迟回调
		"""
		self.getSkill( skillID ).onSkillHit( self, target, hitTime )

	def onTimerDelayArrive( self, skillID, target, hitTime, index ):
		"""
		"""
		skill = self.getSkill( skillID )
		if skill is None:
			KBEDebug.CRITICAL_MSG( "%i: skill %i not exist." % ( self.id, skillID ) )
			return csstatus.SKILL_NOT_EXIST
		skill.onArrive( self, target, hitTime, index )

	def receiveSkillHit( self, casterID, skillID, hitTime, index ):
		"""
		<Define Method>
		接受技能打击效果
		"""
		skill = self.getSkill( skillID )
		if skill is None:
			KBEDebug.CRITICAL_MSG( "%i: skill %i not exist." % ( self.id, skillID ) )
			return csstatus.SKILL_NOT_EXIST
		caster = KBEngine.entities.get( casterID, None )
		skill.getHit( hitTime, index ).receive( skill, caster, self )

#---------buff相关------------------------------------------------------
	def getBuff( self, buffID ):
		return BuffLoader.g_buffs[ buffID ]
	
	def getBuffData( self, index ):
		if index in self.attrBuffs:
			return self.attrBuffs[ index ]
		return None
		
	def getBuffDatasByID( self, buffID ):
		data = []
		for buffData in self.attrBuffs.values():
			if buffData.buffID == buffID:
				data.append( buffData )
		return data
	
	def setAttrBuffsForClient( self, clientBuffs):
		self.attrBuffsForClient = clientBuffs
	
	def receiveBuffHit( self, casterID, buffID, attrName, index ):
		"""
		<Define Method>
		接受技能打击效果
		"""
		buff = self.getBuff( buffID )
		caster = KBEngine.entities.get( casterID, None )
		buff.getHit( attrName, index ).receive( buff, caster, self )

	def addBuff( self, caster, buffID ):
		if len(self.attrBuffs) > csconst.BUFF_AMOUNT_MAX:
			KBEDebug.ERROR_MSG("EntityID : %s has Buffs amount: %s addBuffID : %s !!!Are you sure we need this many Buffs here? Please confirm your config."%(self.id, len(self.attrBuffs), buffID))

		buff = self.getBuff( buffID )
		if not buff:
			KBEDebug.ERROR_MSG("buffID = %s is not in config:"%buffID)
			return False
		if caster.spaceID != self.spaceID:
			return False
		return buff.receive( caster, self )
		
	def onAddBuff( self, buffData ):
		"""
		添加一个Buff。
		"""
		# 处理其它功能模块支持
		if self.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
			self.client.RefreshAroundBoxStatus(csdefine.SPELL_BOX_LISTEN_EVENT_HAS_BUFF)
			self.spaceStrategy_onAddBuff(buffData.buffID)
		elif self.getEntityFlag() == csdefine.ENTITY_FLAG_SPELL:
			self.allClients.CLIENT_RefreshBoxStatus()

		buff = self.getBuff( buffData.buffID )
		buffData.index = self.newBuffIndex()
		self.attrBuffs[ buffData.index ] = buffData
		self.attrBuffs.upClientData( self )
		self.triggerEventBuffAdd(buff)
		buff.doBegin( self, buffData )

		if buffData.holdTime != 0:
			self.buffHoldTimerRefresh() #开始计划
		else:
			if buffData.index in self.attrBuffs:
				self.removeBuff( buffData.index, csdefine.BUFF_END_RESON_BY_TIME_OVER )

	def findBuffsByBuffID( self, buffID ):
		"""
		查找指定类型的所有buff索引。 通过BUFFID寻找
		@return: 找到则返回相应的索引列表，找不到则返回[]
		"""
		buffs = []
		for index, buff in self.getAttrBuffs().items() :
			if buff.buffID == buffID:
				buffs.append( index )

		return buffs

	def findBuffsByBuffScript( self, buffScript ):
		"""
		查找指定脚本的buff
		@return: 找到则返回相应的索引列表，找不到则返回[]
		"""
		buffs = []
		for index, buff in self.getAttrBuffs().items() :
			if buff.className == buffScript:
				buffs.append( index )
		
		return buffs

	def findLastBuffByBuffID( self, buffID ):
		"""
		获取最近加的某ID的buff索引
		"""
		findIndex = -1
		for index, buff in self.getAttrBuffs().items():
			if buff.buffID == buffID and index > findIndex:
				findIndex = index
		return findIndex

	def findLastBuffByBuffScript( self, buffScript ):
		"""
		获取最近加的某脚本的buff索引
		"""
		findIndex = -1
		for index, buff in self.getAttrBuffs().items():
			buffIns = self.getBuff( buff.buffID )
			if buffIns.__class__.__name__ == buffScript and index > findIndex:
				findIndex = index
		return findIndex

	def newBuffIndex( self ):
		"""
		产生一个新的buffindex
		"""
		# 将范围定在0~1000000
		if self.lastBuffIndex > 1000000:
			self.lastBuffIndex = 0
		index = self.lastBuffIndex
		self.lastBuffIndex += 1
		return index

	def removeAllBuff( self ):
		"""
		移除所有的buff
		"""
		for buffIndex in list(self.attrBuffs):
			buffData = self.getBuffData( buffIndex )
			self.stopBuff( buffData )

		self.buffHoldTimerRefresh()
		self.onRemoveAllBuff()

	def removeBuff( self, buffIndex , reason = csdefine.BUFF_END_RESON_BY_INTERRUPT ):
		"""
		移除一个buff
		"""
		buffData = self.getBuffData( buffIndex )
		if not buffData:
			self.buffHoldTimerRefresh()
			return False
		
		self.stopBuff( buffData, reason )

		self.buffHoldTimerRefresh()
		self.onRemoveBuff(buffData)
		return True

	def onRemoveBuff(self, buffData ):
		if self.isDestroyed:
			return

		self.attrBuffs.upClientData( self )
		if self.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE and self.client:
			self.client.RefreshAroundBoxStatus(csdefine.SPELL_BOX_LISTEN_EVENT_HAS_BUFF)
		elif self.getEntityFlag() == csdefine.ENTITY_FLAG_SPELL:
			self.allClients.CLIENT_RefreshBoxStatus()
		#由于怪物和玩家 用的都是这个接口 怪物没有通知其它客户端的需求
		if self.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
			self.notifyClientRemoveBuff(buffData)

	def onRemoveAllBuff(self):
		if self.isDestroyed:
			return

		self.attrBuffs.upClientData( self )
		if self.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE and self.client:
			self.client.RefreshAroundBoxStatus(csdefine.SPELL_BOX_LISTEN_EVENT_HAS_BUFF)
		elif self.getEntityFlag() == csdefine.ENTITY_FLAG_SPELL:
			self.allClients.CLIENT_RefreshBoxStatus()

	
	def timeOverEndBuff( self, buffIndex ):
		"""buff时间结束"""
		self.removeBuffByIndex( buffIndex, csdefine.BUFF_END_RESON_BY_TIME_OVER )
	
	def removeBuffByID( self, buffID, reason = csdefine.BUFF_END_RESON_BY_INTERRUPT ):
		"""
		通过id移除buff
		"""
		isSucceed = True
		buffList = list(self.attrBuffs.getBuffByBuffID(buffID))
		if not buffList:
			isSucceed = False
		for buffData in buffList:
			if buffData.buffID == buffID:
				if not self.removeBuff( buffData.index, reason ):
					isSucceed = False
		self.attrBuffs.delBuffByBuffID(buffID)
		return isSucceed
		
	def removeBuffByIndex( self, buffIndex, reason = csdefine.BUFF_END_RESON_BY_INTERRUPT ):
		"""
		通过index移除buff
		"""
		isSucceed = False
		if buffIndex in self.attrBuffs:
			if self.removeBuff( buffIndex, reason ):
				isSucceed = True
		return isSucceed

	def removeBuffByEffect( self, holdEffectName ):
		"""
		通过持有效果移除buff
		"""
		for index in list(self.attrBuffs):
			buff = self.getBuff( self.getBuffData(index).buffID )
			if buff.holdEffect( holdEffectName ):
				self.removeBuff( index )
	
	def reloadBuff( self, buffIndex, buffRemainTime ):
		"""
		上线重新加载buff
		"""
		buffData = self.getBuffData( buffIndex )
		buff = self.getBuff( buffData.buffID )
		buff.doReload( self, buffData )
		self.buffHoldTimerRefresh() #开始计划
	
	def stopBuff( self, buffData, reason = csdefine.BUFF_END_RESON_BY_INTERRUPT ):
		"""
		停止buff效果，并不删除
		"""
		buff = self.getBuff( buffData.buffID )
		if buff:
			buff.doEnd( self, buffData,reason )
		if buffData.timerID != 0:
			self.popTimer( buffData.timerID )
			buffData.timerID = 0

	def clearBuff(self, buffData, reason):
		"""
		清除buff数据
		"""
		if reason != csdefine.BUFF_END_RESON_BY_OFFLINE:
			self.attrBuffs.pop(buffData.index)
		if buffData.index in self.removeBuffList:
			self.removeBuffList.remove(buffData.index)

	def onBuffLoop( self, buffIndex ):
		"""
		效果每次作用
		"""
		buffData = self.getBuffData( buffIndex )
		buff = self.getBuff( buffData.buffID )
		buff.doLoop( self, buffData )

	def getAttrBuffs( self ):
		return self.attrBuffs

	def roleCalculateBuffsOnDestroy( self ):
		"""
		玩家销毁时计算buff数据，针对下线是否保存及继续计时的处理
		"""
		removeList = []
		for idx, buffData in self.attrBuffs.items() :
			
			buff = self.getBuff( buffData.buffID )
			if not buff:
				removeList.append( idx )
				KBEDebug.CRITICAL_MSG( "Buff(index:%s, buffID:%s) is None,Player(%s)." %( buffData.index, buffData.buffID, self.playerName ) )
				continue
			if buff.getSaveType() == csdefine.BUFF_OFFLINE_SAVE_TYPE_NULL:				#下线不保存
				removeList.append( idx )
			elif buffData.holdTime < 0:													#永久buff
				buffData.endTime = 0
			elif buff.getSaveType() == csdefine.BUFF_OFFLINE_SAVE_TYPE_NOT_CONTINUE:	#下线保存，不继续计时
				buffData.endTime = buffData.endTime - Functions.getTime()
				if buffData.endTime <= 1:
					removeList.append( idx )
			elif buff.getSaveType() == csdefine.BUFF_OFFLINE_SAVE_TYPE_AGAIN:			#下线保存，重新计时
				buffData.endTime = buffData.holdTime
			self.stopBuff( buffData, csdefine.BUFF_END_RESON_BY_OFFLINE )
		for idx in removeList :
			self.attrBuffs.pop( idx )	
		self.attrBuffs.upClientData( self )
		self.cacheBuff = []	
		
	def roleCalculateBuffsOnInit( self ):
		"""
		玩家初始化时重新计算buff数据，针对下线是否保存及继续计时的处理
		"""
		removeList = []
		for idx, buffData in self.attrBuffs.items() :
			buff = self.getBuff( buffData.buffID )
			if not buff:
				removeList.append( idx )
				KBEDebug.CRITICAL_MSG( "Buff(index:%s, buffID:%s) is None,Player(%s)." %( buffData.index, buffData.buffID, self.playerName ) )
				continue
			if buff.getSaveType() == csdefine.BUFF_OFFLINE_SAVE_TYPE_NULL:				#下线不保存
				removeList.append( idx )
			elif buffData.holdTime < 0:													#永久buff
				buff.endTime = 0
			elif buff.getSaveType() == csdefine.BUFF_OFFLINE_SAVE_TYPE_NOT_CONTINUE:	#下线保存，不继续计时
				buffData.endTime = buffData.endTime + Functions.getTime()
			elif buff.getSaveType() == csdefine.BUFF_OFFLINE_SAVE_TYPE_AGAIN:			#下线保存，重新计时
				buffData.endTime = buff.calculateEndTime( buffData.holdTime )
			elif buff.getSaveType() == csdefine.BUFF_OFFLINE_SAVE_TYPE_CONTINUE:		#下线保存，继续计时
				if buff.isTimeout( buffData ):
					removeList.append( idx )
		
		for idx in removeList :
			self.attrBuffs.pop( idx )
		
		# 重新设置index
		buffDataList = list( self.getAttrBuffs().values() )
		self.attrBuffs.clear()
		buffIndex = 0
		for buffData in buffDataList:
			buff = self.getBuff( buffData.buffID )
			if buff.isTimeout( buffData ):
				continue
			buffData.index = buffIndex
			buffRemainTime = buff.getBuffRemainTime( buffData )
			self.attrBuffs[ buffIndex ] = buffData
			self.reloadBuff( buffIndex, float( buffRemainTime ) )
			buffIndex += 1
		self.lastBuffIndex = buffIndex
		self.attrBuffs.upClientData( self )
		self.buffHoldTimerRefresh()

	# buff tick	
	def addBuffHoldTick( self ):	
		if self.buffHoldTickTimerID:
			self.popTimer( self.buffHoldTickTimerID )
			self.buffHoldTickTimerID = 0

		nextTime = round( Functions.convertTime( self.nextBuffEndTickValue - Functions.getTime() ), 1 )
		if nextTime >= 0.1:
			self.buffHoldTickTimerID= self.addTimerCallBack( nextTime,  "onBuffHoldTick", () )
		else:
			self.onBuffHoldTick()
	
	def onBuffHoldTick( self ):
		"""
		结束定时器回调
		"""
		self.buffHoldTickTimerID = 0
		tempList = list( self.cacheBuff )
		for buffData in tempList:
			if buffData.endTime == 0:
				continue
			if buffData.index not in self.attrBuffs:
				continue
			if buffData.index in self.removeBuffList:
				continue

			buff = self.getBuff(buffData.buffID)
			if buff and buff.isTimeout(buffData):
				self.removeBuffList.append(buffData.index)
				self.timeOverEndBuff( buffData.index )
			else:
				break

		#防止定时器被刷新很快的时候，回调时间不对的问题,如果BUFF列表不为空，而已定时器已经停止时，直接再进行一次刷新（CST-6029）
		if len(self.attrBuffs) and self.buffHoldTickTimerID == 0:
			self.buffHoldTimerRefresh()

	def buffHoldTimerRefresh( self ):
		"""
		刷新buff结束定时器
		"""

		if len( self.attrBuffs ) == 0:
			self.cacheBuff = []
			self.nextBuffEndTickValue = 0
			return
		
		buffList = list(filter(lambda buffData:self.getBuff(buffData.buffID) and buffData.endTime > 0 and buffData.index not in self.removeBuffList, self.attrBuffs.values()))
		sortList = sorted(buffList, key = lambda buffData: buffData.endTime, reverse=False )
		self.cacheBuff = list(sortList)
		if len( sortList ):
			self.nextBuffEndTickValue = sortList[0].endTime
		else:
			self.nextBuffEndTickValue = 0
		if self.nextBuffEndTickValue != 0:
			self.addBuffHoldTick()

	def skill_onClientActorCreate( self, srcEntityID ):
		"""
		Exposed method
		自己在某客户端被创建出来
		"""
		#buff处理
		if not self.validatePlayerClientCall( srcEntityID ):
			return
		for index, buffData in self.attrBuffs.items():
			buff = self.getBuff( buffData.buffID )
			if buff:
				buff.onClientActorCreate( self, buffData, srcEntityID )
		
		#技能处理
		if self.isCastingSkill():
			skill = self.getSkill( self.castingSkillID )
			skill.onClientActorCreate( self, srcEntityID )
		
		#持有效果处理
		for effectData in self.holdEffectData:
			if effectData.sourceType == csdefine.HOLD_EFFECT_SOURCE_TYPE_FIX_ID:	#这里只重新加载通过固定ID添加的持有效果，因为buff和skill添加的会在buff脚本和skill脚本中处理
				effect = EffectLoader.g_effects.getHoldEffect( effectData.sourceID )
				effect.onClientActorCreate( effectData, self, srcEntityID )

#-------------buff叠加相关------------------------------------------
	def stackBuff( self, buffIndex ):
		"""
		<define method>
		叠加buff
		"""
		for buffData in list(self.attrBuffs.values()):
			if buffData.index != buffIndex:
				continue
			buff = self.getBuff( buffData.buffID )
			buff.doStack( self, buffData )

	def resetBuffEndTime( self, buffIndex ):
		"""
		<define method>
		重置持续时间
		"""
		for buffData in list(self.attrBuffs.values()):
			if buffData.index != buffIndex:
				continue
			buff = self.getBuff( buffData.buffID )
			buffData.endTime = buff.calculateEndTime( buffData.holdTime )
			self.onResetBuffEndTime( buffData.index, buffData.holdTime )
			self.buffHoldTimerRefresh()
	
	def onResetBuffEndTime( self, buffIndex, buffTime ):
		"""
		重置buff持续时间回调
		"""
		self.allClients.OnResetBuffEndTime( buffIndex, buffTime )

#-----------持续效果相关-----------------------------------------
	def getNewHoldEffectIndex( self ):
		"""
		获取一个新的固定ID的持有效果的index
		"""
		self.lastHoldEffectIndex += 1
		return self.lastHoldEffectIndex
	
	def addHoldEffectData( self, newEffectData ):
		"""
		添加持续效果数据
		"""
		self.holdEffectData.append( newEffectData )

	def removeHoldEffectData( self, index ):
		"""
		移除持有效果数据
		"""
		for effectData in self.holdEffectData:
			if effectData.index == index:
				self.holdEffectData.remove( effectData )
				break

#-------------通过效果ID加持有效果----------------------------
	def addFixIDHoldEffect( self, effectID, caster ):
		"""
		添加固定ID的持有效果
		"""
		if caster.spaceID != self.spaceID:
			return -1
		
		effect = EffectLoader.g_effects.getHoldEffect( effectID )
		if effect and effect.canEffect( caster, self ):
			
			effectData = effect.getNewEffectData( caster, self )
			effectData.index = self.getNewHoldEffectIndex()
			effectData.sourceType = csdefine.HOLD_EFFECT_SOURCE_TYPE_FIX_ID
			effectData.sourceID = effectID
			effectData.casterID = caster.id
			
			self.addHoldEffectData( effectData )
			effect.onBegin( effectData, self )
			return effectData.index
		return -1
	
	def removeFixIDHoldEffect( self, index ):
		"""
		移除某固定ID的持有效果
		"""
		for effectData in list( self.holdEffectData ):
			if effectData.index == index:
				effect = EffectLoader.g_effects.getHoldEffect( effectData.sourceID )
				effect.onEnd( effectData, self )
				self.removeHoldEffectData( index )
				break

	def removeFixIDHoldEffectByID( self, effectID):
		"""
		通过效果ID移除固定持有效果
		"""
		for effectData in list( self.holdEffectData ):
			if effectData.sourceID == effectID:
				effect = EffectLoader.g_effects.getHoldEffect( effectData.sourceID )
				effect.onEnd( effectData, self )
				self.removeHoldEffectData( effectData.index )
				
	def removeAllFixIDHoldEffect(self):
		"""
		"""
		while len(self.holdEffectData):
			effectData = self.holdEffectData.pop()
			effect = EffectLoader.g_effects.getHoldEffect( effectData.sourceID )
			effect.onEnd( effectData, self )
	
#-------------通过效果ID加技能效果----------------------------------
	def addFixIDEffect( self, caster, effectID, skill= None ):
		"""
		添加固定ID的技能效果
		"""
		effect = EffectLoader.g_effects.getEffect(effectID)
		if effect:
			if effect.canEffect( skill, caster, self ):
				effect.onReceive( skill, caster, self )
				return True
		return False

#-----------技能事件------------------------------------------------
	def registerSkillEvent( self, eventType, id ):
		"""
		施法者技能事件注册
		"""
		if not eventType in self.casterSkillEventList:
			self.casterSkillEventList[eventType] = []
		self.casterSkillEventList[eventType].append(id)
		
	def unRegisterSkillEvent( self, eventType, id ):
		if eventType in self.casterSkillEventList and id in self.casterSkillEventList[eventType]:
			self.casterSkillEventList[eventType].remove(id)

	def registerReceiverSkillEvent( self, eventType, entityID, skillID ):
		"""
		受术目标注册(仅支持技能目标类型为entity)
		"""
		if not eventType in self.receiverSkillEventList:
			self.receiverSkillEventList[eventType] = []
		self.receiverSkillEventList[eventType].append( (entityID,skillID) )
		
	def unRegisterReceiverSkillEvent( self, entityID, skillID  ):
		for eventType, events in self.receiverSkillEventList.items():
			for event in events:
				if event == (entityID, skillID ):
					self.receiverSkillEventList[eventType].remove( (entityID,skillID) )
			
	def registerCasterBuffEvent( self, eventType, entityID, id ):
		"""
		施法者buff事件注册
		"""
		if not eventType in self.casterbuffEventList:
			self.casterbuffEventList[eventType] = []
		self.casterbuffEventList[eventType].append( (entityID,id) )
		
	def unRegisterCasterBuffEvent( self, eventType, entityID, id ):
		for eventType, events in self.casterbuffEventList.items():
			for event in events:
				if event == (entityID, id ):
					self.casterbuffEventList[eventType].remove( (entityID, id) )

	def registerBuffEvent( self, eventType, id ):
		"""
		受术者buff事件注册
		"""
		if not eventType in self.receiverbuffEventList:
			self.receiverbuffEventList[eventType] = []
		self.receiverbuffEventList[eventType].append(id)
		
	def unRegisterBuffEvent( self, eventType, id ):
		if eventType in self.receiverbuffEventList and id in self.receiverbuffEventList[eventType]:
			self.receiverbuffEventList[eventType].remove(id)
			
	def triggerSkillEvent( self, eventType, triggerID, pDict ):
		"""
		<Define Method>
		触发技能事件
		"""
		self._triggerCasterSkillEventList( eventType, triggerID, pDict )
		self._triggerReceiverBuffEventList( eventType, triggerID, pDict )
		self._triggerReceiverSkillEventList( eventType, triggerID, pDict )
		self._triggerCasterBuffEventList( eventType, triggerID, pDict )
		
	def _triggerCasterSkillEventList( self, eventType, triggerID, pDict ):
		"""触发施法者事件"""
		if eventType in self.casterSkillEventList:
			for id in list(self.casterSkillEventList[eventType]):
				skill = self.getSkill( id )
				skill.triggerSkillEvent( self, eventType, triggerID, pDict )
				
	def _triggerReceiverSkillEventList( self, eventType, triggerID, pDict ):
		"""触发受术者事件"""
		if eventType in self.receiverSkillEventList:
			for casterID, skillID in list(self.receiverSkillEventList[eventType]):
				caster = KBEngine.entities.get( casterID, None )
				skill = self.getSkill( skillID )
				if caster and skill:
					skill.triggerReceiverSkillEvent( caster, self, eventType, triggerID, pDict )

	def _triggerReceiverBuffEventList( self, eventType, triggerID, pDict ):
		"""触发受术者buff事件"""
		if eventType in self.receiverbuffEventList:
			for id in list(self.receiverbuffEventList[eventType]):
				buffData = self.getBuffData( id )
				if buffData:
					buff = self.getBuff(buffData.buffID)
					buff.triggerBuffEvent( self, eventType, triggerID, buffData, pDict )

	def _triggerCasterBuffEventList( self, eventType, triggerID, pDict ):
		"""触发施法者buff事件"""
		if eventType in self.casterbuffEventList:
			for receiverID, id in list(self.casterbuffEventList[eventType]):
				receiver = KBEngine.entities.get( receiverID, None )
				if receiver:
					receiver.triggerCasterBuffEvent( eventType, id, triggerID, pDict )

	def triggerCasterBuffEvent( self, eventType, buffIndex, triggerID, pDict ):
		"""
		<Define Method>
		触发施法者buff事件
		"""
		buffData = self.getBuffData( buffIndex )
		if buffData:
			buff = self.getBuff(buffData.buffID)
			buff.triggerCasterBuffEvent( self, eventType, triggerID, buffData, pDict )


	def OnPlayerMoveChange( self, srcEntityID, MoveType, MoveState ):
		"""
		<Exposed Method>
		移动触发技能事件
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		self.triggerSkillEvent( csdefine.SKILL_EVENT_ROLE_MOVE_CHANGE, self.id, {"MoveType":int(MoveType), "MoveState":int(MoveState)} )

	def OnChangeRoleJumpState(self, oldState, newState):
		"""
		"""
		self.triggerSkillEvent(csdefine.SKILL_EVENT_ROLE_JUMP_STATE_CHANGE, self.id, {"oldState":oldState, "newState":newState})

	def onBulletCollisionBegin( self, srcEntityID, buffOwnerID, buffIndex, targetID, effectID, effectIndex, effectCustomIndex ):
		"""
		<Exposed Method>
		子弹Buff碰撞开始时触发技能事件
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		buffOwner = KBEngine.entities.get( int(buffOwnerID), None )
		if buffOwner:
			buffOwner.triggerSkillEvent( csdefine.SKILL_EVENT_BULLET_COLLISION, buffOwner.id, {"bulletTargetID":int(targetID), "buffIndex":int(buffIndex),
				"effectID": effectID, "effectIndex": effectIndex,"type":"Begin","effectCustomIndex":int(effectCustomIndex)})

	def onBulletCollisionPosBegin( self, srcEntityID, buffOwnerID, buffIndex, Pos, effectID, effectIndex, effectCustomIndex ):
		"""
		<Exposed Method>
		子弹Buff碰撞障碍物时触发技能事件
		"""	
		if not self.validateClientCall( srcEntityID ):
			return
		buffOwner = KBEngine.entities.get( int(buffOwnerID), None )	
		if buffOwner:
			buffOwner.triggerSkillEvent( csdefine.SKILL_EVENT_BULLET_COLLISION, buffOwner.id, {"BlockPos":Pos, "buffIndex":int(buffIndex),
				"effectID": effectID, "effectIndex": effectIndex,"type":"Block","effectCustomIndex":int(effectCustomIndex)})


	def onBulletCollisionArrive( self, srcEntityID, buffOwnerID, buffIndex, targetID, effectID, effectIndex,effectCustomIndex ):
		"""
		<Exposed Method>
		子弹Buff碰撞抵达时触发技能事件
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		buffOwner = KBEngine.entities.get( int(buffOwnerID), None )
		if buffOwner:
			buffOwner.triggerSkillEvent( csdefine.SKILL_EVENT_BULLET_COLLISION, buffOwner.id, {"bulletTargetID":int(targetID), "buffIndex":int(buffIndex),
				"effectID": effectID, "effectIndex": effectIndex,"type":"Arrive","effectCustomIndex":int(effectCustomIndex)})

	def addPerSecondEvent(self):
		"""
		添加每秒触发时间
		"""
		if csdefine.SKILL_EVENT_PER_SECOND_TRIGGER in self.casterSkillEventList or csdefine.SKILL_EVENT_PER_SECOND_TRIGGER in self.receiverSkillEventList:
			if not self.perSecondEventTimer:
				self.perSecondEventTimer = self.addTimerRepeat( 1.0, "triggerSkillEvent", (csdefine.SKILL_EVENT_PER_SECOND_TRIGGER, self.id, {}, ) )

	def removePerSecondEvent(self):
		"""
		移除每秒触发时间
		"""
		if not csdefine.SKILL_EVENT_PER_SECOND_TRIGGER in self.casterSkillEventList and not csdefine.SKILL_EVENT_PER_SECOND_TRIGGER in self.receiverSkillEventList:
			if self.perSecondEventTimer:
				self.popTimer( self.perSecondEventTimer )
				self.perSecondEventTimer = 0

	def onInitiaiveStopBuffEvent( self, srcEntityID, buffIndex ):
		"""
		<Exposed Method>
		"玩家主动停止技能/Buff"事件
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		self.triggerSkillEvent( csdefine.SKILL_EVENT_INITIATIVE_STOP_BUFF, self.id, {"eventBuffIndex":int(buffIndex)} )

	def onInitiaiveStopSkillEvent( self, srcEntityID ):
		"""
		<Exposed Method>
		"玩家主动停止技能/Buff"事件
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		self.triggerSkillEvent( csdefine.SKILL_EVENT_INITIATIVE_STOP_SKIL, self.id, {} )

	def onBuffGuestEndEvent( self, guestBuffIndex ):
		"""
		主从buff，从buff结束事件
		"""
		self.triggerSkillEvent( csdefine.SKILL_EVENT_BUFFGUEST_END, self.id, {"guestBuffIndex":guestBuffIndex} )

	def receiveEffectSkill(self, srcEntityID, detEntityID, skillID):
		"""
		Exposed method
		玩家碰到光效接受技能
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		detEntity = KBEngine.entities.get(int(detEntityID), None)
		if detEntity:
			self.useSkillToEntity(int(skillID), detEntity.id)

	def onRoleChaseEntityOver(self, srcEntityID, skillID, isSuccess):
		"""
		Exposed method
		玩家追击到目标		
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		skill = self.getSkill( skillID )
		if skill:
			skill.onSkillChaseOver(self, isSuccess)

	def onYCJMDrClickEvent( self, srcEntityID, mode ):
		"""
		<Exposed Method>
		勇闯绝命岛鼠标右键模式
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		self.triggerSkillEvent( csdefine.SKILL_EVENT_YCJMD_RCLICK, self.id, {"mode" : mode} )

	def addFlyPatrolEffectList( self, srcEntityID, flyPatrolID, holdEffectList ):
		"""
		添加飞行路径持有效果
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		indexList = self.flyPatrolEffectIndex.get(flyPatrolID, [])
		for holdEffectID in holdEffectList:
			index = self.addFixIDHoldEffect( holdEffectID, self )
			indexList.append(index)
		self.flyPatrolEffectIndex[flyPatrolID] = indexList

	def removeFlyPatrolEffectList( self, srcEntityID, flyPatrolID ):
		"""
		移除飞行路径持有
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		for index in self.flyPatrolEffectIndex.pop(flyPatrolID, []):
			self.removeFixIDHoldEffect(index)		

#-----------物品技能相关--------------------------------------------
	def setUsingItem( self, itemUid ):
		self.usingItemUid = itemUid

	def getUsingItem( self ):
		return self.usingItemUid

#-----------击退buff相关---------------------------------------------
	def addHitFlyTimer( self, delayTime, casterID , actionID, effectID, soundID, actionBeginTime ):
		"""
		添加被击飞timer
		"""
		if self.hitFlyTimer:
			self.popTimer( self.hitFlyTimer )
		self.hitFlyTimer = self.addTimerCallBack( delayTime, "onHitFlyTimer", ( casterID , actionID, effectID, soundID, actionBeginTime ) )

	def onHitFlyTimer( self, casterID , actionID, effectID, soundID, actionBeginTime ):
		"""
		被击飞timer，用于击飞后起身
		"""
		self.setActionIndex()
		self.allClients.BeHitPlayEffect( casterID, self.id, self.actionIndex, actionID, effectID, soundID, actionBeginTime )
		self.hitFlyTimer = 0

	def delHitFlyTimer( self ):
		"""
		取消起身timer
		"""
		if self.hitFlyTimer:
			self.popTimer( self.hitFlyTimer )
			self.hitFlyTimer = 0
	#---------------------- timer --------------------------
	def timerValeDelCB( self, timerArg ):
		"""
		取消一个timer arg的回调，也可能是执行完了
		这里主要是处理掉一些存起来的timerArg
		"""
		pass
		# if timerArg in self.skillHitTimerList:
		# 	self.skillHitTimerList.remove( timerArg )

	def OnChasePlayerFinish( self, srcEntityID ):
		"""
		<Exposed method>
		追逐玩家完成
		"""
		if self.isMoving( True ): return
		self.stopMoving(csdefine.MOVE_TYPE_CHASE)
	
	#---------------------- SkillJump相关 --------------------------
	def onJumpSkillMoveEnd( self, srcEntityID, skillID ):
		"""
		<Exposed method>
		客户端位移完了
		"""
		if srcEntityID != self.getSyncPosClient():	#不是当前同步的那个客户端就不理它
			return
		self.getSkill( skillID ).onJumpSkillMoveEnd( self )
		
	#------------------------模型改变---------------------------------
	def setChangeModel( self, isChangeModel ):
		""""""
		self._isChangeModel = isChangeModel
		
	def isChangeModel( self ):
		""""""
		return self._isChangeModel

	#------------------------晶核炼化---------------------------------
	def stopRefineSpar( self, srcEntityID ):
		"""
		<Exposed Method>
		停止晶石炼化
		"""
		if self.castingSkillID:
			skill = self.getSkill( self.castingSkillID )
			if skill and skill.__class__.__name__ == "SkillItemSpar":
				skill.interrupt( self, csstatus.SKILL_CAST_FAILED )
	
	def onStopFlyPatrol( self, srcEntityID, flyPatrolID ):
		"""
		exposed method
		飞行结束
		"""
		self.triggerSkillEvent( csdefine.SKILL_EVENT_STOP_FLY, self.id, {"flyPatrolID":flyPatrolID} )
		if self.queryTemp( "withdrawPetUID" ) != None:
			self.conjurePet(srcEntityID, str(self.queryTemp( "withdrawPetUID" )))
			self.removeTemp( "withdrawPetUID" )
		
	def hideModle( self, target ):
		"""	
		隐藏模型
		"""
		target.allClients.CLIENT_HideInvisible()

#----------------------------------------玩家心法状态--------------------------------------------------
	def initSkillPosture(self):
		data = SkillPostureLoader.g_skillPosture.getData(self.skillPosture, self.skillPostureLevel)
		if not data:
			return
		if data["HoldEffectID"]:
			self.postureEffectIndex = self.addFixIDHoldEffect(int(data["HoldEffectID"]), self)

	def changeSkillPosture(self, skillPosture, level, skill):
		"""
		切换心法
		"""
		isSame = False
		if self.skillPosture == skillPosture:
			isSame = True
		self.triggerSkillEvent( csdefine.SKILL_EVENT_SKILL_POSTURE_CHANGE, self.id, {"oldSkillPosture":self.skillPosture, "newSkillPosture":skillPosture} )
		self.leaveSkillPosture( self.skillPosture, self.skillPostureLevel, skill, isSame )
		self.enterSkillPosture( skillPosture, level, skill, isSame)
		self.oldCombatPower = self.combatPower
		self.calcAttachProperties(csdefine.CALC_COMBAT_POWER_REASON_PROP)
		self.onCombatPowerChange(self.oldCombatPower, csdefine.CALC_COMBAT_POWER_REASON_PROP)
		if self.isMountOnPet():
			self.transformPet( self.id )

	def enterSkillPosture(self, skillPosture, level, skill, isSame):
		"""
		进入心法状态
		"""
		self.skillPosture = skillPosture
		self.skillPostureLevel = level	
		data = SkillPostureLoader.g_skillPosture.getData(skillPosture, level)
		if not data:
			return			
		if data["HoldEffectID"]:
			self.postureEffectIndex = self.addFixIDHoldEffect(int(data["HoldEffectID"]), self)
			
		if data["EnterEffectID"] and not isSame: #同心法状态的改变不需要触发进入效果。
			self.addFixIDEffect( self, int(data["EnterEffectID"]), skill )

	def leaveSkillPosture(self, skillPosture, level, skill, isSame):
		"""
		离开心法状态
		"""
		data = SkillPostureLoader.g_skillPosture.getData(skillPosture, level)
		if not data:
			return
		if self.postureEffectIndex != -1:
			self.removeFixIDHoldEffect(self.postureEffectIndex)

		if data["LeaveEffectID"] and not isSame: #同心法状态的改变不需要触发离开效果。
			self.addFixIDEffect( self, int(data["LeaveEffectID"]), skill)					

	def getEquipAttachProperties(self):
		"""
		心法状态附加属性
		"""
		attackPropertiesStr = SkillPostureLoader.g_skillPosture.getAttackPropertiesStr(self.skillPosture, self.skillPostureLevel)
		return {"_extra" : attackPropertiesStr}

	def synPositionToTarget(self, target):
		"""
		将自己位置和对方同步
		"""
		if target:
			self.position = target.position

	def setActionIndex(self):
		"""
		设置连续动作标识
		"""
		if self.actionIndex >= 1000000:
			self.actionIndex = 0
		self.actionIndex += 1	
			
	#------------------------击退---------------------------------
	def OnSynHitBackPos( self, srcEntityID, buffID, desPosition ):
		"""
		<Exposed Method>
		客户端遇到障碍物（光墙）会重新计算目标位置同步到服务器
		"""
		
		buffList = self.findBuffsByBuffID( buffID )
		if not buffList:
			return
		pos = KBEMath.Unreal2KBEnginePosition(desPosition)
		self.getAttrBuffs().get(buffList[0]).setTempData("HitBackPostion",pos)