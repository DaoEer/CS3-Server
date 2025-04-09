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


class EffectGangQiDamage( EffectSkillBase ):
	"""
	罡气伤害效果
	"""
	def __init__( self ):
		EffectSkillBase.__init__( self )
		self._rate = 0.0			#罡气攻击比例
		self._extraValue = 0		#罡气伤害固定值
	
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
			self._rate = float( Param1[0] )
			if len(Param1) > 1:
				self._extraValue = int(Param1[1])
			
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
		damage = caster.getGangQiDamage( receiver, self._rate, self._extraValue )
		receiver.recvGangQiDamage( damage )