# -*- coding: utf-8 -*-
#
import KBEngine
import NPC
import Math
import csdefine

class NPCExtCompose( NPC.NPC ):
	"""
	轮回秘境 打造NPC
	"""
	def __init__(self):
		NPC.NPC.__init__(self)

	def CELL_onClientReady( self, srcEntityID ):
		"""
		<Expose method>
		玩家客户端Character Actor已经准备好
		"""
		player = KBEngine.entities.get( srcEntityID )
		space = self.getCurrentSpace()
		spaceObject = space.getScript()
		object = self.getScript()
		if spaceObject.getSpaceType() == csdefine.SPACE_TYPE_DONG_FU:
			if space.belongDBID == player.playerDBID:
				player.recordComposeTool( self, object.dongFuType, object.composeType )
		else:
			if not player.hasDongFu():
				player.recordComposeTool( self, object.dongFuType, object.composeType )
			
	def onComposeBegin( self, player ):
		"""开始打造"""
		spaceObject = self.getScript()
		if spaceObject.actionID:
			player.clientEntity( self.id ).CLIENT_OnPlayAction( spaceObject.actionID, -1.0)
		if spaceObject.particleID and spaceObject.monsterScriptID:
			space = self.getCurrentSpace()
			for monster in space.getEntityMailBoxRecord( spaceObject.monsterScriptID ):
				player.clientEntity( monster.id ).CLIENT_OnPlayParticles( monster.id, spaceObject.particleID, "", 1.0, Math.Vector3(0,0,0) )
			
	def onComposeEnd( self, player ):
		"""打造结束"""
		spaceObject = self.getScript()
		if spaceObject.actionID:
			player.clientEntity( self.id ).CLIENT_StopAction()
			
		if spaceObject.particleID and spaceObject.monsterScriptID:
			space = self.getCurrentSpace()
			for monster in space.getEntityMailBoxRecord( spaceObject.monsterScriptID ):
				player.clientEntity( monster.id ).CLIENT_OnStopParticles()
	
	def onBuildDestroy( self, player ):
		"""打造暂停 建筑被破坏了"""
		pass
#		spaceObject = self.getScript()
#		space = self.getCurrentSpace()
#		if spaceObject.monsterScriptID:
#			for monster in space.getEntityMailBoxRecord( spaceObject.monsterScriptID ):
#				monster.monsterAITriggerEvent(csdefine.ENTITY_EVENT_COMMAND, (monster.id, monster.scriptID, "buildDestroy" ), player)