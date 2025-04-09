# -*- coding: utf-8 -*-

import Math
import math
import csdefine
import csstatus
import KBEDebug
import KBEngine
import csarithmetic
import KBEMath
from ConfigObject.Skill.Skill.SkillSoldierCmdBase import SkillSoldierCmdBase

class SkillSoldierCmdUseSkillToSelf(SkillSoldierCmdBase):
	"""
	对自身使用技能
	"""
	def __init__( self ):
		SkillSoldierCmdBase.__init__( self )
		self.soldierSkillID    = 0	#士兵技能ID
		

	def init( self, dictDat ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		SkillSoldierCmdBase.init( self, dictDat )
		if dictDat["Param1"]:
			self.soldierSkillID = int( dictDat["Param1"] )


	def cast( self, caster, target ):
		"""
		施放技能
		"""
		SkillSoldierCmdBase.cast( self, caster, target )	
		caster.roleCmdUseSkillToSelf(self.soldierSkillID)
		
	
