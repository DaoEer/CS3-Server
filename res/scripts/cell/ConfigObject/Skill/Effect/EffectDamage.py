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
import KBEDebug
import csdefine


class EffectDamage( EffectSkillBase ):
	"""
	物理伤害效果
	"""
	def __init__( self ):
		EffectSkillBase.__init__( self )
		self._damageValue = 0
		self._percent = 0.0
		self._deadEffect = 0				# 死亡时，是否播放特殊效果（暴尸）
		self._isSkipEvent = False 				# 是否跳过事件触发
		self._passiveIDOnKill = 0 		
	
	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		EffectSkillBase.init( self, dictDat, skill )

		# 伤害百分比（浮点型）|固定值（整型）
		if dictDat["Param1"]:
			Param1 = dictDat["Param1"].split("|")
			self._percent = float( Param1[0] )
			if len(Param1) > 1:
				self._damageValue = int(Param1[1])

		# 标记列表（:冒号|竖号分隔，多个代表“且”，留空代表“没有标记”，具体格式与功能由标记定义）
		if dictDat["Param2"]:
			Param2 = dictDat["Param2"].split("|")
			for i in Param2:
				List = i.split(":")
				if List[0] == "IsDoDeadEffect":		# “IsDoDeadEffect”代表“需要播放击杀表现”
					self._deadEffect = 1
				elif List[0] == "IsSkipEvent":		# “IsSkipEvent”代表“需要跳过事件触发”
					self._isSkipEvent = True
				elif List[0] == "IsDoPrivateOnKill":	# “IsDoPrivateOnKill:99900102”代表“此效果击杀时，额外触发被动技能99900102
					self._passiveIDOnKill = int(List[1])
				else:
					KBEDebug.ERROR_MSG("ID:%d  EffectDamage: %s is not a correct tag name "%(skill.getID(), List[0]))



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
		casterID = caster.id
		finalDamage = math.ceil( receiver.HP_Max * self._percent + self._damageValue )
		finalDamage = max(0, finalDamage)
		"""
		if self._percent:
			receiver.equipArmorAbrasion( self._damageValue * self._percent )
		else:
			receiver.equipArmorAbrasion( self._damageValue )
		"""
		skillID = 0
		if skill:
			skillID = skill._id

		receiver.receiveDamage( casterID, skillID, csdefine.DAMAGE_TYPE_PHYSICS, finalDamage, False, False, self._deadEffect, self._actForbid )
		if skill and (skill.getScriptType() == csdefine.SCRIPT_TYPE_BUFF or not skill.isPassiveSkill()): #buff的打击也需要触发
			if not self._isSkipEvent:
				caster.triggerSkillEvent( csdefine.SKILL_EVENT_HURT, receiver.id, { "actForbid": self._actForbid, "type":csdefine.SKILL_EVENT_CASTER_HURT, "takeDamage": finalDamage } )
				receiver.triggerSkillEvent( csdefine.SKILL_EVENT_HURT, caster.id, { "actForbid": self._actForbid, "type":csdefine.SKILL_EVENT_RECEIVER_HURT, "takeDamage":finalDamage } )
				if caster.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE and caster.queryRelation( receiver ) == csdefine.COMBAT_RELATION_ENEMY:
					caster.onStartDoubleHit()
				if receiver.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE and caster.queryRelation( receiver ) == csdefine.COMBAT_RELATION_ENEMY:
					receiver.onStartBeDoubleHit()

		if self._passiveIDOnKill and receiver.isWillDead(int(finalDamage)):
			requestSkill = receiver.getSkill(self._passiveIDOnKill)		
			requestSkill.requestPassiveSkill(caster, receiver.id, {})