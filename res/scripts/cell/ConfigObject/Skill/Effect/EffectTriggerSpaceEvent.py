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


class EffectTriggerSpaceEvent( EffectSkillBase ):
	"""
	触发 副本条件改变事件(收到通知)
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
		return EffectSkillBase.canEffect(self,skill, caster, receiver)

	def onReceive( self, skill, caster, receiver ):
		"""
		效果开始
		"""
		if not caster or not (caster.isInSpaceCopy() or caster.isInSpacePlane()):
			return

		if self.cmd:
			spaceEntity = caster.getCurrentSpace()
			if not spaceEntity:
				return
			spaceEntity.getScript().onConditionChange( spaceEntity, "Skill", None, str(self.cmd), {"casterID":caster.id, "receiverID":receiver.id} )
			



