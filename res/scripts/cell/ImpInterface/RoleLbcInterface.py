#-*- coding: utf-8 -*-


import time
import datetime

import KBEngine
import KBEDebug
import KST
import csconst
import csstatus
import csdefine
import Functions

import LbcData


class RoleLbcInterface:
	"""
	玩家练兵场接口类
	"""
	def __init__(self):
		self.occupyTempData = {} #玩家占领需要临时保存的数据

	def roleLbcLogin(self):
		"""
		"""
		KBEngine.globalData['LbcMgr'].roleLbcLogin(self, self.playerDBID)
	
	def roleLbcLoginCB(self, occupyLbcItem, declareLbcItem):
		"""
		occupyLbcItem:玩家占领的练兵场
		declareLbcItem：玩家宣战的练兵场
		"""
		#如果作为防守方在练兵场争夺时间内上线 需要通知玩家一些信息 
		#如果玩家下线前有占领的练兵场
		if self.occupyInfo.index>0:
			#被人抢夺了
			if self.occupyInfo.index!=occupyLbcItem.index:
				self.statusMessage(csstatus.LBC_LOST_ON_LOGOFF)
			#自己仍然占领
			else:
				#争夺中 这里应该只是弹出一个提示并不做传送处理 玩家自行前往练兵场 因为可能需要先去组队
				if occupyLbcItem.status == csconst.LBC_STATUS_FIGHT:
					self.statusMessage(csstatus.LBC_ENTER_FIGHT)
				#防守成功
				elif occupyLbcItem.status == csconst.LBC_STATUS_OCCUPIED:
					if not self.occupyInfo.isNotified:
						self.statusMessage(csstatus.LBC_DEFENCE_SUCCEED)
						self.occupyInfo.isNotified = 1

		#同步管理器的数据
		self.updateOccupyInfo(occupyLbcItem.line, occupyLbcItem.index, occupyLbcItem.level, occupyLbcItem.lbcName)
		self.updateDeclareInfo(declareLbcItem.line, declareLbcItem.index, declareLbcItem.getClientDeclareInfo())
		self.updateBeDeclaredInfo(occupyLbcItem.getClientDeclareInfo())
		

	def reqOpenLbcMapUI(self, exposed):
		"""
		exposed method
		打开练兵场地图界面
		"""
		self.openLbcMapUI()

	def openLbcMapUI(self):
		"""
		"""
		KBEngine.globalData['LbcMgr'].openLbcMapUI(self, self.occupyInfo.line, self.occupyInfo.index, self.declareInfo.line, self.declareInfo.index)

	def openLbcMapUICB(self, occupyInfo, declareInfo, statusList):
		"""
		"""
		#将我占有的练兵场信息，我宣战的练兵场信息,所有练兵场状态发到客户端
		if self.getClient():
			self.client.OpenLbcMapUI(occupyInfo, declareInfo, statusList)

	def checkGotoLbc(self, line, index):
		"""
		检测能否前往练兵场
		"""
		#不能前往自己的练兵场
		if self.occupyInfo.line==line and self.occupyInfo.index==index:
			KBEDebug.ERROR_MSG("can't occupy self lbc!")
			return False
		# #被宣战 暂时不做 给玩家加个是否被宣战的属性
		# if self.occupyInfo.declarerDBID>0:
		# 	KBEDebug.ERROR_MSG("can't occupy cause your lbc was declared!")
		# 	return False
		#已宣战别人
		if self.declareInfo.index>0:
			KBEDebug.ERROR_MSG("can't occupy cause you have declared other lbc")
			return False
		return True


	def isDeclareTime(self):
		"""
		是否是宣战时间
		"""
		if int(time.strftime('%w')) in csconst.LBC_DECLARE_TIME_WEEK and int(time.strftime('%H')) in csconst.LBC_DECLARE_TIME_HOUR:
			return True
		return False

	def reqGotoLbc(self, exposed, line, index):
		"""
		exposed method
		前往练兵场
		"""
		if not self.checkGotoLbc(line, index):
			return
		KBEngine.globalData['LbcMgr'].gotoLbc(self, line, index)


	def gotoLbc(self, lbcItem):
		"""
		前往练兵场
		"""
		#未占领 
		if lbcItem.status == csconst.LBC_STATUS_NORMAL:
			#低级练兵场无需消耗资源,通过打pve占领
			if lbcItem.level == csdefine.NPCTRAINSOLDIERGROUND_TYPE_LOW_LEVEL:
				#弹出提示 是否前往争夺
				self.inquireMessage(csstatus.LBC_GOTO_LBC_LOW, [], 'replyIsAttackLbcLow', lbcItem)
				return
			#中高级消耗资源可以直接占领练兵场
			elif lbcItem.level == csdefine.NPCTRAINSOLDIERGROUND_TYPE_MIDDLE_LEVEL:
				moneyCost = csconst.LBC_MID_COST_MONEY
				soldierLevel, soldierNum = csconst.LBC_MID_COST_SOLDIER
			elif lbcItem.level == csdefine.NPCTRAINSOLDIERGROUND_TYPE_HIGH_LEVEL:
				moneyCost = csconst.LBC_HIGH_COST_MONEY
				soldierLevel, soldierNum = csconst.LBC_HIGH_COST_SOLDIER
			#条件不满足时，弹出不满足的条件提醒
			#1.你未占领初级练兵场
			if self.occupyInfo.index==0 or self.occupyInfo.level<lbcItem.level-1:
				self.statusMessage(csstatus.LBC_CONDITION_NO_LBC, lbcItem.level-1)
				return
			#2.你4级以上的士兵不足x个
			scriptIDList = self.getOccupySoldierScriptID(soldierLevel, soldierNum)
			if not scriptIDList:
				self.statusMessage(csstatus.LBC_CONDITION_NO_SOLDIER, soldierLevel, soldierNum)
				return
			#3.你的金钱不足xxxx
			if self.getBindMoney()<moneyCost:
				replaceMoney = moneyCost - self.getBindMoney()
				self.inquireMessage(csstatus.NPCSHOP_COST_MONEY_REPLACE_BIND_MONEY, [Functions.moneyToStr(replaceMoney)], "replyIsOccupyLbcMiddleOrHigh", moneyCost, lbcItem, soldierLevel, soldierNum, scriptIDList)
				return
			#满足条件弹出确认交付的提示 这里应该先把以上需要消耗的资源加锁冻结住！暂时不处理
			if self.getClient():
				self.occupyTempData['line'] = lbcItem.line
				self.occupyTempData['index'] = lbcItem.index
				self.occupyTempData['moneyCost'] = moneyCost
				self.occupyTempData['soldierCost'] = (soldierLevel, soldierNum)
				self.client.LbcOccupyCost(soldierLevel, soldierNum, moneyCost, scriptIDList)

		#已占领 
		elif lbcItem.status == csconst.LBC_STATUS_OCCUPIED:
			#周二/周五20:00-21:00宣战， 周三/周六20:00正式争夺
			#在宣战时间内
			if self.isDeclareTime():
				today = datetime.datetime.today()
				nextday = today+datetime.timedelta(days = 1)
				month = nextday.month
				day = nextday.day
				#是否对当前练兵场发起宣战？宣战后XX月XX日20:00正式开启争夺！
				self.inquireMessage(csstatus.LBC_IS_DECLARE, [month,day], 'replyIsDeclare', lbcItem)
			else:
				#已被占领的练兵场需要在周二或者周五20:00-21:00时间段内发起宣战。目前不在时间段内，不可宣战！
				self.statusMessage(csstatus.LBC_NOT_DECLARE_TIME)


	def replyIsAttackLbcLow(self, reply, lbcItem):
		"""
		是否前往低级练兵场争夺
		"""
		if reply:
			#先放弃自己的练兵场
			self.abandonLbc()
			self.enterLbcSpace(lbcItem)

	def replyIsOccupyLbcMiddleOrHigh(self, reply, moneyCost, lbcItem, soldierLevel, soldierNum, scriptIDList):
		"""
		是否使用金币代替绑金消耗资源直接占领中高级练兵场
		"""
		if reply:
			if self.getClient():
				self.occupyTempData['line'] = lbcItem.line
				self.occupyTempData['index'] = lbcItem.index
				self.occupyTempData['moneyCost'] = moneyCost
				self.occupyTempData['soldierCost'] = (soldierLevel, soldierNum)
				self.client.LbcOccupyCost(soldierLevel, soldierNum, moneyCost, scriptIDList)

	def replyIsDeclare(self, reply, lbcItem):
		"""
		是否发起宣战
		"""
		if reply:
			self.declareLbc(self, lbcItem.line, lbcItem.index, self.playerDBID, self.getName(), self.getProfession())


	def declareLbc(self, line, index, occupierDBID, occupierName, occupierProfession):
		"""
		"""
		KBEngine.globalData['LbcMgr'].declare(self, line, index, occupierDBID, occupierName, occupierProfession)


	def declareLbcCB(self, result, line, index, clientDeclareInfo, lbcName, month, day):
		"""
		宣战练兵场的回调
		result 宣战结果
		"""
		#宣战成功
		if result:
			#放弃原先的练兵场
			self.abandonLbc()
			#宣战成功提示
			self.statusMessage(csstatus.LBC_DECLARE_SUCCEED, lbcName, month, day)
			#更新宣战信息
			self.updateDeclareInfo(line, index, clientDeclareInfo)


	def abandonLbc(self):
		"""
		放弃练兵场
		"""
		KBEngine.globalData['LbcMgr'].abandon(self, self.occupyInfo.line, self.occupyInfo.index)

	def abandonLbcCB(self):
		"""
		"""
		self.updateOccupyInfo(0, 0, 0, '')


	def reqSubmitOccupyCost(self, exposed, soldierScriptID):
		"""
		客户端确认提交士兵 如果玩家选择不提交 soldierScriptID传个空字符串
		soldierIDList 天兵营数据 士兵id列表
		"""
		if not soldierScriptID:
			#如果前面加锁了 这里需要解锁
			return
		line = self.occupyTempData['line']
		index = self.occupyTempData['index']
		self.occupyTempData['soldierScriptID'] = soldierScriptID

		self.occupyLbc(line, index)

	def occupyLbc(self, line, index):
		"""
		占领练兵场
		"""
		KBEngine.globalData['LbcMgr'].occupy(self, line, index)


	def occupyLbcCB(self, result, line, index):
		"""
		占领中高级练兵场的回调
		result 占领结果
		"""
		#占领成功
		if result:
			##扣除资源
			moneyCost = self.occupyTempData['moneyCost']
			soldierLevel, soldierNum = self.occupyTempData['soldierCost']
			soldierScriptID = self.occupyTempData['soldierScriptID']
			#扣钱
			self.subBindMoneyAndMoney( moneyCost, csdefine.MONEY_SUN_REASON_OCCUPY_TRAIN_GROUND )
			#扣兵
			self.occupyLbcCostSoldier(soldierScriptID, soldierLevel, soldierNum)
			#占领成功
			self.occupyLbcSucceed(line, index)
		#占领失败
		else:
			#提示占领失败
			self.statusMessage(csstatus.LBC_OCCUPIED_BY_OTHERS)
		#解锁资源冻结
		#更新上线提示状态
		self.occupyInfo.isNotified = 0
		

	def occupyLbcSucceed(self, line, index):
		KBEngine.globalData['LbcMgr'].occupyLbcSucceed(self, self.occupyInfo.line, self.occupyInfo.index, line, index, self.playerDBID, self.playerName, self.profession)


	def occupyLbcSucceedCB(self, line, index, level, lbcName):
		self.statusMessage(csstatus.LBC_OCCUPY_SUCCEED, lbcName)
		self.updateOccupyInfo(line, index, level, lbcName)


	def reqCancelDeclare(self, exposed):
		"""
		exposed method
		撤销宣战
		"""
		self.cancelDeclare()

	def cancelDeclare(self):
		"""
		撤销宣战
		"""
		KBEngine.globalData['LbcMgr'].cancelDeclare(self, self.declareInfo.line, self.declareInfo.index)

	def cancelDeclareCB(self, clientDeclareInfo):
		"""
		"""
		self.updateDeclareInfo(0, 0, clientDeclareInfo)

	def beDeclared(self, month, day, clientDeclareInfo):
		"""
		玩家被宣战
		"""
		#你的练兵场已被他人宣战 XX月XX日20:00正式开启争夺！	
		self.statusMessage( csstatus.LBC_BE_DECLARED, month, day)
		#self.isBeDeclared = True
		self.updateBeDeclaredInfo(clientDeclareInfo)

	def beDeclaredCancel(self, clientDeclareInfo):
		"""
		通知玩家被取消宣战了
		"""
		self.updateBeDeclaredInfo(clientDeclareInfo)


	def notifyDeclarerFight(self, line, index, clientDeclareInfo):
		"""
		通知宣战者进战场
		"""
		if self.getClient():
			self.client.NotifyDeclarerFight(csconst.LBC_FIGHT_COUNT_DOWN, line, index, clientDeclareInfo)


	def notifyOccupierFight(self, line, index, clientDeclareInfo):
		"""
		通知防守者进战场
		"""
		if self.getClient():
			self.client.NotifyOccupierFight(csconst.LBC_FIGHT_COUNT_DOWN, line, index, clientDeclareInfo)


	def occupierGiveUpFight(self, exposed, line, index):
		"""
		exposed method
		占领者放弃争夺
		"""
		pass


	def declarerGiveUpFight(self, exposed, line, index):
		"""
		宣战者放弃争夺
		"""
		self.giveUpAttack(line, index)


	def replyIsProtectLbc(self, reply):
		"""
		是否防守练兵场
		"""
		pass

	def giveUpAttack(self, line, index):
		"""
		放弃进攻
		"""
		KBEngine.globalData['LbcMgr'].giveUpAttack(self, line, index)

	def giveUpAttackCB(self, clientDeclareInfo):
		"""
		"""
		self.updateDeclareInfo(0, 0, clientDeclareInfo)

	def recvLbcFightResult(self, result, reason, lbcItem):
		"""
		收到练兵场争夺战结果
		result :bool 胜/负
		reason :uint8 原因（进攻/防守）
		lbcItem : 战斗结束更新后的练兵场数据
		"""
		#胜利
		if result:
			#更新玩家占领的练兵场信息
			self.updateOccupyInfo(lbcItem.line, lbcItem.index, lbcItem.level, lbcItem.lbcName)
		else:
			#如果是防守方失败 清空玩家占领的练兵场信息
			if reason == csconst.LBC_FIGHT_REASON_DEFENCE:
				self.updateOccupyInfo(0, 0, 0, '')
		#更新上线提示状态
		self.occupyInfo.isNotified = 0


	def updateLbcStatus(self, line, index, status):
		"""
		更新一条练兵场信息
		"""
		statusInfo = {}
		statusInfo['line'] = line
		statusInfo['index'] = index
		statusInfo['status'] = status
		self.client.UpdateLbcStatusInfo(statusInfo)


	def updateOccupyInfo(self, line, index, level, lbcName):
		"""
		更新练兵场占领数据
		"""
		self.occupyInfo.line = line
		self.occupyInfo.index = index
		self.occupyInfo.level = level

		if self.getClient():
			self.client.UpdateOccupyInfo({'level':level, 'lbcName':lbcName})


	def updateDeclareInfo(self, line, index, clientDeclareInfo):
		"""
		更新练兵场宣战数据
		"""
		self.declareInfo.line = line
		self.declareInfo.index = index

		if self.getClient():
			self.client.UpdateDeclareInfo(clientDeclareInfo)

	def updateBeDeclaredInfo(self, clientDeclareInfo):
		"""
		更新被宣战的练兵场数据
		"""
		if self.getClient():
			self.client.UpdateBeDeclaredInfo(clientDeclareInfo)

	def gotoLbcSpaceSingle(self, spaceObj, packArgs, lbcItem):
		"""
		单人进入
		"""
		if self.playerDBID == lbcItem.occupierDBID:	
			enterInfo = spaceObj.getProtectEnterInfo()
		else:
			enterInfo = spaceObj.getAttackEnterInfo()
		#packArgs 数据一改， 牵扯到此数据的所有地方都得修改
		packArgs["belongDBID"] = lbcItem.occupierDBID
		packArgs["lbcItem"] = lbcItem
		self.gotoSpaceUseArg( spaceObj.scriptID, enterInfo[0], enterInfo[1], packArgs )


	def gotoLbcSpaceTeam(self, spaceObj, packArgs, lbcItem):
		"""
		组队进入
		"""
		num = spaceObj.getAllowTeamNumber()
		if len(self.getAllTeamMemberMB()) != num:
			self.statusMessage(csstatus.LBC_CONDITION_MEMBER_AMOUNT)
			return
		for entityMB in self.getAllTeamMemberMB():
			packArgs["lbcItem"] = lbcItem
			packArgs["belongDBID"] = lbcItem.occupierDBID
			packArgs["enterDBIDs"] = self.getAllTeamMemberDBIDs()
			if self.playerDBID == lbcItem.occupierDBID:	
				enterInfo = spaceObj.getProtectEnterInfo()
				packArgs["belongSide"] = csdefine.BELONG_SIDE_PROTECT
			else:
				enterInfo = spaceObj.getAttackEnterInfo()
				packArgs["belongSide"] = csdefine.BELONG_SIDE_ATTACK

			entityMB.cell.gotoSpaceUseArg( spaceObj.scriptID, enterInfo[0], enterInfo[1], packArgs )


	def enterLbcSpace(self, lbcItem):
		"""
		进入练兵场地图
		"""
		if lbcItem.level == csdefine.NPCTRAINSOLDIERGROUND_TYPE_LOW_LEVEL:
			if lbcItem.status == csconst.LBC_STATUS_NORMAL:
				#pve
				spaceScriptID = csconst.LBC_SPACE[lbcItem.level][1]
			else:
				#pvp
				spaceScriptID = csconst.LBC_SPACE[lbcItem.level][0]
		else:
			#中高级只有pvp
			spaceScriptID = csconst.LBC_SPACE[lbcItem.level]

		spaceObj = KST.g_objFactory.getSpaceObject(spaceScriptID)
		if spaceObj is None:
			KBEDebug.ERROR_MSG("not found space[%s] object" %(spaceScriptID))
			return
		#记录进入之前的位置 
		packArgs={
			"lastPos": self.position,
			"lastDir":self.direction,
			"lastSpaceScriptID":self.getCurrentSpace().scriptID
		}
		
		if lbcItem.level == csdefine.NPCTRAINSOLDIERGROUND_TYPE_LOW_LEVEL:
			self.gotoLbcSpaceSingle(spaceObj, packArgs, lbcItem)
		else:
			self.gotoLbcSpaceTeam(spaceObj, packArgs, lbcItem)
		

	def leaveLbcSpace(self, spaceEntity):
		"""
		离开任务地图
		"""
		#返回进图之前的位置
		lastPos = spaceEntity.createArgs.get("lastPos")
		lastDir = spaceEntity.createArgs.get("lastDir")
		lastSpaceScriptID = spaceEntity.createArgs.get("lastSpaceScriptID")
		self.gotoSpace(lastSpaceScriptID, lastPos, lastDir)