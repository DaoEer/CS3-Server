
#cell
from ConfigObject.Skill.Effect.HoldEffect.HoldEffect import HoldEffect
#common
import csdefine


class HoldEffectSubmerge( HoldEffect ):
	"""
	遁地效果
	"""
	def __init__( self ):
		HoldEffect.__init__( self )
	
	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		HoldEffect.init( self, dictDat, skill )

	def onBegin( self, effectData, receiver ):
		"""
		效果开始
		"""
		HoldEffect.onBegin( self, effectData, receiver )
		receiver.allClients.CLIENT_StartSubmerge()


	def onEnd( self, effectData, receiver ):
		"""
		效果结束
		"""
		HoldEffect.onEnd( self, effectData, receiver )
		receiver.allClients.CLIENT_EndSubmerge()
