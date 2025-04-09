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
import csconst



class EffectTriggerCustomEvent( EffectSkillBase ):
	"""
	触发 自定义事件
	"""
	def __init__( self ):
		EffectSkillBase.__init__( self )
		self._eventID = None
	
	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		EffectSkillBase.init( self, dictDat, skill )
		self._eventID = int( dictDat["Param1"] ) if dictDat["Param1"] else None

	def onReceive( self, skill, caster, receiver ):
		"""
		效果开始
		"""
		if self._eventID:
			receiver.triggerSkillEvent( csdefine.SKILL_EVENT_PLAN_CUSTOM, caster.id, { "id" : self._eventID, "actForbid": skill.getActForbid() } )



