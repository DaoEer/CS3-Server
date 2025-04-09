# -*- coding: utf-8 -*-

import KBEngine
import KST
import Math
import math
import KBEMath
import Math
import Define
import Const
import csstatus
import csconst
import time

import LogDefine
from MsgLogger import g_logger
from KBEDebug import *
from CoreInterface import RoleSpaceEffectInterface
from CoreInterface import RolePetInterface
from CoreInterface import RoleCompeteInterface
from CoreInterface import RoleTradeInterface
from CoreInterface import RoleCallEntityInterface
import Functions

class RoleSpaceInterface( RoleSpaceEffectInterface.RoleSpaceEffectInterface ):
	def __init__( self ):
		RoleSpaceEffectInterface.RoleSpaceEffectInterface.__init__( self )
		self.isTeleporting = False

	def setTabDistance(self, value):
		"""
		设置tab键选中距离
		"""
		if value >= 0:
			self.tabDistance = value

	def doEnterSpace( self ):
		"""
		进入一个空间调用
		"""
		self.isSpaceGone = True		#恢复此标志

	def doLeaveSpace( self ):
		"""
		离开一个空间调用（在doEnterSpace之后）
		"""
		pass

	def onEnterSpaceNotify( self, packArgs ):
		"""
		<define method>
		进入某地图
		"""
		self.isTeleporting = False
		self.addTeleportBuff()

		#服务器准备完成取消未决状态
		if self.state == csdefine.ENTITY_STATE_PEAD:
			self.changeState( csdefine.ENTITY_STATE_FREE )

		self.onEnterSpaceScriptNotify(packArgs)

	def onEnterSpaceScriptNotify( self, packArgs ):
		RoleSpaceEffectInterface.RoleSpaceEffectInterface.onEnterSpaceNotify( self, packArgs )
		RolePetInterface.RolePetInterface.onEnterSpaceNotify( self, packArgs )
		oldSpaceScriptID = self.spaceScriptID
		self.spaceScriptID = self.getCurrentSpaceScriptID()
		self.spaceBelongType = self.getCurrentSpace().belongType

		self.getCurrentSpace().onEnter( self, packArgs )
		self.revive_roleEnterSpace()
		self.tong_roleEnterSpace()

		self.spaceEvent_roleEnterSpace()
		self.client.OnEnterSpaceNotify( self.spaceScriptID, self.getCurrentSpaceObject().getSpaceType() )

		self.triggerSkillEvent( csdefine.SKILL_EVENT_SPACE_CHANGE, self.id, { "OldSpaceID" : oldSpaceScriptID, "NewSpaceID" : self.spaceScriptID,"isInNewSpace":1 } )
		self.setClientWalkOffLedges()

	def addTeleportBuff( self ):
		"""
		增加传送保护Buff
		"""
		if self.spaceScriptID != "":
			spaceObj = KST.g_objFactory.getSpaceObject( self.spaceScriptID )
			if spaceObj.getSpaceType() != csdefine.SPACE_TYPE_PLANE:		#进入位面不加保护buff（CST-1857）
				self.addBuff(self, csconst.TELEPORT_PROTECT_BUFFID)	 #添加传送保护buff

	def _onEnterArea( self ):
		"""同地图传送"""
		self.client.OnEnterAreaNotify()
		self.revive_roleEnterSpace()
		self.tong_roleEnterSpace()

	def onLeaveSpaceNotify( self, reason, dstSpaceScriptID, packArgs ):
		"""
		离开某地图
		"""
		self.isTeleporting = True
		self.clearEnemyList()

		if self.getState() != csdefine.ENTITY_STATE_PEAD and self.getState() != csdefine.ENTITY_STATE_DEAD:	#死亡状态传送时将不会加上未决状态
			self.changeState( csdefine.ENTITY_STATE_PEAD )
		if self.vehicleId:
			self.processVehicle()
		self.onLeaveSpaceScriptNotify(reason, dstSpaceScriptID, packArgs)

	def onLeaveSpaceScriptNotify( self, reason, dstSpaceScriptID, packArgs ):
		RoleSpaceEffectInterface.RoleSpaceEffectInterface.onLeaveSpaceNotify( self, reason, dstSpaceScriptID, packArgs )
		RoleCompeteInterface.RoleCompeteInterface.onLeaveSpaceNotify(self)
		RoleTradeInterface.RoleTradeInterface.onLeaveSpaceNotify(self)
		RoleCallEntityInterface.RoleCallEntityInterface.onLeaveSpaceNotify(self)
		self.triggerSkillEvent( csdefine.SKILL_EVENT_SPACE_CHANGE, self.id, { "OldSpaceID" : self.spaceScriptID, "NewSpaceID" : dstSpaceScriptID,"isInNewSpace":0} )
		packArgs[ "leaveReason" ] = reason		# 打包离开原因，副本onLeave方法要用到
		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			spaceEntity.onLeave( self, packArgs )
		self.spaceEvent_roleLeaveSpace()

		if self.getClient():
			self.client.OnLeaveSpaceNotify(self.getCurrentSpace().scriptID, KBEngine.getSpaceData(self.spaceID, Const.SPACE_DATA_SPACE_TYPE))

		self.ChangeRoleJumpState(self.id, csdefine.JUMP_SHOW_STATE_STAND, True)

	def onLoginSpace( self ):
		"""
		<define method>
		登录地图
		"""
		RoleSpaceEffectInterface.RoleSpaceEffectInterface.onLoginSpace( self )
		self.getCurrentSpace().onLogin( self )
		self.revive_roleEnterSpace()
		self.tong_roleEnterSpace()
		self.spaceEvent_roleEnterSpace()
		self.client.OnLoginSpaceNotify( self.spaceScriptID, self.getCurrentSpaceObject().getSpaceType() )
		self.addBuff( self, csconst.TELEPORT_PROTECT_BUFFID )     #添加传送保护buff
		self.setClientWalkOffLedges()

	def gotoSpace( self, spaceScriptID, position, direction ):
		"""
		<define method>
		传送到指定地图（ 无参数 ）
		"""
		currSpaceObj = self.getCurrentSpaceObject()
		spaceObj = KST.g_objFactory.getSpaceObject(spaceScriptID)
		if spaceObj is None:
			ERROR_MSG("not found space[%s] object" %(spaceScriptID))
			return
		if spaceObj.getSpaceType() == csdefine.SPACE_TYPE_PLANE and spaceObj.isInSameBigMap( self.spaceScriptID ):
			self.requestGotoSpacePlane(self.id,spaceScriptID, KBEMath.KBEngine2UnrealPosition( position ), KBEMath.KBEngine2UnrealDirection(direction))
		elif currSpaceObj.getSpaceType() == csdefine.SPACE_TYPE_PLANE and currSpaceObj.isInSameBigMap( spaceScriptID ):
			self.requestGotoSpacePlane(self.id,spaceScriptID, KBEMath.KBEngine2UnrealPosition( position ), KBEMath.KBEngine2UnrealDirection(direction))
		else:
			self.gotoSpaceUseArg( spaceScriptID, Math.Vector3(position), direction, {} )

	def gotoSpaceUE4( self, spaceScriptID, position, direction ):
		"""
		传送到指定地图（ 使用虚幻坐标，面向 ）
		"""
		self.gotoSpaceUseArg( spaceScriptID, Math.Vector3(KBEMath.Unreal2KBEnginePosition( position )), KBEMath.Unreal2KBEngineDirection( direction ), {} )

	def gotoSpaceUseArg( self, spaceScriptID, position, direction, packArgs ):
		"""
		<define method>
		传送到指定地图（有参数）
		"""
		if self.inDestroying():
			return
		#检测能否离开当前地图
		currSpaceObj = KST.g_objFactory.getSpaceObject( self.spaceScriptID )
		result = currSpaceObj.checkLeaveEnable( self, packArgs )
		if result != csstatus.SPACE_ENTER_OR_LEAVE_OK:
			DEBUG_MSG( "Leave condition different:", result )
			self.statusMessage( result )
			return

		spaceObj = KST.g_objFactory.getSpaceObject( spaceScriptID, )
		if not spaceObj:
			DEBUG_MSG("role %s Space(%s) config not exist!"%(self.id, spaceScriptID))
			self.statusMessage( csstatus.GM_ARGS_SPACE_VALUE_ERROR,"")
			return

		result = spaceObj.checkEnterEnable(self, packArgs)
		if result != csstatus.SPACE_ENTER_OR_LEAVE_OK:
			self.statusMessage(result)
			return

		gotoArgs = spaceObj.getPackDomainData( self, packArgs ) #打包参数
		self.base.gotoSpace( spaceScriptID, Math.Vector3(position), direction, gotoArgs )


	def onGotoSpace( self, spaceScriptID, spaceCell, position, direction, packArgs ):
		"""
		<define method>
		执行传送到副本，这里由Base回调使用，不能直接用
		"""
		#处理客户端掉落数据
		self.breakFalling()
		self.teleportPlayerToSpace( spaceScriptID, spaceCell, position, direction, packArgs )

	def teleportPlayerToSpace( self, spaceScriptID, spaceCell, position, direction, packArgs ):
		"""
		传送玩家
		"""
		isSameSpace = ( self.getCurrentSpace().id == spaceCell.id )	# 目标地图id与当前地图的id相同，是相同地图传送
		if isSameSpace:
			self.teleport( spaceCell, Math.Vector3(position), direction )
			self._onEnterArea()
		else:
			self.onLeaveSpaceNotify( Define.LEAVE_SPACE_REASON_TELEPORT, spaceScriptID, packArgs )
			self.teleport( spaceCell, Math.Vector3(position), direction )
			self.onEnterSpaceNotify( packArgs )

	def onTeleportCompleted( self ):
		"""
		传送结束，场景已加载完毕
		"""
		#副本串“未通关所有副本”提示

		self.showFailureNotifyBunchSpace()
		self.getCurrentSpace().onTeleportCompleted( self )
		self.spaceEvent_roleTelCompleted()

	def showFailureNotifyBunchSpace( self ):
		"""
		副本串提示未通关所有子副本
		"""
		record = self.queryTemp( "spaceBunchFailureOutRcd", "" )
		if record:
			bunchObj = KST.g_objFactory.getBunchSpaceObject( record )
			if bunchObj:
				bunchObj.showFailureOutNotify( self )
				record = self.removeTemp( "spaceBunchFailureOutRcd" )

	def requestEntityRecodPos( self, srcEntityID, scriptID ):
		"""
		<exposed method>
		客户端请求地图中指定ScriptID的entity位置（CST-2674）
		"""
		if not self.validateClientCall( srcEntityID ):
			return

		entities = self.getCurrentSpace().getEntityDynamicPosBigMapShow( self, scriptID )
		if not len(entities):
			return

		posStr = "%s#"%scriptID
		for e in entities:

			position = KBEMath.KBEngine2UnrealPosition(e.position)
			posStr += str(position[0]) +" "+ str(position[1]) +" "+ str(position[2]) + "|"
		self.client.OnGetSpaceEntityRecordPos(posStr[:len(posStr)-1])

	def setClientWalkOffLedges(self):
		"""
		设置客户端能否离开寻路边缘
		"""
		isCanWalkOffLedges = self.getCurrentSpaceObject().getCanWalkOffLedges()
		self.client.SetCanWalkOffLedges(isCanWalkOffLedges)

	#--------------------------各种gotoSpace接口-----------------------------
	def gotoSpaceEnterPos( self, spaceScriptID, packArgs ):
		"""
		<define method>
		传送到指定地图入口处
		"""
		spaceObj = KST.g_objFactory.getSpaceObject( spaceScriptID )
		if not spaceObj:
			DEBUG_MSG("Space(%s) config not exist!"%spaceScriptID)
			self.statusMessage( csstatus.GM_ARGS_SPACE_VALUE_ERROR,"")
			return
		enterInfo = spaceObj.getEnterPosInfo()
		self.gotoSpaceUseArg( spaceScriptID, enterInfo[0], enterInfo[1], packArgs )

	def gotoExitSpacePos( self ):
		"""
		<define method>
		传送到ExitSpace配置的地图
		"""
		spaceObject = self.getCurrentSpaceObject()
		exitScriptID, exitPosition, exitDirection = spaceObject.getReviveToExitInfo( self )
		self.gotoSpace( exitScriptID, Math.Vector3(exitPosition), exitDirection )

	def gotoBindSpace( self ):
		"""
		<define method>
		传送到绑定的地图
		"""
		self.gotoSpace( self.reviveSpaceScriptID, Math.Vector3(self.revivePosition), self.reviveDirection )

	def gotoBunchSpace( self, bunchSpaceScriptID, packArgs ):
		"""
		<define method>
		进副本串
		"""
		gotoArgs = KST.g_objFactory.getBunchSpaceObject( bunchSpaceScriptID ).getPackDomainData( self, packArgs ) #打包参数
		KBEngine.globalData["BunchSpaceManager"].gotoBunchSpace( bunchSpaceScriptID, self.base, gotoArgs )

	def gotoMagicMazeExtraSpace(self, belongType, mainSpace, packArgs, spaceName):
		"""
		<define method>
		进幻阵迷宫随机副本
		"""
		gotoArgs = KST.g_objFactory.getSpaceObject( mainSpace ).getPackDomainData( self, packArgs ) #打包参数
		gotoArgs.update({"mainScriptID":mainSpace})
		KBEngine.globalData["MagicMazeSpaceManager"].gotoMagicMazeExtraSpace(belongType, self.base, gotoArgs, spaceName)

	def gotoRingTaskSpace(self, mainSpace, questID, packArgs, isSignOut ):
		"""
		<define method>
		进环任务主场景
		"""
		gotoArgs = KST.g_objFactory.getSpaceObject( mainSpace ).getPackDomainData( self, packArgs ) #打包参数
		gotoArgs["spaceKey"] = str( self.playerDBID )
		KBEngine.globalData["RingTaskSpaceMgr"].gotoRingTaskSpace( self.base, questID, gotoArgs, isSignOut )

	def requestGoToSpace( self, srcEntityID, spaceScriptID, position, direction ):
		"""
		<exposed method>
		客户端请求传送到某地图
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		self.gotoSpaceUE4(spaceScriptID, Math.Vector3(position), direction)

	def requestGotoLineNumberSpace( self, srcEntityID, lineNumber ):
		"""
		<exposed method>
		客户端请求传送到某一线地图
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		if self.getState() in [csdefine.ENTITY_STATE_STALL,csdefine.ENTITY_STATE_DEAD]:
			self.statusMessage( csstatus.STALL_STATE_NOT_CHANGE_LINE )
			self.client.CLIENT_RequestGotoLineNumberSpaceFailure()
			return
		if int(self.getCurrentSpaceData( Const.SPACE_DATA_SPACE_TYPE )) == csdefine.SPACE_TYPE_MULTILINE:
			maxLineNumber = int(self.getCurrentSpaceData(Const.SPACE_DATA_MAX_LINE_NUMBER))
			if lineNumber > maxLineNumber:
				self.statusMessage( csstatus.SPACE_LINENUMBER_IS_CLOSE )
				self.client.CLIENT_RequestGotoLineNumberSpaceFailure()
				return

		self.setTemp("lineNumber",lineNumber)
		self.gotoSpace(self.getCurrentSpaceScriptID(), self.position, self.direction)
		self.removeTemp("lineNumber")

	def requestGotoExitSpace( self, srcEntityID ):
		"""
		<exposed method>
		客户端请求传送到ExitSpace配置地图
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		spaceObject = self.getCurrentSpaceObject()
		exitScriptID, exitPosition, exitDirection = spaceObject.getReviveToExitInfo( self )
		self.gotoSpaceUseArg( exitScriptID, exitPosition, exitDirection, {} )

	def clickedBtnGotoExitSpace( self, srcEntityID ):
		"""
		<exposed method>
		点击离开副本按钮客户端请求传送到ExitSpace配置地图
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		spaceObject = self.getCurrentSpaceObject()
		spaceObject.onClickedBtnGotoExitSpace(self.getCurrentSpace(), self)
		self.addCopyAbandonLog()
		if spaceObject.getCanShowFailedUI():
			self.client.CLIENT_ShowSpaceCopyFailedUI()
		exitScriptID, exitPosition, exitDirection = spaceObject.getReviveToExitInfo( self )
		self.gotoSpaceUseArg( exitScriptID, exitPosition, exitDirection, {} )

	def addCopyAbandonLog(self):
		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			startTime = int(spaceEntity.lifeStartTime)
			if startTime == 0:
				startTime = int(time.time())
			costTime = int(time.time() - startTime)
			scriptID = spaceEntity.getScript().scriptID
			g_logger.roleActiveRecord(LogDefine.ACTIVE_SPACE_TYPE_DEFAULT, self.accountDBID, self.playerDBID,
									  self.getLevel(), "", "", startTime, costTime, LogDefine.ACTIVE_STATE_TYPE_ABANDON, scriptID)


	def clickedBtnGotoExitSpaceByTongTianTa( self, srcEntityID ):
		"""
		<exposed method>
		通天塔点击离开副本按钮 客户端请求传送到ExitSpace配置地图
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		self.isChallenge = 1
		spaceObject = self.getCurrentSpaceObject()
		exitScriptID, exitPosition, exitDirection = spaceObject.getReviveToExitInfo( self )
		self.gotoSpaceUseArg( exitScriptID, exitPosition, exitDirection, {} )

	def requestGotoDynamicRevivePos( self, srcEntityID ):
		"""
		<exposed method>
		客户端请求传送到副本动态复活点
		"""
		if not self.validateClientCall( srcEntityID ):
			return

		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			dynamicReviverPos, dynamicReviverDir = spaceEntity.getDynamicReviverInfo(self.getCamp())
			self.gotoSpace( spaceEntity.scriptID, dynamicReviverPos, dynamicReviverDir )

	def requestGotoRevivePos( self, srcEntityID ):
		"""
		<exposed method>
		客户端请求传送到space文件中reviveScriptID配置的地图
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		spaceObj = self.getCurrentSpaceObject()
		enterSpace,enterPos,enterDir = spaceObj.getReviveInfo()
		self.gotoSpaceUseArg( enterSpace, enterPos, enterDir, {} )

	def testGoToSpace(self, srcEntityID):
		"""
		<exposed method>
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		INFO_MSG("testGoToSpace, spaceScriptID[%s]"%self.spaceScriptID)
		if self.spaceScriptID == "bigmap_1":
			self.gotoSpace("L_YXG", Math.Vector3(-49.6, 12.820, -9.50), Math.Vector3(0.0, 0,0, 0,0))
		elif self.spaceScriptID == "L_YXG":
			self.gotoSpace("bigmap_1", Math.Vector3(-519.0, -13.08, 494.5), Math.Vector3(0.0, 0,0, 0,0))
		INFO_MSG("testGoToSpace over!")

	def DisconnectDeathToSpace( self, srcEntityID ):
		"""
		<exposed method>
		客户端卡死请求传送到指定地图
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		if self.getState() == csdefine.ENTITY_STATE_DEAD:
			self.statusMessage( csstatus.DISCONNECT_DEATH_TO_DEAD )
			return
		remainTime = self.disconnectEndTime - Functions.getTime()
		if remainTime > 0:
			time = int( remainTime/ csconst.TIME_ENLARGE_MULTIPLE )
			self.statusMessage( csstatus.DISCONNECT_DEATH_TO_WAIT,time )
			return
		self.disconnectEndTime = Functions.getTime() + Const.DISCONNECT_CD_TIME * csconst.TIME_ENLARGE_MULTIPLE
		spaceObj = KST.g_objFactory.getSpaceObject( self.spaceScriptID )
		if spaceObj.getSpaceType() == csdefine.SPACE_TYPE_PLANE or spaceObj.getSpaceType() == csdefine.SPACE_TYPE_STORY_COPY:
			self.gotoExitSpacePos()
		elif spaceObj.getSpaceType() == csdefine.SPACE_TYPE_POTENTIAL or spaceObj.getSpaceType() == csdefine.SPACE_TYPE_CHUAN_CHENG:
			self.requestGotoDynamicRevivePos( srcEntityID )
		elif spaceObj.getSpaceType() == csdefine.SPACE_TYPE_COPY or spaceObj.getSpaceType() == csdefine.SPACE_TYPE_JSSLC_CHANCE_COPY:
			self.gotoExitSpacePos()
		elif spaceObj.getSpaceType() in csdefine.SPACE_TYPE_ACTIVITY_LIST:
			self.requestGotoDynamicRevivePos( srcEntityID )
		elif csdefine.DISCONNECT_DEATH_SWITCH:
			self.reviveOnCity()

	#--------------------------位面接口-----------------------------
	def requestGotoSpacePlane( self, srcEntityID, spaceScriptID, position, direction ):
		"""
		<exposed method>
		客户端请求位面传送（进入/离开位面）
		此接口仅供客户端使用
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		CurrSpaceScriptID = self.getCurrentSpaceData( Const.SPACE_DATA_SCRIPT_ID )
		if CurrSpaceScriptID == spaceScriptID:
			return
		self.client.SeamLessLoadLevel()										# 客户端切换关卡结构，无法较好的兼容位面无缝切换，需要特殊处理

		# 因为坐标由客户端同步服务器。该机制可能会造成服务器的坐标比客户端坐标慢一个tick，导致玩家在位面外的结果。所以坐标需要模拟客户端坐标移动。
		#（因为客户端的速度是6米/秒写死，与玩家速度无关，所以这里也暂时不用玩家的速度）
		#position = Math.Vector3(self.position.x + math.sin( self.direction[2] ) * 1.3, self.position.y, self.position.z + math.cos(self.direction[2]) * 1.3 )
		self.gotoSpaceUseArg( spaceScriptID, Math.Vector3(KBEMath.Unreal2KBEnginePosition( position )), Math.Vector3(KBEMath.Unreal2KBEngineDirection( direction )), {} )

	def gotoSpacePlane( self, spaceScriptID ):
		"""
		<Define method>
		进入位面（服务器接口）
		独立接口是因为进入/离开位面的表现不一致
		"""
		self.client.GotoSpacePlane( spaceScriptID )

	def leaveSpacePlane( self, spaceScriptID ):
		"""
		<Define method>
		离开位面（服务器接口）
		"""
		self.client.LeaveSpacePlane( spaceScriptID )

	def gotoTongSpace( self, srcEntityID ):
		"""
		exposed method
		进入帮会领地
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		if self.getState() == csdefine.ENTITY_STATE_DEAD:
			self.statusMessage( csstatus.SKILL_IN_DEAD, "" )
			return
		if self.getState() == csdefine.ENTITY_STATE_FIGHT:
			self.statusMessage( csstatus.CANNOT_FLY_WHILE_FIGHTING, "" )
			return
		currSpaceObj = self.getCurrentSpaceObject()
		if currSpaceObj.getSpaceType() == csdefine.SPACE_TYPE_TONG:
			self.statusMessage( csstatus.PLAYER_IN_TONG_SPACE, "" )
			return

		if self.tongMB:
			self.gotoSpace( Const.TONG_SPACE_SCRIPTID, Const.TONG_SPACE_POSITION, Const.TONG_SPACE_DIRECTION )

	def setLineNumber( self, lineNumber ):
		"""
		设置玩家在第几线
		"""
		self.lineNumber = lineNumber

	def getLineNumber( self ):
		"""
		获得玩家在地图第几线  没有在大地图则为0
		"""
		return self.lineNumber


	def roleSpaceCopyPlaySound(self, voiceIDStr):
		"""
		副本中播放语音
		"""
		#记录播放语音 用于副本语音结束事件中验证
		spaceEntity = self.getCurrentSpace()
		if not spaceEntity:
			return
		voiceIDList = voiceIDStr.split("|")
		for voiceID in voiceIDList:
			param = {voiceID:spaceEntity.id}
			self.playSoundRecords["Space"].update(param)
		self.showMessagePlaySound(voiceIDStr)