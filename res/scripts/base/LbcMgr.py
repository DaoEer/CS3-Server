#-*- coding: utf-8 -*-

#练兵场管理器


import datetime
import KBEngine
import csconst
import csdefine
import csstatus
import Functions
from CoreObject import MgrPersistentObject
from ConfigObject.LbcConfigLoader import g_lbcConfigData
from LbcData import g_lbcData, g_lbcItem
import KST

from ConfigObject.Crond.CrondDatas import CrondDatas
g_CrondDatas = CrondDatas.instance()


class LbcMgr(MgrPersistentObject.MgrPersistentObject):
	"""
	"""
	def __init__(self):
		"""
		"""
		MgrPersistentObject.MgrPersistentObject.__init__(self)
		self.onCompleteInit()
		self.initLbcDatas()


	def initLbcDatas(self):
		"""
		通过配置初始化练兵场信息
		"""
		configData = g_lbcConfigData.lbcConfig
		self.lbcData.init(configData)


	def registerCrond( self ):
		"""
		将活动key 注册到Crond中
		"""
		taskEvents = {
			"LbcMgr_StartFight": "startFight",
		}
		for taskName, callbackName in taskEvents.items():
			for scriptID, cmd in g_CrondDatas.getCrondTaskCmds(taskName):
				KBEngine.globalData["CrondManager"].addScheme( scriptID, cmd, self, callbackName, -1, (scriptID,) )


	def getAttackTime(self):
		"""
		获取进攻时间 进攻时间是第二天的20:00
		"""
		today = datetime.datetime.today()
		nextday = today+datetime.timedelta(days = 1)
		attackTime = datetime.datetime(nextday.year, nextday.month, nextday.day, 20, 0)
		return int(datetime.datetime.timestamp(attackTime))

	def abandon(self, playerCell, line, index):
		"""
		放弃练兵场
		"""
		lbcItem = self.lbcData.getItem(line, index)
		if not lbcItem:
			return
		lbcItem.abandon()
		playerCell.abandonLbcCB()


	def declare(self, playerCell, line, index, declarerDBID, declarerName, declarerProfession):
		"""
		宣战
		@line: 分线
		@lbcLevel: 练兵场等级
		@index: 练兵场序号
		@declareDBID: 宣战者DBID
		"""
		#判断能否宣战
		lbcItem = self.lbcData.getItem(line, index)
		if not lbcItem or not lbcItem.status == csconst.LBC_STATUS_OCCUPIED:
			return
	
		attackTime = self.getAttackTime()
		lbcItem.declare(declarerDBID, declarerName, declarerProfession, attackTime)

		today = datetime.datetime.today()
		nextday = today+datetime.timedelta(days = 1)
		month = nextday.month
		day = nextday.day
		clientDeclareInfo = lbcItem.getClientDeclareInfo()
		playerCell.declareLbcCB(True, line, index, clientDeclareInfo, lbcItem.lbcName, month, day)
		#通知被宣战的玩家 
		KBEngine.lookUpEntityByDBID( "Role", lbcItem.occupierDBID, Functions.Functor(self.notifyPlayerBeDeclared, month, day, clientDeclareInfo))
		


	def cancelDeclare(self, playerCell, line, index):
		"""
		撤销宣战
		"""
		lbcItem = self.lbcData.getItem(line, index)
		if not lbcItem:
			return
		lbcItem.cancelDeclare()
		clientDeclareInfo = lbcItem.getClientDeclareInfo()
		playerCell.cancelDeclareCB(clientDeclareInfo)
		#通知被宣战的玩家 
		KBEngine.lookUpEntityByDBID( "Role", lbcItem.occupierDBID, Functions.Functor(self.notifyPlayerBeDeclaredCancel, clientDeclareInfo))


	def notifyPlayerBeDeclared(self, month, day, clientDeclareInfo, target):
		"""
		通知玩家被取消宣战了
		"""
		if target is False:
			return
		if target is True:
			return
		target.cell.beDeclared(month, day, clientDeclareInfo)

	def notifyPlayerBeDeclaredCancel(self, clientDeclareInfo, target):
		"""
		通知玩家被取消宣战了
		"""
		if target is False:
			return
		if target is True:
			return
		target.cell.beDeclaredCancel(clientDeclareInfo)


	def occupy(self, playerCell, line, index):
		"""
		占领
		@line: 分线
		@index: 练兵场序号
		"""
		lbcItem = self.lbcData.getItem(line, index)
		if not lbcItem or lbcItem.status!=csconst.LBC_STATUS_NORMAL:
			playerCell.occupyLbcCB(False, line, index)	
			return
		playerCell.occupyLbcCB(True,line, index)


	def occupyLbcSucceed(self, playerCell, abandonLine, abandonIndex, occupyLine, occupyIndex, occupierDBID, occupierName, occupierProfession):
		"""
		成功占领练兵场
		"""
		abandonLbcItem = self.lbcData.getItem(abandonLine, abandonIndex)
		abandonLbcItem.abandon()
		occupyLbcItem = self.lbcData.getItem(occupyLine, occupyIndex)
		occupyLbcItem.occupy(occupierDBID, occupierName, occupierProfession)
		playerCell.occupyLbcSucceedCB(occupyLbcItem.line, occupyLbcItem.index, occupyLbcItem.level, occupyLbcItem.lbcName)


		
	def openLbcMapUI(self, playerCell, occupyLine, occupyIndex, declareLine, declareIndex):
		"""
		玩家打开练兵场界面
		"""
		#获取所有练兵场的状态信息
		statusList = self.lbcData.getStatusList()
		occupyLbcItem = self.lbcData.getItem(occupyLine, occupyIndex)
		if not occupyLbcItem:
			occupyInfo = {'level':0, 'lbcName':''}
		else:
			occupyInfo = {'level':occupyLbcItem.level, 'lbcName':occupyLbcItem.lbcName}

		declareLbcItem = self.lbcData.getItem(declareLine, declareIndex)
		if not declareLbcItem:
			clientDeclareInfo = {}
			clientDeclareInfo['level'] = 0
			clientDeclareInfo['line'] = 0
			clientDeclareInfo['lbcName'] = ''
			clientDeclareInfo['status'] = csconst.LBC_STATUS_NORMAL
			clientDeclareInfo['occupierName'] = ''
			clientDeclareInfo['occupierProfession'] = csdefine.CLASS_UNKNOWN
			clientDeclareInfo['declarerName'] = ''
			clientDeclareInfo['declarerProfession'] = csdefine.CLASS_UNKNOWN
			clientDeclareInfo['attackTime'] = 0
		else:
			clientDeclareInfo = declareLbcItem.getClientDeclareInfo()
			

		playerCell.openLbcMapUICB(occupyInfo, clientDeclareInfo, statusList)


	def gotoLbc(self, playerCell, line, index):
		"""
		前往练兵场
		"""
		lbcItem = self.lbcData.getItem(line, index)
		if not lbcItem:
			return

		playerCell.gotoLbc(lbcItem)
		

	def startFight(self):
		"""
		开始练兵场争夺
		"""
		#通知所有需要参与争夺战的玩家
		for line in self.lbcData:
			for lbcItem in self.lbcData[line].values():
				#被占领且被宣战
				if lbcItem.occupierDBID>0 and lbcItem.declarerDBID>0:
					clientDeclareInfo = lbcItem.getClientDeclareInfo()
					KBEngine.lookUpEntityByDBID( "Role",lbcItem.occupierDBID,Functions.Functor( self.notifyOccupierStartFight, lbcItem.line, lbcItem.index, clientDeclareInfo) )
					KBEngine.lookUpEntityByDBID( "Role",lbcItem.declarerDBID,Functions.Functor( self.notifyDeclareStartFight, lbcItem.line, lbcItem.index, clientDeclareInfo) )
		#半分钟之后进图
		self.addTimerCallBack(30, "enterSpace", ())


	def notifyOccupierStartFight( self, line, index, clientDeclareInfo, target):
		"""
		通知玩家争夺战开始
		"""
		if target is False:
			return
		if target is True:
			return
		#练兵场争夺战正式开启 勇士是否前往争夺练兵场！
		target.cell.notifyOccupierFight(line, index, clientDeclareInfo)


	def notifyDeclareStartFight( self, line, index, clientDeclareInfo, target):
		"""
		通知进攻方玩家争夺战开始
		"""
		if target is False or target is True:
			#宣战者不在线 直接视为放弃
			lbcItem.giveUpAttack()
			return

		#练兵场争夺战正式开启 勇士是否前往争夺练兵场！
		target.cell.notifyDeclarerFight(line, index, clientDeclareInfo)
		

	def giveUpAttack(self, playerCell, line, index):
		"""
		玩家放弃争夺
		"""
		lbcItem = self.lbcData.getItem(line, index)
		if not lbcItem:
			return

		lbcItem.giveUpAttack()
		clientDeclareInfo = lbcItem.getClientDeclareInfo()
		playerCell.giveUpAttackCB(clientDeclareInfo)
		

	def enterSpace(self):
		"""
		"""
		#进图
		for line in self.lbcData:
			for lbcItem in self.lbcData[line].values():
				if 	lbcItem.status == csconst.LBC_STATUS_DELCARED:
					KBEngine.lookUpEntityByDBID( "Role",lbcItem.occupierDBID,Functions.Functor( self.notifyOccupierEnterSpace, lbcItem) )
					KBEngine.lookUpEntityByDBID( "Role",lbcItem.declarerDBID,Functions.Functor( self.notifyDeclarerEnterSpace, lbcItem) )
					lbcItem.updateStatus(csconst.LBC_STATUS_FIGHT)
					


	def notifyDeclarerEnterSpace(self, lbcItem, target):
		"""
		通知玩家争夺战结果
		"""
		if target is False:
			return
		if target is True:
			return
		target.cell.enterLbcSpace(lbcItem)

	def notifyOccupierEnterSpace(self, lbcItem, target):
		"""
		通知玩家争夺战结果
		"""
		if target is False:
			return
		if target is True:
			return
		target.cell.enterLbcSpace(lbcItem)


	def notifyPlayerFightResult(self, result, reason, lbcItem, target):
		"""
		通知玩家争夺战结果
		"""
		if target is False:
			return
		if target is True:
			return
		target.cell.recvLbcFightResult(result, reason, lbcItem)


	def attackerWin(self, line, index, playerCell, playerDBID, playerName, playerProfesion):
		"""
		进攻方争夺成功
		"""
		lbcItem = self.lbcData.getItem(line, index)
		if not lbcItem:
			return
		oldOccupierDBID = lbcItem.occupierDBID
		#更新练兵场信息
		lbcItem.attackerWin(playerDBID, playerName, playerProfesion, 0, '', csdefine.CLASS_UNKNOWN, csconst.LBC_STATUS_OCCUPIED, 0)
		if oldOccupierDBID>0:
			KBEngine.lookUpEntityByDBID( "Role",oldOccupierDBID,Functions.Functor( self.notifyPlayerFightResult, False, csconst.LBC_FIGHT_REASON_DEFENCE, lbcItem) )
		playerCell.recvLbcFightResult(True, csconst.LBC_FIGHT_REASON_OFFENCE, lbcItem)

			
	def attackerLose(self, line, index, playerCell):
		"""
		进攻方争夺失败
		"""
		lbcItem = self.lbcData.getItem(line, index)
		if not lbcItem:
			return
		oldOccupierDBID = lbcItem.occupierDBID
		#更新练兵场信息
		lbcItem.attackerLose()
		if oldOccupierDBID:
			KBEngine.lookUpEntityByDBID( "Role",oldOccupierDBID,Functions.Functor( self.notifyPlayerFightResult, True, csconst.LBC_FIGHT_REASON_DEFENCE, lbcItem) )
		playerCell.recvLbcFightResult(False, csconst.LBC_FIGHT_REASON_OFFENCE, lbcItem)


	def roleLbcLogin(self, playerCell, playerDBID):
		"""
		玩家上线
		"""
		occupyLbcItem = self.lbcData.getItemByOccupierDBID(playerDBID)
		declareLbcItem = self.lbcData.getItemByDeclarerDBID(playerDBID)
		playerCell.roleLbcLoginCB(occupyLbcItem, declareLbcItem)


	def saveSpaceNPCInfo( self, guardData ):
		"""
		<define method>
		保存练兵场布防数据
		"""
		for npcInfo in self.spaceNPCInfos:
			if npcInfo["belongDBID"] == guardData["belongDBID"] and npcInfo["spaceScriptID"] == guardData["spaceScriptID"]:
				self.spaceNPCInfos.remove( npcInfo )
				break
		self.spaceNPCInfos.append( guardData )
		

	def requestSpaceNPCInfo( self, spaceCell, DBID, spaceScriptID ):
		"""
		<define method>
		请求练兵场布防数据
		"""
		for npcInfo in self.spaceNPCInfos:
			if npcInfo["belongDBID"] == DBID and npcInfo["spaceScriptID"] == spaceScriptID:
				spaceCell.onRequestSpaceNPCInfo( npcInfo["spaceDatas"] )
				return
		spaceCell.onRequestSpaceNPCInfo( [] )
