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



class EffectTriggerAIEvent( EffectSkillBase ):
	"""
	触发 自定义AI事件(收到通知)
	"""
	def __init__( self ):
		EffectSkillBase.__init__( self )
		self.cmd = None
	
	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		EffectSkillBase.init( self, dictDat, skill )
		self.cmd = dictDat["Param1"] if dictDat["Param1"] else None


	def canEffect( self,skill, caster, receiver ):
		"""
		"""
		if receiver.getEntityFlag() != csdefine.ENTITY_FLAG_MONSTER:
			return False
		return EffectSkillBase.canEffect(self,skill, caster, receiver)

	def onReceive( self, skill, caster, receiver ):
		"""
		效果开始
		"""
		if self.cmd:
			if caster.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
				receiver.monsterAITriggerEvent(csdefine.ENTITY_EVENT_COMMAND, (caster.id, None, self.cmd), caster)
			else:
				receiver.monsterAITriggerEvent(csdefine.ENTITY_EVENT_COMMAND, (caster.id, caster.scriptID, self.cmd), caster)
			



