

#python
import time
import random
#engine
import KBEngine
#common
import csdefine
import KBEDebug
import Functions
import ItemTypeEnum
#data
import csstatus
import Skill.SkillReceiverDefine as SkillReceiverDefine
import Skill.SkillCasterDefine as SkillCasterDefine
#cell
import ConfigObject.Skill.SkillBase.ObjectCondition as ObjectCondition
import ConfigObject.Skill.SkillBase.EventDefine as EventDefine
import ConfigObject.Skill.SkillBase.RequireDefine as RequireDefine
import ConfigObject.Skill.SkillBase.ObjectDefine as ObjectDefine
import ConfigObject.Skill.SkillBase.HitDefine as HitDefine
import ConfigObject.Skill.EffectLoader as EffectLoader
#user_type
import BuffDataType



class Buff:
	def __init__( self ):
		self.isInterruptBuff = 1
		self._id = 0
		self._replaceCondition 	= ObjectCondition.BuffReplaceCondition()
		self._replaceEffectList = []
		self._extraCondition 	= ObjectCondition.BuffExtraCondition()
		self._extraEffectList 	= []
		self._holdTime 			= 0.0
		self._holdEffectList 	= []
		self._holdEffectNames	= []
		self._actForbid = csdefine.ACTION_FORBID_NONE
		self._saveType = csdefine.BUFF_OFFLINE_SAVE_TYPE_NULL
		self._casterInterruptEvent = EventDefine.EventDefine()
		self._targetInterruptEvent = EventDefine.ReceiverEventDefine()
		self._buffName = ""
		self._buffAction = []
		self._buffActionBeginTime = []
		self._buffEffect = ""
		self._buffSound = ""
		self._conflictPriority = csdefine.BUFF_CONFLICT_PRIORITY_NONE
		self._conflictType = csdefine.BUFF_CONFLICT_TYPE_NONE
	
	def init( self, dictDat ):
		"""
		virtual method;
		读取buff配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		self._id = int( dictDat["Name"] )											# buffID
		if len( dictDat[ "ReplaceCondition" ] ) > 0:								# 置换条件
			self._replaceCondition.init( dictDat["ReplaceCondition"] )
		for effectData in dictDat[ "ReplaceEffectList" ]:							# 置换效果列表
			effect = EffectLoader.g_effects.createEffect( effectData )
			self._replaceEffectList.append( effect )
		
		if len( dictDat[ "ExtraCondition" ] ) > 0:									# 额外条件
			self._extraCondition.init( dictDat["ExtraCondition"] )
		for effectData in dictDat[ "ExtraEffectList" ]:								# 额外效果列表
			effect = EffectLoader.g_effects.createEffect( effectData )
			self._extraEffectList.append( effect )
		
		self._holdTime = float( dictDat["HoldTime"] )
		if self._holdTime > 0 and self._holdTime < 0.1:
			self._holdTime = 0.1
		for effectData in dictDat[ "HoldEffectList" ]:								# 持有效果列表
			effect = EffectLoader.g_effects.createEffect( effectData )
			self._holdEffectList.append( effect )
			self._holdEffectNames.append( effectData["HitEffectType"] )
		
		self._saveType = dictDat["SaveType"]										# 下线保存类型
		self._loopTime = float( dictDat["LoopTime"] )								# buff周期时间
		
		self._actForbid = \
		getattr( csdefine, dictDat["TargetActForbid"], csdefine.ACTION_FORBID_NONE )		# 玩法类型限制
		self._casterInterruptEvent.init( dictDat["CasterInterruptBuffEvent"] )
		self._targetInterruptEvent.init( dictDat["TargetInterruptBuffEvent"] )

		self._buffName = dictDat["BuffName"]
		self._buffEffect = dictDat["BuffEffect"]
		self._buffSound = dictDat["BuffSound"]

		actionInfos = dictDat["BuffAction"].split("|")
		for i in actionInfos:
			actionInfo = i.split(":")
			if len( actionInfo ) > 1:
				self._buffAction.append(actionInfo[0])
				self._buffActionBeginTime.append( actionInfo[1] )			
			else:
				self._buffAction.append(actionInfo[0])
				self._buffActionBeginTime.append( "0.0")

	def getScriptType( self ):
		"""
		获得脚本类型
		"""
		return csdefine.SCRIPT_TYPE_BUFF

	def getID( self ):
		"""
		获取id
		"""
		return self._id

	def getBuffName( self ):
		"""
		获得Buff名称
		"""
		return self._buffName
		
	def getActForbid( self ):
		"""
		获取相关开关
		"""
		return self._actForbid

	def getSaveType( self ):
		return self._saveType

	def getHoldTime( self ):
		return self._holdTime

	def getLoopTime( self ):
		return self._loopTime

	def getHit( self, attrName, index ):
		return getattr( self, attrName ).getHit( index )

	def holdEffect( self, effectName ):
		"""
		是否持有某效果
		"""
		return effectName in self._holdEffectNames
		
	def receive( self, caster, receiver ):
		"""
		用于给目标施加一个buff，所有的buff的接收都必须通过此接口，
		此接口必须判断接收者是否为realEntity，

		@param   caster: 施法者
		@type    caster: Entity
		@param receiver: 受击者，None表示不存在
		@type  receiver: Entity
		"""
		if not self.addBuffCheck( caster, receiver ):
			return False
		
		#替换效果
		if self._replaceCondition.valid( caster, receiver, True ) == csstatus.SKILL_GO_ON:
			for effect in self._replaceEffectList:
				if effect.canEffect( self, caster, receiver ):
					effect.onReceive( self, caster, receiver )
			return False
		
		self.receiveSuccess( caster, receiver )
		return True
	
	def receiveSuccess( self, caster, receiver ):
		"""
		通过了免疫、替换等等等的拦截，真正要加buff了
		"""
		self.doBuffReplace(caster, receiver)
		#额外效果
		if self._extraCondition.valid( caster, receiver, True ) == csstatus.SKILL_GO_ON:
			for effect in self._extraEffectList:
				if effect.canEffect( self, caster, receiver ):
					effect.onReceive( self, caster, receiver )
		
		buffData = self.getNewBuffData( caster, receiver )
		receiver.onAddBuff( buffData )
		return True
	
	def addBuffCheck( self, caster, receiver ):
		"""
		添加检测
		"""
			
		#是否有禁止标记
		if receiver.actionForbidSign( self._actForbid ):
			return False

		#是异常抵抗
		if self.checkExceptionResist( receiver ):
			return False

		# 是否可以顶替
		if not self.canBuffReplace(caster, receiver):
			return False

		buffName = self.__class__.__name__
		if buffName in SkillReceiverDefine.Datas:
			flag = receiver.getEntityFlag()
			if flag in SkillReceiverDefine.Datas[buffName]:
				if not SkillReceiverDefine.Datas[buffName][flag]:
					KBEDebug.WARNING_MSG( "receiver(type:%d) in skill buffName(%s) is limit(SkillReceiverDefine)!!"%(flag,buffName) )
				return SkillReceiverDefine.Datas[buffName][flag]

		if buffName in SkillCasterDefine.Datas:
			_flag = caster.getEntityFlag()
			if _flag in SkillCasterDefine.Datas[buffName]:
				if not SkillCasterDefine.Datas[buffName][_flag]:
					KBEDebug.WARNING_MSG( "caster(type:%d) in skill buffName(%s) is limit(SkillCasterDefine)!!"%(_flag,buffName) )
				return SkillCasterDefine.Datas[buffName][_flag]

		return True

	def doBegin( self, receiver, buffData ):
		"""
		效果开始
		"""
		self.isInterruptBuff = 0
		isHit = 1
		self.registerEvent( receiver, buffData )
		self.addHoldEffect( receiver, buffData )
		receiver.setActionIndex()
		receiver.allClients.PlayBuffEffect( buffData.index, buffData.casterID, receiver.actionIndex, self._buffAction, self._buffActionBeginTime, self._buffEffect, self._buffSound )
	
		if self.isInterruptBuff:
			self.doInterrupt( receiver, buffData )
			isHit = 0
		self.isInterruptBuff = 1
		if isHit:
			receiver.triggerEventBuffBegin(self)
			self.doBeginHit( receiver, buffData )

	def doReload( self, receiver, buffData ):
		"""
		上线重新加载buff
		"""
		self.registerEvent( receiver, buffData )
		if buffData.casterIsSelf:		#如果施法者是自己，重新设置自己ID为施法者ID
			buffData.casterID = receiver.id
		self.addHoldEffect( receiver, buffData, True )
		receiver.setActionIndex()
		receiver.allClients.PlayBuffEffect( buffData.index, buffData.casterID, receiver.actionIndex, self._buffAction, self._buffActionBeginTime, self._buffEffect, self._buffSound )

	def doEnd( self, receiver, buffData, reason ):
		"""
		效果结束
		"""
		if reason == csdefine.BUFF_END_RESON_BY_TIME_OVER:
			self.doEndHit( receiver, buffData )
			receiver.triggerEventBuffEnd(self)
		else:
			receiver.triggerEventBuffInterrupt(self)
			
		self.removeHoldEffect( receiver, buffData )
		self.unRegisterEvent( receiver, buffData )
		self.doClear( receiver, buffData, reason )
		receiver.triggerEventBuffRemove(self)

	def doClear( self, receiver, buffData, reason ):
		"""
		清除Buff数据
		"""
		receiver.clearBuff(buffData, reason)
	
	def addHoldEffect( self, receiver, buffData, isReloadBuff = False ):
		"""
		virtual method
		加载持有效果
		"""
		caster = KBEngine.entities.get( buffData.casterID, None )
		for index, effect in enumerate( self._holdEffectList ):
			if isReloadBuff or effect.canEffect( caster, receiver ):	#上线加载时不检测条件
				effectData = effect.getNewEffectData( caster, receiver )
				effectData.index = receiver.getNewHoldEffectIndex()
				effectData.sourceType = csdefine.HOLD_EFFECT_SOURCE_TYPE_BUFF
				effectData.sourceID = self.getID()
				effectData.configIndex = index
				effectData.casterID = caster.id if caster != None else 0
				effectData.buffIndex = buffData.index
				effectData.setTempData( "isReloadBuff", isReloadBuff )		#记录是不是重载buff引起的加载持有效果，某些持有效果需要此信息
				
				receiver.addHoldEffectData( effectData )
				effect.onBegin( effectData, receiver )
	
	def removeHoldEffect( self, receiver, buffData ):
		"""
		virtual method
		移除持有效果
		"""
		for index, effect in enumerate( self._holdEffectList ):
			for effectData in list( receiver.holdEffectData ):
				if effectData.sourceType == csdefine.HOLD_EFFECT_SOURCE_TYPE_BUFF and effectData.configIndex == index and effectData.buffIndex == buffData.index:
					effect.onEnd( effectData, receiver )
					receiver.removeHoldEffectData( effectData.index )

	def onClientActorCreate( self, receiver, buffData, srcEntityID ):
		"""
		virtual method
		receiver在某客户端被创建出来
		"""
		playerEntity = KBEngine.entities.get( srcEntityID )
		if srcEntityID == receiver.id:
			clientEntity = receiver.client if receiver.getClient() else None
		else:
			if not playerEntity: return
			clientEntity = playerEntity.clientEntity( receiver.id )
		
		for index, effect in enumerate( self._holdEffectList ):
			for effectData in receiver.holdEffectData:
				if effectData.sourceType == csdefine.HOLD_EFFECT_SOURCE_TYPE_BUFF and effectData.configIndex == index and effectData.buffIndex == buffData.index:
					effect.onClientActorCreate( effectData, receiver, srcEntityID )

	def doInterrupt( self, receiver, buffData ):
		"""
		"""
		if self.isInterruptBuff:
			self.doInterruptHit( receiver, buffData )
		else:
			self.isInterruptBuff = 1
	
	def doLoop( self, receiver, buffData ):
		"""
		"""
		self.doLoopHit( receiver, buffData )

	def doBeginHit( self, receiver, buffData ):
		"""
		开始打击
		"""
		pass
	
	def doEndHit( self, receiver, buffData ):
		"""
		结束打击
		"""
		pass
	
	def doInterruptHit( self, receiver, buffData ):
		"""
		中断打击
		"""
		pass

	def doLoopHit( self, receiver, buffData ):
		"""
		周期打击
		"""
		pass
	
	def doStack( self, receiver, buffData ):
		"""
		叠加
		"""
		pass

	def getNewBuffData( self, caster, receiver ):
		"""
		"""
		newBuffData = BuffDataType.BuffDataType()
		newBuffData.buffID = self.getID()
		newBuffData.holdTime = self.getHoldTime()
		newBuffData.endTime = self.calculateEndTime( newBuffData.holdTime )
		newBuffData.className = self.__class__.__name__
		
		casterID = 0
		if hasattr( caster, "id" ):
			casterID = caster.id
			if caster.id == receiver.id:
				newBuffData.casterIsSelf = True
		newBuffData.casterID = casterID
		
		return newBuffData

	def getBuffRemainTime( self, buffData ):
		"""
		获取buff剩余时间
		"""
		return Functions.convertTime( buffData.endTime - Functions.getTime() )

	def calculateEndTime( self, holdTime ):
		"""
		根据持续时间计算结束时间
		"""
		if holdTime < 0: return 0
		return Functions.getTime( round( holdTime, 1) )

	def isTimeout( self, buffData ):
		"""
		virtual method.
		检查是否已超时

		@return: BOOL，如果condition的持续时间还没过则返回False，否则返回True
		@rtype:  BOOL
		"""
		if buffData.holdTime < 0: return False		# 无持续时间，永不过期
		return Functions.getTime(0.1) > buffData.endTime

	def registerEvent( self, receiver, buffData ):
		caster = KBEngine.entities.get( buffData.casterID, None )
		self._targetInterruptEvent.registerBuffEvent( buffData, receiver )
		self._casterInterruptEvent.registerBuffEvent( buffData, caster,receiver )
		
		if self._actForbid != csdefine.ACTION_FORBID_NONE:
			receiver.registerBuffEvent( csdefine.SKILL_EVENT_ACT_WORD_CHANGE, buffData.index )
	
	def unRegisterEvent( self, receiver, buffData ):
		caster = KBEngine.entities.get( buffData.casterID, None )
		self._targetInterruptEvent.unRegisterBuffEvent( buffData, receiver )
		self._casterInterruptEvent.unRegisterBuffEvent( buffData, caster, receiver )
		
		if self._actForbid != csdefine.ACTION_FORBID_NONE:
			receiver.unRegisterBuffEvent( csdefine.SKILL_EVENT_ACT_WORD_CHANGE, buffData.index )
		
	def triggerBuffEvent( self, receiver, eventType, triggerID, buffData, pDict ):
		"""
		virtual member
		触发受术者buff事件
		"""
		if eventType == csdefine.SKILL_EVENT_ACT_WORD_CHANGE:
			if pDict.get( "actWord", 0 ) == self._actForbid and pDict.get( "disabled", True ):
				receiver.removeBuff( buffData.index )
				self.doInterrupt( receiver, buffData )				# 触发中断

		if self._targetInterruptEvent.canTriggerEvent( eventType, pDict ):
			if eventType == csdefine.SKILL_EVENT_INITIATIVE_STOP_BUFF:
				if pDict.get( "eventBuffIndex", 0 ) == buffData.index:
					receiver.removeBuff( buffData.index )
					self.doInterrupt( receiver, buffData )					
			else:
				receiver.removeBuff( buffData.index )
				self.doInterrupt( receiver, buffData )				# 触发中断

	def triggerCasterBuffEvent( self, receiver, eventType, triggerID, buffData, pDict ):
		"""
		virtual member
		触发施法者buff事件
		"""
		if self._casterInterruptEvent.canTriggerEvent( eventType, pDict ):
			if eventType == csdefine.SKILL_EVENT_INITIATIVE_STOP_BUFF:
				if pDict.get( "eventBuffIndex", 0 ) == buffData.index:
					receiver.removeBuff( buffData.index )
					self.doInterrupt( receiver, buffData )					
			else:
				receiver.removeBuff( buffData.index )
				self.doInterrupt( receiver, buffData )				# 触发中断

	def updataExtraTips( self, receiver, buffIndex, valueList ):
		"""
		更新需要显示的Tips Key值随意定 可在客户端ChineseCfg表中定义
		"""
		pass

	def showExtraTips( self, receiver, buffIndex, dictData ):
		"""
		通知客户端显示
		"""
		if receiver.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
			receiver.allClients.AddShowBuffExtraTips(buffIndex,dictData)

	def hideExtraTips( self, receiver, buffIndex ):
		"""
		通知客户端隐藏
		"""
		if receiver.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
			receiver.allClients.RemoveBuffExtraTips(buffIndex)

	def addConflictType(self, conflictType):
		"""
		添加buff冲突类型
		"""
		self._conflictType |= conflictType

	def hasConflictType(self, conflictType):
		"""
		是否有该冲突类型
		"""
		return self._conflictType & conflictType != 0

	def doBuffReplace( self, caster, receiver ):
		"""
		处理buff顶替
		"""
		if self._conflictPriority == csdefine.BUFF_CONFLICT_PRIORITY_NONE or self._conflictType == csdefine.BUFF_CONFLICT_TYPE_NONE:
			return
		for buffData in list(receiver.getAttrBuffs().values()):
			buff = caster.getBuff( buffData.buffID )
			if self._conflictPriority >= buff._conflictPriority and self.hasConflictType(buff._conflictType):
				reason = csdefine.BUFF_END_RESON_BY_INTERRUPT
				if buffData.className == self.__class__.__name__:
					reason = csdefine.BUFF_END_RESON_BY_REPLACE
				receiver.removeBuffByID( buffData.buffID,  reason )

	def canBuffReplace( self, caster, receiver ):
		"""
		是否可以顶替buff
		"""
		if self._conflictPriority == csdefine.BUFF_CONFLICT_PRIORITY_NONE or self._conflictType == csdefine.BUFF_CONFLICT_TYPE_NONE:
			return True
		for buffData in list(receiver.getAttrBuffs().values()):
			buff = caster.getBuff( buffData.buffID )
			if self._conflictPriority < buff._conflictPriority and self.hasConflictType(buff._conflictType):
				return False
		return True

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