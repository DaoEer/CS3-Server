# -*- coding: utf-8 -*-

import time
import KBEMath
import KBEDebug
import KBEngine
import csdefine
import Const
import Define
import csconst
import Functions
import csstatus
from ObjectScript.Space.SpaceCopy import SpaceCopy


class SpaceCopyJiYuan( SpaceCopy ):
	"""
	CST-12052 机缘玩法
	"""
	def __init__( self ):
		SpaceCopy.__init__( self )
	
	def initData( self, configData ):
		"""
		"""
		SpaceCopy.initData( self, configData )
		
	def getPackDomainData( self, playerEntity, args ):
		"""
		"""
		packDict = SpaceCopy.getPackDomainData( self, playerEntity, args )
		packDict["level"] = playerEntity.getLevel()
		return packDict
	
	def getReviveToExitInfo( self, playerRole ):
		JiyuanSpaceData = playerRole.queryTemp("JiyuanSpaceData", None)
		exitInfo = SpaceCopy.getReviveToExitInfo( self, playerRole )
		if JiyuanSpaceData is not None: 
			#判断之前的地图是否还存在
			key = Const.GET_SPACE_CELLAPP_KEY_1( JiyuanSpaceData[0] )
			if key in KBEngine.cellAppData:
				exitInfo = ( JiyuanSpaceData[1], JiyuanSpaceData[2], JiyuanSpaceData[3] )
		
		#KBEDebug.DEBUG_MSG("role %s getReviveToExitInfo %s" %(playerRole.id, exitInfo))
		return exitInfo
		
	def onLeave( self, selfEntity, playerRole, packArgs ):
		"""
		"""
		SpaceCopy.onLeave(self, selfEntity, playerRole, packArgs)
		playerRole.removeTemp("JiYuanXinXi")
		playerRole.removeTemp("JiyuanSpaceData")
		

	