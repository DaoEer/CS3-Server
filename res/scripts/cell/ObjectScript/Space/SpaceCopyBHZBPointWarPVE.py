# -*- coding: utf-8 -*-


from ObjectScript.Space.SpaceCopyAttackCityWar import SpaceCopyAttackCityWar
import csdefine
import KBEngine
import Functions
import KBEMath
from ObjectScript.Space.SpaceCopy import SpaceCopy
import csstatus
import Define
import KBEDebug

class SpaceCopyBHZBPointWarPVE( SpaceCopyAttackCityWar ):
	"""
	帮会争霸 据点争夺战 PVE
	"""
	def __init__( self ):
		SpaceCopyAttackCityWar.__init__( self )
		self.enterProtectInfo = ()	# 进入防守方的位置
		self.enterAttackInfo = ()	# 进入进攻方位置数据
		self.rewardIntegral = 0 	# 增加的积分值
		self.rewardRepeatIntegral = 0 #持续增加的积分值
		self.rewardRepeatTime = 0.0 # 持续增加时间
		self.addRewardExp = 0 # 增加经验值

	def initData( self, configData ):
		"""
		virtual method
		"""
		SpaceCopyAttackCityWar.initData( self, configData )
		if configData["SpaceData"].get("enterPos",""):
			enterPosInfos = configData["SpaceData"].get("enterPos","").split("|")
			enterDirInfos = configData["SpaceData"].get("enterDir","").split("|")
			enterPosList = []
			enterDirList = []
			for enterPosInfo in enterPosInfos:
				pos = Functions.vector3TypeConvert(enterPosInfo)
				pos = KBEMath.Unreal2KBEnginePosition( pos )
				enterPosList.append(pos)

			for enterDirInfo in enterDirInfos:
				dir = Functions.vector3TypeConvert(enterDirInfo)
				dir = KBEMath.Unreal2KBEngineDirection( dir )
				enterDirList.append(dir)
			self.enterAttackInfo = (enterPosList[0],enterDirList[0] )
			if len(enterPosList) > 1 and len( enterDirList ) > 1:
				self.enterProtectInfo = (enterPosList[1],enterDirList[1] )

		self.rewardIntegral = configData["SpaceData"].get("rewardIntegral", 0)
		self.rewardRepeatIntegral = configData["SpaceData"].get("rewardRepeatIntegral",0)
		self.rewardRepeatTime = float(configData["SpaceData"].get("rewardRepeatTime",0.0))
		self.addRewardExp = configData["SpaceData"].get("addRewardExp",0)

	def getProtectEnterInfo( self ):
		"""
		获得防守方的进入信息
		"""
		return self.enterProtectInfo

	def getAttackEnterInfo( self ):
		"""
		获得进攻方的进入信息
		"""
		return self.enterAttackInfo

	def getRewardIntegral( self ):
		return self.rewardIntegral

	def getRewardRepeatIntegral( self ):
		return self.rewardRepeatIntegral

	def getRewardRepeatTime( self ):
		return self.rewardRepeatTime

	def getAddRewardExp( self ):
		return self.addRewardExp

	def addEntityMailBoxRecord( self, selfEntity,scriptID, entityMailBox ):
		"""
		"""
		if scriptID in self.notReviveBossScriptID:
			member = selfEntity.GCZMemberDatas.getMemberByName( entityMailBox.getUname() )
			if member == None:
				selfEntity.addGCZMember( entityMailBox.id, entityMailBox, entityMailBox.getUname(), csdefine.BELONG_SIDE_PROTECT, selfEntity.createArgs.get("pointName",""),"" )

		if scriptID in self.commonMonsterScriptIDs:
			if self.commonMonsterScriptIDs.index(scriptID) == 0:
				selfEntity.addGCZMember( 0, entityMailBox, entityMailBox.getUname(), csdefine.BELONG_SIDE_PROTECT, selfEntity.createArgs.get("pointName",""),"" )

	def onEnter( self, selfEntity, playerRole, packArgs ):
		SpaceCopy.onEnter( self, selfEntity, playerRole, packArgs )
		playerRole.setBelongSide( csdefine.BELONG_SIDE_ATTACK )
		selfEntity.addGCZMember( playerRole.playerDBID,playerRole,playerRole.getName(), csdefine.BELONG_SIDE_ATTACK, selfEntity.createArgs.get("pointName",""), playerRole.tongName)
		playerRole.setTemp("isEnter",True)
		selfEntity.delayTransferDataToClient( playerRole )

	def onLogin( self, selfEntity, playerRole ):
		"""
		"""
		SpaceCopy.onLogin( self, selfEntity, playerRole )
		playerRole.setBelongSide( csdefine.BELONG_SIDE_ATTACK )
		selfEntity.addGCZMember( playerRole.playerDBID,playerRole,playerRole.getName(), csdefine.BELONG_SIDE_ATTACK, selfEntity.createArgs.get("pointName",""), playerRole.tongName)
		selfEntity.delayTransferDataToClient( playerRole )
		
	def onTeleportCompleted( self, selfEntity, playerRole ):
		"""
		"""
		SpaceCopyAttackCityWar.onTeleportCompleted( self, selfEntity, playerRole )
		if playerRole.queryTemp("isEnter",False):
			playerRole.statusMessage( csstatus.BHZB_ATTACK_PVEPOINT, selfEntity.createArgs.get("declareTongName",""),selfEntity.createArgs.get("pointName","") )
			playerRole.removeTemp("isEnter")

	def getPackDomainData( self, playerEntity, args ):
		"""
		"""
		packDict = SpaceCopy.getPackDomainData( self, playerEntity, args )
		camp = packDict["camp"]
		pointIndex = packDict["pointIndex"]
		occupyTongDBID = packDict["belongTongDBID"]
		packDict["spaceKey"] = "{0}|{1}".format(pointIndex, occupyTongDBID )
		return packDict

	def getReviveToExitInfo( self, playerRole ):
		KBEngine.globalData["BHZBManager"].onRoleLoginBHZB( playerRole.getCamp(),playerRole.tongDBID, playerRole.playerDBID,playerRole.base, playerRole.captainID )	
		KBEDebug.INFO_MSG("player(%s playerDBID = %d) exit SpaceCopyBHZBPointWarPVE"%(playerRole.getName(),playerRole.playerDBID) )
		return (self._exitScriptID, self._exitPosition, self._exitDirection )

	def onLastPlayerLeave( self, selfEntity, playerRole, packArgs ):
		"""
		virtual method
		最后一个玩家离开副本
		"""
		SpaceCopy.onLastPlayerLeave( self, selfEntity, playerRole, packArgs )
		if packArgs[ "leaveReason" ] == Define.LEAVE_SPACE_REASON_TELEPORT:
			if not selfEntity.isShowSettlementWnd:
				selfEntity.bhzbPointWarEnd()
				selfEntity.addTimerCallBack(1.0,"closeSpace",())
