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

class EffectForcedJump( EffectSkillBase ):
	"""
	技能效果“受迫跳跃”
	"""
	def __init__( self ):
		EffectSkillBase.__init__( self )
		self._height  = 0.0

	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		EffectSkillBase.init( self, dictDat, skill )
		if dictDat["Param1"]:
			self._height = float(dictDat["Param1"])*100

	def canEffect( self, skill, caster, receiver ):
		"""
		效果添加检测
		"""
		if not receiver.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:	#只支持对玩家使用
			return False
		return EffectSkillBase.canEffect( self, skill, caster, receiver )

	def onReceive( self, skill, caster, receiver ):
		"""
		效果开始
		"""
		receiver.client.CLIENT_ForcedJump(self._height)