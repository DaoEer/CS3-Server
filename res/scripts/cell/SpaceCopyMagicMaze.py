# -*- coding: utf-8 -*-

import random
from KBEDebug import *
from SpaceCopy import SpaceCopy
import math
import KBEMath
import Math
import KBEngine
import csdefine
import csstatus
import Const
import copy

class SpaceCopyMagicMaze( SpaceCopy ):
	"""
	幻阵迷宫子副本 基类
	"""
	def __init__( self ) :
		SpaceCopy.__init__( self )
		DEBUG_MSG("createArgs: ",self.createArgs)
		self.hasAllRoleTeleport = False
#------------------------------------------------------------------------------------
		
	def onClientStartMove( self, sProgress ):
		"""
		客户端玩家开始移动
		"""
		sPoint = self.getScript().getFlyInfo( sProgress )[1]
		fPatrolID, pPoint, enterPos = self.getScript().getFlyInfo( self.progress )
		for playerRole in self._spaceRoles:
			DEBUG_MSG("onClientStartMove:fPatrolID is %s,sPoint is %s,pPoint is %s,enterPos is %s, sProgress is %s, progress is %s"%(fPatrolID, sPoint, pPoint, enterPos, sProgress, self.progress))
			playerRole.client.FlyToSubSpace( fPatrolID, "", sPoint, pPoint, Const.FLY_SPEED, enterPos )
		
	def onMagicMazeEndFly(self, playerRole):
		"""
		幻阵迷宫结束飞行回调
		"""
		DEBUG_MSG("onMagicMazeEndFly:playerID is %s"%playerRole.id)
		progress = self.progress
		fPatrolID, pPoint, enterPos = self.getScript().getFlyInfo( progress )
		self.playerNotEndFlyList.append(playerRole.id)
		playerRole.position = Math.Vector3(KBEMath.Unreal2KBEnginePosition( enterPos ))
		playerRole.client.StopFlyToSubSpace(fPatrolID)

	def onMagicMazeFallDown(self, playerRole):
		"""
		幻阵迷宫掉落死亡回调
		"""
		progress = self.progress
		fPatrolID, pPoint, enterPos = self.getScript().getFlyInfo( progress )
		playerRole.position = Math.Vector3(KBEMath.Unreal2KBEnginePosition( enterPos ))
		
	def closeSpace( self ):
		"""
		<define method>
		关闭副本唯一入口，所有关闭副本操作（base或cell）都应该走此接口
		"""
		
		DEBUG_MSG("Close space(%s)! scriptID:%s."%( self.id, self.scriptID ))
		self.clearCellAppDataBeforeClose()
		
		if len( self._spaceRoles ):
			self.getScript().onCloseSpace(self, True)
			self.addTimerCallBack( 5, "closeSpace", () )	#5秒后再次关闭
			DEBUG_MSG("Delay close space(%s) reason 1! scriptID:%s."%( self.id, self.scriptID ))
		
		elif len( self._readyEnterRoles ):
			self.getScript().onCloseSpace(self, False)
			self._readyEnterRoles = []
			self.addTimerCallBack( 5, "closeSpace", () )	#5秒后再次关闭
			DEBUG_MSG("Delay close space(%s) reason 2! scriptID:%s."%( self.id, self.scriptID ))
		
		else:
			belongType,spaceKey = self.getScript().getPlayerBelongTypeAndSpaceKey(self)
			if "isSpecialSpace" in self.createArgs and self.createArgs["isSpecialSpace"]:
				KBEngine.globalData["MagicMazeSpaceManager"].onSpaceDelete(belongType, spaceKey, self.scriptID, True,self.createArgs["mainScriptID"])
			else:
				KBEngine.globalData["MagicMazeSpaceManager"].onSpaceDelete(belongType, spaceKey, self.scriptID, False,self.createArgs["mainScriptID"])
			self.destroySelf()
	
	
	