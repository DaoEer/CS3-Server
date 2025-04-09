# -*- coding: utf-8 -*-


from ConfigObject.Skill.Effect.EffectSkillBase import EffectSkillBase
import csdefine

class EffectStopRandomDestroyFloorXDGX( EffectSkillBase ):
	"""
	环任务仙岛归墟 停止随机销毁格子
	"""
	def __init__( self ):
		EffectSkillBase.__init__( self )
		self.stopTime = 0.0 #停止的时间
	
	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		EffectSkillBase.init( self, dictDat, skill )
		self.stopTime = float( dictDat["Param1"] )

	def onReceive( self, skill, caster, receiver ):
		"""
		效果开始
		"""
		spaceEntity = receiver.getCurrentSpace()
		if spaceEntity:
			spaceEntity.stopRandomDestroyFloor( self.stopTime )


