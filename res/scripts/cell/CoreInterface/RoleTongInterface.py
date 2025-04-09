# -*- coding: utf-8 -*-

import KBEDebug
import KBEngine
import csstatus
import csdefine
import csconst
import Const
import ItemFactory
import TongLoader
import ItemTypeEnum
import Functions
from ConfigObject.Trade.TradeMgr import g_tradeMgr

class RoleTongInterface( object ):
	def __init__( self ):
		object.__init__( self )
	
	def tongOnInit( self, tongMB, leaderDBID, tongTitle, tongGrade, contribution, tongShopLevel, tongSmithyLevel, allocation, BHLDAllocation ):
		"""
		define method
		请求初始化信息回调
		"""
		self.tongMB = tongMB
		self.tongLeaderDBID = leaderDBID
		self.tongTitle = tongTitle
		self.tongGrade = tongGrade
		self.tongContribution = contribution
		self.tongShopLevel = tongShopLevel
		self.tongSmithyLevel = tongSmithyLevel
		self.tongAllocation = allocation
		self.BHLDAllocation = BHLDAllocation
		self.tongMB.UpdateTongMemberInfo(self.playerDBID, self.level, self.spaceScriptID,self.getRoleBarracksSoldierAmount(),self.getMilitaryRank())
		
	def tongOnInitErr( self ):
		"""
		define method
		初始化信息失败
		"""
		self.tongDBID = 0
		self.tongMB = None
		self.tongName = ""
		if self.getCurrentSpaceScriptID() == Const.TONG_SPACE_SCRIPTID:
			self.gotoBindSpace()
	
	def tongCreate( self, srcEntityID, tongName ):
		"""
		exposed method
		创建帮会
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		if len( tongName.encode("gbk") ) > csconst.TONG_NAME_LENGTH_UPPER_LIMIT:
			self.statusMessage( csstatus.TONG_NAME_REACH_MAX )
			return
		if self.level < Const.TONG_CREATE_MIX_LEVEL:
			self.statusMessage( csstatus.TONG_CREATE_CANNOT_REACH_LEVEL )
			return
		if self.jingjieLevel < Const.TONG_CREATE_MIX_JINJIELEVEL:
			self.statusMessage( csstatus.TONG_CREATE_NO_ENOUGH_DAOHENG )
			return
			
		if not self.isEnoughBindMoney( Const.TONG_CREATE_NEED_MONEY ):
			payItems = {}
			cost = Const.TONG_CREATE_NEED_MONEY - self.bindMoney
			payItems.update({csdefine.TRADE_PAY_ITEM_BIND_MONEY : self.bindMoney})
			payItems.update({csdefine.TRADE_PAY_ITEM_MONEY : cost})
			payItems.update({csdefine.TRADE_PAY_ITEM_CREATETONG : tongName})
			self.inquireMessage( csstatus.NPCSHOP_COST_MONEY_REPLACE_BIND_MONEY, [Functions.moneyToStr(cost)], 
				"replayTongCreate", payItems )
		else:
			payItems = {}
			payItems.update({csdefine.TRADE_PAY_ITEM_BIND_MONEY : Const.TONG_CREATE_NEED_MONEY})
			payItems.update({csdefine.TRADE_PAY_ITEM_CREATETONG : tongName})
			self.requestPay( csdefine.TRADE_TYPE_CREATE_TONG, 0, payItems, () )
		
	def replayTongCreate(self, reply, payDict):
		"""金币代付绑定金币"""
		if reply:
			self.requestPay( csdefine.TRADE_TYPE_CREATE_TONG, 0, payDict, () )
		
	def tongOnCreate( self, tongMB, leaderDBID, tongTitle, tongGrade, contribution, tongShopLevel, tongSmithyLevel, allocation, BHLDAllocation ):
		"""
		define method
		请求初始化信息回调
		"""
		self.tongOnInit( tongMB, leaderDBID, tongTitle, tongGrade, contribution, tongShopLevel, tongSmithyLevel, allocation, BHLDAllocation )
		self.initDailyQuest()

	def tongInviteJoin( self, srcEntityID, beInviteID ):
		"""
		exposed method
		邀请入帮
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		if self.tongMB is None:return
		if self.tongHasGrade( csdefine.TONG_GRADE_INVITE ):
			beInviter = KBEngine.entities.get( beInviteID )
			if beInviter is None:
				KBEDebug.ERROR_MSG("Can not find entity(%d)"%beInviteID)
				return
			if beInviter.getLevel() < csconst.TONG_JOIN_MIX_LEVEL:
				self.statusMessage( csstatus.TONG_CANOT_JOIN_NOT_ENOUGH_LEVEL, "" )
				return
			if beInviter.tongMB:
				self.statusMessage( csstatus.TONG_CANOT_INVITE_HAS_TONG, "" )
				return
			if self.getCamp() != beInviter.getCamp():
				self.statusMessage( csstatus.TONG_CANOT_INVITE_CAMP, "" )
				return
			
			self.tongMB.inviteJoinTong(self.playerName, self.getCamp(), self.base, beInviter.base)
			#beInviter.base.tongBeInviteJoin( self.playerName, self.tongName, self.getCamp(),str(self.tongDBID), self.base, self.tongMB)
		else:
			self.statusMessage( csstatus.TONG_CANOT_INVITE_NOT_ENOUGH_GRADE )
				
	
	def tongOnJoin( self, tongMB, tongDBID, tongName, tongTitle, tongGrade ):
		"""
		define method
		成功入会的回调
		"""
		self.tongDBID = tongDBID
		self.tongMB = tongMB
		self.tongName = tongName
		self.tongTitle = tongTitle
		self.tongGrade = tongGrade
		self.tongMB.UpdateTongMemberInfo(self.playerDBID, self.level, self.spaceScriptID, self.getRoleBarracksSoldierAmount(),self.getMilitaryRank())
		self.initDailyQuest()
		#self.writeToDB()
		
	def onLeaveTong( self ):
		"""
		define method
		离开帮会
		"""
		self.tongDBID = 0
		self.tongMB = None
		self.tongName = ""
		self.tongTitle = 0
		self.tongGrade = 0
		self.removeQuestType( csdefine.QUEST_TYPE_DAILY )			# 移除帮会任务
		#self.writeToDB()
		if self.getCurrentSpaceScriptID() == Const.TONG_SPACE_SCRIPTID:
			self.gotoBindSpace()

		#帮会掠夺战
		spaceEntity = self.getCurrentSpace()
		if hasattr(spaceEntity, "leaveTongOnActivity"):
			spaceEntity.leaveTongOnActivity(self)

	def onSetTitle( self, titleID, grades ):
		"""
		define method
		设置玩家的帮会成员职位
		"""
		self.tongTitle = titleID
		self.tongGrade = grades
		
	def isTongLeader( self ):
		"""是否是帮主"""
		if self.tongMB:
			return self.tongLeaderDBID == self.playerDBID
		return False
		
	def onLeaderChange( self, leaderDBID ):
		"""
		define method
		帮主改变
		"""
		self.tongLeaderDBID = leaderDBID
		
	def tongDismissChangeConToMoney( self, money ):
		"""
		define method
		帮会解散 帮贡转化为钱
		"""
		self.addBindMoney( money, csdefine.MONEY_ADD_REASON_TONGCONTRI_TO_MONEY )
		
	def getTongSalary( self, srcEntityID ):
		"""
		exposed method
		领取俸禄
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		if self.tongMB:
			self.tongMB.getSalary( self.playerDBID )

	def getTongTitle( self ):
		"""
		获得自己帮会职位
		"""
		return self.tongTitle
		
	def onGetTongSalary( self, itemID ):
		"""
		define method
		获得帮贡
		"""
		itemInst = ItemFactory.ItemFactoryInst.createDynamicItem(itemID)
		if itemInst:
			state = self.addItem(itemInst , csdefine.ITEM_ADD_BY_TONG_SALARY )
			if state != csstatus.ITEM_GO_ON:
				self.statusMessage( state )
				self.tongMB.onGetSalaryFail( self.playerDBID )
				self.client.OnGetSalaryFail()
		
	def donateMoney( self, srcEntityID, moneyStr ):
		"""
		exposed method
		捐献
		"""
		if not self.validateClientCall( srcEntityID ):
			return

		if self.isPWKitBagLock():
			#先判定背包是否上锁
			self.client.CLIENT_openInputKBPW()
			return False

		money = int(moneyStr)
		if not self.validateClientCall( srcEntityID ):
			return
		if self.tongMB:
			if self.money >= money:
				self.tongMB.donateMoney( self.playerDBID, money )
				
	def onDonateMoney( self, money ):
		"""
		define method
		捐献回调
		"""
		if not self.subMoney( money, csdefine.MONEY_SUB_REASON_TONG_DONATE ):
			KBEDebug.ERROR_MSG("Player donate money err!has not enought money!")
	
	def tongHasGrade( self, grade ):
		"""是否有某个权限"""
		newGrade = 1 << grade
		return self.tongGrade & newGrade

	def addContribution( self, value ):
		"""
		增加帮贡
		"""
		if self.tongMB:
			self.tongMB.addContribution( self.playerDBID, value )
		
	def onContributionChange( self, contribution ):
		"""
		define method
		帮贡改变
		"""
		self.tongContribution = contribution
		
	def onTongShopLevelChange( self, shopLevel ):
		"""
		define method
		帮会商店等级改变
		"""
		self.tongShopLevel = shopLevel
		
	def onTongSmithyLevelChange( self, smithyLevel ):
		"""
		define method
		帮会铁匠铺等级改变
		"""
		self.tongSmithyLevel = smithyLevel



	def addTongBlockList(self,srcEntityID, memberDBID):
		"""
		屏蔽用户消息
		<Exposed method>
		"""
		if not self.validateClientCall(srcEntityID):
			return
		if self.tongMB:
			self.tongMB.notifyAddTongBlockMember(str(self.playerDBID), memberDBID)


	def removeTongBlockList(self,srcEntityID, memberDBID):
		"""
		取消屏蔽
		<Exposed method>
		"""
		if not self.validateClientCall(srcEntityID):
			return
		if self.tongMB:
			self.tongMB.notifyRemoveTongBlockMember(str(self.playerDBID), memberDBID)



	#--------------------------------帮会仓库---------------------------------------
	def CELL_requestSaveTongItem(self, srcEntityID, srcorder, bagID):
		"""
		<Exposed method>
		请求存物品到帮会仓库
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		if self.doKBOpratorCheck() != csdefine.KB_OPRATOR_CAN_GO:return
		srcItem = self.getItemInstByOrder( srcorder )
		if srcItem.bindType == ItemTypeEnum.BINDED_STATE:
			return
		if srcItem:
			if self.tongMB:
				srcItem.setLock( True )
				self.tongMB.requestSaveTongItem( self, self.playerName, srcorder, srcItem, bagID )
		else:
			KBEDebug.ERROR_MSG("Save item err!cannot find order(%d)"%srcorder)
	
	def onRequestSaveTongItem( self, srcorder, dstorder, isSuccess ):
		"""
		define method
		物品保存到帮会仓库回调
		"""
		if isSuccess:
			self.itemsBag.removeByOrder(srcorder)
			self.client.CLIENT_removeItem( srcorder )
	
	def CELL_requestTakeTongItem(self, srcEntityID, srcorder):
		"""
		<Exposed method>
		请求从帮会仓库取出物品
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		if not self.tongHasGrade( csdefine.TONG_GRADE_STORAGE ):
			self.statusMessage( csstatus.TONG_NOT_ENOUGH_GRADE )
			return
		if self.doKBOpratorCheck() != csdefine.KB_OPRATOR_CAN_GO:return
		if self.tongMB:
			self.tongMB.requestTakeTongItem( self, self.playerName, srcorder )
		
	def onRequestTakeTongItem( self, srcorder, srcitem, isSuccess ):
		"""
		define method
		从帮会仓库取出物品回调
		"""
		if isSuccess and srcitem:
			freeOrder = self.getFreeOrderByItemInst( srcitem.getKitBagType() )
			if freeOrder:
				srcitem.setLock( False )
				srcitem.setOrder(freeOrder)
				srcitem.ownerID = self.playerDBID
				self.itemsBag.addItem( srcitem )
				self.client.CLIENT_swapItemFromBagToTongStore( freeOrder, srcorder )
			else:
				self.statusMessage( csstatus.NPCSHOP_BAG_ENOUGH )
				self.base.onRequestTakeTongItemFail( srcorder, srcitem )
	
	def CELL_swapTongStoreItem( self, srcEntityID, srcorder, dstorder ):
		"""
		Exposed method
		交换帮会仓库物品位置
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		srcorder = int( srcorder )
		dstorder = int( dstorder )
		if srcorder == dstorder:return
		srcBagType = self.getBagTypeByOrder( srcorder )
		dstBagType = self.getBagTypeByOrder( dstorder )
		if srcBagType == ItemTypeEnum.BAG_STORE or dstBagType == ItemTypeEnum.BAG_STORE:
			return								# 不支持，帮会仓库的物品放入玩家仓库
		
		if srcBagType == dstBagType:			# 仓库物品位置互换
			if srcBagType == ItemTypeEnum.BAG_TONG_STORE:
				self.tongMB.swapTongItemAC( self, srcorder, dstorder )
				return
				
#		if self.tongHasGrade( csdefine.TONG_GRADE_STORAGE ):
#			self.statusMessage( csstatus.TONG_NOT_ENOUGH_GRADE )
#			return
		if self.doKBOpratorCheck() != csdefine.KB_OPRATOR_CAN_GO:return
		if srcBagType == ItemTypeEnum.BAG_TONG_STORE:
			dstitem = self.getItemInstByOrder( dstorder )
			if dstitem:
				if dstitem.isBinded():
					self.statusMessage( csstatus.TONG_STORAGE_CANT_STORE )
					return
				dstitem.setLock( True )
			self.tongMB.swapItemFromTongStoreToBag( self, self.playerName, srcorder, dstorder, dstitem )
		elif dstBagType == ItemTypeEnum.BAG_TONG_STORE:
			srcitem = self.getItemInstByOrder( srcorder )
			if srcitem:
				srcitem.setLock( True )
			self.tongMB.swapItemFromBagToTongStore( self, self.playerName, srcorder, dstorder, srcitem )
		
	def onSwapItemToTongStore( self, srcorder, dstorder, dstitem ):
		"""
		define method
		仓库与其他包括交换物品回调
		@param srcorder 背包order
		@param dstorder 仓库order
		@param dstitem  拖入背包的item
		"""
		srcitem = self.itemsBag[ srcorder ]
		if srcitem:
			self.itemsBag.removeByOrder(srcorder)
		if dstitem:
			dstitem.setOrder( srcorder )
			dstitem.ownerID = self.playerDBID
			dstitem.setLock( False )
			self.itemsBag.addItem(dstitem)
		self.client.CLIENT_swapItemFromBagToTongStore( srcorder, dstorder )
		
	def CELL_requestRemoveTongStoreItem( self, srcEntityID, sUID ):
		"""
		exposed method
		帮会仓库移除物品
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		if self.tongHasGrade( csdefine.TONG_GRADE_STORAGE ):
			self.statusMessage( csstatus.TONG_CANOT_DESTROY_PUBLIC_ITEM )
			return
		if self.tongMB:
			self.tongMB.requestRemoveTongStoreItem( self, int( sUID ) )

	def replyRemoveTongStoreItem( self, reply, order, playerMB):
		"""
		"""
		playerMB.client.CLIENT_OnSetGridEnabledByOrderID(order,True)
		if self.tongMB:
			self.tongMB.removeTongStoreItem( reply, order, playerMB )
	
	def sortTongStoreItem( self, srcEntityID, bagID ):
		"""
		exposed method
		帮会仓库分类
		"""
		if srcEntityID == self.id and self.tongMB:
			self.tongMB.sortTongStoreItem( self, bagID )
			
	#--------------------------------帮会技能学习---------------------------------------
	def startStudyTongSkill( self, srcEntityID, skillID ):
		"""
		exposed method
		开始学习帮会技能
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		if skillID in self.attrSkills:
			return
		preSkill = TongLoader.g_TongLoader.getPreSkill( skillID )
		if preSkill and preSkill not in self.attrSkills:
			KBEDebug.ERROR_MSG("Study tong skill err!!player cannot find preSkill(%d),skillID(%d)" % (preSkill, skillID))
			return
		
		reqXiuweiLevel = TongLoader.g_TongLoader.getSkillReqConditionByName( skillID, "StudyReqXiuweiLevel" )
		if self.xiuwei < reqXiuweiLevel:
			self.statusMessage( csstatus.TONG_STUDY_SKILL_NO_ENOUGH_XIUWEI )
			return
			
		reqMoney = TongLoader.g_TongLoader.getSkillReqConditionByName( skillID, "StudyReqMoney" )
		payItems = {}
		payItems[csdefine.TRADE_PAY_ITEM_MONEY] = reqMoney
		payItems[csdefine.TRADE_PAY_ITEM_LEARNTONGSKILL] = skillID
		
		self.requestPay(csdefine.TRADE_TYPE_LEAR_TONG_SKILL, 0, payItems, preSkill, skillID )
		
	def onSuccessPayTongSkill( self, preSkill, skillID ):
		"""
		学习帮会技能，成功支付回调
		"""
		if preSkill:
			self.removeSkill(preSkill, csdefine.SKILL_REMOVE_REASON_LEARN_SKILL)
		self.addSkill(skillID)
		self.client.OnFinishLearnSkill(skillID)
	
	def tong_roleLevelUp( self ):
		"""
		"""
		if self.tongMB:
			self.tongMB.UpdateTongMemberInfo(self.playerDBID, self.level, self.spaceScriptID,self.getRoleBarracksSoldierAmount(),self.getMilitaryRank())
			
	def tong_roleEnterSpace( self ):
		"""
		"""
		if self.tongMB:
			self.tongMB.UpdateTongMemberInfo(self.playerDBID, self.level, self.spaceScriptID,self.getRoleBarracksSoldierAmount(),self.getMilitaryRank())

#-----------------------------CST-11386 帮会争霸------------------------------------------------------

	def readyToSignUpBHZBMember( self, srcEntityID, signUpMemberDatas ):
		"""
		define method
		确认帮会争霸成员
		"""
		if not self.validateClientCall( srcEntityID ):
			return

		if not self.tongMB:
			return

		if self.tongTitle not in [csdefine.TONG_TITLE_1,csdefine.TONG_TITLE_3]:
			return

		# allMemberPlayerDBIDs = []
		# for signUpMemberData in signUpMemberDatas:
		# 	if signUpMemberData.captainDBID in allMemberPlayerDBIDs:
		# 		signUpMemberData.captainDBID = ""
		# 	else:
		# 		allMemberPlayerDBIDs.append( signUpMemberData.captainDBID )
		# 	tempList = list(signUpMemberData.memberDBIDs)
		# 	for playerDBID in tempList:
		# 		if not playerDBID:
		# 			continue
		# 		if playerDBID in allMemberPlayerDBIDs:
		# 			signUpMemberData.memberDBIDs.remove(playerDBID)
		# 		else:
		# 			allMemberPlayerDBIDs.append( playerDBID )

		self.tongMB.readyToSignUpBHZBMember( signUpMemberDatas, self.base )
		# spaceEntity = self.getCurrentSpace()
		# if spaceEntity and spaceEntity.getScript().getSpaceChildType() == csdefine.SPACE_TYPE_CHILD_BHZB_HOME_BARRACKS:
		# 	tempDict = {}
		# 	for signUpMemberData in signUpMemberDatas:
		# 		if signUpMemberData.groupID not in tempDict:
		# 			tempDict[signUpMemberData.groupID] = []
		# 		if signUpMemberData.captainDBID:
		# 			tempDict[signUpMemberData.groupID].append( int(signUpMemberData.captainDBID) )
		# 		tempDict[signUpMemberData.groupID].extend( [int(i) for i in signUpMemberData.memberDBIDs if i] )
		# 	spaceEntity.changeMemberGroup( self.tongDBID, tempDict)

	def gmSignUpBHZB( self ):
		"""
		GM 测试 报名帮会争霸
		"""
		from BHZBMSignMemberInfo import BHZBMSignMemberInfo
		info = BHZBMSignMemberInfo()
		info.signID = 1
		info.groupID = 1
		info.captainDBID = str( self.playerDBID )
		info.memberDBIDs = []
		if self.tongMB:
			self.tongMB.gmSignUpBHZB( info, self.base, self.playerDBID )

#-------------------设置拾取模式------------------------------------------------------------------------
	def reqSetTongAllocation( self, srcEntityID, allocation ):
		"""
		Exposed method
		设置帮会争霸拾取模式
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		
		#比赛期间不让修改拾取模式
		if KBEngine.globalData.get("BHZBALLOCATION", "GUANBI") != "KAIQI":
			self.statusMessage(csstatus.DROPBOX_ALLOCATION_FORBID)
			self.client.onSetTongAllocation(self.tongAllocation)
			return
			
		if self.tongAllocation == allocation:
			self.client.onSetTongAllocation(self.tongAllocation)
			return
		
		self.tongMB.setTongAllocation(self.playerDBID, allocation)
		
	def OnUpdateTongAllocation( self, allocation ):
		"""
		"""
		if self.tongMB is None:
			return
		
		self.tongAllocation = allocation
		
		if self.getClient():
			self.client.onSetTongAllocation(self.tongAllocation)
			
	def reqSetTongBHLDAllocation( self, srcEntityID, allocation ):
		"""
		Exposed method
		设置帮会掠夺拾取模式
		"""
		if not self.validateClientCall( srcEntityID ):
			return
			
		#比赛期间不让修改拾取模式
		if KBEngine.globalData.get("BHLDALLOCATION", "GUANBI") != "KAIQI":
			self.statusMessage(csstatus.DROPBOX_ALLOCATION_FORBID)
			self.client.onSetTongBHLDAllocation(self.BHLDAllocation)
			return
		
		if self.BHLDAllocation == allocation:
			self.client.onSetTongBHLDAllocation(self.BHLDAllocation)
			return
		
		self.tongMB.setTongBHLDAllocation(self.playerDBID, allocation)
		
	def OnUpdateTongBHLDAllocation( self, allocation ):
		"""
		"""
		if self.tongMB is None:
			return
		
		self.BHLDAllocation = allocation
		
		if self.getClient():
			self.client.onSetTongBHLDAllocation(self.BHLDAllocation)