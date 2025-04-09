# -*- coding: utf-8 -*-

from ConfigObject.Skill.Buff.BuffLoop import BuffLoop
import KBEDebug
import Math
import math
import KST
import csdefine
import KBEngine


class BuffGhostEye( BuffLoop ):
	"""
	鬼瞳buff
	"""
	def __init__( self ):
		BuffLoop.__init__( self )
		self._Maxdistance = 200.0
		self._offsetFront = 0.0
		self._offsetLeft = 0.0
	
	def init( self, dictDat ):
		"""
		virtual method;
		读取buff配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		BuffLoop.init( self, dictDat )
		if self._loopTime == 0.0:		# CST-9200提供缺省支持
			self._loopTime = 1.0
		self._scriptID = dictDat["Param1"]
		if dictDat["Param2"]:
			self._Maxdistance = float(dictDat["Param2"])
		if dictDat["Param3"]:
			offset = dictDat["Param3"].split("|")
			self._offsetFront = float( offset[0] )
			if len(offset) >= 2:
				self._offsetLeft = float( offset[1] )
	
	def doBegin( self, receiver, buffData ):
		"""
		效果开始
		"""
		BuffLoop.doBegin( self, receiver, buffData )
		yaw = receiver.direction.z
		position = Math.Vector3( receiver.position )
		if self._offsetFront:
			position.x += self._offsetFront * math.sin( yaw )
			position.z += self._offsetFront * math.cos( yaw )
		if self._offsetLeft:
			position.x += self._offsetLeft * math.sin( yaw - math.pi/2 )
			position.z += self._offsetLeft * math.cos( yaw - math.pi/2 )
		GhostEye = receiver.createEntityByScriptID( self._scriptID, position, Math.Vector3( receiver.direction ), {} )
		buffData.setTempData( "GhostEyeID", GhostEye.id )
	
	def doReload( self, receiver, buffData ):
		"""
		上线重新加载buff
		"""
		BuffLoop.doReload( self, receiver, buffData )

	
	def doLoopHit( self, receiver, buffData ):
		"""
		周期打击
		"""
		BuffLoop.doLoopHit( self, receiver, buffData )
		GhostEyeID = buffData.getTempData( "GhostEyeID", -1 )
		GhostEye = KBEngine.entities.get( GhostEyeID )
		if GhostEye and receiver:
			_AOI = receiver.getCurrentSpaceObject().getSpaceAoi()
			_Maxdistance = min(_AOI, self._Maxdistance)
			if receiver.position.distTo( GhostEye.position ) > _Maxdistance:
				receiver.removeBuff( buffData.index )
	
	def doEnd( self, receiver, buffData,reason ):
		"""
		效果结束
		"""
		BuffLoop.doEnd( self, receiver, buffData,reason )
		GhostEyeID = buffData.getTempData( "GhostEyeID", -1 )
		GhostEye = KBEngine.entities.get( GhostEyeID )
		if GhostEye:
			GhostEye.destroySelf()