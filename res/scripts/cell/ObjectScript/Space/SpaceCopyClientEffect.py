# -*- coding: utf-8 -*-

import csdefine
import csstatus
import KBEDebug
import KBEngine
from ObjectScript.Space.SpaceCopy import SpaceCopy


class SpaceCopyClientEffect( SpaceCopy ):
	"""
	
	"""
	def __init__( self ):
		SpaceCopy.__init__( self )
		self._spellBoxMapEmissive = {}
		self._spellOrder = []
		
	def initData( self, configData ):
		"""
		virtual method
		"""
		SpaceCopy.initData( self, configData )
		for tempStr in configData["SpaceData"]["spellBoxMapEmissive"].split( "|" ):
			scriptID, id = tempStr.split( ":" )
			self._spellBoxMapEmissive[scriptID] = int(id)
	
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
				self.onConditionChange( spaceEntity, "", spaceEntity.id, "ZSGSPELL", "")
			else:
				for e in spaceEntity._spaceRoles:
					KBEDebug.ERROR_MSG("Gossip order wrong")
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
		