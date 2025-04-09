#############
#妖魔化身：密探对话功能
#############
import KBEngine
import ObjectScript.NPC.NPC as NPC


class NPCSpy( NPC.NPC ):
	def __init__( self ):
		NPC.NPC.__init__( self )

	def gossipWith(self, selfEntity, srcEntityID):
		"""
		处理玩家请求与NPC对话的信息
		"""
		player = KBEngine.entities.get( srcEntityID, None )
		msg = selfEntity.queryTemp("TalkMsg","")
		if player and msg:
			player.showMessagePlaySound( msg )


