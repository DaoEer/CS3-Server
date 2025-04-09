# -*- coding: utf-8 -*-

from ObjectScript.Space.SpaceCopy import SpaceCopy
import KBEDebug
import Math
import csdefine
import csconst
import time
import Functions

class SpaceCopyTongCampWarBase( SpaceCopy ):
	"""
	CST-8722 帮会阵营战  大本营
	"""
	def __init__( self ):
		SpaceCopy.__init__( self )
		self.initJinYuan = 0
		self.initCallNumber = 0
		self.levelAddJinYuan = 0
		self.levelAddCallNumber = 0
	
	def initData( self, configData ):
		"""
		virtual method
		"""
		SpaceCopy.initData( self, configData )
		self.initJinYuan = configData["SpaceData"].get( "initJinYuan", 0 )
		self.initCallNumber = configData["SpaceData"].get("initCallNumber",0)
		self.levelAddJinYuan = configData["SpaceData"].get("levelAddJinYuan",0)
		self.levelAddCallNumber = configData["SpaceData"].get( "levelAddCallNumber",0 )

	def onEnter( self, selfEntity, playerRole, packArgs ):
		SpaceCopy.onEnter( self, selfEntity, playerRole, packArgs )
		tongLevel = packArgs["tongLevel"]
		initJinYuan = self.initJinYuan
		initCallNumber = self.initCallNumber
		if tongLevel > 1:
			initJinYuan = (tongLevel - 1) * self.levelAddJinYuan + self.initJinYuan
			initCallNumber = (tongLevel - 1) * self.levelAddCallNumber + self.initCallNumber
		selfEntity.warInfos.addMember( packArgs["tongDBID"],packArgs["tongName"],playerRole.playerDBID,playerRole,tongLevel,initJinYuan,initCallNumber, packArgs["camp"] )

	def onLogin( self, selfEntity, playerRole ):
		"""
		"""
		SpaceCopy.onLogin( self, selfEntity, playerRole )
		tongObject = selfEntity.warInfos.get( playerRole.tongDBID, None )
		if not tongObject:
			return
		selfEntity.warInfos.addMember( tongObject.tongDBID,tongObject.tongName,playerRole.playerDBID,playerRole,tongLevel,0,0,tongObject.camp )

	def onLeave( self, selfEntity, playerRole, packArgs ):
		"""
		virtual method
		玩家离开副本
		"""
		SpaceCopy.onLeave( self, selfEntity, playerRole, packArgs )

