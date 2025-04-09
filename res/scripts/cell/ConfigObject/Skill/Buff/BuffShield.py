# -*- coding: utf-8 -*-

import KBEngine
import KBEDebug
import csdefine
import ItemTypeEnum
from ConfigObject.Skill.Buff.BuffHold import BuffHold
import json

class BuffShield( BuffHold ):
	"""
	护盾Buff
	"""
	def __init__( self ):
		BuffHold.__init__( self )
		self.damageType = []			#伤害类型列表
		self.reduceDamageRatio = 0.0 	#伤害抵扣率
		self.reduceDamageValue = 0.0	#伤害抵扣固定值
		self.shieldValue = 0			#护盾值
		self.shieldPercent = 0.0		#护盾值百分比
		self.shieldValueMaxRatio = 1	#护盾最上限
		self._triggerSkillId = 0		#破盾后释放技能
		self.shieldCount = -1			#护盾抵挡次数 小于0表示不限制次数 0或者1 都可以抵挡1次
		self.shieldCountMax = -1		#护盾抵挡次数上限 小于0表示不限制次数
		self.shieldCountMin = 1			#护盾抵挡次数下限

	def init( self, dictDat ):
		"""
		virtual method;
		读取buff配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		BuffHold.init( self, dictDat )
		self.damageType = [2**int(i) for i in dictDat["Param1"].split("|")]

		if dictDat["Param2"]:
			Param2 = dictDat["Param2"].split("|")
			if len(Param2) > 0:
				self.shieldPercent = float(Param2[0])
			if len(Param2) > 1:		
				self.shieldValue = int(Param2[1])
			if len(Param2) > 2:
				self.shieldValueMaxRatio = float(Param2[2]) if float(Param2[2]) >1.0 else 1.0

		Param3 = dictDat["Param3"].split("|")
		self.reduceDamageRatio = float( Param3[0] ) if Param3[0] else 0.0
		if len(Param3) > 1:
			self.reduceDamageValue = float(Param3[1])
		#self.shieldCount = int(dictDat["Param4"]) if len( dictDat["Param4"] ) > 0 else -1
		Param4 = dictDat["Param4"].split("|")
		self.shieldCount = int(Param4[0]) if Param4[0] else -1
		if len(Param4) > 1:
			self.shieldCountMax = int(Param4[1])
		if self.shieldCountMax < 0:
			self.shieldCountMin = self.shieldCountMax
			self.shieldCountMax = ItemTypeEnum.MAXLIMITVALUE
		self._triggerSkillId = int( dictDat["Param5"] ) if len( dictDat["Param5"] ) > 0 else 0
		if self.shieldCount == 0:
			self.shieldCount = 1

	def receiveSuccess( self, caster, receiver ):
		"""
		通过了免疫、替换等等等的拦截，真正要加buff了
		重载掉此方法，叠加buff只增加护盾值和护盾抵挡次数
		"""
		for buffData in receiver.getAttrBuffs().values():
			if buffData.buffID == self.getID():				#只叠加第一个找到的buff，理论上也只会有一个
				receiver.stackBuff( buffData.index )
				receiver.resetBuffEndTime( buffData.index )
				return True
		return BuffHold.receiveSuccess( self, caster, receiver )

	def registerEvent( self, receiver, buffData ):
		"""
		virtual method
		"""
		BuffHold.registerEvent( self, receiver, buffData )
		receiver.registerBuffEvent( csdefine.SKILL_EVENT_SHIELD_BROKEN, buffData.index )

	def unRegisterEvent( self, receiver, buffData ):
		"""
		virtual method
		"""
		BuffHold.unRegisterEvent( self, receiver, buffData )
		receiver.unRegisterBuffEvent( csdefine.SKILL_EVENT_SHIELD_BROKEN, buffData.index )

	def triggerBuffEvent( self, receiver, eventType, triggerID, buffData, pDict ):
		"""
		virtual member
		触发技能事件
		"""
		if eventType == csdefine.SKILL_EVENT_SHIELD_BROKEN:
			buffIndex = pDict.get( "buffIndex", 0 )
			if buffIndex == buffData.index:
				receiver.removeBuff(buffIndex)
				receiver.useSkillToEntity( self._triggerSkillId,triggerID )
		BuffHold.triggerBuffEvent( self, receiver, eventType, triggerID, buffData, pDict )

	def doBegin( self, receiver, buffData ):
		"""
		效果开始
		"""
		BuffHold.doBegin( self, receiver, buffData )
		buffData.setTempData("DamgeType",self.damageType)
		buffData.setTempData("ReduceDamageRatio",self.reduceDamageRatio)
		buffData.setTempData("reduceDamageValue",self.reduceDamageValue)

		shieldValue = self.shieldValue + int(receiver.HP_Max * self.shieldPercent)
		shieldValueMax = int(shieldValue * self.shieldValueMaxRatio)
		shieldValueMin = shieldValueMax if shieldValueMax<0 else 0    # 护盾上限＜0时, 下限＝上限＜0
		shieldCount = self.shieldCount
		shieldValue = max(shieldValue, shieldValueMin)
		shieldValue = min(shieldValue, shieldValueMax) 
		shieldCount = max(shieldCount, self.shieldCountMin)
		shieldCount = min(shieldCount, self.shieldCountMax)
		buffData.setTempData("ShieldValue",shieldValue)
		buffData.setTempData("ShieldCount",shieldCount)
		self.updataExtraTips(receiver,buffData.index,[self.shieldValue,self.shieldCount])

	def updataExtraTips( self, receiver, buffIndex, valueList ):
		"""
		添加需要显示的Tips  Key值随意定 可在客户端ChineseCfg表中定义
		"""
		BuffHold.updataExtraTips( self, receiver, buffIndex, valueList )
		tempDict = {}
		if len(valueList) == 2:
			tempDict["ShieldValue"] = valueList[0]
			tempDict["ShieldCount"] = valueList[1]
		self.showExtraTips( receiver, buffIndex, json.dumps(tempDict) )

	def doReload( self, receiver, buffData ):
		"""
		上线重新加载buff
		"""
		BuffHold.doReload( self, receiver, buffData )
		buffData.setTempData("DamgeType",self.damageType)
		buffData.setTempData("ReduceDamageRatio",self.reduceDamageRatio)
		buffData.setTempData("reduceDamageValue", self.reduceDamageValue)
		buffData.setTempData("ShieldValue",buffData.getTempData("ShieldValue"))
		buffData.setTempData("ShieldCount",buffData.getTempData("ShieldCount"))
		self.updataExtraTips(receiver,buffData.index,[buffData.getTempData("ShieldValue"),buffData.getTempData("ShieldCount")])

	def doEnd( self, receiver, buffData, reason ):
		"""
		效果结束
		"""
		BuffHold.doEnd( self, receiver, buffData, reason )
		self.hideExtraTips( receiver, buffData.index )

	def doStack( self, receiver, buffData ):
		"""
		叠加
		"""
		shieldValue = self.shieldValue + int(receiver.HP_Max * self.shieldPercent)
		shieldValueMax = int(shieldValue * self.shieldValueMaxRatio)
		shieldValueMin = shieldValueMax if shieldValueMax<0 else 0	# 护盾上限＜0时, 下限＝上限＜0
		shieldValue += buffData.getTempData("ShieldValue")	#护盾值
		shieldCount = buffData.getTempData("ShieldCount")	#护盾抵挡次数
		shieldCount += self.shieldCount
		shieldValue = max(shieldValue, shieldValueMin)
		shieldValue = min(shieldValue, shieldValueMax)
		shieldCount = max(shieldCount, self.shieldCountMin)
		shieldCount = min(shieldCount, self.shieldCountMax)
		buffData.setTempData("ShieldValue",shieldValue)
		buffData.setTempData("ShieldCount",shieldCount)
		self.updataExtraTips(receiver,buffData.index,[shieldValue, shieldCount])
