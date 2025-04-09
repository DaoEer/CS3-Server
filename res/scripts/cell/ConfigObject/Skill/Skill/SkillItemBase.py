# -*- coding: utf-8 -*-

import Math
import csdefine
import csstatus
from ConfigObject.Skill.SkillBase.Skill import Skill


class SkillItemBase( Skill ):
	"""
	物品技能基类
	"""
	def __init__( self ):
		Skill.__init__( self )
