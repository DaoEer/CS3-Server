# -*- coding: utf-8 -*-

from CoreObject.SpaceObject import SpaceObject
import Const
import KBEDebug
import KBEngine

class SpaceMultiLine( SpaceObject ):
	def __init__( self ):
		SpaceObject.__init__( self )
		self.setCurrentSpaceData( Const.SPACE_DATA_LINE_NUMBER,self.spaceKey )
		
	def setMaxLineNumber( self, maxLineNumber ):
		"""
		设置最大线数
		"""
		self.setCurrentSpaceData( Const.SPACE_DATA_MAX_LINE_NUMBER, str(maxLineNumber) )
		
#------------------ 地图频道发言 -------------------------------------
	def onSendChatMessage( self, playerDBID, chatData ):
		"""
		"""
		SpaceObject.onSendChatMessage(self, playerDBID, chatData)
		KBEngine.globalData["SpaceManager"].remoteCallDomain( self.scriptID,"onSendChatMessage",(self.id, playerDBID, chatData))
		
	def onSendChatMessageFromBase(self, playerDBID, chatData):
		"""
		"""
		SpaceObject.onSendChatMessage(self, playerDBID, chatData)
