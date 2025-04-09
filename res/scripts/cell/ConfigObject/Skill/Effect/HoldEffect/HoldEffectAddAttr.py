# -*- coding: utf-8 -*-


"""
usage:
	Buff持有效果,onBegin 和 onEnd 必须成对存在，分别做buff添加和删除，增添的效果

attribute:
	pass

member function:
	pass

callback:
	pass

"""


#cell
from ConfigObject.Skill.Effect.HoldEffect.HoldEffect import HoldEffect
#common
import csdefine
import KBEDebug
import ItemTypeEnum



class HoldEffectAddAttr( HoldEffect ):
	"""
	战斗属性 增益/减损 效果
	"""
	def __init__( self ):
		HoldEffect.__init__( self )
		self._propertiesList = []
		self._attrPercent = 0						# 百分比
		self._attrValue = 0							#
	
	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		HoldEffect.init( self, dictDat, skill )
		if not dictDat["Param1"]:
			KBEDebug.ERROR_MSG("Skill HoldEffectAddAttr config is none! SkillID=%s" % skill.getID())
		propertiesList = dictDat["Param1"].split("|")
		if len(propertiesList) != len(set(propertiesList)):
			KBEDebug.ERROR_MSG("Skill HoldEffectAddAttr has duplicate configuration! SkillID=%s" % skill.getID())
		for properties in propertiesList:
			self._propertiesList.append(int(properties))
		if dictDat["Param2"]:
			self._attrPercent = int(float(dictDat["Param2"]) * ItemTypeEnum.PRECENTRATIO)
		if dictDat["Param3"]:
			self._attrValue = int(dictDat["Param3"])


	def onBegin( self, effectData, receiver ):
		"""
		效果开始
		"""
		HoldEffect.onBegin( self, effectData, receiver )
		for properties in self._propertiesList:
			if properties in ItemTypeEnum.PROPERTYIDTOSTR:
				temp = {}
				if self._attrPercent:
					# attrProperty = ItemTypeEnum.PROPERTYIDTOSTR[self._properties] + "_percent"
					# temp[attrProperty] = self._attrPercent
					temp.update({"_percent": {properties: self._attrPercent}})
				if self._attrValue:
					# attrProperty = ItemTypeEnum.PROPERTYIDTOSTR[self._properties] + "_value"
					# temp[attrProperty] = self._attrValue
					temp.update({"_value": {properties: self._attrValue}})

				receiver.setBuffProperties(temp)
				receiver.calcAttachProperties()
			else:
				KBEDebug.ERROR_MSG("entity(id:%d) receive HoldEffect add attr(num:%d) error!!(id:%d)" % (receiver.id, properties, effectData.index))

	def onEnd( self, effectData, receiver ):
		"""
		效果结束
		"""
		for properties in self._propertiesList:
			if properties in ItemTypeEnum.PROPERTYIDTOSTR:
				temp = {}
				if self._attrPercent:
					temp.update({"_percent": {properties: 0 - self._attrPercent}})
				# attrProperty = ItemTypeEnum.PROPERTYIDTOSTR[self._properties] + "_percent"
				# temp[attrProperty] = -self._attrPercent
				if self._attrValue:
					# attrProperty = ItemTypeEnum.PROPERTYIDTOSTR[self._properties] + "_value"
					# temp[attrProperty] = -self._attrValue
					temp.update({"_value": {properties: 0 - self._attrValue}})

				receiver.setBuffProperties(temp)
				receiver.calcAttachProperties()
		HoldEffect.onEnd(self, effectData, receiver)


