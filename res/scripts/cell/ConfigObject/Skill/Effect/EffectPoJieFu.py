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
import KBEngine
from ConfigObject.Skill.Effect.EffectSkillBase import EffectSkillBase
#common
import csdefine



class EffectPoJieFu( EffectSkillBase ):
	"""
	破界符
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
		spaceEntity = receiver.getCurrentSpace()
		if spaceEntity:
			KBEngine.globalData["SpaceLunHuiMiJinMgr"].requestOccupyBuildData( int( spaceEntity.spaceKey ), receiver.groundPosDict )
	



