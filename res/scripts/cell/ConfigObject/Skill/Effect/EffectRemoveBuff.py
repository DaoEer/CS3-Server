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


#cell
from ConfigObject.Skill.Effect.EffectSkillBase import EffectSkillBase
import KBEDebug
#common
import csdefine

class EffectRemoveBuff( EffectSkillBase ):
	"""
	移除buff效果（可扩展多种移除方式）
	"""
	def __init__( self ):
		EffectSkillBase.__init__( self )
		#self._type = 0（通过ID移除，通过效果移除..）
		self._buffIdList = []

	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		EffectSkillBase.init( self, dictDat, skill )
		if not dictDat["Param1"]:
			KBEDebug.ERROR_MSG("Skill EffectRemoveBuff config is none! SkillID=%s" % skill.getID())
		buffList = dictDat["Param1"].split("|")
		if len(buffList) != len(set(buffList)):
			KBEDebug.ERROR_MSG("Skill EffectRemoveBuff has duplicate configuration! SkillID=%s" % skill.getID())
		for buffID in buffList:
			self._buffIdList.append(int(buffID))

	def onReceive( self, skill, caster, receiver ):
		"""
		效果开始
		"""
		for buffID in self._buffIdList:
			receiver.removeBuffByID(buffID)


