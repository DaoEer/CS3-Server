# -*- coding: utf-8 -*-
import KBEngine
import KBEDebug
import Math
import KST
import KBEMath
import csdefine
import csstatus
import Functions
import SpaceContainer
from ObjectScript.ObjectScriptBase.GameScript import GameScript
from ConfigObject import PatrolRouteLoader
from ConfigObject.NavmeshLoader import g_navmeshLoader
from ObjectScript.SpawnPoint.SpawnPointFactory import g_spawnPointFactory
import Const
from KBEDebug import *

class SpaceBase( GameScript ):
	"""
	空间领域
	"""
	def __init__( self ):
		GameScript.__init__( self )
		self._spaceType = csdefine.SPACE_TYPE_NORMAL
		self._belongType = []		#同一个副本可以有多种归属
		self._spawnFile = ""
		self._navmeshPath = ""
		self._patrolRouteFile = ""
		self._reviveType = ""
		self._reviveScriptID = ""
		self._revivePosition = Math.Vector3(0.0, 0.0, 0.0)
		self._reviveDirection = Math.Vector3(0.0, 0.0, 0.0)
		self._exitScriptID = ""
		self._exitPosition = Math.Vector3(0.0, 0.0, 0.0)
		self._exitDirection = Math.Vector3(0.0, 0.0, 0.0)
		self._relationMode = ""
		self._spaceAoi = Const.DEFAULT_AOI_RADIUS
		self._roleRelationRule = csdefine.ROLE_RELATION_RULE_CAMP
		self._roleIsCanCompete = 0 		#默认不可切磋
		self._holdEffectIDs = []
		self._allowUseSkillIDs = []		#该Space中允许使用的技能
		self._forbidUseSkillIDs = []	#该Space中不允许使用的技能
		self._forbidUseTeleportPoint = False	#当前地图是否点击传送点传送出去
		self._tabDistance = 0			#tab选中距离
		self._spaceHPModifyRatio = 1.0
		self._spaceDamageModifyRatio = 1.0
		self._spaceChildType = csdefine.SPACE_TYPE_NORMAL
		self._navmeshLayers = 1
		self._spaceName = ""
		self.spaceIntroduce = {}		# 场景语音
		self.sceneVoiceTriggerNum = 0	# 场景语音触发次数（默认为0：重复触发）
		self._isAllowJoinTeam = 1		# 是否允许组队
		self._bossScriptIDList = []		# 世界Boss列表
		self._bossPositionList = []		# 世界Boss位置列表
		self._bossRefreshTime = 0.0		# 世界Boss刷新时间
		self._allowUseItemTypes = [] 	# 该Space中允许使用的物品类型
		self._forbidUseItemTypes = []	# 该Space中不允许使用的物品类型
		self._allowUseItemIDs = []		# 该Space 中允许使用的物品ID
		self._forbidUseItemIDs = []		# 该Space 中不允许使用的物品ID
		self._disableAssistJump = 0		# 在副本中关闭玩家的辅助跳跃
		self._isCanOpenBarracks = 1 	# 该地图能否打开天兵营
		self._bossIDForMessageList = []	# 标记地图中Boss的scriptID，如果副本的boss是通过self._bossScriptIDList来创建的，那么此处可以不用填
	
	def initData( self, configData ):
		GameScript.initData( self, configData )
		self._spaceType = getattr( csdefine, configData[ "spaceType" ] )
		self._belongType = [ int(i) for i in configData[ "belongType" ].split("|") ]
		self._spawnFile = configData.get( "SpawnFile", "" )
		self._navmeshPath = configData.get( "NavmeshPath", "" )
		self._spaceAoi = float( configData.get( "SpaceAoi", Const.DEFAULT_AOI_RADIUS ) )
		self._reviveType = configData["SpaceData"].get( "reviveType", "" )
		self._reviveScriptID = configData["SpaceData"].get( "reviveScriptID", "")
		self._revivePosition = KBEMath.Unreal2KBEnginePosition( Math.Vector3( configData["SpaceData"].get( "revivePosition", (0.0,0.0,0.0)) ) )
		self._reviveDirection = KBEMath.Unreal2KBEngineDirection( Math.Vector3( configData["SpaceData"].get( "reviveDirection", (0.0,0.0,0.0)) ))
		self._patrolRouteFile = configData.get( "PatrolRouteFile", "" )
		if self._patrolRouteFile:
			PatrolRouteLoader.g_patrolRouteLoader.initSpacePatrolRoute( self.scriptID, self._patrolRouteFile )
		self._relationMode = configData.get( "EnfityRelationMode", "RelationDefault" )
		rule = configData.get( "RoleRelationRule", "" )
		if rule != "":
			self._roleRelationRule = getattr( csdefine, rule )

		if "spaceChildType" in configData:
			self._spaceChildType = getattr( csdefine, configData["spaceChildType"] )
		else:
			self._spaceChildType = self._spaceType
		if "RoleIsCanCompete" in configData:
			self._roleIsCanCompete = configData["RoleIsCanCompete"]
		
		spaceHoldEffect = configData.get( "SpaceHoldEffect", "" )
		if spaceHoldEffect != "":
			self._holdEffectIDs = [ int(i) for i in spaceHoldEffect.split("|") ]

		if "ExitSpace" in configData:
			self._exitScriptID = configData["ExitSpace"].get( "ScriptID", "")
			posStr = configData["ExitSpace"].get( "Position", "" )
			pos = Functions.vector3TypeConvert( posStr )
			if pos:
				self._exitPosition = KBEMath.Unreal2KBEnginePosition( pos )
			dirStr = configData["ExitSpace"].get( "Direction", "" )
			dir = Functions.vector3TypeConvert( dirStr )
			if dir:
				self._exitDirection = KBEMath.Unreal2KBEngineDirection( dir )

		self._allowUseSkillIDs = configData.get("AllowUseSkillIDs",[])
		self._forbidUseSkillIDs = configData.get("ForbidUseSkillIDs",[])
		self._forbidUseTeleportPoint = configData.get("ForbidUseTeleportPoint", False)
		self._tabDistance = configData.get("TabDistance", 0)

		self._spaceHPModifyRatio = configData["SpaceData"].get("spaceHPModifyRatio",1.0)
		self._spaceDamageModifyRatio = configData["SpaceData"].get("spaceDamageModifyRatio",1.0)
		self._isCanWalkOffLedges = configData["SpaceData"].get("isCanWalkOffLedges", 0)

		self._spaceName = configData.get("SpaceName","")
		self._isAllowJoinTeam = configData.get("IsAllowJoinTeam",1)

		self.setReviveType()
		if self._navmeshPath:
			self._navmeshLayers = g_navmeshLoader.calcNavmeshLayers( self._navmeshPath )

		if "spaceIntroduce" in configData["SpaceData"]:
			self.spaceIntroduce = configData["SpaceData"].get( "spaceIntroduce", {} )

		if "sceneVoiceTriggerNum" in configData["SpaceData"]:
			self.sceneVoiceTriggerNum = configData["SpaceData"].get( "sceneVoiceTriggerNum", 0 )

		#-----世界Boss刷新数据-----------
		bossScriptIDList = configData["SpaceData"].get( "bossScriptIDList", "" )
		if bossScriptIDList != "":
			self._bossScriptIDList = bossScriptIDList.split("|")
		bossPositionList = configData["SpaceData"].get( "bossPositionList", "" )
		if bossPositionList != "":
			self._bossPositionList = bossPositionList.split("|")
		if "bossRefreshTime" in configData["SpaceData"]:
			 self._bossRefreshTime = float( configData["SpaceData"].get( "bossRefreshTime", 0.0 ) )
		self._isShowFailedUI = configData["SpaceData"].get("isShowFailedUI", 0)

		self._allowUseItemTypes = configData.get("AllowUseItemTypes",[])
		self._forbidUseItemTypes = configData.get("ForbidUseItemTypes",[])
		self._allowUseItemIDs = configData.get("AllowUseItemIDs",[])
		self._forbidUseItemIDs = configData.get("ForbidUseItemIDs",[])

		if "disableAssistJump" in configData["SpaceData"]:
			self._disableAssistJump = configData["SpaceData"].get( "disableAssistJump", 0 )

		if "isCanOpenBarracks" in configData["SpaceData"]:
			self._isCanOpenBarracks = configData["SpaceData"].get( "isCanOpenBarracks", 1 )
			
		#在不是通过self.bossScriptIDList来创建boss的地图中填写，主要是在杀死boss掉落的时候，如果爆出圣阶物品需要有消息提示
		bossIDForMessageList = configData["SpaceData"].get("bossIDForMessage", "")
		if bossIDForMessageList != "":
			self._bossIDForMessageList = bossIDForMessageList.split("|")

	def getSpaceType( self ):
		return self._spaceType

	def isInSameBigMap( self, mapScriptID ):
		"""
		是否在同一大地图
		"""
		return False

	def getSpaceChildType( self ):
		return self._spaceChildType

	def getSpaceName( self ):
		"""
		获得SpaceName
		"""
		return self._spaceName

	def getRoleIsCanCompete(self):
		return self._roleIsCanCompete
	
	def getSpaceAoi( self ):
		"""
		"""
		return self._spaceAoi

	def getAllowUseSkillIDs( self ):
		"""
		获得space允许使用的技能ID列表
		"""
		return self._allowUseSkillIDs

	def getForbidUseSkillIDs( self ):
		"""
		获得space不允许使用的技能ID列表
		"""
		return self._forbidUseSkillIDs

	def getAllowUseItemTypes( self ):
		"""
		获得space允许使用的物品类型
		"""
		return self._allowUseItemTypes

	def getForbidUseItemTypes( self ):
		"""
		获得space不允许使用的物品类型
		"""
		return self._forbidUseItemTypes

	def getAllowUseItemIDs( self ):
		"""
		获得space允许使用的物品ID列表
		"""
		return self._allowUseItemIDs

	def getForbidUseItemIDs( self ):
		"""
		获得space不允许使用的物品ID列表
		"""
		return self._forbidUseItemIDs
		
	def getForbidUseTeleportPoint( self ):
		"""
		获得space是否允许玩家通过点击传送点传送出去
		"""
		return self._forbidUseTeleportPoint
		
	def getCanWalkOffLedges(self):
		"""
		获得是否能离开寻路边缘
		"""
		return bool(self._isCanWalkOffLedges)

	def getCanShowFailedUI(self):
		"""
		是否在中途退出副本显示失败界面
		"""
		return bool(self._isShowFailedUI)

	def canJoinTeam( self ):
		"""
		该地图是否能组队
		"""
		return bool(self._isAllowJoinTeam)

	def initEntity( self, selfEntity ):
		"""
		初始化space entity要做的事情
		"""
		if self._spawnFile:
			KST.startLoadSpaceSpawnPoint(self.scriptID)
			
		if self._navmeshPath:
			try:
				g_navmeshLoader.loadSpaceNavmesh( selfEntity.spaceID, self._navmeshPath )
			except:
				ERROR_MSG("scriptID(%s) NavmeshPath(%s) is error!!please check!!"%(self.scriptID,self._navmeshPath))

		selfEntity.setCurrentSpaceData( Const.SPACE_DATA_SCRIPT_ID, self.scriptID )
		selfEntity.setCurrentSpaceData( Const.SPACE_DATA_SPACE_ID, str( selfEntity.id ) )
		selfEntity.setCurrentSpaceData( Const.SPACE_DATA_BELONG_TYPE, str( selfEntity.belongType ) )
		selfEntity.setCurrentSpaceData( Const.SPACE_DATA_REVIVE_TYPE, self._reviveType )
		selfEntity.setCurrentSpaceData( Const.SPACE_DATA_SPACE_TYPE, str( self._spaceType ) )
		selfEntity.setCurrentSpaceData( Const.SPACE_DATA_RELATION_MODE, self._relationMode )
		selfEntity.setSpaceHPModifyRatio( float(self._spaceHPModifyRatio) )
		selfEntity.setSpaceDamageModifyRatio(float(self._spaceDamageModifyRatio))
		
	def setReviveType( self ):
		"""
		设置复活类型  CST-2208
		"""
		if self._reviveType == "":
			self._reviveType = "0|1|5"
		if str(csdefine.REVIVE_ON_REVIVE_SPACE) not in self._reviveType.split("|") and str(csdefine.REVIVE_ON_SPACE_COPY) not in self._reviveType.split("|") and str(csdefine.REVIVE_ON_RETURN_POINT) not in self._reviveType.split("|"):
			self._reviveType = "0|1|5"
	
	def beforeDestroy( self, selfEntity ):
		"""
		销毁前做一些事
		"""
		g_navmeshLoader.stopLoadNavmeshOver(selfEntity.spaceID)
		
	def createSpawnPoint( self, selfEntity ):
		"""加载刷新点"""
		if self._spawnFile:
			g_spawnPointFactory.initSpawnPoint( selfEntity, self._spawnFile )
		
	def getReviveInfo( self ):
		return ( self._reviveScriptID, self._revivePosition, self._reviveDirection )

	def getReviveToExitInfo( self, playerRole ):
		return ( self._exitScriptID, self._exitPosition, self._exitDirection )
	
	def getPackDomainData( self, playerEntity, args ):
		if "packBelongType" in args:		#打包了副本归属类型
			belongType = args.pop( "packBelongType" )
		else:
			if playerEntity.spaceScriptID == self.scriptID:	# 相同scriptID的地图传送（有可能是同地图传送）
				spaceEntity = playerEntity.getCurrentSpace()
				if spaceEntity:
					belongType = spaceEntity.belongType
				elif playerEntity.isInTeam() and csdefine.SPACE_BELONG_TEAM in self._belongType:
					belongType = csdefine.SPACE_BELONG_TEAM
				elif (not playerEntity.isInTeam()) and csdefine.SPACE_BELONG_PERSON in self._belongType:
					belongType = csdefine.SPACE_BELONG_PERSON
				else:
					belongType = self._belongType[ 0 ]
			elif playerEntity.isInTeam() and csdefine.SPACE_BELONG_TEAM in self._belongType:
				belongType = csdefine.SPACE_BELONG_TEAM
			elif (not playerEntity.isInTeam()) and csdefine.SPACE_BELONG_PERSON in self._belongType:
				belongType = csdefine.SPACE_BELONG_PERSON
			else:						#没打包又不是相同scriptID的地图传送，就取配置的第一个值
				belongType = self._belongType[ 0 ]
		
		return SpaceContainer.getPickContainerData( belongType, self.scriptID, playerEntity, args )
	
	def checkLeaveEnable( self, player, params ):
		"""
		virtual method
		检测离开条件
		"""
		return csstatus.SPACE_ENTER_OR_LEAVE_OK
		
	def checkEnterEnable( self, player, params ):
		"""
		virtual method
		检测进入条件
		"""
		# CST-11488 程序内容需求（0级）——限制地图不能组队功能
		# 如果目标地图不允许组队，则传送失败
		if not self.canJoinTeam() and player.isInTeam():
			return csstatus.SPACE_CANT_ENTER_IN_TEAM
		return csstatus.SPACE_ENTER_OR_LEAVE_OK
	
	def teleportEntity( self, selfEntity, roleBase, position, direction, packArgs ):
		roleBase.cell.onGotoSpace( self.scriptID, selfEntity, Math.Vector3(position), direction, packArgs )
	
	def onEnter( self, selfEntity, playerRole, packArgs ):
		playerRole.remoteCall("setViewRadius", ( self.getSpaceAoi(), Const.DEFAULT_AOI_EXTRA_RADIUS ) )
		playerRole.setSpaceRelationRule( self._roleRelationRule )
		playerRole.setTabDistance(self._tabDistance)
		playerRole.setIsCanOpenBarracks( self._isCanOpenBarracks )
		if self._holdEffectIDs:
			for id in self._holdEffectIDs:
				index = playerRole.addFixIDHoldEffect( id, playerRole )
				if index != -1:
					playerRole.spaceHoldEffectIndex.append( index )
				KBEDebug.DEBUG_MSG( "Role add space holdEffect on enter! space:%s, roleID:%s, effectID:%s, resultIndex:%s, currIndexList:%s."%(self.scriptID, playerRole.id, id, index, playerRole.spaceHoldEffectIndex) )

	def onTeleportCompleted( self, selfEntity, playerRole ):
		# 播放场景语音
		if self.spaceIntroduce:
			if self.sceneVoiceTriggerNum:
				if selfEntity.scriptID not in playerRole.sceneVoiceTriggerNum:
					playerRole.showMessagePlaySound( self.spaceIntroduce["voiceID"] )
					playerRole.sceneVoiceTriggerNum[ selfEntity.scriptID ] = 1
				elif playerRole.sceneVoiceTriggerNum[ selfEntity.scriptID ] < self.sceneVoiceTriggerNum:
					playerRole.showMessagePlaySound( self.spaceIntroduce["voiceID"] )
					playerRole.sceneVoiceTriggerNum[ selfEntity.scriptID ] += 1
			else:
				playerRole.showMessagePlaySound( self.spaceIntroduce["voiceID"] )
	
	def onLeave( self, selfEntity, playerRole, packArgs ):
		if self._holdEffectIDs:
			for index in playerRole.spaceHoldEffectIndex:
				playerRole.removeFixIDHoldEffect( index )
				KBEDebug.DEBUG_MSG( "Role remove space holdEffect on leave! space:%s, roleID:%s, effecIndex:%s."%(self.scriptID, playerRole.id, index) )
			playerRole.spaceHoldEffectIndex = []
	
	def onLogin( self, selfEntity, playerRole ):
		playerRole.remoteCall("setViewRadius", ( self.getSpaceAoi(), Const.DEFAULT_AOI_EXTRA_RADIUS ) )
		playerRole.setSpaceRelationRule( self._roleRelationRule )
		playerRole.setIsCanOpenBarracks( self._isCanOpenBarracks )
		if self._holdEffectIDs:
			for id in self._holdEffectIDs:
				index = playerRole.addFixIDHoldEffect( id, playerRole )
				if index != -1:
					playerRole.spaceHoldEffectIndex.append( index )
				KBEDebug.DEBUG_MSG( "Role add space holdEffect on login! space:%s, roleID:%s, effectID:%s, resultIndex:%s, currIndexList:%s."%(self.scriptID, playerRole.id, id, index, playerRole.spaceHoldEffectIndex) )

	def onPlayerDie( self, selfEntity, playerID, playerMB ):
		"""
		"""
		pass

	def onMonsterDie( self, selfEntity, monsterID, monsterScriptID ):
		"""
		"""
		pass

	def onMonsterHPChanged( self, selfEntity, monsterEntity ):
		"""
		"""
		pass

	def onTriggerBox( self, selfEntity, boxID, boxScriptID ):
		"""
		"""
		pass

	def onNPCObjectDestroy( self, selfEntity, enityID, entityScriptID ):
		"""
		"""
		pass

	def onPlayerGetItem( self, selfEntity, playerRole, itemID, amount ):
		"""
		"""
		pass

	def onPlayerRemoveItem( self, selfEntity, playerRole, itemID, amount ):
		"""
		"""
		pass

	def onPlayerUseItem( self, selfEntity, playerRole, itemInstID, amount ):
		"""
		"""
		pass

	def onPlayerUseTitle( self, selfEntity, playerRole, titleID ):
		"""
		"""
		pass
		
	def onSpaceSpawnPointLoadOver( self, selfEntity ):
		"""刷新点加载完成回调"""
		KST.loadOverSpaceSpawnPoint(self.scriptID)
		
	def onAddPotential( self, selfEntity, playerRole, potential, reason):
		pass
		
	def onAddExp( self, selfEntity, playerRole, exp, reason):
		pass
		
	def onAddXiuWei( self, selfEntity, playerRole, xiuwei, reason):
		pass
	
	def onTeamCaptainChange(self, selfEntity):
		pass

	def getNavmeshLayers(self):
		"""
		获得导航层数
		"""
		return self._navmeshLayers

	def getBossRefreshInfo( self ):
		"""
		获取世界Boss刷新数据
		"""
		return ( self._bossScriptIDList, self._bossPositionList )

	def getCountDownTime( self ):
		"""
		获取倒计时时间
		"""
		return self._bossRefreshTime

	def getDisableAssistJump(self):
		"""获取是否在此副本中关闭玩家辅助跳跃的标志"""
		return self._disableAssistJump
		
	def addShengJieItemNotify(self, selfEntity, itemInst, dropRewardOrSpaceReward, role, params):
		"""
		玩家在地图中获得圣阶物品通知
		dropRewardOrSpaceReward: 掉落:0 / 副本奖励:1
		"""
		if itemInst is None:
			return
		
		#杀怪掉落
		if dropRewardOrSpaceReward == 0:
			scriptID = params.get("scriptID", "")
			bossIDList = self._bossScriptIDList if len(self._bossScriptIDList) else self._bossIDForMessageList
			if scriptID in bossIDList:
				bossName = params.get("name", "")
				messageArg = "{}|{}|{}|{}".format(role.getName(), self.getSpaceName(), bossName, itemInst.getItemDir("ItemName"))
				selfEntity.globalWorld(csstatus.ITEM_ADD_IN_SPACE_WIN_BOSS, messageArg)
			else:
				messageArg = "{}|{}|{}".format(role.getName(), self.getSpaceName(), itemInst.getItemDir("ItemName"))
				selfEntity.globalWorld(csstatus.ITEM_ADD_IN_SPACE, messageArg)
		else:
			messageArg = "{}|{}|{}".format(role.getName(), self.getSpaceName(), itemInst.getItemDir("ItemName"))
			selfEntity.globalWorld(csstatus.ITEM_ADD_IN_SPACE, messageArg)
			
			#策划要求掉落加一个光效就好了
			if role.getClient():
				role.client.CLIENT_PlaySound(Const.SHENGJIE_ITEM_GET_SOUND)
				role.client.CLIENT_PlayEffect(Const.SHENGJIE_ITEM_GET_EFFECTID)
		
	def isSpaceCopy(self):
		"""
		是否是副本地图（GM使用）
		"""
		return False