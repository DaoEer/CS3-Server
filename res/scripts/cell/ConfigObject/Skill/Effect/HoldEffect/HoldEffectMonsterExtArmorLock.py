import csdefine
import KBEngine
from ConfigObject.Skill.Effect.HoldEffect.HoldEffect import HoldEffect


class HoldEffectMonsterExtArmorLock( HoldEffect ):
	"""
	MonsterExtArmorLock怪物的金钟罩效果
	"""
	def __init__( self ):
		HoldEffect.__init__( self )
		self._outTime = 0

	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		HoldEffect.init( self, dictDat, skill )
		if dictDat["Param1"]:
			self._outTime = float( dictDat["Param1"] )

	def onBegin( self, effectData, receiver ):
		"""
		效果开始
		"""
		HoldEffect.onBegin( self, effectData, receiver )
		receiver.allClients.EnterArmorLock()

	def onEnd( self, effectData, receiver ):
		"""
		效果结束
		"""
		receiver.allClients.ExitArmorLock( self._outTime )
		HoldEffect.onEnd( self, effectData, receiver )

	def onClientActorCreate( self, effectData, receiver, srcEntityID ):
		"""
		virtual method
		receiver在某客户端被创建出来
		"""
		HoldEffect.onClientActorCreate( self, effectData, receiver, srcEntityID )
		
		if srcEntityID == receiver.id:
			clientEntity = receiver.client
		else:
			playerEntity = KBEngine.entities.get( srcEntityID )
			if not playerEntity:
				return
			clientEntity = playerEntity.clientEntity( receiver.id )
		
		clientEntity.EnterArmorLock()