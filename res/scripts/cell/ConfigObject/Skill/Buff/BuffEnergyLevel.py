# -*- coding: utf-8 -*-
import KBEngine
from ConfigObject.Skill.Buff.BuffLoop import BuffLoop
import csdefine
import math
import KBEDebug
import json

def _Compare( x, y, operation ):
	if operation == 0:
		if x == y:
			return True
		return False
	elif operation == 1:
		if x > y:
			return True
		return False
	elif operation == 2:
		if x < y:
			return True
		return False
	elif operation == 3:
		if x >= y:
			return True
		return False
	elif operation == 4:
		if x <= y:
			return True
		return False
	elif operation == 5:
		if x != y:
			return True
		return False
	return False

class BuffEnergyLevel( BuffLoop ):
	"""
	能级Buff
	"""
	def __init__( self ):
		BuffLoop.__init__( self )
		self._initValue = 0
		self._ceilValue = 0
		self._energyEffect = {}		# {能量下界:[持有效果, 持有效果...]}
		self._respondList = []		# [(原能量值要求类型,数量指标,新能量值要求类型,数量指标,触发技能), ...]
		self._interruptList = ()    # (新能量值要求类型,数量指标)
		self._isLocal = False
		
	def init( self, dictDat ):
		"""
		virtual method;
		读取buff配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		BuffLoop.init( self, dictDat )
		Param1 = dictDat["Param1"].split("|")
		self._initValue = max(int(Param1[0]), 0)
		self._ceilValue = int(Param1[1])

		# 能量下界1;持有效果:持有效果:持有效果…|能量下界2;持有效果:持有效果:持有效果…
		Param2 = dictDat["Param2"].split("|")
		for i in Param2:
			infos = i.split(";")
			holdEffects = [int(j) for j in infos[1].split(":")]
			self._energyEffect[int(infos[0])] = holdEffects

		# 原能量值要求类型;数量指标;新能量值要求类型;数量指标;触发技能|...
		Param3 = dictDat["Param3"].split("|")
		for i in Param3:
			infos = [int(j) for j in i.split(";")]
			self._respondList.append((infos[0], infos[1], infos[2], infos[3], infos[4]))

		# 新能量值要求类型|数量指标
		Param4 = [int(j) for j in dictDat["Param4"].split("|")]
		self._interruptList= (Param4[0], Param4[1])

		# 标记列表（:冒号|竖号分隔，多个代表“且”，留空代表“没有标记”，具体格式与功能由标记定义）
		if dictDat and dictDat["Param5"]:
			Param5 = dictDat["Param5"].split("|")
			for i in Param5:
				List = i.split(":")
				if List[0] == "IsLocal":	# “IsLocal”代表“只有施法者可见”
					self._isLocal = True

	def addBuffCheck( self, caster, receiver ): 
		"""
		添加检测
		"""
		return BuffLoop.addBuffCheck( self, caster, receiver )

	def receiveSuccess( self, caster, receiver ):
		"""
		通过了免疫、替换等等等的拦截，真正要加buff了
		重载掉此方法，叠加buff只增加护盾值和护盾抵挡次数
		"""
		for buffData in list(receiver.getAttrBuffs().values()):
			if buffData.buffID == self.getID() and self._isLocal and buffData.casterID == caster.id:
				receiver.stackBuff( buffData.index )
				receiver.resetBuffEndTime( buffData.index )
				return True
		return BuffLoop.receiveSuccess( self, caster, receiver )

	def doBegin( self, receiver, buffData ):
		"""
		效果开始
		"""
		BuffLoop.doBegin( self, receiver, buffData )
		buffData.setTempData( "EnergyVale", self._initValue )
		self.initialHoldEffect( receiver, self._initValue, buffData)
		self.updataExtraTips(receiver,buffData.index,[buffData.getTempData("EnergyVale", 0)])

	def doEnd( self, receiver, buffData, reason ):
		"""
		效果结束
		"""
		BuffLoop.doEnd( self, receiver, buffData, reason )
		effectIndexs = buffData.getTempData("EffectIndexs", [])
		for i in effectIndexs:
			receiver.removeFixIDHoldEffect(i)
		self.hideExtraTips( receiver, buffData.index )

	def doLoopHit( self, receiver, buffData ):
		"""
		周期打击
		"""
		BuffLoop.doLoopHit( self, receiver, buffData )

	def doStack( self, receiver, buffData ):
		"""
		叠加
		"""
		oldEnergyVale = buffData.getTempData( "EnergyVale")
		newEnergyVale = math.ceil( self._initValue + oldEnergyVale )
		newEnergyVale = max(0, newEnergyVale)
		newEnergyVale = min(self._ceilValue, newEnergyVale)
		buffData.setTempData( "EnergyVale", newEnergyVale )
		self.updataExtraTips(receiver,buffData.index,[buffData.getTempData("EnergyVale", 0)])

		caster = KBEngine.entities.get( buffData.casterID, None )
		self.onChangeEnergy(receiver, caster, oldEnergyVale, newEnergyVale, buffData)

	def registerEvent( self, receiver, buffData ):
		"""
		virtual method
		"""
		BuffLoop.registerEvent( self, receiver, buffData )
		receiver.registerBuffEvent( csdefine.SKILL_EVENT_ADD_ENERGY, buffData.index )
		# 受术者者注册销毁事件
		receiver.registerBuffEvent( csdefine.SKILL_EVENT_DESTROY, buffData.index )
		# 施法者注册传送地图，销毁事件	
		caster = KBEngine.entities.get( buffData.casterID, None )
		if caster:
			caster.registerCasterBuffEvent( csdefine.SKILL_EVENT_SPACE_CHANGE, receiver.id, buffData.index )
			caster.registerCasterBuffEvent( csdefine.SKILL_EVENT_DESTROY, receiver.id, buffData.index )

	def unRegisterEvent( self, receiver, buffData ):
		"""
		virtual method
		"""
		BuffLoop.unRegisterEvent( self, receiver, buffData )
		receiver.unRegisterBuffEvent( csdefine.SKILL_EVENT_ADD_ENERGY, buffData.index )
		# 受术者者注销销毁事件
		receiver.unRegisterBuffEvent( csdefine.SKILL_EVENT_DESTROY, buffData.index )
		# 施法者注销传送地图，销毁事件	
		caster = KBEngine.entities.get( buffData.casterID, None )
		if caster:
			caster.unRegisterCasterBuffEvent( csdefine.SKILL_EVENT_SPACE_CHANGE, receiver.id, buffData.index )
			caster.unRegisterCasterBuffEvent( csdefine.SKILL_EVENT_DESTROY, receiver.id, buffData.index )

	def triggerBuffEvent( self, receiver, eventType, triggerID, buffData, pDict ):
		"""
		virtual member
		触发技能事件
		"""
		if eventType == csdefine.SKILL_EVENT_ADD_ENERGY and self.getID() == pDict.get("EnergyBuffID", 0):
			if not self._isLocal or (self._isLocal and buffData.casterID == triggerID):
				addValue = pDict.get("addValue", 0)
				percent = pDict.get("percent", 0.0)
				isBuffAgainTime = pDict.get("IsBuffAgainTime", False)
				oldEnergyVale = buffData.getTempData( "EnergyVale")
				newEnergyVale = math.ceil( oldEnergyVale * percent + addValue + oldEnergyVale )
				newEnergyVale = max(0, newEnergyVale)
				newEnergyVale = min(self._ceilValue, newEnergyVale)
				buffData.setTempData( "EnergyVale", newEnergyVale )
				self.updataExtraTips(receiver,buffData.index,[buffData.getTempData("EnergyVale", 0)])
				caster = KBEngine.entities.get( buffData.casterID, None )
				self.onChangeEnergy(receiver, caster, oldEnergyVale, newEnergyVale, buffData)
				if isBuffAgainTime:
					self.energyRefreshHoldTime(receiver, buffData)
		# 持有者销毁时，中断Buff
		if eventType in [ csdefine.SKILL_EVENT_DESTROY ]:
			receiver.removeBuff( buffData.index )
			self.doInterrupt( receiver, buffData )				# 触发中断
		BuffLoop.triggerBuffEvent( self, receiver, eventType, triggerID, buffData, pDict )

	def triggerCasterBuffEvent( self, receiver, eventType, triggerID, buffData, pDict ):
		"""
		virtual member
		触发施法者buff事件
		"""
		# 施法者传送地图时，销毁时中断Buff
		if eventType in [ csdefine.SKILL_EVENT_SPACE_CHANGE, csdefine.SKILL_EVENT_DESTROY ]:
			receiver.removeBuff( buffData.index )
			self.doInterrupt( receiver, buffData )		
		BuffLoop.triggerCasterBuffEvent( self, receiver, eventType, triggerID, buffData, pDict )

	def onChangeEnergy(self, receiver, caster, oldEnergyVale, newEnergyVale, buffData):
		"""
		能量改变回调
		"""
		self.respondHoldEffect(receiver, oldEnergyVale, newEnergyVale, buffData)
		self.respondInterruptBuff(receiver, newEnergyVale, buffData)
		if caster:
			self.respondEnergySkill(receiver, caster, oldEnergyVale, newEnergyVale)

	def initialHoldEffect(self, receiver, initEnergyVale, buffData):
		"""
		"""
		EnergyList = sorted(self._energyEffect)
		addList = []
		for index, i in enumerate(EnergyList):
			if initEnergyVale >= i and initEnergyVale < EnergyList[index+1]:
				addList = self._energyEffect[i]
		if not addList:
			return
		removeList = buffData.getTempData("EffectIndexs", [])
		for i in removeList:
			receiver.removeFixIDHoldEffect(i)

		EffectIndexs = []
		for i in addList:
			index = receiver.addFixIDHoldEffect(i, receiver)
			EffectIndexs.append(index)
		buffData.setTempData("EffectIndexs", EffectIndexs)

	def respondHoldEffect(self, receiver, oldEnergyVale, newEnergyVale, buffData):
		"""
		能量改变添加持有效果
		"""
		EnergyList = sorted(self._energyEffect)
		addList = []
		# 能量值＜第一个下界时，没有持有效果
		# 能量递增
		if newEnergyVale > oldEnergyVale:
			for i in EnergyList:
				if i>oldEnergyVale and i <= newEnergyVale:
					addList = self._energyEffect[i]
		elif newEnergyVale < oldEnergyVale:  # 能量递减
			for i in EnergyList:
				if i>= newEnergyVale and i < oldEnergyVale:
					addList = self._energyEffect[i]

		if not addList:
			return
		removeList = buffData.getTempData("EffectIndexs", [])
		for i in removeList:
			receiver.removeFixIDHoldEffect(i)

		EffectIndexs = []
		for i in addList:
			index = receiver.addFixIDHoldEffect(i, receiver)
			EffectIndexs.append(index)
		buffData.setTempData("EffectIndexs", EffectIndexs)

	def respondEnergySkill(self, receiver, caster, oldEnergyVale, newEnergyVale):
		"""
		触发响应技能
		"""
		for i in self._respondList:
			if _Compare(oldEnergyVale, i[1], i[0]) and _Compare(newEnergyVale, i[3], i[2]):
				caster.useSkillToEntity( i[4], receiver.id)

	def respondInterruptBuff(self, receiver, newEnergyVale, buffData):
		"""
		能量值满足条件中断buff
		"""
		if _Compare(newEnergyVale, self._interruptList[1], self._interruptList[0]):
			receiver.removeBuff( buffData.index )
			self.doInterrupt( receiver, buffData )				# 触发中断

	def energyRefreshHoldTime(self, receiver, buffData):
		"""
		刷新buff的持续时间
		"""
		receiver.resetBuffEndTime( buffData.index )

	def updataExtraTips( self, receiver, buffIndex, valueList ):
		"""
		添加需要显示的Tips  Key值随意定 可在客户端ChineseCfg表中定义
		"""
		BuffLoop.updataExtraTips( self, receiver, buffIndex, valueList )
		tempDict = {}
		if len(valueList) == 1:
			tempDict["BuffEnergyValue"] = valueList[0]
			tempDict["BuffEnergyCeilValue"] = self._ceilValue
		self.showExtraTips( receiver, buffIndex, json.dumps(tempDict) )
