# -*- coding: utf-8 -*-


from ConfigObject.Skill.Effect.EffectSkillBase import EffectSkillBase
import csdefine

class EffectDestroyGridXDGX( EffectSkillBase ):
	"""
	环任务仙岛归墟 周围格子自爆
	"""
	def __init__( self ):
		EffectSkillBase.__init__( self )
		self.range = 0.0
	
	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		EffectSkillBase.init( self, dictDat, skill )
		self.range = float( dictDat["Param1"] )

	def onReceive( self, skill, caster, receiver ):
		"""
		效果开始
		"""
		spaceEntity = receiver.getCurrentSpace()
		if spaceEntity:
			floorIDList = spaceEntity.getFloorIDListByRange( self.range, receiver.position )
			if not len(floorIDList):
				return
			for floorID in floorIDList:
				spaceEntity.removeFloorByFloorID( floorID )

		



