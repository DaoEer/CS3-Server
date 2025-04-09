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
from ConfigObject.Skill.EffectLoader import g_effects
#common
import csdefine
import KBEDebug



class EffectAddFixIDEffect( EffectSkillBase ):
	"""
	根据ID获取相关的技能效果
	"""
	def __init__( self ):
		EffectSkillBase.__init__( self )
		self._effectType = csdefine.SKILL_EFFECT_TYPE_POSITIVE
		self._effectID = 0
		self._maxStackLayer = 1
	
	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		EffectSkillBase.init( self, dictDat, skill )
		self._effectType = int( dictDat["Param1"] )
		self._effectID = int( dictDat["Param2"] )
		if dictDat["Param3"]:
			self._maxStackLayer = int( dictDat["Param3"] )
		mapEffect = g_effects.getEffect(self._effectID)
		if mapEffect is None:
			KBEDebug.ERROR_MSG( "Effect script(EffectAddFixIDEffect) can't find the effectID(%d)!"%self._effectID )
			return
		if mapEffect.__module__ in ["EffectAddFixIDEffect", "HoldEffectAddFixIDEffect"]:
			KBEDebug.ERROR_MSG( "Effect(%d) script(EffectAddFixIDEffect) can't add %s again!"%(self._effectID, mapEffect.__module__ ) )

	def onReceive( self, skill, caster, receiver ):
		"""
		效果开始
		"""
		mapEffect = g_effects.getEffect(self._effectID)
		if mapEffect:
			caster,receiver = self.changeForEffectType( caster, receiver )
			for i in range(self._maxStackLayer):
				if mapEffect.canEffect( skill, caster, receiver ):
					mapEffect.onReceive( skill, caster, receiver )
		else:
			KBEDebug.ERROR_MSG( "Skill(%i) effect script(EffectAddFixIDEffect) can't find the effectID(%d)!"%(skill.getID(), self._effectID) )

	def changeForEffectType( self, caster, receiver ):
		"""
		通过作用类型改变技能效果
		"""
		if self._effectType == csdefine.SKILL_EFFECT_TYPE_POSITIVE:					# 正作用
			return caster,receiver
		elif self._effectType == csdefine.SKILL_EFFECT_TYPE_REACTION:				# 反作用
			return receiver,caster
		elif self._effectType == csdefine.SKILL_EFFECT_TYPE_DIDE:					# 副作用
			return caster,caster
		elif self._effectType == csdefine.SKILL_EFFECT_TYPE_CATALYSIS:				# 催化作用
			return receiver,receiver
		else:
			return caster,receiver
		
