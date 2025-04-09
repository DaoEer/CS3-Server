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

import KBEDebug

class EffectAddBuff( EffectSkillBase ):
	"""
	添加buff效果
	"""
	def __init__( self ):
		EffectSkillBase.__init__( self )
		self._buffID = 0
	
	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		EffectSkillBase.init( self, dictDat, skill )
		if dictDat["Param1"] == "":
			KBEDebug.CRITICAL_MSG( "skillID: %s Buffer config error!! ( %s )"%( skill._id, str( dictDat ), ) )
			return
		self._buffID = int( dictDat["Param1"] )

	def onReceive( self, skill, caster, receiver ):
		"""
		效果开始
		"""
		receiver.addBuff( caster, self._buffID )



