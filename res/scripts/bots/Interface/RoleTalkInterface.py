# -*- coding: utf-8 -*-
import KBEngine
class RoleTalkInterface:
	
	def __init__(self):
		pass
		
	def onSetGossipText(self, NPCID, gossipText):
		pass
		
	def onAddGossipOption(self, key, title, type):
		pass
		
	def onGossipComplete(self, key):
		pass
	
	def onSetMonsterGossipText(self, monsterID, gossipText ):
		pass
		
	def onAddMonsterGossipOption(self, key, title, type):
		pass
	
	def onMonsterGossipComplete(self, key):
		pass
		
	def openStoreWindow( self ):
		pass
	def RefreshAroundBoxStatus( sel, int1 ):
		pass
		
	def onPlayGossipVoice(self, voiceID):
		pass
	def onShowOptionTalkDes( self, p1, p2, p3 ):
		pass
	def onShowDefaultOption( self, p1, p2 ):
		pass
