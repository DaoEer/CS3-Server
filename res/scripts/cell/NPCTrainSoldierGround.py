# -*- coding: utf-8 -*-
#
import KBEngine
import CoreInterface.NPCAmbulantInterface as NPCAmbulantInterface
import NPC
import csdefine
import Const
import Functions
import datetime
import time
import cschannel_msgs
import csstatus
import KST
import csconst
import KBEDebug

class NPCTrainSoldierGround(NPC.NPC):
	"""
	练兵场
	"""
	def __init__(self):
		self.index = self.group
		self.lineNumber = int(self.getCurrentSpaceData( Const.SPACE_DATA_LINE_NUMBER ))
		spaceEntity = self.getCurrentSpace()
		if spaceEntity and spaceEntity.getScript().getSpaceChildType() == csdefine.SPACE_TYPE_CHILD_STAND_MAP:
			spaceEntity.addTrainSoldierGroundData(self.lineNumber,self.index,self.occupyPlayerDBID,self.occupyPlayerName, self.occupyPlayerProfession ,self.declareWarState,self.declareWarTime, self.declarePlayerName,self.declarePlayerDBID,self.declarePlayerProfession )
		
		NPC.NPC.__init__( self )
		self.trainGroundType = self.getScript().getTrainGroundType()
		self.checkDeclareTrainSoldierGround()

	def CELL_onClientReady( self, srcEntityID ):
		"""
		<Expose method>
		客户端Character Actor已经准备好
		"""
		player = KBEngine.entities.get(srcEntityID,None)
		if not player or not player.getClient():
				return
		if player.clientEntity( self.id ):
			IsOwnSide = player.playerDBID == self.occupyPlayerDBID
			player.clientEntity( self.id ).CLIENT_CreateTrainSoldierGroundArea( self.scriptID, IsOwnSide )

	def setSelfEntityFlagExt(self):
		"""
		virtual method
		"""
		self.setEntityFlagExt(csdefine.ENTITY_FLAG_EXT_NPC_TRAINSOLDIERGROUND)

	def getIndex( self ):
		return self.index

	def getLineNumber( self ):
		return self.lineNumber

	def getTrainGroundType( self ):
		return self.trainGroundType

	def getOccupyPlayerDBID( self ):
		"""
		"""
		return self.occupyPlayerDBID

	def getDeclareWarDBID( self ):
		"""
		"""
		return self.declarePlayerDBID

	def setOccupyData( self, occupyPlayerDBID, occupyPlayerName, occupyPlayerProfession ):
		"""
		设置被占领的数据
		"""
		self.occupyPlayerDBID = occupyPlayerDBID
		self.occupyPlayerName = occupyPlayerName
		self.occupyPlayerProfession = occupyPlayerProfession
		self.setDclareWarState( csdefine.NPCTRAINSOLDIERGROUND_STATE_CAN_BE_DECLARE )

	def setDclareWarState( self, declareWarState ):
		"""
		设置练兵场状态
		"""
		self.declareWarState = declareWarState
		if self.declareWarState == csdefine.NPCTRAINSOLDIERGROUND_STATE_CAN_BE_DECLARE:
			self.declareWarTime = 0
			self.fightEndTime = ""
			self.notifyFightTime = ""
			self.declarePlayerDBID = 0
			self.declarePlayerName = ""
			self.declarePlayerProfession = 0

	def setDeclareWarTime( self ):
		"""
		设置宣战的时间
		"""
		self.setDclareWarState( csdefine.NPCTRAINSOLDIERGROUND_STATE_CAN_NOT_BE_DECLARE )
		self.declareWarTime = Functions.getTime()

	def getPackTrainGroundData( self ):
		"""
		"""
		dict = {}
		dict["occupyPlayerDBID"] = self.occupyPlayerDBID
		dict["occupyPlayerName"] = self.occupyPlayerName
		dict["occupyPlayerProfession"] = self.occupyPlayerProfession
		dict["declarePlayerName"] = self.declarePlayerName
		dict["declarePlayerDBID"] = self.declarePlayerDBID
		dict["declarePlayerProfession"] = self.declarePlayerProfession
		return dict

	def setDeclareWarData( self, declarePlayerName, declarePlayerDBID, declarePlayerProfession ):
		"""
		设置宣战的数据
		"""
		self.declarePlayerName = declarePlayerName
		self.declarePlayerDBID = declarePlayerDBID
		self.declarePlayerProfession = declarePlayerProfession
		self.setDeclareWarTime()
		spaceEntity = self.getCurrentSpace()
		if spaceEntity and spaceEntity.getScript().getSpaceChildType() == csdefine.SPACE_TYPE_CHILD_STAND_MAP:
			spaceEntity.updateDeclareTrainSoldierGroundData( self.index,self.lineNumber,self.declarePlayerDBID, self.declarePlayerName, self.declarePlayerProfession, self.declareWarTime,self.declareWarState )

	def clearDeclareWarData( self ):
		"""
		清除宣战的数据
		"""
		self.setDclareWarState( csdefine.NPCTRAINSOLDIERGROUND_STATE_CAN_BE_DECLARE )
		spaceEntity = self.getCurrentSpace()
		if spaceEntity and spaceEntity.getScript().getSpaceChildType() == csdefine.SPACE_TYPE_CHILD_STAND_MAP:
			spaceEntity.updateDeclareTrainSoldierGroundData( self.index,self.lineNumber,self.declarePlayerDBID, self.declarePlayerName, self.declarePlayerProfession, self.declareWarTime,self.declareWarState )

	def declareTrainSoldierGround( self, playerID ):
		"""
		跟练兵场 宣战
		"""
		if self.declareWarState != csdefine.NPCTRAINSOLDIERGROUND_STATE_CAN_BE_DECLARE:
			return
		if datetime.datetime.now().hour < self.getScript().getStartHour() or datetime.datetime.now().hour > self.getScript().getEndHour():
			return
		player = KBEngine.entities.get( playerID,None)
		if not player:
			return
		if player.getIsDeclareWar():
			return
		if self.occupyPlayerDBID == player.playerDBID:
			return
		if self.occupyPlayerDBID <= 0:
			if self.trainGroundType == csdefine.NPCTRAINSOLDIERGROUND_TYPE_LOW_LEVEL:
				self.setDeclareWarData( player.getName(), player.playerDBID,player.getProfession() )
				player.setIsDeclareWar( True )
				spaceName = self.getScript().getEnterPVESpace()
				player.sendIsJoinDeclareWarMsg( self.lineNumber, self.index, spaceName, self, self.occupyPlayerDBID,self.trainGroundType,self.getUname(),self.getPackTrainGroundData() )
			elif self.trainGroundType == csdefine.NPCTRAINSOLDIERGROUND_TYPE_MIDDLE_LEVEL or self.trainGroundType == csdefine.NPCTRAINSOLDIERGROUND_TYPE_HIGH_LEVEL:
				if not player.isOccupyTrain( self.getScript().getRequireOccupyType() ):
					player.statusMessage( csstatus.TRAIN_SOLDIER_GROUND_DECLAR_FORBIG_TRAINTYPE,"" )
					return
				if player.getBindMoney() + player.getMoney() < self.getScript().getRequireMoney():
					player.statusMessage( csstatus.MONEY_NOT_ENOUGH )
					return
				player.openBarracksByOccupyTrainGround(self.id, self.getScript().getRequireSoldierAmount(),self.getScript().getRequireSoldierLevel())
		else:
			self.setDeclareWarData( player.getName(), player.playerDBID,player.getProfession() )
			spaceEntity = self.getCurrentSpace()
			if spaceEntity and spaceEntity.getScript().getSpaceChildType() == csdefine.SPACE_TYPE_CHILD_STAND_MAP:
				roleMB = spaceEntity.getRoleMBByPlayerDBID( self.occupyPlayerDBID )
				declareTime = Functions.convertTime( self.declareWarTime )
				dtime = datetime.datetime.fromtimestamp( declareTime )
				enterTimes = datetime.datetime( dtime.year, dtime.month, dtime.day, 0, 0,0,0 ).timestamp() + 24 * 60 * 60 + 20 * 60 * 60
				declareStr = str(dtime.month) + cschannel_msgs.MONTH + str( dtime.day ) + cschannel_msgs.DAY
				enterTime = datetime.datetime.fromtimestamp( enterTimes )
				enterStr = str(enterTime.month) + cschannel_msgs.MONTH + str( enterTime.day) + cschannel_msgs.DAY
				self.notifyFightTime = str(int(enterTimes) * csconst.TIME_ENLARGE_MULTIPLE)
				self.checkDeclareTrainSoldierGround()
				self.openTrainSoldierGroundDetails(player)
				if roleMB == None:
					KBEngine.globalData["TrainSoldierGroundManager"].notifyOccupyPlayer( self.occupyPlayerDBID, declareStr, enterStr, self.declarePlayerName )
					return
				roleMB.statusMessage( csstatus.TRAIN_SOLDIER_GROUND_DECLARWAR_MSG, declareStr, self.declarePlayerName, enterStr )

	def cancelDeclareTrainSoldierGround( self, playerID ):
		"""
		取消练兵场宣战
		"""
		if self.declareWarState != csdefine.NPCTRAINSOLDIERGROUND_STATE_CAN_NOT_BE_DECLARE:
			return
		if datetime.datetime.now().hour < self.getScript().getStartHour() or datetime.datetime.now().hour > self.getScript().getEndHour():
			return
		player = KBEngine.entities.get( playerID,None)
		if not player:
			return
		if self.declarePlayerDBID != player.playerDBID:
			return
		self.clearDeclareWarData()
		player.setIsDeclareWar( False )

	def checkDeclareTrainSoldierGround( self ):
		"""
		检查练兵场宣战
		"""
		if self.declareWarTime <= 0:
			self.clearDeclareWarData()
			return
		if not self.notifyFightTime:
			self.clearDeclareWarData()
			return
		# declareTime = Functions.convertTime( self.declareWarTime )
		# dectime = datetime.datetime.fromtimestamp( declareTime )
		# hour = self.getScript().getStartHour()
		# endTime = datetime.datetime( dectime.year, dectime.month, dectime.day, hour, 0,0,0 ).timestamp() + 24 * 59 * 60
		notifyFightTime = Functions.convertTime(  int(self.notifyFightTime) )
		remainTime = int( notifyFightTime ) - time.time() - 60 #提前60秒提示
		if remainTime > 0:
			if self.notifyID > 0:
				self.popTimer( self.notifyID )
				self.notifyID = 0
			self.notifyID = self.addTimerCallBack( remainTime, "notifyDeclareWarPlayer",() )
		else:
			self.clearDeclareWarData()

	def notifyDeclareWarPlayer( self ):
		"""
		提醒宣战的玩家
		"""
		spaceEntity = self.getCurrentSpace()
		if spaceEntity and spaceEntity.getScript().getSpaceChildType() == csdefine.SPACE_TYPE_CHILD_STAND_MAP:
			if self.occupyPlayerDBID > 0:
				spaceName = self.getScript().getEnterPVPSpace()
			else:
				spaceName = self.getScript().getEnterPVESpace()
			roleMB = spaceEntity.getRoleMBByPlayerDBID( self.declarePlayerDBID )
			if roleMB == None:
				KBEngine.globalData["TrainSoldierGroundManager"].notifyDeclareWarPlayer( self.lineNumber, self.index, spaceName, self.declarePlayerDBID, self, self.occupyPlayerDBID,self.trainGroundType,self.getUname(),self.getPackTrainGroundData() )
			else:
				# 发送争夺练兵场提示框
				roleMB.sendIsJoinDeclareWarMsg( self.lineNumber, self.index, spaceName, self, self.occupyPlayerDBID,self.trainGroundType,self.getUname(),self.getPackTrainGroundData() )

			if self.occupyPlayerDBID > 0:
				occupyRoleMB = spaceEntity.getRoleMBByPlayerDBID( self.occupyPlayerDBID )
				if occupyRoleMB == None:
					KBEngine.globalData["TrainSoldierGroundManager"].notifyOccupyWarPlayer( self.lineNumber, self.index, spaceName, self.occupyPlayerDBID, self, self.occupyPlayerDBID,self.trainGroundType,self.getUname(),self.getPackTrainGroundData() )
				else:
					occupyRoleMB.sendIsJoinDeclareWarMsg( self.lineNumber, self.index, spaceName, self, self.occupyPlayerDBID,self.trainGroundType,self.getUname(),self.getPackTrainGroundData() )

	def calculatFightEndTime( self, spaceScriptID ):
		"""
		计算战斗结束的时间
		"""
		spaceObj = KST.g_objFactory.getSpaceObject( spaceScriptID )
		if not spaceObj:
			return
		self.fightEndTime = str(spaceObj.getSpaceLife() * csconst.TIME_ENLARGE_MULTIPLE + Functions.getTime())

	def openTrainSoldierGroundDetails( self, player ):
		"""
		打开对话面板
		"""
		if self.declareWarState == csdefine.NPCTRAINSOLDIERGROUND_STATE_CAN_BE_DECLARE:
			if player.getClient():
				player.client.OpenTrainSoldierGroundDetails( self.getUname(), self.lineNumber, self.declareWarState,[],[],1, self.trainGroundType,self.id,self.notifyFightTime,False)
		else:
			occupyName = ""
			occupyProFession = -1
			if self.occupyPlayerDBID > 0:
				occupyName = self.occupyPlayerName
				occupyProFession = self.occupyPlayerProfession
			else:
				occupyName = self.getUname()
			declareName = ""
			declareProfession = -1
			isCanClickCancelDec = player.playerDBID == self.declarePlayerDBID
			if self.declarePlayerDBID > 0:
				declareName = self.declarePlayerName
				declareProfession = self.declarePlayerProfession
			if player.getClient():
				player.client.OpenTrainSoldierGroundDetails( self.getUname(), self.lineNumber, self.declareWarState,[ declareName, occupyName ],[declareProfession,occupyProFession],1, self.trainGroundType,self.id,self.notifyFightTime,isCanClickCancelDec )

	def gmNotifyDeclareWarPlayer( self ):
		"""
		GM 命令 提示玩家参加争夺战
		"""
		if self.notifyID > 0:
			self.popTimer( self.notifyID )
			self.notifyID = 0

		self.notifyDeclareWarPlayer()
