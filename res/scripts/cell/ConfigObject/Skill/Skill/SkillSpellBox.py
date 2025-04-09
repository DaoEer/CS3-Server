# -*- coding: utf-8 -*-


"""
usage:
	SpellBox技能类

attribute:
	pass

member function:
	pass

callback:
	pass

"""


#cell
import ConfigObject.Skill.SkillBase.CombatSkill as CombatSkill
#common
import csdefine
import KBEDebug


class SkillSpellBox( CombatSkill.CombatSkill ):
	"""
	"""
	def __init__( self ):
		CombatSkill.CombatSkill.__init__( self )
		
	def init( self, dictDat ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		CombatSkill.CombatSkill.init( self, dictDat )
		
		if not self._targetType == csdefine.SKILL_CAST_OBJECT_TYPE_ENTITY:
			KBEDebug.ERROR_MSG("skill(id:%d) target type(%s) is err!should be 'TargetLock'!"%( self._id, self._targetType) )

	def onSkillBegin( self, caster, target ):
		"""
		virtual method
		技能开始
		"""
		target.getObject().notify_OtherClientForbidInteractive(caster.id)
		CombatSkill.CombatSkill.onSkillBegin( self, caster, target )

	def interrupt( self, caster, reason, target = None ):
		"""
		virtual method
		技能中断
		"""
		CombatSkill.CombatSkill.interrupt( self, caster, reason, target )
		if target:
			target.allClients.CLIENT_SpellBoxInterrupted()
		
	def onSkillEnd( self, caster, target, castResult ):
		"""
		virtual method.
		技能结束
		"""
		CombatSkill.CombatSkill.onSkillEnd( self, caster, target, castResult )
		if castResult and target.getObject():
			spellbox = target.getObject()
			if hasattr( spellbox, "onPlayerIntonateOver" ):
				spellbox.onPlayerIntonateOver( caster.id )