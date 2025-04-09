# -*- coding: utf-8 -*-
import KBEngine
import Math
import KBEMath
import KBEDebug
import Functions
from ObjectScript.Space.SpaceCopyMagicMazeChildCopy import SpaceCopyMagicMazeChildCopy

class SpaceCopyZhenShaGong( SpaceCopyMagicMazeChildCopy ):
	"""
	镇煞宫副本
	"""
	def __init__( self ):
		SpaceCopyMagicMazeChildCopy.__init__( self )
		self._spellBoxMapEmissive = {}
		self._spellOrder = []
		self._succeedSound = ""
		self._failedSound = ""

	def initData( self, configData ):
		"""
		virtual method
		"""
		SpaceCopyMagicMazeChildCopy.initData( self, configData )
		for tempStr in configData["SpaceData"]["spellBoxMapEmissive"].split( "|" ):
			scriptID, id = tempStr.split( ":" )
			self._spellBoxMapEmissive[scriptID] = int(id)
		self.blastPosition = KBEMath.Unreal2KBEnginePosition(Functions.vector3TypeConvert( configData["SpaceData"]["blastPosition"] ))
		self.blastScriptID = configData["SpaceData"]["blastScriptID"]
		self._succeedSound = configData["SpaceData"]["succeedSound"]
		self._failedSound = configData["SpaceData"]["failedSound"]

	def onSpellGossipOver(self, spaceEntity, scriptID ):
		"""
		交互顺序
		"""
		self._spellOrder.append(scriptID)
		if len(self._spellOrder) == len(self._spellBoxMapEmissive):
			randList = spaceEntity.queryTemp("randomList")
			gossipList = []
			for i in self._spellOrder:
				gossipList.append(self._spellBoxMapEmissive[i])
			if randList == gossipList:
				for e in spaceEntity._spaceRoles:
					e.client.SpaceZSGGossipComplete()
					e.showMessagePlaySound(self._succeedSound)
				self.onConditionChange( spaceEntity, "", spaceEntity.id, "ZSGSPELL", "")
			else:
				direction = Math.Vector3(0.0, 0.0, 0.0)
				spaceEntity.createEntityByScriptID(self.blastScriptID, self.blastPosition,direction, { "spawnPos": self.blastPosition, "spawnDir": direction})
				for e in spaceEntity._spaceRoles:
					e.showMessagePlaySound(self._failedSound)
			self.clearSpellBoxBuff(spaceEntity, self._spellOrder)
			self._spellOrder.clear()

	def clearSpellBoxBuff(self, spaceEntity, scriptIDList):
		"""
		清除颜色
		"""
		for scriptID in scriptIDList:
			idList = spaceEntity.getEntityRecord( scriptID )
			for id in idList:
				entity = KBEngine.entities.get( id, None )
				if not entity:
					continue
				for buffData in entity.getAttrBuffs().values():  #策划为了表现延迟两秒移除buff
					entity.addTimerCallBack(2.0 , "removeBuffByID",( buffData.buffID, ))