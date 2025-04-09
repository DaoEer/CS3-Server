
# -*- coding: utf-8 -*-
import KBEngine
import KBEDebug
import csdefine
from ConfigObject.Barracks.BarracksMgr import g_barracksMgr
import copy
import Const
import KST
import csstatus
import random
import Functions

class RoleBarracksInterface:
	"""
	玩家兵营接口
	"""
	def __init__( self ):
		"""
		初始化
		"""
		self.isRequest = False
		self.checkBarracksSoldiersUnLock()

	def checkBarracksSoldiersUnLock( self ):
		"""
		检查兵营中兵是否解锁
		"""
		items = []
		barracksSoldierScriptIDs = g_barracksMgr.getBarracksItemsBySoldierType( csdefine.BARRACKS_SOLDIER_COMMON_TYPE )
		for barracksSoldierScriptID in barracksSoldierScriptIDs:
			items.append( g_barracksMgr.getBarracksItemByScriptID(csdefine.BARRACKS_SOLDIER_COMMON_TYPE,barracksSoldierScriptID) )
		soldierScriptIDs = ( g_barracksMgr.getBarracksItemsBySoldierType( csdefine.BARRACKS_SOLDIER_GUARD_TYPE ) )
		for soldierScriptID in soldierScriptIDs:
			items.append( g_barracksMgr.getBarracksItemByScriptID(csdefine.BARRACKS_SOLDIER_GUARD_TYPE,soldierScriptID) )
		for item in items:
			if item and item.checkBarracksItemIsUnLock( self ):
				self.addUnLockSoldiers( item.scriptID )

	def addUnLockSoldiers( self, scriptID ):
		"""
		增加解锁的兵种
		"""
		if scriptID not in self.unLockSoldiers:
			self.unLockSoldiers.append( scriptID )
	
	def requestOpenBarracks( self, srcEntityID ):
		"""
		exposed method
		请求打开兵营
		"""
		if self.isRequest:
			return
		self.isRequest = True
		if not self.validateClientCall( srcEntityID ):
			return
		if not self.isCanOpenBarracks:
			return
		if self.getClient():
			self.client.InitRoleBarracksUnLockSoldiers( self.unLockSoldiers )
			self.client.InitRoleArmyDatas( list( self.roleArmyDatas.values() ) )

		if self.roleBarracksMgr.initRoleBarracksDataToClient( csdefine.BARRACKS_SOLDIER_COMMON_TYPE, self ):
			if self.roleBarracksMgr.initRoleBarracksDataToClient( csdefine.BARRACKS_SOLDIER_GUARD_TYPE, self ):
				if self.getClient():
					self.client.InitRoleBarracksDataOver( csdefine.BARRACKS_SOLDIER_GUARD_TYPE )
					self.isRequest = False

	def requestBuyBarracksSoldier( self, srcEntityID, soldierType, scriptID, count ):
		"""
		exposed method
		请求招募某个兵
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		barracksItem = g_barracksMgr.getBarracksItemByScriptID( soldierType, scriptID )
		if not barracksItem:
			return

		soldiers = self.roleBarracksMgr.getBarracksSoldiersByScriptID( soldierType, scriptID )
		if len( soldiers ) + count > barracksItem.getMaxHaveAmount():
			return

		if not barracksItem.checkBarracksItemIsUnLock(self):
			return

		payItems ={}
		payItems[ csdefine.TRADE_PAY_ITEM_MONEY ] = barracksItem.getCostMoney() * count

		self.requestPay( csdefine.TRADE_TYPE_ROLE_RARRACKS, self.id, payItems, soldierType, scriptID,count )

	def onSuccessPayBarracksItem( self, soldierType, scriptID, count ):
		"""
		招募成功
		"""
		maxExp = g_barracksMgr.getSoldierMaxExpByLevel( scriptID, 1 )
		skillIDDatas = g_barracksMgr.getSoldierSkillIDsByScriptID(scriptID)
		barracksItem = g_barracksMgr.getBarracksItemByScriptID( soldierType, scriptID )
		while count > 0:
			self.roleBarracksMgr.addBarracksSoldier( soldierType, scriptID, maxExp, self, skillIDDatas, 1, barracksItem.soldierName )
			count -= 1
		if self.tongMB:
			self.tongMB.UpdateTongMemberInfo(self.playerDBID, self.level, self.spaceScriptID, self.getRoleBarracksSoldierAmount(),self.getMilitaryRank())
		#self.writeToDB()
		
	def checkBarracksCount(self, soldierType, scriptID, count = 0):
		"""
		检查士兵数量是否超过最大值
		"""
		barracksItem = g_barracksMgr.getBarracksItemByScriptID( soldierType, scriptID )
		if not barracksItem:
			return False
		soldiers = self.roleBarracksMgr.getBarracksSoldiersByScriptID( soldierType, scriptID )
		if len( soldiers ) + count > barracksItem.getMaxHaveAmount():
			self.statusMessage(csstatus.ITEM_ADD_BARRACKS_AMOUNT_TOO_MAX, barracksItem.soldierName + "|" + barracksItem.soldierName)
			return False
			
		return True
			
	def addSoldier(self, soldierType, scriptID, level, count):
		"""
		添加士兵
		"""
		maxExp = g_barracksMgr.getSoldierMaxExpByLevel( scriptID, level)
		skillIDDatas = g_barracksMgr.getSoldierSkillIDsByScriptID(scriptID)
		barracksItem = g_barracksMgr.getBarracksItemByScriptID( soldierType, scriptID )
		while count > 0:
			self.roleBarracksMgr.addBarracksSoldier( soldierType, scriptID, maxExp, self, skillIDDatas, level, barracksItem.soldierName )
			count -= 1
		if self.tongMB:
			self.tongMB.UpdateTongMemberInfo(self.playerDBID, self.level, self.spaceScriptID, self.getRoleBarracksSoldierAmount(),self.getMilitaryRank())
		#self.writeToDB()


	def requestReviveGuard(self, srcEntityID, scriptID):
		"""
		exposed method
		请求复活亲卫
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		soldiers = self.roleBarracksMgr.getBarracksSoldiersByScriptID( csdefine.BARRACKS_SOLDIER_GUARD_TYPE, scriptID )		
		
		if not soldiers or soldiers[0].isActive:
			return
		level = soldiers[0].level
		
		money = g_barracksMgr.getReviveCost(scriptID, level)
		if money<0:
			return
		payItems ={}
		payItems[ csdefine.TRADE_PAY_ITEM_MONEY ] = money

		self.requestPay( csdefine.TRADE_TYPE_BARRACKS_REVIVE, self.id, payItems, scriptID )

	def onSuccessPayReviveGuard(self, scriptID):
		"""
		复活成功
		"""
		soldiers = self.roleBarracksMgr.getBarracksSoldiersByScriptID( csdefine.BARRACKS_SOLDIER_GUARD_TYPE, scriptID )
		if not soldiers or soldiers[0].isActive:
			return
		soldiers[0].setActive(True, self)
		#self.writeToDB()



	def saveArmyData( self, srcEntityID, armyData ):
		"""
		exposed method
		保存部队数据
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		#验证下客户端传来的数据
		firstGudSoldiers = self.roleBarracksMgr.getBarracksSoldiersByScriptID( csdefine.BARRACKS_SOLDIER_GUARD_TYPE, armyData.firstGuardScriptID )
		if len( firstGudSoldiers ) <= 0: # 说明客户端传来的第一个守卫数据错误了  立即修正
			if self.getClient():
				self.client.RemoveRoleBarracksData( armyData.firstGuardScriptID )
			armyData.firstGuardScriptID = ""
		if self.checkSaveArmyDataGudSoldier( armyData.id, armyData.firstGuardScriptID ):
			armyData.firstGuardScriptID = ""
		secondGudSoldiers = self.roleBarracksMgr.getBarracksSoldiersByScriptID( csdefine.BARRACKS_SOLDIER_GUARD_TYPE, armyData.secondGuardScriptID )
		if len( secondGudSoldiers ) <= 0: # 说明客户端传来第二个守卫数据错误了  立即修正
			if self.getClient():
				self.client.RemoveRoleBarracksData( armyData.secondGuardScriptID )
			armyData.secondGuardScriptID = ""
		if self.checkSaveArmyDataGudSoldier( armyData.id, armyData.secondGuardScriptID ):
			armyData.secondGuardScriptID = ""
		soldiers = copy.copy(self.roleBarracksMgr.getBarracksSoldiersByScriptID( csdefine.BARRACKS_SOLDIER_COMMON_TYPE, armyData.soldierScriptID ))
		aleardyUseSoldierIDs = self.checkSaveArmyDataComSoldier( armyData.id, armyData.soldierScriptID )
		removeSoldiers = []
		for soldier in soldiers:
			if soldier.id in aleardyUseSoldierIDs:
				removeSoldiers.append(soldier)
		for removeSoldier in removeSoldiers:
			soldiers.remove(removeSoldier)
		if len( soldiers ) <= 0: # 说明客户端传来兵的数据错误了  立即修正
			if self.getClient():
				self.client.RemoveRoleBarracksData( armyData.soldierScriptID )
			armyData.soldierScriptID = ""
			armyData.soldierIDs = []
		else: #验证里面兵的数据
			if len( armyData.soldierIDs ) <= 0: # 如果没有兵 默认补满
				tempSoldiers = sorted( soldiers, key = lambda e :e.getLevel(), reverse = True )
				armyMaxAmount = 0
				barracksItem = g_barracksMgr.getBarracksItemByScriptID( tempSoldiers[0].getSoldierType(), tempSoldiers[0].getScriptID())
				if barracksItem:
					armyMaxAmount = barracksItem.getArmyMaxAmount()
				if len(tempSoldiers) < armyMaxAmount:
					armyMaxAmount = len(tempSoldiers)
				resultSoldiers = tempSoldiers[:armyMaxAmount]
				for soldier in resultSoldiers:
					armyData.soldierIDs.append( soldier.id )
			else:
				roleSoldierIDs = []
				tempNeedToRemoveIDs =[]
				for soldier in soldiers:
					roleSoldierIDs.append( soldier.id )
				for soldierID in armyData.soldierIDs:
					if soldierID not in roleSoldierIDs:
						if self.getClient():
							self.client.RemoveRoleBarracksSoldierData(armyData.soldierScriptID,soldierID)
						tempNeedToRemoveIDs.append( soldierID )
				for removeID in tempNeedToRemoveIDs:
					if removeID in armyData.soldierIDs:
						armyData.soldierIDs.remove( removeID )

		if armyData.id in self.roleArmyDatas:
			for soldier in soldiers:
				if soldier.id in self.roleArmyDatas[armyData.id].soldierIDs:
					soldier.setIsInArmy(False,self)
			del self.roleArmyDatas[armyData.id]

		self.roleArmyDatas[armyData.id] = armyData

		for soldier in soldiers:
			if soldier.id in armyData.soldierIDs:
				soldier.setIsInArmy(True,self)
		if self.getClient():
			self.client.SaveArmyDataCB( armyData )

	def checkSaveArmyDataGudSoldier( self, armyDataID,guardScriptID ):
		"""
		检查部队的亲卫数据
		"""
		for roleArmyData in self.roleArmyDatas.values():
			if roleArmyData.id != armyDataID:
				if roleArmyData.firstGuardScriptID == guardScriptID or roleArmyData.secondGuardScriptID == guardScriptID:
					return True
		return False

	def checkSaveArmyDataComSoldier( self, armyDataID, soldierScriptID ):
		"""
		检查部队的士兵数据
		"""
		soldierIDs = []
		for roleArmyData in self.roleArmyDatas.values():
			if roleArmyData.id != armyDataID and roleArmyData.soldierScriptID == soldierScriptID:
				soldierIDs.extend( roleArmyData.soldierIDs )
		return soldierIDs

	def divideExpToSoldiers( self, srcEntityID, soldierType, scriptID,exp ):
		"""
		exposed method
		平分经验给小兵
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		# 当玩家经验值不足时
		if self.barracksExp < exp:
			return
		soldiers = self.roleBarracksMgr.getBarracksSoldiersByScriptID( soldierType, scriptID )
		if not len( soldiers ):
			return
		addExp = int(exp / len(soldiers))
		remain = exp - addExp * len(soldiers)
		totalRemainExp = 0
		needLevelStatuMsgs = []
		isUpMaxLevel = False
		for soldier in soldiers:
			remainExp,needLevelStatuMsg,tempIsUpMaxLevel = self.soldierAddExp( soldier, addExp, soldierType, scriptID )
			if isUpMaxLevel == False and tempIsUpMaxLevel != isUpMaxLevel:
				isUpMaxLevel = tempIsUpMaxLevel
			totalRemainExp += remainExp
			if needLevelStatuMsg > 0 and needLevelStatuMsg not in needLevelStatuMsgs:
				needLevelStatuMsgs.append(needLevelStatuMsg)

		totalRemainExp += remain
		#self.barracksExp = self.barracksExp - exp + totalRemainExp
		self.addBarracksExp( totalRemainExp -  exp )
		# for statusLevel in needLevelStatuMsgs:
		# 	self.statusMessage( csstatus.BARRACKS_UP_LEVEL_MSG,statusLevel )
		if isUpMaxLevel:
			self.statusMessage( csstatus.BARRACKS_UP_MAX_LEVEL_MSG )

	def addBarracksExp( self, addExp ):
		"""
		添加barracksExp
		"""
		oldExp = self.barracksExp
		if addExp >0:
			realAddExp = int ( addExp *  1 + ( self.barracksExpRate / 100 ) )
			self.barracksExp = realAddExp + oldExp
			self.statusMessage( csstatus.ACCOUNT_GET_BARRACKS_EXP, realAddExp)
		else:
			self.barracksExp = self.barracksExp + addExp
			self.statusMessage( csstatus.ACCOUNT_LOSE_BARRACKS_EXP, -addExp )

	def soldierAddExp( self, soldier, addExp, soldierType, scriptID ):
		"""
		兵增加经验
		"""
		needLevelStatuMsg = 0
		isUpMaxLevel = False
		barracksItem = g_barracksMgr.getBarracksItemByScriptID( soldierType, scriptID )
		if not barracksItem:
			return addExp,needLevelStatuMsg,isUpMaxLevel
		level = soldier.getLevel()
		if level >= barracksItem.getMaxUpLevel():
			return addExp,needLevelStatuMsg,isUpMaxLevel
		allExp = soldier.getExp() + addExp
		maxExp = g_barracksMgr.getSoldierMaxExpByLevel( soldier.getScriptID(), soldier.getLevel() )
		if not maxExp:
			KBEDebug.ERROR_MSG("scriptID(%s) level = %i soldierAddExp is Error "%( soldier.getScriptID(), soldier.getLevel() ))
			return addExp,needLevelStatuMsg,isUpMaxLevel
		if not barracksItem.checkBarracksItemLevelIsUnLock( self,level ):
			return addExp,needLevelStatuMsg,isUpMaxLevel

		remainExp = 0
		exp = 0
		if allExp < maxExp:
			exp = allExp
		
		while allExp >= maxExp and maxExp != 0:
			level += 1
			if not barracksItem.checkBarracksItemLevelIsUnLock( self,level ):
				needLevelStatuMsg = level
				remainExp = allExp - maxExp
				exp = 0
				break
			allExp -= maxExp
			exp = allExp
			maxExp = g_barracksMgr.getSoldierMaxExpByLevel( soldier.getScriptID(), level )
			if not maxExp:
				isUpMaxLevel = True
				exp = g_barracksMgr.getSoldierMaxExpByLevel( soldier.getScriptID(), level )
				remainExp = allExp - maxExp
				break

		soldier.setLevel( level, self )
		maxExp = g_barracksMgr.getSoldierMaxExpByLevel( soldier.getScriptID(), level )
		soldier.setMaxExp( maxExp )
		soldier.setExp( exp, self )
		return remainExp,needLevelStatuMsg,isUpMaxLevel

	def getRoleArmyDatas( self ):
		return self.roleArmyDatas
		
	def getRoleArmyDataByID( self, id ):
		return self.roleArmyDatas.get(id, None)

	def onSoliderDead( self, index, soldierType, scriptID, id ):
		"""
		小兵死亡
		"""
		if len(self.roleArmyDatas):
			roleArmyData = self.roleArmyDatas.get( index, None )
			if not roleArmyData:
				return
			#self.roleBarracksMgr.removeBarracksSoldiersByScriptID( soldierType,scriptID, id )
			if soldierType == csdefine.BARRACKS_SOLDIER_GUARD_TYPE:
				# if roleArmyData.firstGuardScriptID == scriptID:
				# 	roleArmyData.firstGuardScriptID = ""
				# elif roleArmyData.secondGuardScriptID == scriptID:
				# 	roleArmyData.secondGuardScriptID = ""
				soldiers = self.roleBarracksMgr.getBarracksSoldiersByScriptID( csdefine.BARRACKS_SOLDIER_GUARD_TYPE, scriptID )
				if soldiers:
					soldiers[0].setActive(False, self)

			elif soldierType == csdefine.BARRACKS_SOLDIER_COMMON_TYPE:
				self.roleBarracksMgr.removeBarracksSoldiersByScriptID( soldierType,scriptID, id )
				if roleArmyData.soldierScriptID == scriptID and id in roleArmyData.soldierIDs:
					roleArmyData.soldierIDs.remove( id )
					if self.tongMB:
						self.tongMB.UpdateTongMemberInfo(self.playerDBID, self.level, self.spaceScriptID, self.getRoleBarracksSoldierAmount(),self.getMilitaryRank())
			#self.writeToDB()
			return

		spaceEntity = self.getCurrentSpace()
		if spaceEntity and spaceEntity.getScript().getSpaceChildType() == csdefine.SPACE_CHILD_TYPE_GCZ:
			spaceEntity.removeRoleArmyDefaultData( self, self.callArmyIndex, soldierType, scriptID, id )


	def onCommanderDead(self):
		"""
		将领死亡处理
		"""
		#设置
		pass

	def dismissArmyData( self, srcEntityID, armyID ):
		"""
		解散某支部队
		"""
		if not self.validateClientCall( srcEntityID ):
			return

		if armyID not in self.roleArmyDatas:
			return

		soldiers = self.roleBarracksMgr.getBarracksSoldiersByScriptID( csdefine.BARRACKS_SOLDIER_COMMON_TYPE, self.roleArmyDatas[armyID].soldierScriptID )
		for soldier in soldiers:
			if soldier.id in self.roleArmyDatas[armyID].soldierIDs:
				soldier.setIsInArmy(False,self)
		del self.roleArmyDatas[armyID]
		#self.writeToDB()
		if self.getClient():
			self.client.CLIENT_OnDismissArmyData( armyID )

	def guardSoldierSkillUpLevel( self, srcEntityID, guardScriptID, guardSoldierID,skillID, exp ):
		"""
		亲卫技能升级
		"""
		if not self.validateClientCall( srcEntityID ):
			return

		# 当玩家经验值不足时
		if self.barracksExp < exp:
			return

		guardSoldiers = self.roleBarracksMgr.getBarracksSoldiersByScriptID( csdefine.BARRACKS_SOLDIER_GUARD_TYPE, guardScriptID )
		if not len( guardSoldiers ):
			return

		guardSoldier = None
		for soldier in guardSoldiers:
			if soldier.id == guardSoldierID:
				guardSoldier = soldier
				break
		if guardSoldier == None:
			return

		for index in range( len(guardSoldier.skillIDDatas) ):
			skillIDData = guardSoldier.skillIDDatas[index]
			if skillIDData.skillID != skillID:
				continue
			allExp = skillIDData.getCurExp() + exp
			if skillIDData.getMaxExp() == 0:
				return
			maxExp = skillIDData.getMaxExp()
			remainExp = 0
			realexp = 0
			curSkillID = 0
			lastSkillID = skillIDData.skillID
			if allExp < maxExp:
				realexp = allExp
				curSkillID = skillID
			while allExp >= maxExp and maxExp != 0:
				nextSkillID = g_barracksMgr.getSoldierNextSkillIDByScriptID( guardScriptID, skillID )
				if nextSkillID == 0:
					realexp = maxExp
					remainExp = allExp - maxExp
					curSkillID = skillID
					break
				allExp -= maxExp
				realexp = allExp
				curSkillID = nextSkillID
				skillID = nextSkillID
				maxExp = g_barracksMgr.getSoldierSkillReqExpByScriptID( guardScriptID, curSkillID )
				if not maxExp:
					remainExp = allExp
					realexp = maxExp
					break

			skillIDData.setCurExp( realexp )
			skillIDData.setMaxExp( maxExp )
			skillIDData.setSkillID( curSkillID )
			self.addBarracksExp( remainExp - exp )
			#self.writeToDB()
			if self.getClient():
				self.client.OnUpdateGuardSoldierSkill( guardScriptID,guardSoldierID,lastSkillID, skillIDData )
			break

	def setCallArmyIndex( self, callArmyIndex ):
		"""
		设置召出部队Index
		"""
		self.callArmyIndex = callArmyIndex

	def getRoleBarracksSoldierAmount( self ):
		"""
		获得玩家天兵兵力数量
		"""
		scriptIDs = self.roleBarracksMgr.getBarracksSoldiersScriptIDsBySoldierType( csdefine.BARRACKS_SOLDIER_COMMON_TYPE )
		soldiers = []
		for scriptID in scriptIDs:
			soldiers.extend(self.roleBarracksMgr.getBarracksSoldiersByScriptID( csdefine.BARRACKS_SOLDIER_COMMON_TYPE, scriptID))

		return len( soldiers )

	def enterTrainSoldierGround( self, srcEntityID ):
		"""
		进入练兵场
		"""
		if not self.validateClientCall( srcEntityID ):
			return

		if self.getLevel() < Const.OPEN_TRAIN_SOLDIER_GROUND_LEVEL:
			return

		KBEngine.globalData["TrainSoldierGroundManager"].enterHomeBarracks( self.base, self.playerDBID )

	def getRoleBarracksSoldierModelNumbers( self ):
		"""
		获得玩家兵营兵种的模型列表
		"""
		modelNumbers = []
		for roleArmyData in self.roleArmyDatas.values():
			soldierObj = KST.g_objFactory.getMonsterObject( roleArmyData.soldierScriptID )
			if not soldierObj:
				continue
			modelNumberStr = soldierObj.getEntityProperty( "modelNumber","" )
			if modelNumberStr:
				modelNumbers.append( modelNumberStr )
			
		return modelNumbers
		
	def canDispatch(self, barrackID):
		"""部队 能否被派遣"""
		if barrackID in self.roleArmyDatas:
			return self.roleArmyDatas[barrackID].canDispatch()
		return False

	def setIsCanOpenBarracks( self, isCanOpenBarracks ):
		"""
		设置是否可以打开天兵营
		"""
		self.isCanOpenBarracks = isCanOpenBarracks

	def openBarracksByOccupyTrainGround( self, npcID, requireSoldierAmount, requireSoldierLevel ):
		"""
		打开兵营占领练兵场
		"""
		allSoldiers = self.roleBarracksMgr.getBarracksSoldiersBySoldierType( csdefine.BARRACKS_SOLDIER_COMMON_TYPE )
		for soldiers in allSoldiers:
			if self.getClient():
				self.client.InitBarracksByOccupyTrainGround( soldiers )
		if self.getClient():
			self.client.InitBarracksByOccupyTrainGroundOver( npcID, requireSoldierAmount, requireSoldierLevel )

	def sureToOccupyTrainGround( self, srcEntityID, npcID, soldierScriptID ):
		"""
		exposed method
		通过消耗士兵和消耗金钱
		确认占领练兵场
		"""
		if not self.validateClientCall( srcEntityID ):
			return

		npcEntity = KBEngine.entities.get( npcID, None )
		if not npcEntity:
			return
		requireSoldierAmount = npcEntity.getScript().getRequireSoldierAmount()
		requireSoldierLevel = npcEntity.getScript().getRequireSoldierLevel()
		requireMoney = npcEntity.getScript().getRequireMoney()
		soldierIDs = self.getRemoveSoldierIDByRequireSoldierLevel( soldierScriptID, requireSoldierLevel, requireSoldierAmount )
		if not len(soldierIDs):
			return
		if self.getBindMoney() < requireMoney:
			replaceMoney = requireMoney - self.getBindMoney()
			self.inquireMessage(csstatus.NPCSHOP_COST_MONEY_REPLACE_BIND_MONEY, [Functions.moneyToStr(replaceMoney)], "replacePayToOccupyTrainGround", requireMoney, soldierIDs, soldierScriptID, npcEntity)
			return
		self.subBindMoney( requireMoney, csdefine.MONEY_SUN_REASON_OCCUPY_TRAIN_GROUND )
		for soldierID in soldierIDs:
			self.roleBarracksMgr.removeBarracksSoldiersByScriptID( csdefine.BARRACKS_SOLDIER_COMMON_TYPE,soldierScriptID, soldierID )
		KBEngine.globalData["TrainSoldierGroundManager"].addOccupyTrainSoldierGroundDatas( npcEntity.getLineNumber(), npcEntity.getIndex(), self.playerDBID, self.getName(),self.getProfession(),self.base )

	def replacePayToOccupyTrainGround(self, reply, requireMoney, soldierIDs, soldierScriptID, npcEntity):
		"""
		消耗金币代替绑金
		确认占领练兵场
		"""
		if reply:
			if self.subBindMoneyAndMoney( requireMoney, csdefine.MONEY_SUN_REASON_OCCUPY_TRAIN_GROUND ):
				for soldierID in soldierIDs:
					self.roleBarracksMgr.removeBarracksSoldiersByScriptID( csdefine.BARRACKS_SOLDIER_COMMON_TYPE,soldierScriptID, soldierID )
				KBEngine.globalData["TrainSoldierGroundManager"].addOccupyTrainSoldierGroundDatas( npcEntity.getLineNumber(), npcEntity.getIndex(), self.playerDBID, self.getName(),self.getProfession(),self.base )
			else:
				self.statusMessage( csstatus.MONEY_NOT_ENOUGH )
	
	def occupyLbcCostSoldier(self, soldierScriptID, soldierLevel, soldierNum):
		"""
		占领练兵场消耗士兵
		"""
		tempSoldierIDs = []
		soldiers = self.roleBarracksMgr.getBarracksSoldiersByScriptID( csdefine.BARRACKS_SOLDIER_COMMON_TYPE, soldierScriptID )
		for soldier in soldiers:
			if soldier.getLevel() >= soldierLevel:
				#激活并且不在部队中
				if soldier.isActive and not soldier.isInArmy:
					tempSoldierIDs.append( soldier.id )
		if not len( tempSoldierIDs ) >= soldierNum:
			KBEDebug.ERROR_MSG("soldierNum = %d  < requireNum( %d )"%(len(tempSoldierIDs), soldierNum))
			return

		for soldierID in  random.sample( tempSoldierIDs, soldierNum ):
			self.roleBarracksMgr.removeBarracksSoldiersByScriptID( csdefine.BARRACKS_SOLDIER_COMMON_TYPE, soldierScriptID, soldierID )


	def getRemoveSoldierIDByRequireSoldierLevel( self, soldierScriptID, requireSoldierLevel, requireSoldierAmount ):
		"""
		"""
		tempSoldierIDs = []
		soldiers = self.roleBarracksMgr.getBarracksSoldiersByScriptID( csdefine.BARRACKS_SOLDIER_COMMON_TYPE, soldierScriptID )
		for soldier in soldiers:
			if soldier.getLevel() >= requireSoldierLevel:
				tempSoldierIDs.append( soldier.id )

		if len( tempSoldierIDs ) >= requireSoldierAmount:
			return random.sample( tempSoldierIDs, requireSoldierAmount )
		return []

	def isArmyHasLiveMember( self, armyID ):
		"""
		某部队是否还有存活的成员
		"""
		armyData = self.roleArmyDatas[armyID]
		if armyData.firstGuardScriptID:
			firstGudSoldiers = self.roleBarracksMgr.getBarracksSoldiersByScriptID( csdefine.BARRACKS_SOLDIER_GUARD_TYPE, armyData.firstGuardScriptID )
			if len( firstGudSoldiers ) and firstGudSoldiers[0].isActive:
				return True
		
		if armyData.secondGuardScriptID:
			secondGudSoldiers = self.roleBarracksMgr.getBarracksSoldiersByScriptID( csdefine.BARRACKS_SOLDIER_GUARD_TYPE, armyData.secondGuardScriptID )
			if len( secondGudSoldiers ) and secondGudSoldiers[0].isActive:
				return True
		
		if len(armyData.soldierIDs) != 0:
			return True
		
		return False

	def getDefaultArmyIndex( self ):
		"""
		获得默认出战部队的Index
		第一支部队没有值就用第二只部队 以此类推
		"""
		for armyID in self.roleArmyDatas.keys():
			if self.isArmyHasLiveMember( armyID ):
				return armyID
		return -1

	def getOccupySoldierScriptID( self, reqLevel, reqAmount):
		"""
		获取符合交付条件的scriptID列表
		"""
		scriptIDList = []
		if csdefine.BARRACKS_SOLDIER_COMMON_TYPE in self.roleBarracksMgr:
			soldierList = self.roleBarracksMgr.getBarracksSoldiersBySoldierType(csdefine.BARRACKS_SOLDIER_COMMON_TYPE)
		else:
			return []

		count=0
		for soldiers in soldierList:
			if count >= reqAmount:
				break
			count=0
			for soldier in soldiers:
				if soldier.getLevel() >= reqLevel and soldier.isActive and not soldier.isInArmy:
					count+=1
					if count >= reqAmount:
						scriptIDList.append(soldier.getScriptID())
						break

		return scriptIDList

	def gmClearBarracksData( self, scriptID = "" ):
		"""
		清除天兵营小兵数据
		"""
		allSoldiers = []
		if not scriptID:
			for soldiers in self.roleBarracksMgr.getBarracksSoldiersBySoldierType( csdefine.BARRACKS_SOLDIER_COMMON_TYPE ):
				allSoldiers.extend( soldiers )
			for soldiers in self.roleBarracksMgr.getBarracksSoldiersBySoldierType( csdefine.BARRACKS_SOLDIER_GUARD_TYPE ):
				allSoldiers.extend( soldiers )
		else:
			soldierType = csdefine.BARRACKS_SOLDIER_COMMON_TYPE
			barracksSoldierScriptIDs = g_barracksMgr.getBarracksItemsBySoldierType( csdefine.BARRACKS_SOLDIER_COMMON_TYPE )
			if scriptID not in barracksSoldierScriptIDs:
				soldierType = csdefine.BARRACKS_SOLDIER_GUARD_TYPE
			allSoldiers.extend(self.roleBarracksMgr.getBarracksSoldiersByScriptID( soldierType, scriptID ))

		for soldier in allSoldiers:
			for armyData in self.roleArmyDatas.values():
				if armyData.soldierScriptID != soldier.getScriptID():
					continue
				if soldier.id in armyData.soldierIDs:
					armyData.soldierIDs.remove(soldier.id)
			self.roleBarracksMgr.removeBarracksSoldiersByScriptID( soldier.getSoldierType(),soldier.getScriptID(), soldier.id )
