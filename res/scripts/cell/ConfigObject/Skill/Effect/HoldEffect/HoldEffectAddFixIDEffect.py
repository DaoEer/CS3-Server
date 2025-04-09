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
from ConfigObject.Skill.EffectLoader import g_effects
#common
import csdefine
import KBEDebug
import KBEngine


class HoldEffectAddFixIDEffect( HoldEffect ):
	"""
	持有效果：添加固定ID的持有效果
	"""
	def __init__( self ):
		HoldEffect.__init__( self )
		self._effectID = 0
	
	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		HoldEffect.init( self, dictDat, skill )
		self._effectID = int(dictDat["Param1"])
		holdEffect = g_effects.getHoldEffect(self._effectID)
		if holdEffect is None:
			KBEDebug.ERROR_MSG( "Effect script(HoldEffectAddFixIDEffect) can't find the effectID(%d)!" %self._effectID )
			return
		if holdEffect.__module__ in ["EffectAddFixIDEffect", "HoldEffectAddFixIDEffect"]:
			KBEDebug.ERROR_MSG( "Effect(%d) script(HoldEffectAddFixIDEffect) can't add %s again!"%(self._effectID, holdEffect.__module__ ) )

	def onBegin( self, effectData, receiver ):
		"""
		效果开始
		"""
		HoldEffect.onBegin( self, effectData, receiver )
		caster = KBEngine.entities.get( effectData.casterID, None )
		if caster:
			index = receiver.addFixIDHoldEffect( self._effectID, caster )
			if index != -1:
				effectData.setTempData( "recordEffectIndex", index )

	def onEnd( self, effectData, receiver ):
		"""
		效果结束
		"""
		index = effectData.getTempData( "recordEffectIndex", -1 )
		if index != - 1:
			receiver.removeFixIDHoldEffect( index )

		HoldEffect.onEnd( self, effectData, receiver )