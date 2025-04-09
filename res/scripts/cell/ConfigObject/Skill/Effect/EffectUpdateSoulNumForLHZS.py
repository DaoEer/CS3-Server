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

import math
#cell
from ConfigObject.Skill.Effect.EffectSkillBase import EffectSkillBase

#common
import csdefine



class EffectUpdateSoulNumForLHZS( EffectSkillBase ):
	"""
	更新灵魂能量槽 --灵魂之誓副本
	"""
	def __init__( self ):
		EffectSkillBase.__init__( self )
	
	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		EffectSkillBase.init( self, dictDat, skill )



	def onReceive( self, skill, caster, receiver ):
		"""
		效果开始
		"""
		if receiver.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
			return
		from SpaceCopyLingHunZhiShi import SpaceCopyLingHunZhiShi as SpaceCopyLingHunZhiShi
		spaceEntity = caster.getCurrentSpace()
		if not isinstance(spaceEntity, SpaceCopyLingHunZhiShi):
			return
		spaceEntity.addSoulNum(receiver)
		

