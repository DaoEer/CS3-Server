# -*- coding: utf-8 -*-


"""
usage:
	Buff持有效果,onBegin 和 onEnd 必须成对存在，分别做buff添加和删除，增添的效果

attribute:
	pass

member function:
	pass

callback:
	pass

"""


#cell
from ConfigObject.Skill.Effect.HoldEffect.HoldEffect import HoldEffect
#common
import csdefine


class HoldEffectHide( HoldEffect ):
	"""
	持有效果：隐身效果
	"""
	def __init__( self ):
		HoldEffect.__init__( self )
		self._enterTime = 0					# 透明淡入时间
		self._outTime = 0					# 透明淡出时间
	
	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		HoldEffect.init( self, dictDat, skill )
		self._enterTime = float( dictDat["Param1"] ) if len( dictDat["Param1"] ) > 0 else 0.0
		self._outTime = float( dictDat["Param2"] ) if len( dictDat["Param2"] ) > 0 else 0.0

	def onBegin( self, effectData, receiver ):
		"""
		效果开始
		"""
		HoldEffect.onBegin( self, effectData, receiver )
		receiver.effectStateInc( csdefine.EFFECT_STATE_HIDE )
		receiver.allClients.StartHideCharacter( self._enterTime )

	def onEnd( self, effectData, receiver ):
		"""
		效果结束
		"""
		receiver.effectStateDec( csdefine.EFFECT_STATE_HIDE )
		receiver.allClients.EndHideCharacter( self._outTime )
		HoldEffect.onEnd( self, effectData, receiver )

	def onClientActorCreate( self, effectData, receiver, srcEntityID ):
		"""
		virtual method
		receiver在某客户端被创建出来
		"""
		HoldEffect.onClientActorCreate( self, effectData, receiver, srcEntityID )
		receiver.client.StartHideCharacter( 0.0 )