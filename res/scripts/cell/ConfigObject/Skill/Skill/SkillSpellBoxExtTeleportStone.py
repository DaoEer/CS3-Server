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
import ConfigObject.Skill.Skill.SkillSpellBox as SkillSpellBox
#common
import csdefine
import KBEDebug
import KBEngine


class SkillSpellBoxExtTeleportStone( SkillSpellBox.SkillSpellBox ):
	"""
	传送石
	"""
	def __init__( self ):
		SkillSpellBox.SkillSpellBox.__init__( self )
		
	def init( self, dictDat ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		SkillSpellBox.SkillSpellBox.init( self, dictDat )
		

	def onSkillBegin( self, caster, target ):
		"""
		virtual method
		技能开始
		"""
		SkillSpellBox.SkillSpellBox.onSkillBegin(self, caster, target)
		
		for mb in caster.getAllTeamMemberMB():
			if mb.id == caster.id:
				continue
			entity = KBEngine.entities.get( mb.id, None )
			if not entity or entity.spaceID != caster.spaceID:
				continue
			entity.addTimerCallBack(1.0,"roleTeamSpellBoxFollow",(caster.id, self.getSkillTotalTime()-1.0))#策划希望队友一秒后再收到弹窗
	
		
	def onSkillEnd( self, caster, target, castResult ):
		"""
		virtual method.
		技能结束
		"""	
		if castResult and target.getObject():
			spellbox = target.getObject()
			if hasattr( spellbox, "onPlayerIntonateOver" ):
				spellbox.onPlayerIntonateOver( caster.id )		
		SkillSpellBox.SkillSpellBox.onSkillEnd(self, caster, target, castResult )
	