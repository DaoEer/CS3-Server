# -*- coding: utf-8 -*-


"""
usage:
	战斗技能类

attribute:
	pass

member function:
	pass

callback:
	pass

"""


#cell
import ConfigObject.Skill.SkillBase.Skill as Skill
#common
import csdefine
import KBEDebug


class CombatSkill( Skill.Skill ):
	"""
	"""
	def __init__( self ):
		Skill.Skill.__init__( self )
		self._isShowIntonateUI = False							# 顯示吟唱條界面
		self._intonateName = ""									# 吟唱名字
		self._iconName = "" 									# 图标
		
	def init( self, dictDat ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		self._isInstantSkill = False
		Skill.Skill.init( self, dictDat )
		self._isShowIntonateUI = dictDat["ShowIntonate"]
		self._intonateName = dictDat["IntonateName"]
		iconName = dictDat["SkillIcon"].strip().split(".")
		if len(iconName)>1:
			self._iconName = iconName[len(iconName)-1]    #"SkillIcon": "/Game/Textures/Icons/T_Icon_2258_D.T_Icon_2258_D", 只需要T_Icon_2258_D这部分 暂时用技能图标

	

	def onSkillBegin( self, caster, target ):
		"""
		virtual method
		技能开始
		"""
		if caster.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ) and self._isShowIntonateUI:
			caster.intonateSpell( self.getSkillTotalTime(), self.getID() )

		if caster.isEntityFlag( csdefine.ENTITY_FLAG_MONSTER ) and self._isShowIntonateUI:
			caster.allClients.OnShowIntonateBar(caster.id , self.getSkillTotalTime(), self.getID())

		Skill.Skill.onSkillBegin( self, caster, target )
		
	def onSkillEnd( self, caster, target, castResult ):
		"""
		virtual method.
		技能结束
		"""
		if caster.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ) and self._isShowIntonateUI:
			caster.intonateSpellOver()

		if caster.isEntityFlag( csdefine.ENTITY_FLAG_MONSTER ) and self._isShowIntonateUI:
			caster.allClients.OnHideIntonateBar(caster.id )

			
		Skill.Skill.onSkillEnd( self, caster, target, castResult )