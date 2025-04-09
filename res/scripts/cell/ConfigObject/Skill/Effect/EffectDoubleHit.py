# -*- coding: utf-8 -*-


from ConfigObject.Skill.Effect.EffectSkillBase import EffectSkillBase
import KBEDebug
import csdefine

class EffectDoubleHit( EffectSkillBase ):
	"""
	连击效果
	"""
	def __init__( self ):
		EffectSkillBase.__init__( self )
		self._times = 1


	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		EffectSkillBase.init( self, dictDat, skill )
		if dictDat["Param1"]:
			self._times = int(dictDat["Param1"])

	def canEffect( self, skill, caster, receiver ):
		"""
		效果添加检测
		"""
		if caster.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
			KBEDebug.ERROR_MSG("EffectDoubleHit only for Role. Please have a check!!!!!!!!! ")
			return False
		return EffectSkillBase.canEffect( self, skill, caster, receiver )

	def onReceive( self, skill, caster, receiver ):
		"""
		效果开始
		"""
		if skill and (skill.getScriptType() == csdefine.SCRIPT_TYPE_BUFF or not skill.isPassiveSkill()):
			caster.onStartDoubleHit(self._times)
			if receiver.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
				receiver.onStartBeDoubleHit()