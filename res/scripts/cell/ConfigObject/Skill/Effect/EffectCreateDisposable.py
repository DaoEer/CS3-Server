# -*- coding: utf-8 -*-

import math
import time
import json
import KST
import Math
import KBEDebug
import csdefine
from ConfigObject.Skill.Effect.EffectSkillBase import EffectSkillBase

class EffectCreateDisposable( EffectSkillBase ):
	"""
	召唤"一次性的随从单位"效果
	"""
	def __init__( self ):
		EffectSkillBase.__init__( self )
		self._scriptID = ""
		self._offsetFront = 0.0
		self._offsetLeft = 0.0
		self._lifeTime = 0.0
	
	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		EffectSkillBase.init( self, dictDat, skill )
		self._scriptID = dictDat["Param1"]
		
		if dictDat["Param2"]:
			offset = dictDat["Param2"].split("|")
			self._offsetFront = float( offset[0] )
			if len(offset) >= 2:
				self._offsetLeft = float( offset[1] )
				
		if dictDat["Param3"]:
			self._lifeTime = float(dictDat["Param3"])

	def onReceive( self, skill, caster, receiver ):
		"""
		效果开始
		"""
		yaw = receiver.direction.z
		position = Math.Vector3( receiver.position )
		if self._offsetFront:
			position.x += self._offsetFront * math.sin( yaw )
			position.z += self._offsetFront * math.cos( yaw )
		if self._offsetLeft:
			position.x += self._offsetLeft * math.sin( yaw - math.pi/2 )
			position.z += self._offsetLeft * math.cos( yaw - math.pi/2 )
		params = {}
		params.update( {"scriptID":self._scriptID} )
		params.update( {"ownerID": receiver.id})
		params.update( {"spawnPos":position} )
		params.update( {"spawnDir":Math.Vector3(receiver.direction)} )
		receiver.callDisposableMonster(params, self._lifeTime)
		
		