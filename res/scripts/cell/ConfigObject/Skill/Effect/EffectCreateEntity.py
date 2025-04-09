# -*- coding: utf-8 -*-

from ConfigObject.Skill.Effect.EffectSkillBase import EffectSkillBase
import KBEDebug
import Math
import math
import KST
import csdefine

class EffectCreateEntity( EffectSkillBase ):
	"""
	目标位置创建entity
	"""
	def __init__( self ):
		EffectSkillBase.__init__( self )
		self._scriptID = ""
		self._offsetFront = 0.0
		self._offsetLeft = 0.0
	
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
			
		object_ = KST.g_objFactory.getObject( self._scriptID )
		if(object_):
			params = {}
			if not object_.hasScriptFlag( csdefine.FLAG_CAN_FLY ):
				rayCastList = receiver.navmeshRaycast( receiver.position, position )
				if rayCastList:
					position = rayCastList[0]
					params = { "parent" : receiver.parent }
			params.update( {"spawnPos": position, "spawnDir":Math.Vector3( receiver.direction ) } )
			receiver.createEntityByScriptID( self._scriptID, position, Math.Vector3( receiver.direction ), params )



