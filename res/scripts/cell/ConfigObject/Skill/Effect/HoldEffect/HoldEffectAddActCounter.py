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
import KBEDebug


class HoldEffectAddActCounter( HoldEffect ):
	"""
	持有效果：加动作限制字
	"""
	def __init__( self ):
		HoldEffect.__init__( self )
		self.actList = []
	
	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		HoldEffect.init( self, dictDat, skill )
		self.actList = [int(i) for i in dictDat["Param1"].split("|")]

	def onBegin( self, effectData, receiver ):
		"""
		效果开始
		"""
		HoldEffect.onBegin( self, effectData, receiver )
		receiver.actCounterIncList( self.actList )

	def onEnd( self, effectData, receiver ):
		"""
		效果结束
		"""
		receiver.actCounterDecList( self.actList )
		HoldEffect.onEnd( self, effectData, receiver )
