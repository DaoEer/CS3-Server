# -*- coding: utf-8 -*-


"""
usage:
	Buff持有效果基类,onBegin 和 onEnd 必须成对存在，分别做buff添加和删除，增添的效果

attribute:
	pass

member function:
	pass

callback:
	pass

"""

import KBEDebug
import HoldEffectDataType
#data
import Skill.SkillReceiverDefine as SkillReceiverDefine
import Skill.SkillCasterDefine as SkillCasterDefine


class HoldEffect():
	"""
	Buff持有效果基类（开始和结束对应）
	"""
	def __init__( self ):
		pass
	
	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		pass

	def getNewEffectData( self, caster, receiver ):
		"""
		virtual method
		生成持有效果数据
		"""
		effectData = HoldEffectDataType.HoldEffectDataType()
		return effectData
		
	def canEffect( self, caster, receiver ):
		"""
		效果添加检测
		"""
		effectName = self.__class__.__name__
		if effectName in SkillReceiverDefine.Datas:
			flag = receiver.getEntityFlag()
			if flag in SkillReceiverDefine.Datas[effectName]:
				if not SkillReceiverDefine.Datas[effectName][flag]:
					KBEDebug.WARNING_MSG( "receiver(type:%d) in skill effectName(%s) is limit(SkillReceiverDefine)!!"%(flag,effectName) )
				return SkillReceiverDefine.Datas[effectName][flag]

		if effectName in SkillCasterDefine.Datas:
			_flag = caster.getEntityFlag()
			if _flag in SkillCasterDefine.Datas[effectName]:
				if not SkillCasterDefine.Datas[effectName][_flag]:
					KBEDebug.WARNING_MSG( "caster(type:%d) in skill effectName(%s) is limit(SkillCasterDefine)!!"%(_flag,effectName) )
				return SkillCasterDefine.Datas[effectName][_flag]

		return True

	def onBegin( self, effectData, receiver ):
		"""
		效果开始
		"""
		receiver.addPerSecondEvent()

	def onEnd( self, effectData, receiver ):
		"""
		效果结束
		"""
		receiver.removePerSecondEvent()

	def onClientActorCreate( self, effectData, receiver, srcEntityID ):
		"""
		virtual method
		receiver在某客户端被创建出来
		"""
		pass


