# -*- coding: utf-8 -*-


from ConfigObject.Skill.Effect.EffectSkillBase import EffectSkillBase
import csdefine
import random
import KBEMath

class EffectRandomTeleportFloorXDGX( EffectSkillBase ):
	"""
	环任务仙岛归墟 随机传送到某个格子
	"""
	def __init__( self ):
		EffectSkillBase.__init__( self )
	
	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		EffectSkillBase.init( self, dictDat, skill )

	def onReceive( self, skill, caster, receiver ):
		"""
		效果开始
		"""
		spaceEntity = receiver.getCurrentSpace()
		if not spaceEntity or not spaceEntity.floorIDList:
			return
		random.shuffle(spaceEntity.floorIDList)
		floorIDList = random.sample( spaceEntity.floorIDList,1)
		position = spaceEntity.getFloorPositionByFloorID( floorIDList[0] )
		receiver.allClients.TeleportToDstPosition(KBEMath.KBEngine2UnrealPosition(position))
		receiver.position = position
