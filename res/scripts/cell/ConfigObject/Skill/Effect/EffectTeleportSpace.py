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
import Math
import csdefine


class EffectTeleportSpace( EffectSkillBase ):
	"""
	玩家传送至指定地图
	"""
	def __init__( self ):
		EffectSkillBase.__init__( self )
		self._spaceName = ""
		self._position = ()
		self._direction = ()

	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		EffectSkillBase.init( self, dictDat, skill )
		self._spaceName = dictDat["Param1"]

		position = dictDat["Param2"].split(" ")
		direction = dictDat["Param3"].split(" ")
		self._position = Math.Vector3( eval(position[0]), eval(position[1]), eval(position[2]) )
		self._direction = Math.Vector3( eval(direction[0]), eval(direction[1]), eval(direction[2]) )

	def onReceive( self, skill, caster, receiver ):
		"""
		效果开始
		"""
		if receiver.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE: return

		# 当参数不填是默认传送当前地图
		if not self._spaceName:
			self._spaceName = receiver.getCurrentSpaceScriptID()
		receiver.gotoSpaceUE4( self._spaceName, self._position, self._direction )
