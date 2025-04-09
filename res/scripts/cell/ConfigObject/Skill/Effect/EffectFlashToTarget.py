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
import KBEDebug
#common
import csdefine
import math
import csarithmetic
import Math

class EffectFlashToTarget( EffectSkillBase ):
	"""
	瞬移到目标位置
	"""
	def __init__( self ):
		EffectSkillBase.__init__( self )
		self._offsetFront = 0.0
		self._offsetLeft = 0.0
		self._directionType = csdefine.BUFF_HIT_TYPE_CATORE_DIRECTION
		self._isSwap = False #是否交换施法者和受术者

	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		EffectSkillBase.init( self, dictDat, skill )
		if dictDat["Param1"]:
			offset = dictDat["Param1"].split("|")
			self._offsetFront = float( offset[0] )
			if len(offset) >= 2:
				self._offsetLeft = float( offset[1] )

		if dictDat["Param2"]:
			self._directionType = int( dictDat["Param2"] )

		if dictDat["Param3"]:
			self._isSwap = bool( int(dictDat["Param3"]) )

	def onReceive( self, skill, caster, receiver ):
		"""
		效果开始
		"""
		if caster.getState() == csdefine.ENTITY_STATE_PEAD or receiver.getState() == csdefine.ENTITY_STATE_PEAD:
			return

		if caster.spaceID != receiver.spaceID:
			return

		if not self._isSwap:
			casterPosition = Math.Vector3( caster.position )
			receiverPosition = Math.Vector3( receiver.position )
			casterDirection = Math.Vector3( caster.direction )
			receiverDirection = Math.Vector3( receiver.direction )
		else:
			casterPosition = Math.Vector3( receiver.position )
			receiverPosition = Math.Vector3( caster.position )
			casterDirection = Math.Vector3( receiver.direction )
			receiverDirection = Math.Vector3( caster.direction )

		yaw = receiverDirection.z
		position = Math.Vector3( receiverPosition )	

		if self._offsetFront:
			position.x += self._offsetFront * math.sin( yaw )
			position.z += self._offsetFront * math.cos( yaw )
		if self._offsetLeft:
			position.x += self._offsetLeft * math.sin( yaw - math.pi/2 )
			position.z += self._offsetLeft * math.cos( yaw - math.pi/2 )
 		
		if not self._isSwap:
			raycastList = receiver.navmeshRaycast(receiverPosition,position)
		else:
			raycastList = caster.navmeshRaycast(receiverPosition,position)
		if raycastList:
			position = raycastList[0]
		
		position = Math.Vector3(position)
		recvDir = Math.Vector3(receiverDirection)
		if self._directionType == csdefine.BUFF_HIT_TYPE_CASTER_DIRECTION:
			recvDir.z = casterDirection.z
			#receiver.direction.z = caster.direction.z
		elif self._directionType == csdefine.BUFF_HIT_TYPE_CASTER_RDIRECTION:
			recvDir.z = casterDirection.z + math.pi
		elif self._directionType == csdefine.BUFF_HIT_TYPE_CATORE_DIRECTION:
			if receiverPosition.z == position.z and receiverPosition.x == position.x:
				recvDir.z = casterDirection.z
			else:
				recvDir.z = csarithmetic.getYawByVector3(receiverPosition-position)
		elif self._directionType == csdefine.BUFF_HIT_TYPE_CATORE_RDIRECTION:
			if receiverPosition.z == position.z and receiverPosition.x == position.x:
				recvDir.z = receiverDirection.z
			else:
				recvDir.z = csarithmetic.getYawByVector3(position- receiverPosition)
		elif self._directionType == csdefine.BUFF_HIT_TYPE_RECEIVER_DIRECTION:
			recvDir.z = receiverDirection.z
		elif self._directionType == csdefine.BUFF_HIT_TYPE_RECEIVER_RDIRECTION:
			recvDir.z += math.pi

		if not self._isSwap:
			if caster.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
				spaceEntity = caster.getCurrentSpace()
				if spaceEntity:
					caster.gotoSpace( spaceEntity.scriptID, position, recvDir )
			else:
				caster.setPosition( position )
				caster.setDirection( recvDir )
				if receiver.parent:
					caster.parent = receiver.parent
		else:
			if receiver.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
				spaceEntity = receiver.getCurrentSpace()
				if spaceEntity:
					receiver.gotoSpace( spaceEntity.scriptID, position, recvDir )
			else:
				receiver.setPosition( position )
				receiver.setDirection( recvDir )
				if receiver.parent:
					caster.parent = receiver.parent
