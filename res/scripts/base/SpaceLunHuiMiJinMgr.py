# -*- coding: utf-8 -*-

import KST
import KBEngine
from CoreObject import MgrPersistentObject
import KBEDebug
from ConfigObject.Crond.CrondDatas import CrondDatas
g_CrondDatas = CrondDatas.instance()
from PetEpitome import OriginPetEpitome
import csstatus
import csdefine
import ItemTypeEnum
import ComposeScheme
import Functions
import ItemFactory
import cschannel_msgs
import KBEMath
import Math
import csconst
import time
import Const
import random
from ObjectScript.Pet.PetFactory import g_petFactory

MAX_LINE = 4
TRIGGER_LINE_PLAYER_AMOUNT = 250
LINE_MAX_PLAYER_AMOUNT = 300

class SpaceLunHuiMiJinMgr( MgrPersistentObject.MgrPersistentObject ):
	"""
	轮回秘境管理器
	"""
	def __init__( self ):
		MgrPersistentObject.MgrPersistentObject.__init__( self )

#		self.lineNumberDict = {}					#{lineNumber:[playerDBID,playerDBID...]}  玩家存在洞府，线是固定的
		self.lineNumberToPlayerDBID = {}			#{lineNumber:[playerDBID,playerDBID...]} 不存在洞府的玩家
		self.lineNumberToPlayerDBIDUseTologin = {}	#该数据主要用于玩家登陆时的找lineNumber处理
		
		self.chartTimer = -1						# 阵图timer
		self.defaultReplyTimer  = -1				# 默认应战timer
#		self.BFOutLineDatas = {}					# 玩家下线后的阵图数据 {playerDBID : [玩家的灵能， 每分钟扣除的灵能， 是否激活状态]}
		self.playerDBIDMapDongFu = {}				# 玩家DBID对应洞府，便于查找!不保存数据库
		self.initDFDatas()
		
#		self.toolComposeScheme = {}					# 轮回秘境 工具打造计划{DBID:ComposeScheme}
#		self.toolAlchemist = {}						# 工具打造储物柜
#		self.tripodAlchemist = {}					# 乾坤鼎打造存物柜
		self._beginNewToolScheme()
		self.protectTimer = -1
		self._calculationProtectTime()
		self.repairTimer = -1
		self._calculationRepairTime()
		self.guardReviveTimer = -1					# 守卫复活时间
		self._calculationReviveTime()				# 洞府守卫
		
		self.playerInfo = {}
		
		self.register()
		self.onCompleteInit()
		self.initBatteleFormations()

	def register( self ):
		"""
		注册
		"""
		taskEvents = { 	"SpaceLunHuiMiJinMgr_Notice":"onActiveNotice",
						"SpaceLunHuiMiJinMgr_Start":"onActiveStart",
						"SpaceLunHuiMiJinMgr_End":"onActiveEnd",
						"SpaceLunHuiMiJinMgr_StartDropOriginPet": "onStartDropOriginPet",
						"SpaceLunHuiMiJinMgr_EndDropOriginPet": "onEndDropOriginPet",
						
						"SpaceLunHuiMiJinMgr_PlunderNoticeStart":"onPlunderActiveNoticeStart",
						"SpaceLunHuiMiJinMgr_PlunderNoticeEnd":"onPlunderActiveNoticeEnd",
						"SpaceLunHuiMiJinMgr_PlunderBeforeStart":"onPlunderActiveBeforeStart",
						"SpaceLunHuiMiJinMgr_PlunderStart":"onPlunderActiveStart",
						"SpaceLunHuiMiJinMgr_PlunderEnd":"onPlunderActiveEnd",
						
						"SpaceLunHuiMiJinMgr_WrestNoticeStart":"onWrestActiveNoticeStart",
						"SpaceLunHuiMiJinMgr_WrestNoticeEnd":"onWrestActiveNoticeEnd",
						"SpaceLunHuiMiJinMgr_WrestBeforeStart":"onWrestActiveBeforeStart",
						"SpaceLunHuiMiJinMgr_WrestStart":"onWrestActiveStart",
						"SpaceLunHuiMiJinMgr_WrestEnd":"onWrestActiveEnd",
												
		 }
		for taskName, callbackName in taskEvents.items():
			for scriptID, cmd in g_CrondDatas.getCrondTaskCmds(taskName):
		 		KBEngine.globalData["CrondManager"].addScheme( scriptID, cmd, self, callbackName, -1,() )

	def onActiveNotice( self, cmd, *callbackArgs ):
		"""
		活动公告
		"""
		pass

	def onActiveStart( self, cmd, *callbackArgs ):
		"""
		活动开始(开始刷怪)
		"""
		KBEngine.globalData["SpaceManager"].remoteCallDomain( csconst.LUN_HUI_MI_JIN_SCRIPTID, "activityStart", () )

	def onActiveEnd( self, cmd, *callbackArgs ):
		"""
		活动结束(停止刷怪)
		"""
		KBEngine.globalData["SpaceManager"].remoteCallDomain( csconst.LUN_HUI_MI_JIN_SCRIPTID, "activityEnd", () )

	def onStartDropOriginPet( self, cmd, *callbackArgs ):
		"""
		开始掉落原兽
		"""
		KBEngine.globalData["DropOriginPet"] = 1

	def onEndDropOriginPet( self, cmd, *callbackArgs):
		"""
		停止掉落原兽
		"""
		KBEngine.globalData["DropOriginPet"] = 0
		
	def onPlunderActiveNoticeStart( self, cmd ):
		"""洞府掠夺战 报名开始"""
		KBEngine.globalData["LHMJ_PlunderActiveReady"] = 1
	
	def onPlunderActiveNoticeEnd( self, cmd ):
		"""洞府掠夺战 报名结束"""
		KBEngine.globalData["LHMJ_PlunderActiveReady"] = 0
		for dfObj in self.playerDBIDMapDongFu.values():
			if dfObj.canChallengeOther():
				if dfObj.challengePlayerDBID in self.playerDBIDMapDongFu:
					if self.playerDBIDMapDongFu[dfObj.challengePlayerDBID].canChallengeOther():		# 对方玩家挑战了别人，或者被别人挑战了
						dfObj.doDefaultChallenge()
					else:
						dfObj.replyChallenge( csdefine.CHANLLENGE_REPLY_NO, True )
				else:
					dfObj.doDefaultChallenge()
	
	def onPlunderActiveBeforeStart( self, cmd ):
		"""洞府掠夺战活动即将开始"""
		pass
	
	def onPlunderActiveStart( self, cmd ):
		"""洞府掠夺战活动开始"""
		KBEngine.globalData["LHMJ_PlunderActive"] = 1
		self.occupiedFoundation.onActiveStart()
		
	def onPlunderActiveEnd( self, cmd ):
		"""洞府掠夺战结束"""
		KBEngine.globalData["LHMJ_PlunderActive"] = 0
		self.occupiedFoundation.onActiveEnd( 0 )
		
	def onWrestActiveNoticeStart( self, cmd ):
		"""洞府争夺战 报名开始"""
		KBEngine.globalData["LHMJ_ChallengeActiveReady"] = 1
		
	def onWrestActiveNoticeEnd( self, cmd ):
		"""洞府争夺战 报名结束"""
		KBEngine.globalData["LHMJ_ChallengeActiveReady"] = 0
		for dfObj in self.playerDBIDMapDongFu.values():
			if dfObj.canChallengeOther():
				if dfObj.challengePlayerDBID in self.playerDBIDMapDongFu:
					if self.playerDBIDMapDongFu[dfObj.challengePlayerDBID].canChallengeOther():		# 对方玩家挑战了别人，或者被别人挑战了
						dfObj.doDefaultChallenge()
					else:
						dfObj.replyChallenge( csdefine.CHANLLENGE_REPLY_NO, True )
				else:
					dfObj.doDefaultChallenge()
		
	def onWrestActiveBeforeStart( self, cmd ):
		"""洞府争夺战即将开始"""
		pass
	
	def onWrestActiveStart( self, cmd ):
		"""洞府争夺战开始"""
		KBEngine.globalData["LHMJ_ChallengeActive"] = 1
		self.occupiedFoundation.onActiveStart()
		
	def onWrestActiveEnd( self, cmd ):
		"""洞府争夺战结束"""
		KBEngine.globalData["LHMJ_ChallengeActive"] = 0
		self.occupiedFoundation.onActiveEnd( 1 )
		
	def initDFSpace( self ):
		"""创建已有的洞府Space"""
		if self.lineNumberDict:
			KBEngine.globalData["SpaceManager"].remoteCallDomain( csconst.LUN_HUI_MI_JIN_SCRIPTID, "initDFSpace", ( list(self.lineNumberDict.keys()), ) )
		
	def addLineNumberDict( self, playerDBID, lineNumber ):
		"""
		define method
		记录某线存在洞府的玩家
		"""
		if lineNumber in self.lineNumberDict:
			if playerDBID not in self.lineNumberDict[lineNumber]:
				self.lineNumberDict[lineNumber].append( playerDBID )
		else:
			self.lineNumberDict[lineNumber] = [playerDBID]
		self.onPlayerChange()

	def incPlayerAmount( self, playerDBID, lineNumber ):
		"""
		define method
		增加玩家所在的线
		"""
		if lineNumber in self.lineNumberDict:
			if playerDBID in self.lineNumberDict[ lineNumber ]:
				return

		if lineNumber in self.lineNumberToPlayerDBID:
			if playerDBID not in self.lineNumberToPlayerDBID[ lineNumber ]:
				self.lineNumberToPlayerDBID[ lineNumber ].append( playerDBID )
		else:
			self.lineNumberToPlayerDBID[lineNumber] = [playerDBID]

		if lineNumber in self.lineNumberToPlayerDBIDUseTologin:
			if playerDBID not in self.lineNumberToPlayerDBIDUseTologin[lineNumber]:
				self.lineNumberToPlayerDBIDUseTologin[lineNumber].append( playerDBID )
		else:
			self.lineNumberToPlayerDBIDUseTologin[lineNumber] = [playerDBID]
		self.onPlayerChange()

	def decPlayerAmount( self, playerDBID, lineNumber ):
		"""
		define method
		删除玩家所在的线
		"""
		if lineNumber in self.lineNumberToPlayerDBID and playerDBID in self.lineNumberToPlayerDBID[lineNumber]:
			self.lineNumberToPlayerDBID[lineNumber].remove(playerDBID)

		if lineNumber in self.lineNumberToPlayerDBIDUseTologin and playerDBID in self.lineNumberToPlayerDBIDUseTologin[lineNumber]:
			self.lineNumberToPlayerDBIDUseTologin[lineNumber].remove(playerDBID)
		self.onPlayerChange()

	def findFreeSpaceNumberOnLogin( self ):
		"""
		登陆时找到空闲的spaceNumber
		"""
		if not self.lineNumberToPlayerDBIDUseTologin:
			return 1
		for lineNumber, playerDBIDList in self.lineNumberToPlayerDBIDUseTologin.items():
			tempNum = 0
			if lineNumber in self.lineNumberDict:
				tempNum = len( list( self.lineNumberDict[lineNumber] ) )
			if len( playerDBIDList ) < TRIGGER_LINE_PLAYER_AMOUNT - tempNum :
				return lineNumber
		lineNumberList = list(self.lineNumberToPlayerDBIDUseTologin.keys())
		if max(lineNumberList) < MAX_LINE:
			return (max(lineNumberList) + 1)
		for lineNumber, playerDBIDList in self.lineNumberToPlayerDBIDUseTologin.items():
			playerDBIDList = self.lineNumberToPlayerDBIDUseTologin.get(lineNumber,[])
			if len(playerDBIDList) < LINE_MAX_PLAYER_AMOUNT:
				return lineNumber
		return None

	def requestLineNumberDataOnLogin( self, roleMB, playerDBID, pickArgs ):
		"""
		define method
		登陆请求玩家所在线
		"""
		currentLineNumber = None
		for lineNumber, playerDBIDList in self.lineNumberDict.items():
			if playerDBID in playerDBIDList:
				currentLineNumber = lineNumber
				break
		if currentLineNumber == None:
			currentLineNumber = self.findFreeSpaceNumberOnLogin()
			if currentLineNumber == None:
				ERROR_MSG("Has no Space[%s] Can Enter Player" %(csconst.LUN_HUI_MI_JIN_SCRIPTID))
				return
			else:
				self.incPlayerAmount( playerDBID, currentLineNumber )
		KBEngine.globalData["SpaceManager"].remoteCallDomain( csconst.LUN_HUI_MI_JIN_SCRIPTID, "createAppointSpaceItem", ( roleMB, currentLineNumber, pickArgs ) )

	def findFreeSpaceNumber( self ):
		"""
		找到空闲的spaceNumber
		"""
		if not self.lineNumberToPlayerDBID:
			return 1
		for lineNumber, playerDBIDList in self.lineNumberToPlayerDBID.items():
			tempNum = 0
			if lineNumber in self.lineNumberDict:
				tempNum = len( list( self.lineNumberDict[lineNumber] ) )
			if len(playerDBIDList) < TRIGGER_LINE_PLAYER_AMOUNT - tempNum:
				return lineNumber
		lineNumberList = list(self.lineNumberToPlayerDBID.keys())
		if max(lineNumberList) < MAX_LINE:
			return (max(lineNumberList) + 1)
		for lineNumber, playerDBIDList in self.lineNumberToPlayerDBID.items():
			playerDBIDList = self.lineNumberToPlayerDBID.get( lineNumber, [] )
			if len(playerDBIDList) < LINE_MAX_PLAYER_AMOUNT:
				return lineNumber
		return None

	def requestLineNumberData( self, roleMb, playerDBID, position, direction, pickArgs ):
		"""
		define method
		玩家传送到对应线
		"""
		currentLineNumber = None
		for lineNumber, playerDBIDList in self.lineNumberDict.items():
			if playerDBID in playerDBIDList:
				currentLineNumber = lineNumber
				break
		if currentLineNumber == None:
			currentLineNumber = self.findFreeSpaceNumber()
			if currentLineNumber == None:
				ERROR_MSG("Has no Space[%s] Can Enter Player" %(csconst.LUN_HUI_MI_JIN_SCRIPTID))
				return
			else:
				self.incPlayerAmount( playerDBID, currentLineNumber )
		KBEngine.globalData["SpaceManager"].remoteCallDomain( csconst.LUN_HUI_MI_JIN_SCRIPTID, "gotoAppointSpaceItem", ( roleMb, currentLineNumber, position, direction, pickArgs ) )

	def onPlayerChange( self ):
		"""
		更新数据
		"""
		lineNumberToPlayerNum = {}
		lineNumberToPlayerNum.update( self.lineNumberToPlayerDBID )
		lineNumberToPlayerNum.update( self.lineNumberDict )
		KBEngine.globalData[ "lineNumberToPlayerNum" ] = lineNumberToPlayerNum


#----------------------------------------------------------------------------------------------------
# 轮回秘境打造功能
#----------------------------------------------------------------------------------------------------
	def _beginNewToolScheme( self, minScheme = None ):
		"""初始化打造功能"""
		if minScheme:
			self.popTimer( self.composeTimer )
		elif len(self.toolComposeScheme):
			minScheme = self.toolComposeScheme.getMinTimeScheme()
			
		if minScheme is None:return
		if minScheme.endTime <= time.time():					# 已经可以打造了
			self.onComposeTool()
			return
		self.composeTimer = self.addTimerCallBack(int(minScheme.endTime - time.time()) , "onComposeTool", ())
		
	def requestComposeData(self, playerBase, playerDBID, composeType):
		"""
		<define method>
		请求打造相关数据
		"""
		_composeType = composeType
		endTime = 0.0
		freeNum = 0
		itemID = 0
		successRate = 0.0
		scheme = self.toolComposeScheme.getScheme(playerDBID, composeType)
		if scheme is None and composeType == csdefine.COMPOSE_TOOL_NORMAL:		# 工具打造跟装备打造，同一个界面
			scheme = self.toolComposeScheme.getScheme(playerDBID, csdefine.COMPOSE_TOOL_GREEN_EQUIP)
		if not scheme is None:
			_composeType = scheme.composeType
			endTime = scheme.endTime
			itemID = scheme.itemID
			successRate = scheme.successRate
			scheme.playerMB = playerBase
		
		if composeType == csdefine.COMPOSE_TOOL_TRIPOD:
			freeNum = self.tripodAlchemist.getFreeNum(playerDBID, ItemTypeEnum.BAG_ALCHEMIST_LOCKERS)
			self.tripodAlchemist.sendItemsToClient(playerBase, playerDBID)
			unLockNum = self.tripodAlchemist.getUnlockNum(playerDBID)
		else:
			freeNum = self.toolAlchemist.getFreeNum(playerDBID, ItemTypeEnum.BAG_WORK_SHOP_LOCKERS)
			self.toolAlchemist.sendItemsToClient(playerBase, playerDBID) 
			unLockNum = self.toolAlchemist.getUnlockNum(playerDBID)
		if playerBase:
			playerBase.cell.onRequestComposeData(_composeType, endTime, itemID, freeNum, unLockNum, successRate)

	def addToolComposeScheme(self, playerBase, scheme ):
		"""
		<define method>
		打造计划
		"""
		scheme.playerMB = playerBase
		playerDBID = scheme.playerDBID
		minScheme = self.toolComposeScheme.getMinTimeScheme()
		self.toolComposeScheme.addScheme(scheme)
		if minScheme is None:
			self._beginNewToolScheme()
		elif scheme.endTime < minScheme.endTime:						# 比当前计划还要优先
			self._beginNewToolScheme( scheme )
		
	def reduceComposeTime(self, playerDBID, _time):
		"""
		<define method>
		绿装减少打造时间
		"""
		scheme = self.toolComposeScheme.getScheme(playerDBID, csdefine.COMPOSE_TOOL_GREEN_EQUIP)
		if not scheme is None:
			minScheme = self.toolComposeScheme.getMinTimeScheme()
			minTime = minScheme.endTime
			scheme.reduceComposeTime( _time )
			if scheme.endTime < minTime:
				self._beginNewToolScheme( scheme )
		
	def onComposeTool(self):
		"""
		开始工具打造
		"""
		scheme = self.toolComposeScheme.getMinTimeScheme()
		self.toolComposeScheme.removeScheme(scheme)
		result, item = scheme.doCompose()
		if item:				
			if scheme.composeType == csdefine.COMPOSE_TOOL_TRIPOD:
				self.tripodAlchemist.addPlayerItem(scheme.playerMB, scheme.playerDBID, item, ItemTypeEnum.BAG_ALCHEMIST_LOCKERS )
			else:
				self.toolAlchemist.addPlayerItem(scheme.playerMB, scheme.playerDBID, item, ItemTypeEnum.BAG_WORK_SHOP_LOCKERS )
				
		bAddItem = item is not None
		if scheme.playerMB and scheme.playerMB.client:				# 如果有mailBox
			scheme.playerMB.cell.onFinishCompose(scheme.composeType, bAddItem )
			scheme.playerMB.client.CLIENT_OnFinishCompose(scheme.composeType, scheme.itemID, result)
			
		else:							# 现在玩家上线了，就必定有mailbox
			self._onLookupRoleBaseByName(scheme.name, result, scheme.composeType, scheme.itemID, bAddItem, None)
#			KST.g_baseAppEntity.lookupRoleBaseByName( scheme.name,Functions.Functor(self._onLookupRoleBaseByName, \
#				scheme.name, result, scheme.composeType, scheme.itemID, bAddItem))
		self._beginNewToolScheme()
	
	def _onLookupRoleBaseByName(self, name, result, composeType, itemID, bAddItem, baseMB ):
		""""""
		itemData = ItemFactory.ItemFactoryInst.getItemData(itemID)
		itemName = itemData["ItemName"]
		if baseMB:
			baseMB.cell.onFinishCompose(composeType, bAddItem )
			baseMB.client.CLIENT_OnFinishCompose(composeType, itemID, result)
		else:
			if composeType == csdefine.COMPOSE_TOOL_TRIPOD:
				msgTitle = cschannel_msgs.COMPOSE_TRIPOD_RESULT_TITLE
				if result:
					msgContent = cschannel_msgs.COMPOSE_TRIPOD_RESULT_SUCCESS % itemName
				else:
					msgContent = cschannel_msgs.COMPOSE_TRIPOD_RESULT_FAIL % itemName
		
			else:
				msgTitle = cschannel_msgs.COMPOSE_TOOL_RESULT_TITLE
				if result:
					msgContent = cschannel_msgs.COMPOSE_TOOL_RESULT_SUCCESS % itemName
				else:
					if composeType == csdefine.COMPOSE_TOOL_NORMAL:
						msgContent = cschannel_msgs.COMPOSE_TOOL_RESULT_FAIL % itemName
					else:
						msgContent = cschannel_msgs.COMPOSE_TOOL_GREEP_RESULT_FAIL % itemName
			KBEngine.globalData["MailManager"].sendWithMailbox(None, None, name, csdefine.MAIL_SENDER_TYPE_SYS, \
				cschannel_msgs.MAIL_SEND_SYSTEM, msgTitle, msgContent, 0, 0, [], 0, 0)
		
	def requestTakeToolItem(self, playerCell, playerDBID, composeType, order):
		"""
		<define method>
		取物品
		"""
		if composeType == csdefine.COMPOSE_TOOL_TRIPOD:
			item = self.tripodAlchemist.pop(playerCell, playerDBID, order)
		else:
			item = self.toolAlchemist.pop(playerCell, playerDBID, order)
		if item:
			playerCell.onRequestTakeToolItem(composeType, item)
		else:
			ERROR_MSG("player(dbid:%d) take tool(type:%d) item err!cannot find item(%d)"%(playerDBID, composeType, order))
	
	def GM_finishCompose( self, playerMB, playerDBID ):
		"""
		<define method>
		GM 指令设置完成 打造
		"""
		scheme = self.toolComposeScheme.getMinTimeScheme()
		if scheme is None:return
		isMinScheme = False
		if scheme.playerDBID == playerDBID:
			isMinScheme = True
			self.popTimer( self.composeTimer )
		schemeList = []
		scheme = self.toolComposeScheme.getScheme(playerDBID, csdefine.COMPOSE_TOOL_NORMAL)
		if not scheme is None:
			schemeList.append( scheme )
		scheme = self.toolComposeScheme.getScheme(playerDBID, csdefine.COMPOSE_TOOL_GREEN_EQUIP)
		if not scheme is None:
			schemeList.append( scheme )
		scheme = self.toolComposeScheme.getScheme(playerDBID, csdefine.COMPOSE_TOOL_TRIPOD)
		if not scheme is None:
			schemeList.append( scheme )
		for scheme in schemeList:
			self.toolComposeScheme.removeScheme(scheme)
			result, item = scheme.doCompose()
			if item:				
				if scheme.composeType == csdefine.COMPOSE_TOOL_TRIPOD:
					self.tripodAlchemist.addPlayerItem(playerMB, scheme.playerDBID, item, ItemTypeEnum.BAG_ALCHEMIST_LOCKERS )
				else:
					self.toolAlchemist.addPlayerItem(playerMB, scheme.playerDBID, item, ItemTypeEnum.BAG_WORK_SHOP_LOCKERS )
			bAddItem = item is not None
			playerMB.onFinishCompose(scheme.composeType, bAddItem )
			playerMB.client.CLIENT_OnFinishCompose(scheme.composeType, scheme.itemID, result)
		if isMinScheme:
			self._beginNewToolScheme()
#----------------------------------------------------------------------------------------------------
# 轮回秘境洞府功能
#----------------------------------------------------------------------------------------------------
	def requestPlayerDFDatas( self, baseMB, playerDBID, lineNumber, offset):
		"""
		define method
		请求某条线的洞府数据
		"""
		totalPage, freeDFNum, DFDatas = self.occupiedFoundation.getDFDataByLineNumber( playerDBID, lineNumber, offset )
		baseMB.client.OnRequestPlayerDFDatas(lineNumber, list(self.occupiedFoundation.keys()), totalPage, freeDFNum, DFDatas)

	def requestDFDatas( self, baseMB, playerDBID, lineNumber, offset):
		"""
		define method
		请求某条线的洞府数据
		"""
		totalPage, freeDFNum, DFDatas = self.occupiedFoundation.getDFDataByLineNumber( playerDBID, lineNumber, offset )
		baseMB.client.OnRequestDFDatas(totalPage, freeDFNum, DFDatas)
		
	def requestDFDatasByPage( self, baseMB, playerDBID, lineNumber, page, offset ):
		"""
		define method
		请求第几页的洞府数据
		"""
		baseMB.client.OnRequestDFDatasByPage( self.occupiedFoundation.getDFDataByPage( playerDBID, lineNumber, page, offset) )

	def initDFDatas( self ):
		""""""
		for lineNumber, lnDFs in self.occupiedFoundation.items():
			for group, dfObj in lnDFs.items():
				if dfObj.playerDBID:
					self.playerDBIDMapDongFu[dfObj.playerDBID] = dfObj

	def addOccupiedFoundationPos(self, lineNumber, group, position, dongFuMail, dongFuType):
		"""
		define method
		增加基地数据
		"""
		self.occupiedFoundation.addDongFuData( lineNumber, group, dongFuMail, position, dongFuType )
		objData = self.occupiedFoundation[lineNumber][group]
		
		if objData.occupyProtectTime:
			if int(time.time()) >= objData.occupyProtectTime:
				objData.occupyProtectTime = 0.0
				objData.dongFuState = csdefine.LHMJ_BUILD_STATE_NONE
			else:
				dongFuMail.updateOccupyTime( objData.occupyProtectTime )
		dongFuMail.updateDongFuState(objData.dongFuState, objData.getBuildLevel( csdefine.LHMJ_BUIILD_LING_QUAN), objData.playerDBID, self.getLTShowDatasbyDF(objData.playerDBID))
		
		# 恢复阵图数据
		if objData.batteleID:
			id = objData.playerMB.id if objData.playerMB else 0
			npcID = objData.dongFuBase.id
			itemInst = ItemFactory.ItemFactoryInst.createDynamicItem(objData.batteleID, 1, {"uid" : 0})
			KBEngine.globalData["SpaceManager"].remoteCallDomain( csconst.LUN_HUI_MI_JIN_SCRIPTID, "createCellEntityByScriptID", 
			( id, objData.playerDBID, lineNumber, itemInst.outScriptID, npcID, objData.group) )
	
	def _calculationProtectTime( self ):
		"""计算地基的保护时间"""
		if self.protectTimer != -1:return
		objData = self.occupiedFoundation.getMinProtectDongFu()
		if objData:
			if objData.occupyProtectTime <= time.time():
				self.dealOutProtectTime(objData)
				return
			self.protectTimer = self.addTimerCallBack(objData.occupyProtectTime - time.time(), "dealOutProtectTime", (objData,) )
			
	def dealOutProtectTime( self, objData ):
		"""处理过了保护时间的地基"""
		objData.occupyProtectTime = 0.0
		objData.dongFuState = csdefine.LHMJ_BUILD_STATE_NONE
		if objData.dongFuBase:
			objData.dongFuBase.onProtectTimeOut()
		if objData.playerMB:
			objData.playerMB.cell.onProtectTimeOut()
		objData.playerMB = None
		objData.playerDBID = 0
		objData.playerName = ""
		self.protectTimer = -1
		self._calculationProtectTime()
			
	def findFreeBuild( self, lineNumber ):
		"""寻找 可占领的建筑"""
		hasRequest = []
		for key, objData in self.occupiedFoundation[lineNumber].items():
			if objData.dongFuState == csdefine.LHMJ_BUILD_STATE_NONE:					# 先去配置没有人申请的建筑
				return key
			if objData.dongFuState == csdefine.LHMJ_BUILD_STATE_REQUEST:
				hasRequest.append(key)
		if hasRequest:										# 如果都被申请了，只能随机一个！然后，看谁先占领
			return random.choice( hasRequest )
		return None

	def gmSetOccupiedFoundation( self, playerCell, lineNumber, group ):
		"""
		<define method>
		GM指令设置 地基
		"""
		objData = self.occupiedFoundation[lineNumber][group]
		if objData.dongFuState in [csdefine.LHMJ_BUILD_STATE_NONE, csdefine.LHMJ_BUILD_STATE_REQUEST]:
			objData.dongFuState = csdefine.LHMJ_BUILD_STATE_REQUEST
			playerCell.updateGroundPosDict( group, objData.position )

	def requestOccupiedFoundation( self, playerCell, lineNumber, group ):
		"""
		<define method>
		请求地基位置
		"""
		index = None
		if group != -1:
			objData = self.occupiedFoundation[lineNumber][group]
			if objData.dongFuState in [csdefine.LHMJ_BUILD_STATE_NONE, csdefine.LHMJ_BUILD_STATE_REQUEST]:
				index = group
				
		if index == None:			# 被占领了，就重新找
			index = self.findFreeBuild( lineNumber )
			if index:
				objData = self.occupiedFoundation[lineNumber][index]
				objData.dongFuState = csdefine.LHMJ_BUILD_STATE_REQUEST
				playerCell.updateGroundPosDict( index, objData.position )
			else:
				playerCell.client.statusMessage( csstatus.LHMJ_BUILD_IS_FULL, "" )
				return
		playerCell.client.OnNotifyBuildPos( KBEMath.KBEngine2UnrealPosition(objData.position), objData.dongFuBase.id )

	def requestOccupyBuild( self, playerBase, lineNumber, group, playerDBID, playerName ):
		"""
		define method
		占领基地
		"""
		objData = self.occupiedFoundation[lineNumber][group]
		if objData.dongFuState in [csdefine.LHMJ_BUILD_STATE_NONE, csdefine.LHMJ_BUILD_STATE_REQUEST]:
			objData.dongFuState = csdefine.LHMJ_BUILD_STATE_OCUPPY
			id = 0
			if self.occupiedFoundation[lineNumber][group].dongFuBase:
				id = self.occupiedFoundation[lineNumber][group].dongFuBase.id
			self.occupiedFoundation.updateDongFuOccupyData( lineNumber, group, playerBase, playerDBID, playerName, csconst.LHMJ_BUILD_OCCUPY_TIME + time.time() )
			self._calculationProtectTime()
			playerBase.cell.onRequestOccupyBuild( id )
		else:
			playerBase.client.statusMessage( csstatus.OCCUPY_BUILD_FAILURE, "")

	def onBuildDongFuFinish( self, lineNumber, group, playerDBID ):
		"""
		define method
		洞府建造完成回调
		"""
		self.addLineNumberDict(playerDBID, lineNumber)
		objData = self.occupiedFoundation[lineNumber][group]
		objData.onInitPlayerMB( objData.playerMB )
		self.playerDBIDMapDongFu[playerDBID] = objData
		minObj = self.occupiedFoundation.getMinProtectDongFu()
		if objData:
			objData.dongFuState = csdefine.LHMJ_BUILD_STATE_READY
			objData.occupyProtectTime = 0.0
			if objData == minObj:
				self.popTimer( self.protectTimer )
				self.protectTimer = -1
				self._calculationProtectTime()

	def requestOccupyBuildData( self, lineNumber, groundPosDict ):
		"""
		define method
		请求数据(使用破界符)
		"""
		for key in groundPosDict.keys():
			objData = self.occupiedFoundation[lineNumber][key]
			if objData.dongFuBase:
				objData.dongFuBase.stopParticles()
	
	def updateDongFuLevel( self, playerDBID, buildType, level ):
		"""
		define method
		更新洞府建筑等级
		"""
		objData = self.playerDBIDMapDongFu[playerDBID]
		objData.setBuildLevel( buildType, level )
#----------------------------------------------------------------------------------------------------
# 洞府建筑功能
#----------------------------------------------------------------------------------------------------
	def getLTShowDatasbyDF(self, belongDBID ):
		"""
		获取灵田种植数据（客户端要在洞府建筑显示，只显示 4个）
		"""
		datas = []
		if belongDBID in self.lingTianData:
			ltDatas = self.lingTianData[belongDBID]
			for scriptID in csconst.LHMJ_LING_TIAN_INIT_SCRIPT:
				if scriptID in ltDatas:
					datas.append(ltDatas[scriptID])
		return datas

	def requestSpaceNPCInfo( self, spaceCell, belongDBID, spaceScriptID ):
		"""
		define method
		请求数据
		"""
		# 因为mgr在同一个base，所以只发一次！然后，在这里转发
		KBEngine.globalData["TrainSoldierGroundManager"].requestSpaceNPCInfo( spaceCell, belongDBID, spaceScriptID )
		dfLevel = 1
		level = 1
		datas = []
		dfObj = self.playerDBIDMapDongFu[belongDBID]
		if belongDBID in self.lingTianData:
			datas = list( self.lingTianData[belongDBID].values() )
		hasGuardRTime = False
		if dfObj.guardReviveTime > 0:
			hasGuardRTime = True
		spaceCell.onRequestDFDatas(dfObj.buildLevels, datas, list(dfObj.destroyBuild), dfObj.guardType, self.shouLanData.getPetSimpleData( belongDBID ), hasGuardRTime )
		if dfObj.isChallengeing():			# 因为洞府的数据需要加载完了，才能执行活动
			spaceCell.onChallengeActiveStart()
		
	def saveLingTianInfo( self, belongDBID, scriptID, seedNum, growthStage, growTime ):
		"""
		define method
		保存灵田数据
		"""
		self.lingTianData.addLingTianData( belongDBID, scriptID, seedNum, growthStage, growTime )
		if scriptID in csconst.LHMJ_LING_TIAN_INIT_SCRIPT and growthStage == 1:					# 只在种植第一阶段更新
			dfObj = self.playerDBIDMapDongFu[belongDBID]
			if dfObj.dongFuBase:
				dfObj.dongFuBase.updateLTDatas( self.getLTShowDatasbyDF( belongDBID ) )
		
	def removeLingTianInfo( self, belongDBID, scriptID ):
		"""
		define method
		收获，移除保存的灵田数据
		"""
		self.lingTianData.removeLingTianData( belongDBID, scriptID )
		if scriptID in csconst.LHMJ_LING_TIAN_INIT_SCRIPT:
			dfObj = self.playerDBIDMapDongFu[belongDBID]
			if dfObj.dongFuBase:
				dfObj.dongFuBase.updateLTDatas( self.getLTShowDatasbyDF( belongDBID ) )
		
	def changeGuardType( self, belongDBID, oldType, newType ):
		"""
		define method
		置换守卫类型
		"""
		self.playerDBIDMapDongFu[belongDBID].changeGuardType( oldType, newType )
		
	def requestOriginPet( self, playerMB, playerDBID ):
		"""
		<define method>
		请求原兽数据
		"""
		if playerDBID in self.shouLanData:
			for petObj in self.shouLanData[playerDBID].values():
				playerMB.client.CLIENT_addOriginPet( petObj )
		
	def generateOriginPet( self, playerCMB, playerDBID, scriptID, quality, solution, camp ):
		"""
		<define method>
		生成原兽
		"""
		pet = OriginPetEpitome()
		pet.generatePetAttr( scriptID, quality, solution, camp )
		self.shouLanData.addPet( playerDBID, pet )
		playerCMB.client.CLIENT_addOriginPet( pet )
		self.noticeSpaceDFAddOriginPet( playerDBID, pet )
		
	def noticeSpaceDFAddOriginPet( self, playerDBID, pet ):
		"""通知洞府，增加原兽"""
		if playerDBID in self.playerDBIDMapDongFu:			# 有洞府
			dfObj = self.playerDBIDMapDongFu[playerDBID]
			pickArgs = {"spaceKey": str(playerDBID), "belongType" : csdefine.SPACE_BELONG_PERSON}
			petData = {}
			petData["uid"] = pet.uid
			petData["scriptID"] = pet.scriptID
			petData["quality"] = pet.quality
			petData["bEvolution"] = pet.isEvolution()
			KBEngine.globalData["SpaceManager"].remoteCallDomain( csconst.DONGFU_MAP_SPACESCRIPTID[dfObj.dongFuType], "onAddOriginPet", ( pickArgs, petData ) )
		
	def noticeSpaceDFRemoveOriginPet( self, playerDBID, uid, directDel = False ):
		"""通知洞府，移除原兽"""
		if playerDBID in self.playerDBIDMapDongFu:			# 有洞府
			dfObj = self.playerDBIDMapDongFu[playerDBID]
			pickArgs = {"spaceKey":str( playerDBID ), "belongType" : csdefine.SPACE_BELONG_PERSON}
			KBEngine.globalData["SpaceManager"].remoteCallDomain( csconst.DONGFU_MAP_SPACESCRIPTID[dfObj.dongFuType], "onRemoveOriginPet", ( pickArgs, uid, directDel ) )
		
	def noticSpaceDFExChangeOriginPet( self, playerDBID, pet, uid ):
		"""通知洞府，交互位置"""
		if playerDBID in self.playerDBIDMapDongFu:			# 有洞府
			dfObj = self.playerDBIDMapDongFu[playerDBID]
			pickArgs = {"spaceKey": str(playerDBID), "belongType" : csdefine.SPACE_BELONG_PERSON}
			petData = {}
			petData["uid"] = pet.uid
			petData["scriptID"] = pet.scriptID
			petData["bEvolution"] = pet.isEvolution()
			KBEngine.globalData["SpaceManager"].remoteCallDomain( csconst.DONGFU_MAP_SPACESCRIPTID[dfObj.dongFuType], "onExChangeOriginPet", ( pickArgs, petData, uid ) )
		
	def activePetEnterFence( self, playerDBID, pet ):
		"""
		<define method>
		出战幻兽进入兽栏
		"""
		self.shouLanData.addPet( playerDBID, pet )
		self.noticeSpaceDFAddOriginPet( playerDBID, pet )
		
	def petOutsideFromFence( self, playerMB, playerDBID, uid ):
		"""
		<define method>
		幻兽出栏，并召唤到玩家身边
		"""
		originPet = self.shouLanData.getPet( playerDBID, uid )
		if originPet is None:return
		
		if not originPet.isEvolution():
			KBEDebug.ERROR_MSG("Pet(%d) cannot outside!as it not evolution"%uid)
			return
		if originPet.isCDTime():
			playerMB.client.statusMessage(csstatus.PET_CANNOT_OUTSIDE_CD_TIME, "")
			return
		self.shouLanData.popPet( playerDBID, uid )
		playerMB.petOutsideFromFence( originPet )
		playerMB.client.CLIENT_OnPetOutsideFromFence( str(uid) )
		self.noticeSpaceDFRemoveOriginPet( playerDBID, uid, True )
	
	def exChangePetFromFence( self, playerMB, playerDBID, originPet, leaveUID ):
		"""
		<define method>
		出战幻兽 与 兽栏交换
		"""
		leavePet = self.shouLanData.popPet( playerDBID, leaveUID )
		self.shouLanData.addPet( playerDBID, originPet )
		playerMB.petOutsideFromFence( leavePet )
		self.noticSpaceDFExChangeOriginPet( playerDBID, originPet, leaveUID )
	
	def freePetFromFence( self, playerMB, playerDBID, uid ):
		"""
		<define method>
		原兽放生
		"""
		if self.shouLanData.popPet( playerDBID, uid ):
			playerMB.client.CLIENT_OnFreePetFromFence( str( uid ) )
			playerMB.onUpdateOriginPetVolume( self.shouLanData.getPetNum( playerDBID ) )
			self.noticeSpaceDFRemoveOriginPet( playerDBID, uid, False )
	
	def canFeedOriginPet( self, playerMB, pet, item ):
		"""原兽能否喂养"""
		if pet is None or item is None:
			return False
		petObjectScript = g_petFactory.getObject( pet.scriptID )
		if not item.canFeedPet( petObjectScript.foodType, pet.quality ):
			KBEDebug.ERROR_MSG("Can feed pet(%s)！as foodType(%d) is wrong"%(pet.scriptID, item.foodType))
			return False
		if pet.isCDTime():
			playerMB.client.statusMessage( csstatus.CANOT_FEED_PET_AS_CD_COOL , "" )
			return False
		if item.__class__.__name__ == "ItemPetFood":
			return not pet.canEvolution()
		elif item.__class__.__name__ == "ItemPetExpFood":			# 已经进化，才能食经验
			if not pet.isEvolution():
				playerMB.client.statusMessage( csstatus.PET_CANT_FOOD_WILDNESS, "" )
				return False
			return True
		KBEDebug.ERROR_MSG("Can feed pet!as item script(%s) is err!"%item.__module__)
		return False
		
	def feedOriginPet( self, playerMB, playerDBID, uid, itemID, num, spaceType ):
		"""
		<define method>
		喂养原兽
		"""
		originPet = self.shouLanData.getPet( playerDBID, uid )
		item = ItemFactory.ItemFactoryInst.createDynamicItem( itemID, 1, {"uid":0})
		if self.canFeedOriginPet( playerMB, originPet, item ):
			if item.__class__.__name__ == "ItemPetFood":
				wildness = 0
				for i in range(0, num):
					wildness += item.getOriginPetWildness( originPet.quality )
				originPet.reduceWildness( wildness )
				cdTime = Functions.getTime(item.getCDTime(spaceType) * num)
				originPet.setCDTime(cdTime)
				playerMB.client.CLIENT_OnFeedPetWildness( str(uid), originPet.wildness, str(cdTime) )
			elif item.__class__.__name__ == "ItemPetExpFood":			# 已经进化，才能食经验
				exp = 0
				for i in range(0, num):
					exp += item.getPetExp(originPet.quality)
				originPet.addExp( playerMB, exp )
				cdTime = Functions.getTime(item.getCDTime(spaceType) * num)
				originPet.setCDTime(cdTime)
				playerMB.client.CLIENT_OnFeedPetExp( str(uid), originPet.step, originPet.exp, str(cdTime) )
				playerMB.client.statusMessage( csstatus.PET_GET_EXP, originPet.getName()+ "|" + str(exp))
				
			playerMB.cell.remoteSuccessPay( )
		else:
			playerMB.cell.remoteFailPay( )
		
	def GM_clearPetCDTime( self, playerMB, playerDBID ):
		"""
		<define method>
		移除所有的幻兽喂养CD
		"""
		if playerDBID in self.shouLanData:
			for pet in self.shouLanData[playerDBID].values():
				pet.setCDTime(0)
			playerMB.client.CLIENT_clearPetCDTime()
		
	def evolutionOriginPet( self, playerMB, playerDBID, uid ):
		"""
		<define method>
		原兽进化
		"""
		pet = self.shouLanData.getPet( playerDBID, uid )
		if pet and pet.canEvolution() and not pet.isEvolution():
			pet.evolution()
			playerMB.client.CLIENT_onEvolutionPet( str(uid) )
			playerMB.cell.remoteSuccessPay( )
		else:
			playerMB.cell.remoteFailPay( )
	
	def onPetCorralDestroy( self, srcPlayerMB, srcPlayerDBID, petUID, dstPlayerMB, dropPro ):
		"""
		<define method>
		兽栏被击破，幻兽逃跑（或掉落）
		"""
		pet = self.shouLanData.popPet( srcPlayerDBID, petUID )
		if pet:
			if not pet.quality in dropPro:
				KBEDebug.ERROR_MSG("can not find pet(%d) quality(%d) drop probability!"%(petUID, pet.quality), dropPro )
				return
			if srcPlayerMB:
				srcPlayerMB.client.CLIENT_OnFreePetFromFence( str( petUID ) )
			if random.randint(1,100) <= dropPro[pet.quality]:
				dstPlayerMB.onGetPetByKillPetCorral( pet )
				self.noticeSpaceDFRemoveOriginPet( srcPlayerDBID, petUID, True )
			else:
				self.noticeSpaceDFRemoveOriginPet( srcPlayerDBID, petUID, False )			# 逃跑了，谁都别要
#----------------------------------------------------------------------------------------------------
# 轮回秘境 阵图功能
#----------------------------------------------------------------------------------------------------
	def initBatteleFormations( self ):
		"""开启服务器，重新计时"""
		hasBF = False
		for playerDBID, playerDatas in self.BFOutLineDatas.items():
			if playerDatas[2]:
				hasBF = True
				break
		if hasBF:
			self.chartTimer = self.addTimerRepeat( csconst.LUN_HUI_MI_JING_SOUME_TIME, "onArriveOneMinute", () )
	
	def onSpaceDongFuCreateFinish( self, belongDBID, spaceNumber ):
		"""洞府创建完毕回调，恢复数据"""
		if belongDBID in self.BFOutLineDatas:
			if self.BFOutLineDatas[belongDBID][2] == 0:			# 下线后，被取消激活了
				return
		if belongDBID in self.playerDBIDMapDongFu:
			dfObj = self.playerDBIDMapDongFu[belongDBID]
			if dfObj.batteleID:
				item = ItemFactory.ItemFactoryInst.createDynamicItem( dfObj.batteleID, 1, {"uid" : 0})
				KBEngine.globalData["SpaceManager"].remoteCallDomain( csconst.DONGFU_MAP_SPACESCRIPTID[dfObj.dongFuType], "createBattleformation", (spaceNumber, item.insScriptID, item.insPos, item.insDir))

	def activeBatteleFormations(self, playerDBID, itemID, scriptID):
		"""
		define method
		激活 阵图
		"""
		dfObj = self.playerDBIDMapDongFu[playerDBID]
		dfObj.openBattele( itemID )
		id = dfObj.playerMB.id if dfObj.playerMB else 0
		lineNumber = dfObj.lineNumber
		npcID = dfObj.dongFuBase.id if dfObj.dongFuBase else 0
		KBEngine.globalData["SpaceManager"].remoteCallDomain( csconst.LUN_HUI_MI_JIN_SCRIPTID, 
		"createCellEntityByScriptID", ( id, playerDBID, lineNumber, scriptID, npcID, dfObj.group ) )
		
	def closeBattleFormations(self, playerDBID ):
		"""
		define method
		关闭 阵图
		"""
		if playerDBID in self.playerDBIDMapDongFu:
			dfObj = self.playerDBIDMapDongFu[playerDBID]
			if dfObj.batteleID:
				currentLineNumber = dfObj.lineNumber
				KBEngine.globalData["SpaceManager"].remoteCallDomain( csconst.LUN_HUI_MI_JIN_SCRIPTID, "destroyCellEntityByScriptID", ( currentLineNumber, dfObj.group ) )
				if playerDBID in self.BFOutLineDatas:			# 玩家下线了，销毁洞府的阵图
					KBEngine.globalData["SpaceManager"].remoteCallDomain( csconst.DONGFU_MAP_SPACESCRIPTID[dfObj.dongFuType], "destroyBattleformation", (currentLineNumber,))
				dfObj.closeBattele()
		
	def onPlayerOnline( self, playerBase, playerDBID):
		"""
		define methods
		玩家上线了
		"""
		if playerDBID in self.BFOutLineDatas:
			remainPsionic, per, isActive = self.BFOutLineDatas.pop(playerDBID)
			playerBase.cell.onInitBFCallBack(remainPsionic, isActive)
			if len(self.BFOutLineDatas) == 0:
				self.popTimer( self.chartTimer )
				self.chartTimer = -1
		if playerDBID in self.playerDBIDMapDongFu:
			dfObj = self.playerDBIDMapDongFu[playerDBID]
			dfObj.onInitPlayerMB( playerBase )
		elif playerDBID in self.loseDFPlayer:
			data = self.loseDFPlayer.pop(playerDBID)
			playerBase.cell.onDFBeingOccupy( data["level"] )
			playerBase.client.statusMessage( csstatus.LHMJ_DF_BEING_OCCUPY, data["name"] )
		else:							# 洞府可能被占领了~~
			playerBase.cell.onInitDongFuErr()
		playerBase.cell.onUpdateOriginPetVolume( self.shouLanData.getPetNum(playerDBID) )
		
		self.toolComposeScheme.onPlayerOnLine( playerDBID, playerBase )
		self.pauseToolComposeScheme.onPlayerOnLine( playerDBID, playerBase )
		self.requestComposeData( playerBase, playerDBID, csdefine.COMPOSE_TOOL_TRIPOD)
		self.requestComposeData( playerBase, playerDBID, csdefine.COMPOSE_TOOL_NORMAL)
	
	def onPlayerOffLine( self, playerDBID ):
		"""
		<define method>
		玩家下线
		"""
		self.toolComposeScheme.onPlayerOffLine( playerDBID )
		self.pauseToolComposeScheme.onPlayerOffLine( playerDBID )
		if playerDBID in self.playerDBIDMapDongFu:
			self.playerDBIDMapDongFu[playerDBID].onPlayerOffLine()
	
	def onChallengePlayerOnLine( self, playerBase, playerDBID, belongDBID ):
		"""
		define methods
		挑战玩家上线了
		"""
		if belongDBID in self.playerDBIDMapDongFu:
			self.playerDBIDMapDongFu[belongDBID].onChallengePlayerOnLine( playerBase, playerDBID )
		else:
			playerBase.cell.onRequestLHMJChallengeReplyNo()
		
	def onChallengePlayerOffLine( self, playerDBID ):
		"""
		<define method>
		挑战玩家下线
		"""
		if playerDBID in self.playerDBIDMapDongFu:
			self.playerDBIDMapDongFu[playerDBID].onChallengePlayerOffLine()
	
	def onOpenBFPlayerOutLine( self, playerDBID, psionic, perPsionic ):
		"""
		define methods
		激活 阵图的玩家下线了
		"""
		self.BFOutLineDatas[playerDBID] = [psionic, perPsionic, 1]
		if self.chartTimer == -1:
			self.chartTimer = self.addTimerRepeat( csconst.LUN_HUI_MI_JING_SOUME_TIME, "onArriveOneMinute", () )
			
	def onArriveOneMinute( self ):
		""""""
		# playerDatas  [玩家的灵能，每分钟消耗灵能，是否激活状态, 占领的洞府索引， 大地图创建的scriptID]
		for playerDBID, playerDatas in self.BFOutLineDatas.items():			
			if playerDatas[2]:
				if playerDatas[0] >= playerDatas[1]:
					playerDatas[0] -= playerDatas[1]
				else:
					playerDatas[2] = 0
					self.closeBattleFormations( playerDBID )

#----------------------------------------------------------------------------------------------------
# 轮回秘境 洞府掠夺/争夺战功能
#----------------------------------------------------------------------------------------------------
	def requestLHMJChallenge( self, playerBase, playerName, playerDBID, accountDBID, playerLevel, level, lineNumber, group ):
		"""
		define method
		对洞府发起挑战
		"""
		ownerDF = self.playerDBIDMapDongFu.get( playerDBID, None )
		if ownerDF and not ownerDF.canChallengeOther():
			playerBase.statusMessage( csstatus.CHALLENGE_PEOPLE_TOO_MUSH, "" )
			return
		if lineNumber in self.occupiedFoundation and group in self.occupiedFoundation[lineNumber]:
			dfObj = self.occupiedFoundation[lineNumber][group]
			if dfObj.dealChallenge( playerBase, playerName, playerDBID, level ):
				playerBase.cell.onRequestLHMJChallenge( dfObj.playerDBID )
				playerBase.client.OnRequestLHMJChallenge(lineNumber, dfObj.playerName)
				if self.defaultReplyTimer == -1:
					self.addDefaultChallengeTimer( dfObj )
				self.playerInfo[playerDBID] = (accountDBID, playerLevel)
					
	def replayLHMJChallenge(self, playerDBID, accountDBID, playerLevel, reply):
		"""
		define method
		回应洞府挑战
		"""
		dfObj = self.playerDBIDMapDongFu[playerDBID]
		dfObj.replyChallenge( reply )
		self.playerInfo[playerDBID] = (accountDBID, playerLevel)
	
	def onReplyChallenge( self, playerDBID, challengePlayerDBID ):
		"""同意洞府挑战"""
		if challengePlayerDBID in self.playerDBIDMapDongFu:
			self.playerDBIDMapDongFu[challengePlayerDBID].setChallengeOtherDBID( playerDBID )
	
	def addDefaultChallengeTimer( self, dfObj ):
		"""
		"""
		ctime = dfObj.challengeDefaultTime - time.time()
		if ctime <= 0:
			if dfObj.challengePlayerDBID in self.playerDBIDMapDongFu:
				if self.playerDBIDMapDongFu[dfObj.challengePlayerDBID].canChallengeOther():		# 对方玩家挑战了别人，或者被别人挑战了
					dfObj.doDefaultChallenge()
				else:
					dfObj.replyChallenge( csdefine.CHANLLENGE_REPLY_NO, True )
			else:
				dfObj.doDefaultChallenge()
			newDfObj = self.occupiedFoundation.getMinDefaultReplyTime()
			if newDfObj.isNotReply():
				self.addDefaultChallengeTimer( newDfObj )
				return
		else:
			self.defaultReplyTimer = self.addTimerCallBack( dfObj.challengeDefaultTime - time.time(), "dealDefaultChallengeTimer", (dfObj,))
		
	def dealDefaultChallengeTimer( self, dfObj ):
		""""""
		self.dealDefaultChallengeTimer = -1
		if dfObj.challengePlayerDBID in self.playerDBIDMapDongFu:
			if self.playerDBIDMapDongFu[dfObj.challengePlayerDBID].canChallengeOther():		# 对方玩家挑战了别人，或者被别人挑战了
				dfObj.doDefaultChallenge()
			else:
				dfObj.replyChallenge( csdefine.CHANLLENGE_REPLY_NO, True )		# 如果有挑战了，走拒绝应战流程
		else:
			dfObj.doDefaultChallenge()
		newDfObj = self.occupiedFoundation.getMinDefaultReplyTime()
		if newDfObj.isNotReply():
			self.addDefaultChallengeTimer( newDfObj )
			return
	
	def onMonsterCoverBeAttack(self, belongDBID, playerName):
		"""
		define method
		洞府外的 保护罩被攻击了
		"""
		if belongDBID in self.playerDBIDMapDongFu:
			self.playerDBIDMapDongFu[belongDBID].onMonsterCoverBeAttack( playerName )
	
	def onMonsterCoverBeKill(self, belongDBID, result):
		"""
		define method
		洞府外的 保护罩被破坏了
		"""
		if belongDBID in self.playerDBIDMapDongFu:
			self.playerDBIDMapDongFu[belongDBID].onMonsterCoverBeKill( result )
			
	def noticeAPlayerEnter(self, belongDBID, playerName):
		"""
		define method
		攻方玩家进入洞府
		"""
		if belongDBID in self.playerDBIDMapDongFu:
			self.playerDBIDMapDongFu[belongDBID].noticeAPlayerEnter( playerName )
	
	def onGuardDead( self, belongDBID ):
		"""
		define method
		洞府守卫死亡
		"""
		if belongDBID in self.playerDBIDMapDongFu:
			self.playerDBIDMapDongFu[belongDBID].onGuardDead()
	
	def onDFBuildDestroy(self, belongDBID, buildType, itemStr):
		"""
		define method
		洞府建筑 被破坏
		"""
		self.playerDBIDMapDongFu[belongDBID].onBuildDestroy( buildType, itemStr )
			
		isMinScheme = False
		scheme = None
		minScheme = self.toolComposeScheme.getMinTimeScheme()
		if minScheme is None:return
		if minScheme.playerDBID == belongDBID:
			isMinScheme = True
			self.popTimer( self.composeTimer )
		if buildType == csdefine.LHMJ_BUIILD_QIAN_KU_DING:
			scheme = self.toolComposeScheme.getScheme(belongDBID, csdefine.COMPOSE_TOOL_TRIPOD)			# 建筑被打坏了，就不能打造了
		elif buildType == csdefine.LHMJ_BUIILD_GONG_FANG:
			scheme = self.toolComposeScheme.getScheme(belongDBID, csdefine.COMPOSE_TOOL_NORMAL)
			if scheme is None:
				scheme = self.toolComposeScheme.getScheme(belongDBID, csdefine.COMPOSE_TOOL_GREEN_EQUIP)
		
		if not scheme is None:
			self.toolComposeScheme.removeScheme( scheme )
			self.pauseToolComposeScheme.addScheme( scheme )
			scheme.endTime -= int( time.time() )		# 将结束时间修改为 还需多少秒结束
		if isMinScheme:
			self._beginNewToolScheme()
		
	def _calculationRepairTime( self, minDfObj = None ):
		"""计算建筑修复"""
		if minDfObj:
			self.popTimer( self.repairTimer )
		else:
			minTime, minDfObj = self.occupiedFoundation.getMinRepairTimeDF()
		if minDfObj:
			buildType, minTime = minDfObj.getMinRepairData()
			if minTime <= time.time():
				self.onRepairDFBuildFinish( minDfObj.playerDBID, buildType )
				return
			self.repairTimer = self.addTimerCallBack(minTime - time.time(), "onRepairDFBuildFinish", ( minDfObj.playerDBID, buildType ))
		
	def beginRepairDFBuild( self, playerDBID, buildType, endTime ):
		"""
		define method
		开始修复建筑
		"""
		minTime, minDfObj = self.occupiedFoundation.getMinRepairTimeDF()
		dfObj = self.playerDBIDMapDongFu[playerDBID]
		dfObj.beginRepairBuild( buildType, endTime )
		if minDfObj:
			if endTime < minTime:
				self._calculationRepairTime( dfObj )
		else:
			self._calculationRepairTime( dfObj )
		
	def onRepairDFBuildFinish(self, belongDBID, buildType):
		"""
		洞府建筑 修复完成
		"""
		dfObj = self.playerDBIDMapDongFu[belongDBID]
		dfObj.onBuildRepair( buildType )
		
		scheme = None
		minScheme = self.toolComposeScheme.getMinTimeScheme()
		if buildType == csdefine.LHMJ_BUIILD_QIAN_KU_DING:
			scheme = self.pauseToolComposeScheme.getScheme(belongDBID, csdefine.COMPOSE_TOOL_TRIPOD)			# 建筑被打坏了，就不能打造了
		elif buildType == csdefine.LHMJ_BUIILD_GONG_FANG:
			scheme = self.pauseToolComposeScheme.getScheme(belongDBID, csdefine.COMPOSE_TOOL_NORMAL)
			if scheme is None:
				scheme = self.pauseToolComposeScheme.getScheme(belongDBID, csdefine.COMPOSE_TOOL_GREEN_EQUIP)
		elif buildType == csdefine.LHMJ_BUIILD_LING_QUAN:
			self._calculationReviveTime( dfObj )
			
		if not scheme is None:
			self.toolComposeScheme.addScheme( scheme )
			self.pauseToolComposeScheme.removeScheme( scheme )
			scheme.endTime += time.time()
			if minScheme is None:
				self._beginNewToolScheme(scheme)
			else:
				if minScheme.endTime < scheme.endTime:
					self._beginNewToolScheme( scheme )
			self.requestComposeData(scheme.playerMB, playerDBID, scheme.composeType)
		self._calculationRepairTime()
	
	def GM_setBuildRepairTime( self, playerDBID, buildType, endTime ):
		"""
		gm指令设置建筑修复时间
		"""
		minTime, minDfObj = self.occupiedFoundation.getMinRepairTimeDF()
		if not minDfObj:
			DEBUG_MSG("No building is repairing in mgr.")
			return
		
		dfObj = self.playerDBIDMapDongFu[playerDBID]
		dfObj.beginRepairBuild( buildType, endTime )
		
		if endTime < minTime:
			self._calculationRepairTime( dfObj )
	
	def addDFActiveStage( self, belongDBID ):
		"""
		define method
		增加洞府活动阶段
		"""
		if belongDBID in self.playerDBIDMapDongFu:
			self.playerDBIDMapDongFu[belongDBID].addDFActiveStage()
		
	def doActiveReward( self, belongDBID, belongSide, result, rewards, gifts, destroyBuids, startTime, activeTime, deadNum ):
		"""
		define method
		活动结算，攻守方 可能不在洞府
		"""
		dongFuObj = self.playerDBIDMapDongFu[belongDBID]
		playerDBID = dongFuObj.playerDBID
		if belongSide == csdefine.BELONG_SIDE_ATTACK:
			playerDBID = dongFuObj.challengePlayerDBID
		
		accountDBID, playerLevel = self.playerInfo.get(playerDBID, (0, 0))
			
		self.playerDBIDMapDongFu[belongDBID].doActiveReward( belongSide, result, rewards, gifts, destroyBuids, startTime, activeTime, deadNum, accountDBID, playerLevel )
		
	def onOccupyPlayerDF( self, baseMB, playerName, dstPlayerDBID, srcPlayerDBID ):
		"""
		define method
		占领其他玩家的洞府
		"""
		self.closeBattleFormations( srcPlayerDBID )
		self.closeBattleFormations( dstPlayerDBID )
		srcDF = self.playerDBIDMapDongFu.pop( srcPlayerDBID )
		oldName = srcDF.playerName
		self.lineNumberDict[srcDF.lineNumber].remove( srcPlayerDBID )
		if not dstPlayerDBID in self.lineNumberDict[srcDF.lineNumber]:
			self.lineNumberDict[srcDF.lineNumber].append( dstPlayerDBID )
			
		if dstPlayerDBID in self.playerDBIDMapDongFu:
			msgID = csstatus.DONG_FU_OCCUPY_BY_HASDF
			dstDF = self.playerDBIDMapDongFu.pop( dstPlayerDBID )
			self.lineNumberDict[dstDF.lineNumber].remove( dstPlayerDBID )
			self.lineNumberDict[dstDF.lineNumber].append( srcPlayerDBID )
			self.changeDongFuMaster(srcDF.playerMB, srcDF.playerName, srcPlayerDBID, dstDF )		# 对方有洞府，就交换洞府
		else:
			msgID = csstatus.DONG_FU_OCCUPY_BY_JADE
			if srcDF.playerMB:
				srcDF.playerMB.cell.onDFBeingOccupy( srcDF.getBuildLevel(csdefine.LHMJ_BUIILD_LING_QUAN) )
				srcDF.playerMB.client.statusMessage( csstatus.LHMJ_DF_BEING_OCCUPY, playerName )
			else:
				self.loseDFPlayer.addData( srcPlayerDBID, playerName, srcDF.getBuildLevel(csdefine.LHMJ_BUIILD_LING_QUAN) )
		self.changeDongFuMaster( baseMB, playerName, dstPlayerDBID , srcDF)
		baseMB.cell.onOccupyPlayerDFCallBack()
		baseMB.client.OnOccupyPlayerDFCB( msgID, oldName )
		
	def changeDongFuMaster( self, baseMB, playerName, playerDBID, dfObj ):
		"""洞府 易主"""
		dfObj.changeMaster( baseMB, playerName, playerDBID )
		self.playerDBIDMapDongFu[playerDBID] = dfObj 
		self.lineNumberDict[dfObj.lineNumber].append( playerDBID )
		dfObj.dongFuBase.updateDongFuState(dfObj.dongFuState, dfObj.getBuildLevel( csdefine.LHMJ_BUIILD_LING_QUAN), playerDBID, self.getLTShowDatasbyDF(playerDBID))
	
	def onFinishDFActive( self, playerDBID ):
		"""
		define method
		洞府活动已经完成
		"""
		if playerDBID in self.playerDBIDMapDongFu:
			dfObj = self.playerDBIDMapDongFu[playerDBID]
			dfObj.onFinishActive()
			self._calculationReviveTime( dfObj )
			
	def _calculationReviveTime( self, dfObj = None ):
		"""守卫复活时间"""
		if self.guardReviveTimer != -1:
			return
		if dfObj:
			if dfObj.canCalRevTime():
				remainTime = dfObj.guardReviveTime - time.time()
				if remainTime <= 0:
					dfObj.onGuardRevive()
					self._calculationReviveTime()
				else:
					self.guardReviveTimer = self.addTimerCallBack( remainTime, "doGuardReviveTime", (dfObj.playerDBID,) )
			return
		dfObj = self.occupiedFoundation.getMinGReviveTime()
		if dfObj and dfObj.canCalRevTime():
			self._calculationReviveTime( dfObj )
		
	def doGuardReviveTime( self, playerDBID ):
		""""""
		self.guardReviveTimer = -1
		if playerDBID in self.playerDBIDMapDongFu:
			self.playerDBIDMapDongFu[playerDBID].onGuardRevive()
		self._calculationReviveTime()
	
	def GM_doDefaultDFChallenge( self ):
		"""
		define method
		执行默认处理
		"""
		self.occupiedFoundation.doDefaultChallenge()
	
	def GM_clearDFData( self ):
		"""
		define method
		因为之前开发时候出的一些bug，
		所以，提gm指令清除一些数据
		"""
		if 0 in self.occupiedFoundation:
			self.occupiedFoundation.pop(0)
		if 0 in self.lineNumberDict:
			self.lineNumberDict.pop(0)
			
		for playerDBID in list(self.playerDBIDMapDongFu.keys()):
			dfObj = self.playerDBIDMapDongFu[playerDBID]
			if dfObj.playerName == "":
				dfObj.playerDBID = 0
				dfObj.buildLevels[csdefine.LHMJ_BUIILD_LING_QUAN] = 1
				dfObj.buildLevels[csdefine.LHMJ_BUIILD_GONG_FANG] = 1
				dfObj.buildLevels[csdefine.LHMJ_BUIILD_QIAN_KU_DING] = 1
				dfObj.buildLevels[csdefine.LHMJ_BUIILD_SHOU_LAN] = 1
				dfObj.buildLevels[csdefine.LHMJ_BUIILD_LING_TIAN] = 1
				dfObj.dongFuState = csdefine.LHMJ_BUILD_STATE_NONE
				if dfObj.dongFuBase:
					dfObj.dongFuBase.onProtectTimeOut()
				self.playerDBIDMapDongFu.pop( playerDBID )
		# 清除重复占领洞府的数据
		for lineNumber, dongFuGroups in self.occupiedFoundation.items():
			for group, dfObj in dongFuGroups.items():
				if dfObj.playerDBID in self.playerDBIDMapDongFu:
					if dfObj != self.playerDBIDMapDongFu[dfObj.playerDBID]:
						dfObj.playerName = ""
						dfObj.playerDBID = 0
						dfObj.buildLevels[csdefine.LHMJ_BUIILD_LING_QUAN] = 1
						dfObj.buildLevels[csdefine.LHMJ_BUIILD_GONG_FANG] = 1
						dfObj.buildLevels[csdefine.LHMJ_BUIILD_QIAN_KU_DING] = 1
						dfObj.buildLevels[csdefine.LHMJ_BUIILD_SHOU_LAN] = 1
						dfObj.buildLevels[csdefine.LHMJ_BUIILD_LING_TIAN] = 1
						dfObj.dongFuState = csdefine.LHMJ_BUILD_STATE_NONE
						if dfObj.dongFuBase:
							dfObj.dongFuBase.onProtectTimeOut()