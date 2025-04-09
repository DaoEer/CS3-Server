# -*- coding: utf-8 -*-

import KBEDebug
from SpaceCopy import SpaceCopy
import csdefine
import Const
import KBEMath
import Math
import csstatus

class SpaceCopyThirdTongStarcraft( SpaceCopy ):
	"""
	帮会争霸 第三场
	"""
	def __init__( self ) :
		SpaceCopy.__init__( self )
		self.camp = self.createArgs["camp"]
		self.tongSide = {}
		self.tongSignUpPlayerDBIDs = {}
		self.integralTimer = {}	#增加积分的Timer
		self.checkTimer = {}	#检测是否有玩家的Timer
		self.readyToDelIntegralTimer = {}	#准备移除增加积分的Timer
		self.occupySpellBoxDict = {}	# 红方:[boxScriptID,] 蓝方:[boxScriptID]
	
	def signUpThirdStarcraftField( self, tongDBID, playerDBID,player,signUpSuccSound,fullSound ):
		"""
		报名第三场内场
		"""
		if tongDBID not in self.tongSignUpPlayerDBIDs:
			self.tongSignUpPlayerDBIDs[tongDBID] = []
		signUpPlayerDBIDs = self.tongSignUpPlayerDBIDs[tongDBID]
		if len( signUpPlayerDBIDs ) >= self.getScript().getLimitEnterFieldNumber():
			player.showMessagePlaySound( fullSound )
			return
		if len(signUpPlayerDBIDs) < self.getScript().getLimitEnterFieldNumber() and playerDBID not in signUpPlayerDBIDs:
			self.tongSignUpPlayerDBIDs[tongDBID].append(playerDBID)
			player.showMessagePlaySound( signUpSuccSound )

	def teleportEnterField( self ):
		"""
		传送报名人员进入内场
		"""
		for tongDBID, signUpPlayerDBIDs in self.tongSignUpPlayerDBIDs.items():
			for playerDBID in signUpPlayerDBIDs:
				index = signUpPlayerDBIDs.index(playerDBID)
				member = self.warInfos.getMember( tongDBID, playerDBID )
				if not member:
					continue
				index = index//2
				if self.tongSide.get( tongDBID,0 ) == csdefine.TONG_BELONG_RED_SIDE:
					enterPos,enterDir = self.getScript().getEntrFieldInfoByIndex( index * 2 )
				else:
					enterPos,enterDir = self.getScript().getEntrFieldInfoByIndex( (index * 2 + 1) )
				member.roleMB.actCounterInc( csdefine.ACTION_FORBID_USE_ITEM )
				if member.roleMB.getAllClients():
					member.roleMB.changeDirection(enterDir, csdefine.REASON_CHANGE_DIR_FORCE)
					member.roleMB.allClients.TeleportToDstPosition(Math.Vector3(KBEMath.KBEngine2UnrealPosition(tuple(enterPos))))

	def fieldFightEnd( self,value ):
		"""
		内场战斗结束
		value 增加的积分值
		"""
		for tongDBID, signUpPlayerDBIDs in self.tongSignUpPlayerDBIDs.items():
			for playerDBID in signUpPlayerDBIDs:
				self.addTongIntegral( tongDBID, value )
				member = self.warInfos.getMember( tongDBID, playerDBID )
				if not member:
					continue
				member.roleMB.actCounterDec( csdefine.ACTION_FORBID_USE_ITEM )

		self.tongSignUpPlayerDBIDs = {}

	def addTongIntegral( self, tongDBID, value ):
		"""
		给某个帮会增加积分
		"""
		self.getScript().addTongIntegral( self, tongDBID, value )

	def occupySpellBox( self, boxScriptID, player ):
		"""
		占领水晶 同一方是不会重复占领水晶
		"""
		time = self.getScript().addIntegralTimer
		integral = self.getScript().addIntegral
		checkTime = self.getScript().checkAddIntegralTimer
		checkRange = self.getScript().checkAddIntegralRange
		side = self.tongSide[player.tongDBID]

		if side == csdefine.TONG_BELONG_RED_SIDE:
			buffID = self.getScript().redSideAddBuffID
			needRemoveBuffID = self.getScript().buleSideAddBuffID
			enemySide = csdefine.TONG_BELONG_BLUE_SIDE
		else:
			buffID = self.getScript().buleSideAddBuffID
			needRemoveBuffID = self.getScript().redSideAddBuffID
			enemySide = csdefine.TONG_BELONG_RED_SIDE
		boxEntityList = self.getEntityMailBoxRecord( boxScriptID )
		for boxEntity in boxEntityList:
			if boxEntity.findBuffsByBuffID( needRemoveBuffID ):
				boxEntity.removeBuffByID( needRemoveBuffID )
			boxEntity.addBuff( boxEntity, buffID )
		if boxScriptID in self.integralTimer:
			timer = self.integralTimer[boxScriptID]
			self.popTimer(timer)
			del self.integralTimer[boxScriptID]
		if boxScriptID in self.checkTimer:
			timer = self.checkTimer[boxScriptID]
			self.popTimer(timer)
			del self.checkTimer[boxScriptID]
		if boxScriptID in self.readyToDelIntegralTimer:
			self.popTimer( self.readyToDelIntegralTimer[boxScriptID] )
			del self.readyToDelIntegralTimer[boxScriptID]
		if enemySide in self.occupySpellBoxDict and boxScriptID in self.occupySpellBoxDict[enemySide]:
			self.occupySpellBoxDict[enemySide].remove(boxScriptID)
			self.notifyClientRemoveOccupySpellBox( enemySide, boxScriptID )
			statusID = csstatus.THIRD_TONG_STARCRAFT_BEOCCUPY_SPAR
		else:
			statusID = csstatus.THIRD_TONG_STARCRAFT_OCCUPY_SPAR

		timerID = self.addTimerRepeat(time,"addTongIntegral",(player.tongDBID,integral))
		checkTimerID = self.addTimerRepeat(checkTime,"checkHasPlayer",(player.tongDBID,checkRange,boxScriptID,side)  )
		self.integralTimer[boxScriptID] = timerID
		self.checkTimer[boxScriptID] = checkTimerID
		if side not in self.occupySpellBoxDict:
			self.occupySpellBoxDict[side] = []
		self.occupySpellBoxDict[side].append(boxScriptID)
		self.notifyClientAddOccupySpellBox( side, boxScriptID )
		self.addTongMemberOccupy( player.tongDBID,player )
		if player.tongDBID not in self.warInfos.keys():
			return
		tong = self.warInfos[player.tongDBID]
		for mem in self.warInfos.getMembers():
			mem.roleMB.statusMessage( statusID,tong.tongName )

	def checkHasPlayer( self, tongDBID, checkRange,boxScriptID,side ):
		"""
		检查某个范围内是否有某个帮会的玩家
		"""
		boxEntitys = self.getEntityMailBoxRecord( boxScriptID )
		if not len(boxEntitys):
			self.delAddIntegralAndCheckTimer(boxScriptID,side)
			return
		roleList = boxEntitys[0].entitiesInRangeExtCircle( checkRange, "Role" )
		isFindBelongTongRole = False
		for role in roleList:
			if role.tongDBID == tongDBID and role.getState() != csdefine.ENTITY_STATE_DEAD:
				isFindBelongTongRole = True
				break
		if not isFindBelongTongRole:
			if boxScriptID not in self.readyToDelIntegralTimer:
				timerID = self.addTimerCallBack(10.0,"delAddIntegralAndCheckTimer",(boxScriptID,side))
				self.readyToDelIntegralTimer[boxScriptID] = timerID
		else:
			if boxScriptID in self.readyToDelIntegralTimer:
				timerID = self.readyToDelIntegralTimer[boxScriptID]
				self.popTimer(timerID)
				del self.readyToDelIntegralTimer[boxScriptID]

	def delAddIntegralAndCheckTimer( self, boxScriptID, side ):
		"""
		删除增加积分的timer和检查的timer
		"""
		if boxScriptID in self.integralTimer:
			self.popTimer( self.integralTimer[boxScriptID] )
			del self.integralTimer[boxScriptID]
		if boxScriptID in self.checkTimer:
			self.popTimer( self.checkTimer[boxScriptID] )
			del self.checkTimer[boxScriptID]
		if boxScriptID in self.readyToDelIntegralTimer:
			self.popTimer( self.readyToDelIntegralTimer[boxScriptID] )
			del self.readyToDelIntegralTimer[boxScriptID]
		if side in self.occupySpellBoxDict and boxScriptID in self.occupySpellBoxDict[side]:
			self.occupySpellBoxDict[side].remove(boxScriptID)
			self.notifyClientRemoveOccupySpellBox( side, boxScriptID )

		if side == csdefine.TONG_BELONG_RED_SIDE:
			buffID = self.getScript().redSideAddBuffID
		else:
			buffID = self.getScript().buleSideAddBuffID
		boxEntitys = self.getEntityMailBoxRecord( boxScriptID )
		if len(boxEntitys):
			boxEntitys[0].removeTemp("belongTongDIBD")
			boxEntitys[0].removeBuffByID(buffID)
			boxEntitys[0].removeTemp("gossipTong")
			boxEntitys[0].allClients.CLIENT_RefreshBoxStatus()

	def notifyClientAddOccupySpellBox( self, side, boxScriptID ):
		"""
		通知客户端 增加占领某个水晶
		"""
		for player in self._spaceRoles:
			if player.getClient():
				player.client.CLIENT_AddThirdTongStarcraftOccupySpellBox( side, boxScriptID )

	def notifyClientRemoveOccupySpellBox( self, side, boxScriptID ):
		"""
		通知客户端 移除占领某个水晶
		"""
		for player in self._spaceRoles:
			if player.getClient():
				player.client.CLIENT_RemoveThirdTongStarcraftOccupySpellBox( side, boxScriptID )

	def notifyClientAllOccupySpellBox( self, player ):
		"""
		通知客户端 所有占领的数据
		"""
		for side, boxScriptIDs in self.occupySpellBoxDict.items():
			if not len(boxScriptIDs):
				continue
			player.client.CLIENT_ReceiveThirdTongStarcraftAllOccupySpellBox( side, boxScriptIDs )

	def getReviveInfoByTongDBID( self, tongDBID ):
		"""
		获得某一方的复活点
		"""
		return self.getScript().getReviveInfoBySide(self.tongSide.get(tongDBID,0))

	def kill( self, killTongDBID, killRole,dieTongDBID,dieRole ):
		"""
		击杀
		"""
		if killTongDBID in self.tongSignUpPlayerDBIDs and killRole.playerDBID in self.tongSignUpPlayerDBIDs[killTongDBID]:
			return
		self.warInfos.kill( killTongDBID, killRole,dieTongDBID,dieRole )

	def addTongMemberAssists( self, killRole,tongDBID, assistsRole ):
		"""
		增加帮会成员的助攻数
		"""
		if tongDBID in self.tongSignUpPlayerDBIDs and killRole.playerDBID in self.tongSignUpPlayerDBIDs[tongDBID]:
			return
		self.warInfos.addTongMemberAssists( tongDBID, assistsRole )

	def addTongMemberOccupy( self, tongDBID, occupyRole ):
		"""
		增加帮会成员的水晶占领数
		"""
		self.warInfos.addTongMemberOccupy( tongDBID, occupyRole )
