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



class EffectAbsorbHP( EffectSkillBase ):
	"""
	吸血效果
	"""
	def __init__( self ):
		EffectSkillBase.__init__( self )
		self._percent = 0.0
		self._extraValue = 0
		self._cureRate = 0.0
	
	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		EffectSkillBase.init( self, dictDat, skill )
		if dictDat["Param1"]:
			Param1 = dictDat["Param1"].split("|")
			self._percent = float( Param1[0] )
			if len(Param1) > 1:
				self._extraValue = int( Param1[1] )
				
		if dictDat["Param2"]:
			self._cureRate = float( dictDat["Param2"] )

	def canEffect( self, skill, caster, receiver  ):
		"""
		效果添加检测
		"""
		if receiver.getState() == csdefine.ENTITY_STATE_DEAD:
			return False

		return EffectSkillBase.canEffect( self, skill, caster, receiver )

	def onReceive( self, skill, caster, receiver ):
		"""
		效果开始
		"""
		finalDamage = math.ceil( receiver.HP_Max * self._percent + self._extraValue )	#吸血量＝生命值上限×效果加成值＋效果附加值
		finalDamage = max(0, finalDamage)
		skillID = 0
		if skill:
			skillID = skill._id
		receiver.receiveDamage( caster.id, skillID, csdefine.DAMAGE_TYPE_MAGIC, finalDamage, False, False, 0, self._actForbid )
		if caster.getState() != csdefine.ENTITY_STATE_DEAD:
			caster.addHP( math.ceil(finalDamage * self._cureRate) )
		if skill and (skill.getScriptType() == csdefine.SCRIPT_TYPE_BUFF or not skill.isPassiveSkill()): #buff的打击也需要触发
			caster.triggerSkillEvent( csdefine.SKILL_EVENT_HURT, receiver.id, { "actForbid": self._actForbid, "type":csdefine.SKILL_EVENT_CASTER_HURT, "takeDamage": finalDamage } )
			receiver.triggerSkillEvent( csdefine.SKILL_EVENT_HURT, caster.id, { "actForbid": self._actForbid, "type":csdefine.SKILL_EVENT_RECEIVER_HURT, "takeDamage":finalDamage } )
			if caster.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE and caster.queryRelation( receiver ) == csdefine.COMBAT_RELATION_ENEMY:
				caster.onStartDoubleHit()
			if receiver.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE and caster.queryRelation( receiver ) == csdefine.COMBAT_RELATION_ENEMY:
				receiver.onStartBeDoubleHit()
