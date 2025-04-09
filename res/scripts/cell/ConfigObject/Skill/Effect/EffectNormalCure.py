# -*- coding: utf-8 -*-


"""
usage:
	效果

attribute:
	pass

member function:
	pass

callback:
	pass

"""

import math
#cell
from ConfigObject.Skill.Effect.EffectSkillBase import EffectSkillBase
#common
import csdefine
import KBEDebug
import ItemTypeEnum


class EffectNormalCure( EffectSkillBase ):
	"""
	标准治疗 CST-10638
	"""
	def __init__( self ):
		EffectSkillBase.__init__( self )
		self._addValue = 0
		self._percent = 0.0
		self._isSkipEvent = False
		self._customAttrC = {}					# 施法者属性修正列表
		self._customAttrR = {}					# 受术者属性修正列表
	
	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		EffectSkillBase.init( self, dictDat, skill )

		# 治疗百分比（如“0.5”代表“50%HP上限治疗”）|固定值（整型）
		if dictDat["Param1"]:
			Param1 = dictDat["Param1"].split("|")
			self._percent = max(0.0, float(Param1[0]))
			if len(Param1) > 1:
				self._addValue = max(0, int(Param1[1]))
				
		# 标记列表（:冒号|竖号分隔，多个代表“且”，留空代表“没有标记”，具体格式与功能由标记定义）		
		if dictDat["Param2"]:
			Param2 = dictDat["Param2"].split("|")
			for i in Param2:
				List = i.split(":")
				if List[0] == "IsReAttrC":		# “IsReAttrC:30008:50”代表“施法者物攻校正＋50”
					propertyStr = ItemTypeEnum.PROPERTYIDTOSTR[int(List[1])]
					self._customAttrC[propertyStr]  = int(List[2])
				elif List[0] == "IsReAttrR":	# “IsReAttrR:30010:-50”代表“受术者物防校正－50”
					propertyStr = ItemTypeEnum.PROPERTYIDTOSTR[int(List[1])]
					self._customAttrR[propertyStr] = int(List[2])
				elif List[0] == "IsSkipEvent":	# “IsSkipEvent”代表“需要跳过事件触发”
					self._isSkipEvent = True
				else:
					KBEDebug.ERROR_MSG("EffectAddHP: %s is not a correct tag name "%List[0])
	
	def canEffect( self, skill, caster, receiver ):
		"""
		效果添加检测
		"""
		if receiver.isState( csdefine.ENTITY_STATE_DEAD ):
			return False
		return EffectSkillBase.canEffect( self, skill, caster, receiver )

	def onReceive( self, skill, caster, receiver ):
		"""
		效果开始
		"""
		cure = self.CustomAttrC("cure", caster.cure)
		curecorrection = self.CustomAttrC("curecorrection", caster.curecorrection)
		becuredcorrection = self.CustomAttrR("becuredcorrection",  receiver.becuredcorrection)
		value = cure * self._percent + self._addValue
		value *= curecorrection/ItemTypeEnum.PRECENTRATIO
		value *= becuredcorrection/ItemTypeEnum.PRECENTRATIO
		_value = math.ceil(value)
		value = math.ceil(receiver.HP + value)
		value = max(0, value)
		receiver.setHP( value )
		if receiver.id != caster.id and receiver.queryRelation( caster ) == csdefine.COMBAT_RELATION_NORMAL:
			receiver.addRelatedHatred(caster.id, _value)
		if skill and (skill.getScriptType() == csdefine.SCRIPT_TYPE_BUFF or not skill.isPassiveSkill()):
			if not self._isSkipEvent:
				caster.triggerSkillEvent( csdefine.SKILL_EVENT_CURE, receiver.id, { "actForbid": self._actForbid, "type" : csdefine.SKILL_EVENT_CASTER_CURE } )
				receiver.triggerSkillEvent( csdefine.SKILL_EVENT_CURE, caster.id, { "actForbid": self._actForbid, "type" : csdefine.SKILL_EVENT_RECEIVER_CURE } )
				if caster.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE and caster != receiver and caster.queryRelation( receiver ) == csdefine.COMBAT_RELATION_NORMAL:
					caster.onStartDoubleHit()
				if receiver.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE and caster != receiver and caster.queryRelation( receiver ) == csdefine.COMBAT_RELATION_NORMAL:
					receiver.onStartBeDoubleHit()

	def CustomAttrC(self, propertyStr, propertyValue):
		if propertyStr in self._customAttrC:
			propertyValue += self._customAttrC[propertyStr]
		propertyValue = max(propertyValue, 0)
		return propertyValue

	def CustomAttrR(self, propertyStr, propertyValue):
		if propertyStr in self._customAttrR:
			propertyValue += self._customAttrR[propertyStr]
		propertyValue = max(propertyValue, 0)	
		return propertyValue