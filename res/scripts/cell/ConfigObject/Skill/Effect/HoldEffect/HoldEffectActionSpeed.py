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

#python
import math
import random
#engine
import Math
#cell
from ConfigObject.Skill.Effect.HoldEffect.HoldEffect import HoldEffect
#common
import csdefine
import csarithmetic
import KBEngine



class HoldEffectActionSpeed( HoldEffect ):
	"""
	设置动作播放速率
	"""
	def __init__( self ):
		HoldEffect.__init__( self )
		self._actionSpeed = 1.0
	
	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"", "Param4":"" }
		@type  dictDat: python dict
		"""
		HoldEffect.init( self, dictDat, skill )
		self._actionSpeed = float(dictDat["Param1"])
		if self._actionSpeed <= 0:
			self._actionSpeed = 1.0

	def onBegin( self, effectData, receiver ):
		"""
		效果开始
		"""
		HoldEffect.onBegin( self, effectData, receiver )
		receiver.allClients.SetAnimRateScale( self._actionSpeed )

	def onEnd( self, effectData, receiver ):
		"""
		效果结束
		"""
		receiver.allClients.SetAnimRateScale(1.0)
		HoldEffect.onEnd( self, effectData, receiver )

