# -*- coding: utf-8 -*-


"""
usage:
	技能基类

attribute:
	pass

member function:
	pass

callback:
	pass

"""

#python
import time
import random
#engine
import KBEngine
import KBEMath
#common
import csdefine
import csconst
import KBEDebug
import Functions
import csarithmetic
import QuestEventDefine
import ItemTypeEnum
#data
import csstatus
import Settings
#data
import Skill.SkillReceiverDefine as SkillReceiverDefine
import Skill.SkillCasterDefine as SkillCasterDefine
#cell
import ConfigObject.Skill.SkillBase.ObjectCondition as ObjectCondition
import ConfigObject.Skill.SkillBase.RequireDefine as RequireDefine
import ConfigObject.Skill.SkillBase.ObjectDefine as ObjectDefine
import ConfigObject.Skill.SkillBase.HitDefine as HitDefine
import ConfigObject.Skill.EffectLoader as EffectLoader
import ConfigObject.Skill.SkillBase.EventDefine as EventDefine
import SkillTargetObjImpl



class Skill:
	def __init__( self ):
		self._id 					= 0
		self._name 					= ""
		self._isInstantSkill 		= False
		self._level 				= 0
		#self._description 			= ""
		self._actForbid  			= csdefine.ACTION_FORBID_NONE
		self._targetActForbid 		= csdefine.ACTION_FORBID_NONE
		self._targetType 			= csdefine.SKILL_CAST_OBJECT_TYPE_NONE
		self._isTurnToTarget 		= False
		self._collisionType 		= csdefine.COLLISION_DEFAULT
		self._castRangeMax 			= 0.0
		self._holdEffectList 		= []
		self._casterCoolDown		= {}
		self._targetCoolDown		= {}
		self._casterRequire 		= RequireDefine.newInstance( None )
		self._targetRequire 		= RequireDefine.newInstance( None )
		self._casterCondition 		= ObjectCondition.ObjectCondition()
		self._targetCondition 		= ObjectCondition.ObjectCondition()
		self._hitData 				= HitDefine.SkillHitData()
		self._interruptEvent 		= EventDefine.EventDefine()
		self._receiverInterruptEvent= EventDefine.ReceiverEventDefine()
		self._actionID 				= []
		self._actionBeginTime 		= []
		self._targetActionID 		= []
		self._targetActionBeginTime = []
		self._reTargetRadius		= 0.0
		self._quality				= 0


	def init( self, dictDat ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		self._isPassiveSkill = False												# 是否被动技能
		self._id = int( dictDat["Name"] )											# 技能ID
		self._name = dictDat["SkillName"]											# 技能名称
		self._quality = dictDat["Quality"]
		self._level = int( dictDat["SkillLevel"] )									# 显示等级，待定功能
		#self._description = dictDat[ "Description" ]								# 技能描述
		self._targetType = dictDat[ "TargetType" ]									# 施法目标类型
		self._isTurnToTarget = bool( dictDat.get( "IsTurnToTarget", 0 ) )			# 是否转向目标
		self._collisionType = \
		getattr( csdefine, dictDat["CollisionType"], csdefine.COLLISION_DEFAULT )	# 碰撞类型
		self._actForbid = \
		getattr( csdefine, dictDat["CasterActForbid"], csdefine.ACTION_FORBID_NONE )# 玩法类型限制（不放到objectCondition,因为它还有中断技能作用 ）
		self._targetActForbid = \
		getattr( csdefine, dictDat["TargetActForbid"], csdefine.ACTION_FORBID_NONE )# 玩法类型限制（不放到objectCondition,因为它还有中断技能作用 ）
		self._castRangeMax = dictDat[ "CastRangeMax" ]								# 最大施法距离
		
		for effectData in dictDat[ "CasterHoldEffectList" ]:						# 持有效果列表
			effect = EffectLoader.g_effects.createEffect( effectData )
			self._holdEffectList.append( effect )
		
		for cdata in dictDat["CasterCoolDown"]:											# 施法者技能冷却
			self._casterCoolDown[ cdata["CooldownId"] ] = cdata["CoolDownTime"]

		for cdata in dictDat["TargetCoolDown"]:											# 受术者技能冷却
			self._targetCoolDown[ cdata["CooldownId"] ] = cdata["CoolDownTime"]
		
		if len( dictDat[ "CasterRequireDefine" ] ) > 0: #list
			self._casterRequire = RequireDefine.newInstance( dictDat[ "CasterRequireDefine" ] )		# 施放消耗
		if len( dictDat[ "TargetRequireDefine" ] ) > 0: #list
			self._targetRequire = RequireDefine.newInstance( dictDat[ "TargetRequireDefine" ] )		# 施放消耗
		if len( dictDat[ "CasterCondition" ] ) > 0: #dict							# 施法者条件
			self._casterCondition.init( dictDat["CasterCondition"] )
		if len( dictDat[ "TargetCondition" ] ) > 0: #dict							# 施法目标条件
			self._targetCondition.init( dictDat["TargetCondition"] )
		
		self._castObject = ObjectDefine.newInstance( self._targetType, self )
		self._castObject.init( dictDat )
		
		self._hitData.init( dictDat["HitList"], self )
		
		self._interruptEvent.init( dictDat["CasterInterruptSkillEvent"] )			# 主动技能-中断技能事件
		
		if self._targetType != csdefine.SKILL_CAST_OBJECT_TYPE_POSITION:
			self._receiverInterruptEvent.init( dictDat["TargetInterruptSkillEvent"] )

		actionInfos = dictDat["CasterCastActionId"].split("|")
		for i in actionInfos:
			actionInfo = i.split(":")
			if len( actionInfo ) > 1:
				self._actionID.append(actionInfo[0])
				self._actionBeginTime.append( actionInfo[1] )			
			else:
				self._actionID.append(actionInfo[0])
				self._actionBeginTime.append( "0.0")

		targetActionInfos = dictDat["TargetCastActionId"].split("|")
		for i in targetActionInfos:
			actionInfo = i.split(":")
			if len( actionInfo ) > 1:
				self._targetActionID.append(actionInfo[0])
				self._targetActionBeginTime.append( actionInfo[1] )			
			else:
				self._targetActionID.append(actionInfo[0])
				self._targetActionBeginTime.append( "0.0")

		# 标记列表（:冒号|竖号分隔，多个代表“且”，留空代表“没有标记”，具体格式与功能由标记定义）
		if dictDat and dictDat["Param5"]:
			Param5 = dictDat["Param5"].split("|")
			for i in Param5:
				List = i.split(":")
				if List[0] == "IsReTPRandom":		# 执行目标位置随机偏移
					self._reTargetRadius = float(List[1])

	def getScriptType( self ):
		"""
		获得脚本类型
		"""
		return csdefine.SCRIPT_TYPE_SKILL
				
	def isPassiveSkill( self ):
		"""是否被动技能"""
		return self._isPassiveSkill

	def isInstantSkill( self ):
		"""
		是否瞬发技能
		"""
		return self._isInstantSkill

	def getID( self ):
		"""
		获取技能id
		"""
		return self._id

	def getQuality( self ):
		"""
		获取技能id
		"""
		return self._quality

	def getSkillLevel( self ):
		"""
		获取技能等级
		"""
		return self._level
	
	def getActForbid( self ):
		"""
		获取施法者相关开关
		"""
		return self._actForbid

	def getTargetActForbid(self):
		"""
		获取技能目标相关开关
		"""
		return self._targetActForbid

	def getCollisionType( self ):
		"""
		获取施法碰撞类型
		"""
		return self._collisionType

	def getRangeMax( self, caster, target ):
		"""
		virtual method.
		@param caster: 施法者，通常某些需要武器射程做为距离的法术就会用到。
		@return: 施法最大距离
		"""
		if self._castRangeMax == 0:
			return csdefine.SKILL_CAST_RANGE_MAX
		return self._castRangeMax

	def getTargetType( self ):
		"""
		获取施法目标类型
		"""
		return self._targetType

	def getHit( self, hitTime, index ):
		return self._hitData.getHit( hitTime, index )

	def getSkillTotalTime( self ):
		"""
		获取技能总时间
		"""
		return self._hitData.getTotalTime()
		
	def getHitInstance( self ):
		"""
		"""
		return self._hitData

	def useSkill( self, caster, target ):
		"""
		"""
		if not self.skillDefineCheck(caster, target):  #CST-4084/CST-2113
			return csstatus.SKILL_CAST_FAILED
		# 当配置里的技能目标类型和传过来的技能目标类型不符时
		target = self.adaptiveTarget(caster, target)
		if not target:
			return csstatus.SKILL_CAST_FAILED

		state = self.useableCheck( caster, target )
		if state != csstatus.SKILL_GO_ON:
			return state

		space = caster.getCurrentSpace()
		if space:
			if len(space.getScript().getAllowUseSkillIDs()) and self._id not in space.getScript().getAllowUseSkillIDs():
				return csstatus.SKILL_SPACE_FORBID
			if len(space.getScript().getForbidUseSkillIDs()) and self._id in space.getScript().getForbidUseSkillIDs():
				return csstatus.SKILL_SPACE_FORBID

		caster.beforeUseSkill( self, target )
		self.use( caster, target )
		return csstatus.SKILL_GO_ON

	def useableCheck( self, caster, target ):
		"""
		检查技能是否可以使用
		"""
		#观察者标志位禁止施法
		if caster.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
			if caster.hasFlag( csdefine.ROLE_FLAG_WATCHER ):
				return csstatus.SKILL_STATE_CANT_CAST

		if self._actForbid != csdefine.ACTION_FORBID_NONE: #解决某些如果只需要释放技能，而没有state属性的问题
			#施法者是否有禁止标记
			if caster.actionForbidSign( self._actForbid ):
				return csstatus.SKILL_STATE_CANT_CAST

		#是异常抵抗
		if target.getType() == csdefine.SKILL_TARGET_OBJECT_ENTITY:
			if self.checkExceptionResist( target.getObject() ):
				return csstatus.SKILL_STATE_CANT_CAST

		if self._targetActForbid != csdefine.ACTION_FORBID_NONE: #解决某些如果只需要释放技能，而没有state属性的问题
			#技能目标是否有禁止标记
			if target.getType() == csdefine.SKILL_TARGET_OBJECT_ENTITY:
				if target.getObject().actionForbidSign( self._targetActForbid ):
					return csstatus.SKILL_TARGET_STATE_CANT_CAST

		#检测当前是否正在释放技能
		if caster.isCastingSkill():
			return csstatus.SKILL_IS_CASTING
		
		#检查技能cooldown
		if self.isCasterCooldown( caster ):
			return csstatus.SKILL_NOT_READY

		#目标检查技能cooldown
		if target.getType() == csdefine.SKILL_TARGET_OBJECT_ENTITY:
			if self.isTargetCooldown( target ):
				return csstatus.SKILL_TARGET_NOT_READY

		#施法需求检查
		state = self.checkCasterRequire( caster )
		if state != csstatus.SKILL_GO_ON:
			return state

		#施法目标检查
		if target.getType() == csdefine.SKILL_TARGET_OBJECT_ENTITY:
			state = self.checkTargetRequire( target )
			if state != csstatus.SKILL_GO_ON:
				return state

		#施法者检查
		state = self.castValidCheck( caster, caster )
		if state != csstatus.SKILL_GO_ON:
			return state

		#检查目标是否符合法术施展
		state = self.getCastObject().valid( caster, target )
		if state != csstatus.SKILL_GO_ON:
			return state
		
		#施法目标检查
		state = self.targetValidCheck( caster, target )
		if state != csstatus.SKILL_GO_ON:
			return state
		
		return csstatus.SKILL_GO_ON

	def use( self, caster, target ):
		"""
		"""
		# 转向
		if self._isTurnToTarget:
			caster.turnToSkillTarget( target)
		self.cast( caster, target )

	def cast( self, caster, target ):
		"""
		施放技能
		"""
		if not caster:
			return
		if not target.getObject():
			return
			
		caster.isInterruptSkill[self._id] = 0
		self.registerSkillEvent( caster, target )
		
		if len(self._casterCoolDown):
			caster.setCooldown( self._casterCoolDown )
		# 处理消耗
		self.doCasterRequire( caster )

		# 通知客户端释放技能，播放动作等
		if self._targetType == csdefine.SKILL_CAST_OBJECT_TYPE_POSITION:
			position = target.getObject()
			if self._reTargetRadius > 0.0:
				position = csarithmetic.getPositionByCircular(position, self._reTargetRadius)
			ue4_position = KBEMath.KBEngine2UnrealPosition( position )
			KBEDebug.DEBUG_MSG( "---------Skill Debug(%s): play attack action, %s(%s) to position %s" %( self._id, caster, caster.id, position ) )
			caster.setActionIndex()
			caster.skillActionIndex[self._id] = caster.actionIndex
			caster.allClients.CastSkillToPosition( self._id, int( self.isInstantSkill() ), ue4_position[0], ue4_position[1], ue4_position[2], self._actionID, self._actionBeginTime, caster.actionIndex, caster.id )
		else:
			caster.setActionIndex()
			caster.skillActionIndex[self._id] = caster.actionIndex
			KBEDebug.DEBUG_MSG( "---------Skill Debug(%s): play attack action, %s(%s)" %( self._id, caster, caster.id ) )
			caster.allClients.CastSkillToTarget( self._id, int( self.isInstantSkill() ), target.getObject().id, self._actionID, self._actionBeginTime, caster.actionIndex, caster.id )
			
		# 对技能目标处理cd，消耗， 播放动作
		if target.getType() == csdefine.SKILL_TARGET_OBJECT_ENTITY:
			if len(self._targetCoolDown):
				target.getObject().setCooldown( self._targetCoolDown )
			self.doTargetRequire(target)
			if target.getObject().id != caster.id:
				target.getObject().setActionIndex()
				target.getObject().skillActionIndex[self._id] = caster.actionIndex
				target.getObject().allClients.CLIENT_PlayOneByOneAction(target.getObject().actionIndex, self._targetActionID, self._targetActionBeginTime)

		self.onSkillBegin( caster, target )

	def onSkillBegin( self, caster, target ):
		"""
		virtual method
		技能开始
		"""
		caster.onSkillBegin( self, target )
		target.onSkillBegin( caster )
		isHit = 1

		self.addHoldEffect( caster )		# 添加持有效果

		caster.triggerEventSkillBegin( self )	# 触发施法者“施展开始时”

		if caster.isInterruptSkill.get(self._id, 0):				# 技能中断响应
			caster.interruptSkill( csstatus.SKILL_CAST_FAILED )
			isHit = 0
		caster.isInterruptSkill[self._id] = 1

		if isHit:				# 开始打击
			self._hitData.begin( self, caster, target )


	def onSkillHit( self, caster, target, hitTime ):
		"""
		技能打击
		"""
		self._hitData.onHit( self, caster, target, hitTime )

	def onArrive( self, caster, target, hitTime, index ):
		"""
		技能抵达
		"""
		self._hitData.onHitArrive( self, caster, target, hitTime, index )

	def onSkillEnd( self, caster, target, castResult ):
		"""
		virtual method.
		技能结束
		"""
		caster.onSkillEnd( self, castResult )
		self.removeHoldEffect( caster )
		self.unRegisterSkillEvent( caster, target)
		caster.isInterruptSkill.pop(self._id, 0)

	def addHoldEffect( self, caster ):
		"""
		加载持有效果
		"""
		for index, effect in enumerate( self._holdEffectList ):
			if effect.canEffect( caster, caster ):
				effectData = effect.getNewEffectData( caster, caster )
				effectData.index = caster.getNewHoldEffectIndex()
				effectData.sourceType = csdefine.HOLD_EFFECT_SOURCE_TYPE_SKILL
				effectData.sourceID = self.getID()
				effectData.configIndex = index
				effectData.casterID = caster.id
				
				caster.addHoldEffectData( effectData )
				effect.onBegin( effectData, caster )

	def removeHoldEffect( self, caster ):
		"""
		移除持有效果
		"""
		for index, effect in enumerate( self._holdEffectList ):
			for effectData in list( caster.holdEffectData ):
				if effectData.sourceType == csdefine.HOLD_EFFECT_SOURCE_TYPE_SKILL and effectData.configIndex == index and effectData.sourceID == self.getID():
					effect.onEnd( effectData, caster )
					caster.removeHoldEffectData( effectData.index )

	def onClientActorCreate( self, caster, srcEntityID ):
		"""
		virtual method
		receiver在某客户端被创建出来
		"""
		for index, effect in enumerate( self._holdEffectList ):
			for effectData in caster.holdEffectData:
				if effectData.sourceType == csdefine.HOLD_EFFECT_SOURCE_TYPE_SKILL and effectData.configIndex == index:
					effect.onClientActorCreate( effectData, caster, srcEntityID )

	def isCasterCooldown( self, caster ):
		"""
		施法者技能是否在冷却中
		"""
		for id in self._casterCoolDown:
			for dDict in caster.getCooldown():
				if dDict["id"] == id and ( dDict["endTime"] - Functions.getTime() > 0.1 * csconst.TIME_ENLARGE_MULTIPLE ): #CST-3267 允许服务器time最小精度误差
					return True

		return False

	def isTargetCooldown( self, target ):
		"""
		技能目标是否在冷却中
		"""
		for id in self._targetCoolDown:
			for dDict in target.getObject().getCooldown():
				if dDict["id"] == id and ( dDict["endTime"] - Functions.getTime() > 0.1 * csconst.TIME_ENLARGE_MULTIPLE ): #CST-3267 允许服务器time最小精度误差
					return True

		return False

	def checkCasterRequire( self, caster ):
		"""
		检测施法者消耗是否够
		"""
		return self._casterRequire.validObject( caster, self )

	def checkTargetRequire(self, target):
		"""
		检测技能目标消耗是否够
		"""
		return csconst.SKILL_REQUIRE_MESSAGE.get(self._targetRequire.validObject( target.getObject(), self ),csstatus.SKILL_GO_ON)

	def doCasterRequire( self, caster ):
		"""
		处理施法者消耗
		"""
		self._casterRequire.pay( caster, self )

	def doTargetRequire( self, target ):
		"""
		处理施法者消耗
		"""
		self._targetRequire.pay( target.getObject(), self )


	def getCastObject( self ):
		"""
		取得法术施法目标对像。
		@return:  ObjectDefine Instance
		"""
		return self._castObject

	def castValidCheck( self, caster, target):
		"""
		virtual method.
		校验技能是否可以施展。
		此接口仅仅用于当法术吟唱完后判断是否能对目标施展，
		如果需要判断一个法术是否能对目标使用，应该使用intonateValidityCheck()方法。
		此接口会被intonateValidityCheck()接口调用，如果重载时某些条件需要在吟唱结束后判断，
		则必须重载此接口并加入相关判断，否则只能重载intonateValidityCheck()接口。

		注：此接口是旧版中的validCast()

		@param target: 施展对象
		@type  target: 一个包装过的对象entity 被包装对象可能是 (位置，entity, item)详细请看SkillTargetObjImpl.py
		@return:           INT，see also csdefine.SKILL_*
		@rtype:            INT
		"""
		return self._casterCondition.valid( caster, target, True )

	def targetValidCheck( self, caster, target ):
		"""
		virtual method.
		检查施法目标是否满足吟唱条件
		@return: INT，see also SkillDefine.SKILL_*
		"""
		if target.getType() == csdefine.SKILL_TARGET_OBJECT_POSITION and self._targetCondition.isHasConditions():
			return csstatus.SKILL_CAST_ENTITY_ONLY
		return self._targetCondition.valid( caster, target.getObject(), False )

	def canInterrupt( self, caster, reason ):
		"""
		能否打断
		"""
		return True

	def interrupt( self, caster, reason, target = None ):
		"""
		打断
		"""
		if not self.canInterrupt( caster, reason ):
			return
		caster.triggerEventSkillInterrupt(self)
		self.onSkillEnd( caster, target, False )
		caster.onSkillInterrupted( self.getID(), reason )
		caster.allClients.SkillInterrupted( self.getID(), reason, caster.skillActionIndex.get(self._id, 0))
		caster.skillActionIndex.pop(self._id, 0)
		
	def attachToCaster( self, caster ):
		"""
		"""
		pass
		
	def detachToCaster( self, caster ):
		"""
		"""
		pass

	def registerSkillEvent( self, caster, target ):
		"""注册中断事件"""
		self._interruptEvent.registerEvent( self, caster )
		self._receiverInterruptEvent.registerEvent( self, caster, target )
		
		if self._actForbid != csdefine.ACTION_FORBID_NONE:
			caster.registerSkillEvent( csdefine.SKILL_EVENT_ACT_WORD_CHANGE, self._id )
		# 施法者注册传送地图，销毁事件		
		caster.registerSkillEvent( csdefine.SKILL_EVENT_SPACE_CHANGE, self._id )
		caster.registerSkillEvent( csdefine.SKILL_EVENT_DESTROY, self._id )
		# 受术者者注册传送地图，销毁事件	
		if self.getTargetType() == csdefine.SKILL_CAST_OBJECT_TYPE_ENTITY:
			receiver = target.getObject()
			if receiver:
				receiver.registerReceiverSkillEvent( csdefine.SKILL_EVENT_SPACE_CHANGE, caster.id, self._id )
				receiver.registerReceiverSkillEvent( csdefine.SKILL_EVENT_DESTROY, caster.id, self._id )
	
	def unRegisterSkillEvent( self, caster, target ):
		"""取消中断事件"""
		self._interruptEvent.unRegisterEvent( self, caster )
		
		if self._actForbid != csdefine.ACTION_FORBID_NONE:
			caster.unRegisterSkillEvent( csdefine.SKILL_EVENT_ACT_WORD_CHANGE, self._id )
		# 施法者注册传送地图，销毁事件
		if caster:		
			caster.unRegisterSkillEvent( csdefine.SKILL_EVENT_SPACE_CHANGE, self._id )
			caster.unRegisterSkillEvent( csdefine.SKILL_EVENT_DESTROY, self._id )

		# 受术者者注册传送地图，销毁事件	
		if self.getTargetType() == csdefine.SKILL_CAST_OBJECT_TYPE_ENTITY and target:
			receiver = target.getObject()
			if receiver:
				receiver.unRegisterReceiverSkillEvent( caster.id, self._id )

	def triggerSkillEvent( self, caster, eventType, triggerID, pDict ):
		"""
		virtual method
		触发技能事件
		"""
		if eventType == csdefine.SKILL_EVENT_ACT_WORD_CHANGE:
			if pDict.get( "actWord", 0 ) == self._actForbid and pDict.get( "disabled", True ) \
			and caster.castingSkillID == self._id:
				self.interruptSkill( caster, csstatus.SKILL_CAST_FAILED )
		# 施法者传送地图，销毁中断技能		
		if eventType in [ csdefine.SKILL_EVENT_SPACE_CHANGE, csdefine.SKILL_EVENT_DESTROY ] and caster.castingSkillID == self._id:		#CST-3071：施法目标传送或销毁时中断技能
			self.interruptSkill( caster, csstatus.SKILL_CAST_FAILED )

		if self._interruptEvent.canTriggerEvent( eventType, pDict ) and caster.castingSkillID == self._id:
			self.interruptSkill( caster, csstatus.SKILL_CAST_FAILED )

	def interruptSkill(self, caster, reason ):
		"""
		处理中断的一些逻辑
		"""
		if caster.isInterruptSkill.get(self._id, 0):
			caster.interruptSkill( csstatus.SKILL_CAST_FAILED )
		else:
			caster.isInterruptSkill[self._id] = 1

	def triggerReceiverSkillEvent( self, caster, receiver, eventType, triggerID, pDict ):
		"""
		virtual method
		触发受术目标事件
		"""
		if eventType in [ csdefine.SKILL_EVENT_SPACE_CHANGE, csdefine.SKILL_EVENT_DESTROY ] and caster.castingSkillID == self._id:		#CST-3071：施法目标传送或销毁时中断技能
			caster.interruptSkill( csstatus.SKILL_CAST_FAILED )
		
		if self._receiverInterruptEvent.canTriggerEvent( eventType, pDict ) and caster.castingSkillID == self._id:
			caster.interruptSkill( csstatus.SKILL_CAST_FAILED )

	def skillDefineCheck(self, caster, target):
		"""
		受术者/施法者 可战斗单位要求
		"""
		if target.getType() == csdefine.SKILL_TARGET_OBJECT_POSITION:
			receiver = None
		else:
			receiver = target.getObject()

		skillName = self.__class__.__name__
		if receiver and skillName in SkillReceiverDefine.Datas:
			flag = receiver.getEntityFlag()
			if flag in SkillReceiverDefine.Datas[skillName]:
				if not SkillReceiverDefine.Datas[skillName][flag]:					
					KBEDebug.WARNING_MSG( "receiver(type:%d) in skill skillName(%s) is limit(SkillReceiverDefine)!!"%(flag,skillName) )
				return SkillReceiverDefine.Datas[skillName][flag]

		if skillName in SkillCasterDefine.Datas:
			_flag = caster.getEntityFlag()
			if _flag in SkillCasterDefine.Datas[skillName]:
				if not SkillCasterDefine.Datas[skillName][_flag]:
					KBEDebug.WARNING_MSG( "caster(type:%d) in skill skillName(%s) is limit(SkillCasterDefine)!!"%(_flag,skillName) )
				return SkillCasterDefine.Datas[skillName][_flag]
		return True

	def adaptiveTarget(self, caster, target):
		if self._targetType == csdefine.SKILL_CAST_OBJECT_TYPE_ENTITY and target.getType() == csdefine.SKILL_TARGET_OBJECT_POSITION:
			return None
		elif self._targetType == csdefine.SKILL_CAST_OBJECT_TYPE_POSITION and target.getType() == csdefine.SKILL_TARGET_OBJECT_ENTITY:
			target = SkillTargetObjImpl.createTargetObjPosition(target.getObjectPosition())
		elif self._targetType == csdefine.SKILL_CAST_OBJECT_TYPE_NONE:
			target = SkillTargetObjImpl.createTargetObjEntity(caster)

		return target

	def checkExceptionResist( self, receiver ):
		"""
		是否异常抵抗
		"""
		if self._actForbid == csdefine.ACTION_FORBID_BE_DEPRESS:
			if (ItemTypeEnum.PRECENTRATIO - receiver.depress_resist) < random.randint(0, ItemTypeEnum.PRECENTRATIO ):
				return True
		elif self._actForbid == csdefine.ACTION_FORBID_BE_HIT_BACK:
			if (ItemTypeEnum.PRECENTRATIO - receiver.hitback_resist) < random.randint(0, ItemTypeEnum.PRECENTRATIO ):
				return True
		elif self._actForbid == csdefine.ACTION_FORBID_BE_CONTROL:
			if (ItemTypeEnum.PRECENTRATIO - receiver.control_resist) < random.randint(0, ItemTypeEnum.PRECENTRATIO ):
				return True
		elif self._actForbid == csdefine.ACTION_FORBID_INSANE:
			if (ItemTypeEnum.PRECENTRATIO - receiver.insane_resist) < random.randint(0, ItemTypeEnum.PRECENTRATIO ):
				return True
		return False