# -*- coding: utf-8 -*-


import Math
import math
import csarithmetic
import csdefine
from ConfigObject.Skill.Effect.EffectSkillBase import EffectSkillBase


class EffectCircleRound( EffectSkillBase ):
	"""
	受术者站成一个圈并朝向施法者
	"""
	def __init__( self ):
		EffectSkillBase.__init__( self )
		self.disToCaster = 0.0
	
	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		EffectSkillBase.init( self, dictDat, skill )
		if dictDat["Param1"]:
			self.disToCaster = float( dictDat["Param1"] )

	def onReceive( self, skill, caster, receiver ):
		"""
		效果开始
		"""
		dis = ( receiver.position - caster.position ).length
		if dis < self.disToCaster:		#推出去
			if dis == 0:
				direction = receiver.direction
				direction.normalise()
				dstPos = receiver.position - direction * self.disToCaster
				receiver.position = dstPos
			else:
				yaw = csarithmetic.getYawByVector3( caster.position - receiver.position )
				direction = Math.Vector3( math.sin(yaw), 0.0, math.cos(yaw) )
				direction.normalise()
				dstPos = receiver.position - direction * ( self.disToCaster - dis )
				receiver.position = dstPos
		
		elif dis > self.disToCaster:	#拉过来
			yaw = csarithmetic.getYawByVector3( caster.position - receiver.position )
			direction = Math.Vector3( math.sin(yaw), 0.0, math.cos(yaw) )
			direction.normalise()
			dstPos = receiver.position + direction * ( dis - self.disToCaster )
			receiver.position = dstPos
		
		#朝向施法者
		yaw = csarithmetic.getYawByVector3(caster.position-receiver.position)
		direction = (0.0, 0.0, yaw)
		receiver.changeDirection(direction, csdefine.REASON_CHANGE_DIR_FORCE)