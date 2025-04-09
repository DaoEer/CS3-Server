# -*- coding: utf-8 -*-

import Math
import random
import Functions
import KBEDebug
import KBEMath
import KBEngine
import csdefine
from ConfigObject.Skill.Effect.EffectSkillBase import EffectSkillBase


class EffectTeleportRandomPos( EffectSkillBase ):
	"""
	在圆内（圆心取配置的值）随机取点，闪现过去
	"""
	def __init__( self ):
		EffectSkillBase.__init__( self )
		self._position = None
		self._radius = 0.0
	
	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		EffectSkillBase.init( self, dictDat, skill )
		if dictDat["Param1"]:
			self._position =  KBEMath.Unreal2KBEnginePosition(Functions.vector3TypeConvert( dictDat["Param1"] ))
		self._radius = float( dictDat["Param2"] )

	def onReceive( self, skill, caster, receiver ):
		"""
		效果开始
		"""
		if not receiver.stopMovingForType( csdefine.NORMAL_MOVE ):
			return
		Pos = self._position
		if self._position is None:
			Pos = Math.Vector3(receiver.position)
		positionList = receiver.getRandomPoints( Pos, self._radius, 1, receiver.layer, 0xFFFF )
		if len(positionList):
			receiver.position = positionList[0]