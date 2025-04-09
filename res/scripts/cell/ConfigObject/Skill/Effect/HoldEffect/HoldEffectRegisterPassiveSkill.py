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


class HoldEffectRegisterPassiveSkill( HoldEffect ):
	"""
	持有效果：注册被动技能
	"""
	def __init__( self ):
		HoldEffect.__init__( self )
		self._passiveSkillIdList = []
	
	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		HoldEffect.init( self, dictDat, skill )
		if dictDat["Param1"]:
			passiveSkillIdList = dictDat["Param1"].split("|")
			for passiveSkillID in passiveSkillIdList:
				self._passiveSkillIdList.append(int(passiveSkillID))

	def onBegin( self, effectData, receiver ):
		"""
		效果开始
		"""
		HoldEffect.onBegin( self, effectData, receiver )
		for passiveSkillID in self._passiveSkillIdList:
			skillInst = receiver.getSkill(passiveSkillID)
			if skillInst and skillInst.isPassiveSkill():
				skillInst.attachToCaster(receiver)
			else:
				KBEDebug.ERROR_MSG("skill's HoldEffect config is error, skill(%d) is not passive skill!!" % passiveSkillID)

	def onEnd( self, effectData, receiver ):
		"""
		效果结束
		"""
		for passiveSkillID in self._passiveSkillIdList:
			skillInst = receiver.getSkill(passiveSkillID)
			if skillInst and skillInst.isPassiveSkill():
				skillInst.detachToCaster(receiver)
		HoldEffect.onEnd(self, effectData, receiver)


