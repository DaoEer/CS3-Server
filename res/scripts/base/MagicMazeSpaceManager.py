# -*- coding: utf-8 -*-

import KST
import KBEngine
from CoreObject import MgrPersistentObject
from KBEDebug import *
import LoadModule
import Functions
import random
import Math
import KBEMath
import Const
import csdefine

#记录每个对应的spacekey（teamID或者玩家dbid）的相应进度，是否在主副本中，如果在主副本中，那么在主副本的第几个传送门出口。如果不在主副本中，
#那么传送到对应的子副本的入口处。

DICE_MIN_STEP = 1
DICE_MAX_STEP = 6


class MagicMazeItem( object ):
	"""
	幻阵迷宫相应spacekey管理
	"""
	def __init__(self, belongType, spaceKey, pickArg):
		self.belongType = belongType
		self.spaceKey = spaceKey
		self.progress = 0
		self.isInParentSpace = False
		self.extraRewardRate = 0.0
		self.extraRewardCount = -1
		self.extraDiceStep = 0
		self.extraDiceCount = 0
		self.isDiceForward = 1
		self.finishTime = -1
		self.failureCount = 0
		self.deadCount = 0
		self.extraSpaceName = ""
		self.mainSpaceMB = None
		self.childSpaceMB = None
		self.copyIsComplet = False
		self.extraBuffBonus = 0
		self.mainScriptID = ""
		self.pickArg = pickArg
		self.index = int(pickArg["mainSpace"])
		self.playerRecord = []
	
	def setSpaceExtraReward(self, extraRewardCount, extraRewardRate):
		self.extraRewardRate = extraRewardRate
		self.extraRewardCount = extraRewardCount

	def setSpaceExtraBuffBonus(self, extraBuffBonus):
		self.extraBuffBonus = extraBuffBonus

	def setSpaceExtraDice(self, extraMinDice, extraMaxDice, extraDiceCount, isDiceForward):
		pass
		
	def setSpaceProgress(self, progress):
		self.progress = progress
	
	def setSpaceInParent(self, isInParentSpace):
		self.isInParentSpace = isInParentSpace
		
	def setSpaceFailure(self, failureCount):
		self.failureCount = failureCount
		if self.mainSpaceMB:
			self.mainSpaceMB.cell.remoteScriptCall("onChildSpaceFailure",())
		
	def setSpaceFinishTime(self, finishTime):
		self.finishTime = finishTime
		
	def setSpaceDeadCount(self, deadCount):
		self.deadCount = deadCount
		
	def setMainSpaceMB(self, spaceMB):
		self.mainSpaceMB = spaceMB

	def setMainScriptID(self, mainScriptID):
		self.mainScriptID = mainScriptID
		
	def setChildSpaceMB(self, spaceMB):
		self.childSpaceMB = spaceMB
		
	def setExtraSpaceName(self, extraSpaceName):
		self.extraSpaceName = extraSpaceName
		
	def onChildSpacePlayerDie(self, playerID, playerMB):
		if self.mainSpaceMB:
			self.mainSpaceMB.cell.remoteScriptCall("onPlayerDie",(playerID, playerMB))

	def setCopyIsComplet(self, copyIsComplet):
		self.copyIsComplet = copyIsComplet
		
	def rewardItemToSpacePlayer(self):
		"""
		奖励物品给玩家
		"""
		if self.childSpaceMB != None:
			pass


class ChildSpaceData( object ):
	"""
	子副本space数据
	"""
	def __init__(self, spaceName, type, leavePosStr, leaveDirStr):
		self.spaceName = spaceName
		self.type = type
		
		self.leavePos = Math.Vector3(0.0, 0.0, 0.0)
		leavePos = Functions.vector3TypeConvert( leavePosStr )
		if leavePos:
			self.leavePos = KBEMath.Unreal2KBEnginePosition( leavePos )
			
		self.leaveDir = Math.Vector3(0.0, 0.0, 0.0)
		leaveDir = Functions.vector3TypeConvert( leaveDirStr )
		if leaveDir:
			self.leaveDir = KBEMath.Unreal2KBEngineDirection( leaveDir )

class MagicMazeSpaceManager( MgrPersistentObject.MgrPersistentObject ):
	"""
	幻阵迷宫副本管理器
	"""
	def __init__( self ):
		MgrPersistentObject.MgrPersistentObject.__init__( self )
		self.MagicMazeParentRecord = {}			# 父副本记录，用于cell进副本时预先查找某spaceKey的副本是否存在
		self.MagicMazeParentRecordPlayers = {} 	# 父副本记录，用于cell进副本时人员
		KBEngine.globalData["MagicMazeParentSpaceGlobalRecord"] = {}
		KBEngine.globalData["MagicMazeParentRecordPlayers"] = {}
		self.magicMazeInfo = {}					#记录所有的对应信息，包括副本进度，是否在主副本，附加奖励效果，附加掷骰子的点数、掷骰子向前向后的步数。
		self.mainSpace = {}
		self.multilayerChildSpace = {}
		self.childSpaces = {}
		self.initData()
		
	def initData( self ):
		dataCfg = LoadModule.openJsonCfg("MagicMazeConfig/MagicMazeConfig.json")
		for key, datas in dataCfg.items():
			self.mainSpace[int(key)] = datas.get("mainSpace", "")
			self.multilayerChildSpace[int(key)] = datas.get("childSpaces", "")
		self.onCompleteInit()

	def analyticalData( self, data ):
		"""
		解析数据
		"""
		for index,childSpace in data.items():
			childSpaceData = ChildSpaceData(childSpace["space"],childSpace["type"],childSpace["leavePos"],childSpace["leaveDir"])
			self.childSpaces[int(index)] = childSpaceData
		
	def onChildSpaceSuccess(self, belongType, spaceKey, childSpaceScriptID,mainScriptID):
		magicMazeItem = self.getMagicMazeItem(belongType, spaceKey,mainScriptID)
		if magicMazeItem != None:
			magicMazeItem.setCopyIsComplet( True )
		
	def onChildSpaceFailure(self, belongType, spaceKey, childSpaceScriptID,mainScriptID):
		magicMazeItem = self.getMagicMazeItem(belongType, spaceKey,mainScriptID)
		if magicMazeItem != None:	
			magicMazeItem.setCopyIsComplet( False )
			magicMazeItem.setSpaceFailure(magicMazeItem.failureCount + 1)
		
	def onChildSpacePlayerDie(self, belongType, spaceKey, childSpaceScriptID, playerID, playerMB,mainScriptID):
		magicMazeItem = self.getMagicMazeItem(belongType, spaceKey,mainScriptID)
		if magicMazeItem != None:
			magicMazeItem.onChildSpacePlayerDie(playerID, playerMB)
		
	def onChildSpaceCreate(self, belongType, spaceKey, spaceMB,mainScriptID):
		magicMazeItem = self.getMagicMazeItem(belongType, spaceKey,mainScriptID)
		if magicMazeItem != None:
			magicMazeItem.setChildSpaceMB(spaceMB)
			if magicMazeItem.extraRewardCount > -1:
				spaceMB.cell.remoteScriptCall("onSetSpaceExtraReward",(magicMazeItem.extraRewardCount, magicMazeItem.extraRewardRate, magicMazeItem.extraBuffBonus))
		
	def onChildSpaceDelete(self, belongType, spaceKey, isSpecialSpace,mainScriptID):
		magicMazeItem = self.getMagicMazeItem(belongType, spaceKey,mainScriptID)
		if magicMazeItem != None:
			magicMazeItem.setChildSpaceMB(None)
		
	def onChildSpacePlayerDead(self, belongType, spaceKey, childSpaceScriptID,mainScriptID):
		magicMazeItem = self.getMagicMazeItem(belongType , spaceKey,mainScriptID)
		if magicMazeItem != None:
			magicMazeItem.setSpaceDeadCount(magicMazeItem.deadCount + 1)
		
	def onMainSpaceCreate(self, belongType, spaceKey, spaceMB, mainScriptID):
		magicMazeItem = self.getMagicMazeItem(belongType, spaceKey,mainScriptID)
		if magicMazeItem != None:
			magicMazeItem.setMainSpaceMB(spaceMB)
			magicMazeItem.setMainScriptID(mainScriptID)
			self.MagicMazeParentRecord[(belongType, spaceKey,mainScriptID)] = mainScriptID
			KBEngine.globalData["MagicMazeParentSpaceGlobalRecord"] = self.MagicMazeParentRecord
			playerDict = magicMazeItem.pickArg.get("players",{})
			self.MagicMazeParentRecordPlayers[(belongType, spaceKey,mainScriptID)] = list( playerDict.keys() )
			KBEngine.globalData["MagicMazeParentRecordPlayers"] = self.MagicMazeParentRecordPlayers
		
	def onMainSpaceDelete(self, belongType, spaceKey, mainScriptID):
		magicMazeItem = self.getMagicMazeItem(belongType, spaceKey,mainScriptID)
		if magicMazeItem != None:
			magicMazeItem.setMainSpaceMB(None)
			magicMazeItem.setMainScriptID(None)
		if (belongType, spaceKey,mainScriptID) in self.MagicMazeParentRecord:
			del self.MagicMazeParentRecord[(belongType, spaceKey,mainScriptID)]
			KBEngine.globalData["MagicMazeParentSpaceGlobalRecord"] = self.MagicMazeParentRecord
		if (belongType, spaceKey,mainScriptID) in self.MagicMazeParentRecordPlayers:
			del self.MagicMazeParentRecordPlayers[(belongType, spaceKey,mainScriptID)]
			KBEngine.globalData["MagicMazeParentRecordPlayers"] = self.MagicMazeParentRecordPlayers
			
	def onSpaceDelete(self, belongType, spaceKey, spaceName, isSpecialSpace, mainScriptID):
		if spaceName in self.mainSpace.values():
			self.onMainSpaceDelete(belongType, spaceKey, mainScriptID)
		else:
			self.onChildSpaceDelete(belongType, spaceKey, isSpecialSpace, mainScriptID)
	
	def gotoMagicMazeSpace(self, belongType, spaceKey, pickArg):
		"""
		从外面对话进副本
		"""
		mainScriptID = pickArg["mainScriptID"]
		magicMazeItem = self.getMagicMazeItem(belongType, spaceKey,mainScriptID)
		if magicMazeItem == None:	#初进，初始化副本Item
			magicMazeItem = MagicMazeItem(belongType, spaceKey, pickArg )
			self.magicMazeInfo[(belongType, spaceKey,mainScriptID)] = magicMazeItem
			self.gotoMagicMazeParentSpace( belongType, spaceKey, pickArg )
		elif magicMazeItem.isInParentSpace:	#重进，在父副本
			pickArg["isReteleport"] = True
			self.gotoMagicMazeParentSpace( belongType, spaceKey, pickArg )
		else:	#重进，在子副本
			self.gotoMagicMazeChildSpace( belongType, spaceKey, pickArg )
			
		for pDBID,playerMB in pickArg.get("players", {}).items():	#记录幻阵迷宫进入的次数
			if pDBID not in magicMazeItem.playerRecord:
				magicMazeItem.playerRecord.append( pDBID)
				activityType = magicMazeItem.pickArg.get("activityType", csdefine.ACTIVITY_TYPE_UNKNOWN)
				playerMB.cell.onEnterMagicMazeSpace(activityType)
			
	def gotoMagicMazeChildSpace(self, belongType, spaceKey, pickArg ):
		"""
		幻阵迷宫，父副本进子副本
		"""
		mainScriptID = pickArg["mainScriptID"]
		magicMazeItem = self.getMagicMazeItem(belongType, spaceKey,mainScriptID)
		magicMazeItem.pickArg.update(pickArg)
		self.analyticalData(self.multilayerChildSpace[magicMazeItem.index])
		spaceName = self.childSpaces[magicMazeItem.progress].spaceName
		players = pickArg.get( "players", {} ).values()
		for playerMB in players:
			self.setNextLevelLoading(belongType, spaceKey, playerMB, 0, 0,mainScriptID)
			playerMB.cell.gotoSpaceEnterPos(spaceName, magicMazeItem.pickArg)
		
	def gotoMagicMazeParentSpace(self, belongType, spaceKey, pickArg ):
		"""  
		幻阵迷宫，进父副本
		"""
		mainScriptID = pickArg["mainScriptID"]
		magicMazeItem = self.getMagicMazeItem(belongType, spaceKey,mainScriptID)	#获取相应magicMazeItem记录
		magicMazeItem.pickArg.update( pickArg )
		self.analyticalData(self.multilayerChildSpace[magicMazeItem.index])
		spaceName = self.mainSpace[magicMazeItem.index]
		players = pickArg.get( "players", {} ).values()
		progress = magicMazeItem.progress
		if progress==0:	#刚进副本(包含掉线重进)
			for playerMB in players:
				self.setNextLevelLoading(belongType, spaceKey, playerMB, 0, 0,mainScriptID)
				playerMB.cell.gotoSpaceEnterPos(spaceName, magicMazeItem.pickArg)
		else:
			leavePos = self.childSpaces[progress].leavePos
			leaveDir = self.childSpaces[progress].leaveDir
			for playerMB in players:
				self.setNextLevelLoading(belongType, spaceKey, playerMB, 0, 0,mainScriptID)
				playerMB.cell.gotoSpaceUseArg(spaceName, leavePos, leaveDir, magicMazeItem.pickArg)
			if "isReteleport" in pickArg :	#标记是否是重进（从副本外传送进来）
				pickArg.pop("isReteleport")
			else :
				spaceMB = magicMazeItem.mainSpaceMB
				spaceMB.cell.remoteCall("notifySpaceCopyCountChange",(magicMazeItem.copyIsComplet,))
				magicMazeItem.setCopyIsComplet( False )
		
	def gotoMagicMazeExtraSpace(self, belongType, roleMB, pickArg, extraSpaceName):
		spaceKey = pickArg["spaceKey"]
		mainScriptID = pickArg["mainScriptID"]
		magicMazeItem = self.getMagicMazeItem(belongType, spaceKey,mainScriptID)
		teammates = pickArg.get( "teammates", [] )
		if teammates:
			pickArg.pop("teammates")
		args = {"packBelongType": pickArg["belongType"]}
		pickArg.update(args)
		if magicMazeItem != None:
			roleMB.cell.gotoSpaceEnterPos(extraSpaceName, pickArg)
			for teamMember in teammates:	# 传送队员
				teamMember.cell.gotoSpaceEnterPos(extraSpaceName, pickArg)
		
	def getMagicMazeItem(self, belongType, spaceKey,mainScriptID):
		key = (belongType, spaceKey,mainScriptID)
		if key in self.magicMazeInfo:
			return self.magicMazeInfo[key]
		else:
			return None
	
	def setSpaceExtraReward(self, belongType, spaceKey, extraRewardCount, extraRewardRate,mainScriptID):
		magicMazeItem = self.getMagicMazeItem(belongType, spaceKey,mainScriptID)
		if magicMazeItem != None:
			magicMazeItem.setSpaceExtraReward(extraRewardCount, extraRewardRate)

	def setSpaceExtraDice(self, belongType, spaceKey, extraMinDice, extraMaxDice, extraDiceCount, isDiceForward):
		pass
			
	def setSpaceProgress(self, belongType, spaceKey, progress, mainScriptID ):
		magicMazeItem = self.getMagicMazeItem(belongType, spaceKey,mainScriptID)
		if magicMazeItem != None:
			magicMazeItem.setSpaceProgress( progress )
			
	def setSpaceInParent(self, belongType, spaceKey, isInParentSpace,mainScriptID):
		magicMazeItem = self.getMagicMazeItem(belongType, spaceKey,mainScriptID)
		if magicMazeItem != None:
			magicMazeItem.setSpaceInParent(isInParentSpace)
	
	def setExtraSpaceName(self, belongType, spaceKey, extraSpaceName,mainScriptID):
		magicMazeItem = self.getMagicMazeItem(belongType, spaceKey,mainScriptID)
		if magicMazeItem != None:
			magicMazeItem.setExtraSpaceName(extraSpaceName)

	def setCopyIsComplet(self, belongType, spaceKey, copyIsComplet,mainScriptID):
		magicMazeItem = self.getMagicMazeItem(belongType, spaceKey,mainScriptID)
		if magicMazeItem != None:
			magicMazeItem.setCopyIsComplet(copyIsComplet)

	def deregister( self, belongType, spaceKey,mainScriptID ):
		"""
		删除一支队伍
		"""
		key = (belongType, spaceKey,mainScriptID)
		if key in self.magicMazeInfo:
			magicMazeItem = self.magicMazeInfo.pop(key)
			if magicMazeItem.mainSpaceMB and hasattr(magicMazeItem.mainSpaceMB, "cell"):
				magicMazeItem.mainSpaceMB.cell.closeSpace()

	def setSpaceExtraBuffBonus(self, belongType, spaceKey, extraBuffBonus,mainScriptID):
		magicMazeItem = self.getMagicMazeItem(belongType, spaceKey,mainScriptID)
		if magicMazeItem != None:
			magicMazeItem.setSpaceExtraBuffBonus(extraBuffBonus)

	def setNextLevelLoading( self, belongType, spaceKey, roleMB, isLoad, isLoadDoor, mainScriptID ):
		"""
		找到下一个关卡，通知客户端设置预加载地图。（可问胡婷）
		由于客户端仅在调用切关卡时加载下一关卡。因此需要在goto地图之前就设置下一个要去的地图。
		如：goto子副本前，要设置预加载为父副本，才能在进子副本时加载父副本（从子副本出来时要进入的关卡）。
		"""
		magicMazeItem = self.getMagicMazeItem(belongType, spaceKey,mainScriptID)
		progress = magicMazeItem.progress
		isInParentSpace = magicMazeItem.isInParentSpace
		
		if isInParentSpace:										#当前在父副本，进子副本前，需要提前加载父副本
			roleMB.cell.notifyNextLevel( magicMazeItem.mainScriptID, isLoad, isLoadDoor )
		else:													#当前在子副本，进副本父前，需提前加载下个子副本地图
			self.analyticalData(self.multilayerChildSpace[magicMazeItem.index])
			if progress < len(self.childSpaces):
				spaceName = self.childSpaces[progress+1].spaceName
				roleMB.cell.notifyNextLevel( spaceName, isLoad, isLoadDoor )
	
	def gmClear( self ):
		self.magicMazeInfo.clear()