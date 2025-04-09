# -*- coding: utf-8 -*-


from ObjectScript.Space.SpaceCopy import SpaceCopy
import KBEDebug
import Define
import Functions
import csdefine
import time
import KBEngine
import Const
import KBEMath
import Math
import csstatus

class SpaceCopySecondTongStarcraft( SpaceCopy ):
	"""
	帮会争霸 第二场
	"""
	def __init__( self ):
		SpaceCopy.__init__( self )
		self.reviveInfos = []
		self.delyCloseTime = 0.0
		self.thirdSpaceName = ""
		self.thirdEnterPos = Math.Vector3(0,0,0)
		self.thirdEnterDir = Math.Vector3(0,0,0)
		self.thirdSide = csdefine.TONG_BELONG_RED_SIDE	#哪一方 红方:0 or蓝方:1
		
	def initData( self, configData ):
		"""
		virtual method
		"""
		SpaceCopy.initData( self, configData )
		
		self.delyCloseTime = configData["SpaceData"].get("delyCloseTime",0.0)
		self.thirdSpaceName = configData["SpaceData"].get( "thirdSpaceName","" )
		thirdEnterPosStr = configData["SpaceData"].get( "thirdEnterPos","" )
		thirdEnterPos = Functions.vector3TypeConvert(thirdEnterPosStr)
		self.thirdEnterPos = KBEMath.Unreal2KBEnginePosition(tuple(thirdEnterPos))
		thirdEnterDirStr = configData["SpaceData"].get( "thirdEnterDir","" )
		thirdEnterDir = Functions.vector3TypeConvert(thirdEnterDirStr)
		self.thirdEnterDir = KBEMath.Unreal2KBEnginePosition(tuple(thirdEnterDir))
		thirdSide = configData["SpaceData"].get("thirdSide",0)
		if thirdSide == csdefine.TONG_BELONG_BLUE_SIDE:
			self.thirdSide = csdefine.TONG_BELONG_BLUE_SIDE
		else:
			self.thirdSide = csdefine.TONG_BELONG_RED_SIDE

		enterPosInfos = configData["SpaceData"].get("enterPosList","").split("|")
		enterDirInfos = configData["SpaceData"].get("enterDirList","").split("|")
		enterPosList = []
		enterDirList = []
		for enterPosInfo in enterPosInfos:
			pos = Functions.vector3TypeConvert(enterPosInfo)
			pos = KBEMath.Unreal2KBEnginePosition( tuple(pos) )
			enterPosList.append(pos)

		for enterDirInfo in enterDirInfos:
			dir = Functions.vector3TypeConvert(enterDirInfo)
			dir = KBEMath.Unreal2KBEnginePosition( tuple(dir) )
			enterDirList.append(dir)
		for i in range(0,len(enterPosList)):
			self.reviveInfos.append( (Math.Vector3(enterPosList[i]), Math.Vector3(enterDirList[i])) )

	def initEntity( self, selfEntity ):
		"""
		virtual method
		初始化space entity要做的事情
		"""
		SpaceCopy.initEntity( self, selfEntity )
		selfEntity.addTimerCallBackForScript(self.spaceLife,"onSpaceLifeEnd",())

	def startSpaceLife( self, selfEntity ):
		"""
		开始计时
		"""
		spaceLifeSecond = self.spaceLife + self.delyCloseTime
		selfEntity.lifeTime = self.spaceLife		# 副本时长
		selfEntity.lifeStartTime = time.time()		# 副本计时开始时间
		selfEntity.lifeTimer = selfEntity.addTimerCallBack( spaceLifeSecond, "closeSpace", () )
		selfEntity.addTimerCallBackForScript( spaceLifeSecond - 2, "onTeleportToThirdStarcraft",() )
		selfEntity.lifeNotifyTimer = selfEntity.addTimerCallBackForScript( spaceLifeSecond - Const.SPACE_LIFE_NOTIFY_TIME, "showTimeCountDown", ( csstatus.SPACE_CLOSE_NOTIFY, Const.SPACE_LIFE_NOTIFY_TIME ) )
		for e in selfEntity._spaceRoles:
			e.client.ShowSpaceLife( str(spaceLifeSecond * csconst.TIME_ENLARGE_MULTIPLE + Functions.getTime()), self.isSpaceLifeMoveDown,str( Functions.getTime() ))


	def onSpaceLifeEnd( self, selfEntity ):
		"""
		副本时间到达
		"""
		firstTong = selfEntity.warInfos.getFirstTong()
		for member in selfEntity.warInfos.getMembers():
			member.mailbox.statusMessage( csstatus.TONG_STARCRAFT_SECOND_FIRST_TONG, firstTong.tongName )
		KBEngine.globalData["TongStarcraftManager"].tongStarcraft_ThirdSignUp(selfEntity.camp,firstTong.tongDBID,firstTong.tongName )

	def onTeleportToThirdStarcraft( self, selfEntity ):
		"""
		传送到第三场
		"""
		firstTong = selfEntity.warInfos.getFirstTong()
		members = firstTong.getMembers()
		memberInfos = []
		for member in members:
			memberInfos.append(member.mailbox.base)
		KBEngine.globalData["TongStarcraftManager"].tongStarcraft_gotoThirdStarcraft( selfEntity.camp,firstTong.tongDBID,self.thirdSide,self.thirdSpaceName,self.thirdEnterPos,self.thirdEnterDir,memberInfos )

	def setReviveType( self ):
		"""
		设置复活类型
		"""
		pass

	def getEnterInfo( self, selfEntity,tongDBID ):
		"""
		获得复活信息
		"""
		tongDBIDs = [int(i) for i in selfEntity.spaceKey.split("|")]
		if tongDBID in tongDBIDs:
			index = tongDBIDs.index(tongDBID)
			return self.reviveInfos[index]
		return None

	def onEnter( self, selfEntity, playerRole, packArgs ):
		SpaceCopy.onEnter( self, selfEntity, playerRole, packArgs )
		member = selfEntity.warInfos.getMember( playerRole.tongDBID, playerRole.playerDBID )
		if member:
			if not member.getIsCanFight():
				playerRole.addBuff( playerRole, Const.TONG_STARCRAFT_WATCH_BUFF )
		selfEntity.warInfos.addMember( packArgs["tongDBID"], packArgs["tongName"],packArgs["playerDBID"],playerRole,1)
		
