# -*- coding: utf-8 -*-

import Math
import math
import csdefine
import csstatus
import KBEDebug
import KBEngine
import csarithmetic
import KBEMath
from ConfigObject.Skill.SkillBase.CombatSkill import CombatSkill


class SkillSoldierCmdBase( CombatSkill ):
	"""
	士兵指令技能脚本基类
	"""
	def __init__( self ):
		CombatSkill.__init__( self )
		self.soldierSkillID    = 0	#士兵技能ID
		

	def init( self, dictDat ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		CombatSkill.init( self, dictDat )
		if dictDat["Param1"]:
			self.soldierSkillID = int( dictDat["Param1"] )


	def useableCheck( self, caster, target ):
		"""
		检查技能是否可以使用
		"""
		if caster.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
			return False
		return CombatSkill.useableCheck( self, caster, target )

	def cast( self, caster, target ):
		"""
		施放技能
		"""
		CombatSkill.cast( self, caster, target )	

	
	def onSkillEnd( self, caster, target, castResult ):
		"""
		virtual method.
		技能结束
		"""
		CombatSkill.onSkillEnd( self, caster, target, castResult )
		