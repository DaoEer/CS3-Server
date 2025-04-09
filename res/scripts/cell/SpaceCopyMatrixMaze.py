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
import Define

class SpaceCopyMatrixMaze( SpaceCopy ):
	"""
	幻阵迷宫副本 父副本 第三版
	"""
	def __init__( self ) :
		SpaceCopy.__init__( self )
		self.copyIsComplet = False
		self.result = 0
		self.indexList = []
		self.resultList = []
		
#------------------------------------------------------------------------------------		
	def onMagicMazeEndFly(self, playerRole):
		"""
		幻阵迷宫结束飞行回调
		"""
		fPatrolID, pPoint, enterPos = self.getScript().getFlyInfo( self.progress )
		self.playerNotEndFlyList.append(playerRole.id)
		playerRole.position = Math.Vector3(KBEMath.Unreal2KBEnginePosition( enterPos ))
		playerRole.client.StopFlyToSubSpace(fPatrolID)

	def onMagicMazeFallDown(self, playerRole):
		"""
		幻阵迷宫掉落死亡回调
		"""
		fPatrolID, pPoint, enterPos = self.getScript().getFlyInfo( self.progress )
		playerRole.position = Math.Vector3(KBEMath.Unreal2KBEnginePosition( enterPos ))

	def onClientStartMove( self, player, flySpeed ):
		"""
		客户端玩家开始移动飞行
		"""
		self.flySpeed = int(flySpeed)
		self.playerNotEndFlyList = []
		
		sPoint = self.getScript().getFlyInfo( self.progress )[1]
		self.progress += 1
		KBEngine.globalData["MagicMazeSpaceManager"].setSpaceProgress(self.belongType, self.spaceKey, self.progress,self.createArgs["mainScriptID"])
		fPatrolID, pPoint, enterPos = self.getScript().getFlyInfo(self.progress)
		if player.isInTeam():	#玩家在队伍里
			rangeMems = player.getInRangeTeammate( Define.TEAM_ITEM_PICKUP_RANGE )
			for mem in rangeMems:
				mem.setPosition( player.position )		#先把队员拉到自己身边
				mem.allClients.FlyToSubSpace( fPatrolID, "", sPoint, pPoint, self.flySpeed, enterPos )
		else:
			player.allClients.FlyToSubSpace( fPatrolID, "", sPoint, pPoint, self.flySpeed, enterPos )
		self.addTimerCallBack( self.getScript().flyDelayTime, "onPlayTalkVoice", ())
		self.addTimerCallBack( 6.0, "onStopStory", ())

	def onStopStory( self ):
		"""
		停止播放
		"""
		for playerCell in self._spaceRoles:
			playerCell.client.StopStory()
		

	def notifySpaceCopyCountChange( self, copyIsComplet ):
		"""
		发送副本通知改变计数
		"""
		if self.progress >= 3:
			self.getScript().onConditionChange( self, "", self.id, "complete", "" )
			self.progress = 0
		self.copyIsComplet = copyIsComplet
		self.firstEndFlyPlayer = True

	def onPlayTalkVoice( self ):
		"""
		起飞播放语音
		"""
		voiceID = self.getScript().getFlyVoiceID( self.talkVoiceIndex )
		for playerCell in self._spaceRoles:
			player = KBEngine.entities.get( playerCell.id, None )
			if player:
				player.showMessagePlaySound( voiceID )
		self.talkVoiceIndex += 1

	def onPlaySoundAndNotifyResult( self ):
		"""
		"""
		for player in self._spaceRoles:
			self.indexList.append( self.result)
			self.resultList.append( int(self.copyIsComplet) )
			player.client.CLIENT_MatrixMazeResult( self.indexList, self.resultList )
		self.result += 1
		
	def closeSpace( self ):
		"""
		<define method>
		关闭副本唯一入口，所有关闭副本操作（base或cell）都应该走此接口
		"""
		DEBUG_MSG("Close space(%s)! scriptID:%s."%( self.id, self.scriptID ))
		#self.clearCellAppDataBeforeClose()
		
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
	
	
