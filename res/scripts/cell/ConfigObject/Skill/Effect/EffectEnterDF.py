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
import KBEDebug



class EffectEnterDF( EffectSkillBase ):
	"""
	回洞府
	"""
	def __init__( self ):
		EffectSkillBase.__init__( self )
		self._spaceStr = ""			# 洞府
		self._highSpaceStr = ""		# 高级洞府
	
	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		EffectSkillBase.init( self, dictDat, skill )

		self._spaceStr = dictDat["Param1"]			# 洞府
		self._highSpaceStr = dictDat["Param2"]		# 高级洞府
	
	def canEffect( self, skill, caster, receiver ):
		"""
		效果添加检测
		"""
		if receiver.isState( csdefine.ENTITY_STATE_DEAD ):
			return False
		return EffectSkillBase.canEffect( self, skill, caster, receiver )

	def onReceive( self, skill, caster, receiver ):
		"""
		效果开始
		"""
		packArgs = {}
		packArgs["belongDBID"] = caster.playerDBID
		packArgs["lineNumber"] = caster.caveHouseLine
		packArgs["group"] = caster.getBuildIndex()
		if caster.occupySpaceDF == csdefine.SPACE_TYPE_PRIVATE:
			caster.gotoSpaceEnterPos( self._spaceStr, packArgs )
		elif caster.occupySpaceDF == csdefine.SPACE_TYPE_HIGH_DF:
			caster.gotoSpaceEnterPos( self._highSpaceStr, packArgs )
		else:
			caster.statusMessage( csstatus.LHMJ_HAS_NOT_DONGFU, "" )



