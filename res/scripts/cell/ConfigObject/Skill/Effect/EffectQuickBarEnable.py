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
#common
import csdefine



class EffectQuickBarEnable( EffectSkillBase ):
	"""
	设置界面快捷栏是否可用（0、1、2、3...9）
	"""
	def __init__( self ):
		EffectSkillBase.__init__( self )
		self._isAble = 0
	
	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		EffectSkillBase.init( self, dictDat, skill )
		self._isAble = int( dictDat["Param1"] )

	def onReceive( self, skill, caster, receiver ):
		"""
		效果开始
		"""
		if receiver.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ) and receiver.client:
			receiver.client.SetIsEnabledQuickBar( self._isAble )



