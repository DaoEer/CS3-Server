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
import Math
#cell
from ConfigObject.Skill.Effect.EffectSkillBase import EffectSkillBase
#common
import csdefine
import csarithmetic
import KST
import KBEDebug


class EffectExpelTheSoul( EffectSkillBase ):
	"""
	灵魂出窍效果 --灵魂之誓副本
	"""
	def __init__( self ):
		EffectSkillBase.__init__( self )
		self.effectID = ""
		self.delayDestroyTime = 0.0
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
		if dictDat["Param1"]:
			self.effectID = dictDat["Param1"]
		if dictDat["Param2"]:
			self.delayDestroyTime = float(dictDat["Param2"])
		self._scriptID = dictDat["Param3"]
		
		if dictDat["Param4"]:
			offset = dictDat["Param4"].split("|")
			self._offsetFront = float( offset[0] )
			if len(offset) >= 2:
				self._offsetLeft = float( offset[1] )

	def onReceive( self, skill, caster, receiver ):
		"""
		效果开始
		"""
		spaceEntity = caster.getCurrentSpace()
		if not spaceEntity:
			return
		spaceEntity.getScript().onConditionChange(spaceEntity, "","","send01","")
		p= caster.position - receiver.position
		direction = (0.0,0.0,csarithmetic.getYawByVector3( p ))
		receiver.changeDirection(direction, csdefine.REASON_CHANGE_DIR_FORCE)
		caster.client.ExpelTheSoul(receiver.id, self.effectID, self.delayDestroyTime)

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
			newEntity = receiver.createEntityByScriptID( self._scriptID, position, Math.Vector3( receiver.direction ), params )
			if newEntity:
				newEntity.setTemp("ownerID",receiver.id)

