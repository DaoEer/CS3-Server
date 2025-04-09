# -*- coding: utf-8 -*-
import KBEDebug
from SpaceCopy import SpaceCopy
import csdefine
import KBEMath
import Math
import ItemTypeEnum
import ItemFactory
import KBEngine
import time
import csstatus
import KST
import time
import random
import math
import csarithmetic
import cschannel_msgs
import Functions
import csconst
import ZyjjRewardData
from Reward import RewardBasicValueData
from ConfigObject.MailContentDataLoader import g_mailContentDataLoader

class SpaceCopyCampFiveYCJMD( SpaceCopy ):
	"""
	阵营战场“勇闯绝命岛”（5人） JIRA CST-10463
	"""
	def __init__( self ) :
		SpaceCopy.__init__( self )
		self.hasBeKill = False
		self.isEnd = False
		self.startReduceTime = 0.0
		self.zyjjRewardDatas = ZyjjRewardData.ZyjjRewardDatas()

	def onEnter( self, playerRole, packArgs ):
		""""""
		SpaceCopy.onEnter( self, playerRole, packArgs )
		playerRole.onEnterCampFiveYCJMD()
		camp = playerRole.getFinalCamp()
		if camp == csdefine.CAMP_TAOSIM:
			campStr = cschannel_msgs.CAMP_TAOSIM
		else:
			campStr = cschannel_msgs.CAMP_DEMON
		self.memberDatas.add( playerRole, playerRole.id, playerRole.getName(), playerRole.camp, campStr, playerRole.getLevel() )


	def onLeave( self,  playerRole, packArgs ):
		""""""
		SpaceCopy.onLeave( self, playerRole, packArgs )
		self.memberDatas.leave( playerRole.id )
		#刷新存活人数
		self.showCampYCJMDPopulationUI()

	def onRoleBeKill( self, killEntity, dieEntity, amount ):
		"""
		玩家被击杀 掉落箱子
		"""
		self.hasBeKill = True

		#处理玩家被杀事情
		self.memberDatas.kill( dieEntity.id, killEntity.id )
		pos = Math.Vector3(dieEntity.position)
		pos.x += 3 # 随便偏移一段距离
		self.createSpellBox(self.getScript().getRewardSpellBoxID(), pos, (0.0, 0.0, 0.0), {})
		name = dieEntity.getName()
		campStr = ""
		if dieEntity.getCamp() == csdefine.CAMP_TAOSIM:
			campStr = cschannel_msgs.CAMP_TAOSIM
		else:
			campStr = cschannel_msgs.CAMP_DEMON
		for player in self._spaceRoles:
			player.statusMessage( csstatus.ROLE_LEAVE_TREASURE_BOX, campStr, name)
		
		if killEntity.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
			#击杀者获得经验奖励
			rate = self.getScript().getKillExpRate()
			exp = int(rate * RewardBasicValueData.datas.get(dieEntity.getLevel(), {}).get("exp", 0))
			killEntity.addExp(exp, csdefine.EXP_ADD_REASON_JMZC_KILL_ROLE)
			#击杀者获得功勋奖励
			feats = self.getScript().getKillFeats()
			killEntity.addFeatsRecord(feats, csdefine.FEATS_ADD_REASON_JMZC)
			#击杀者获得军功奖励
			exploits = self.getScript().getKillExploits()
			killEntity.addExploitRecord(exploits)
		

	def onRoleDead( self, dieEntity, amount ):
		"""
		玩家死亡 掉落箱子
		"""
		self.memberDatas.dead( dieEntity.id )
		self.addTimerCallBack( 5.0 , "weedOutPlayerCampYCJMD", ( dieEntity, ))
		dieEntity.statusMessage( csstatus.ROLE_DEAD_OUT, "" )
		
		#处理玩家掉落箱子事情
		roleItemList = dieEntity.getItemListByKBType( ItemTypeEnum.BAG_SPACE_COPY )
		if not len( roleItemList ):
			return
		if len( roleItemList ) < amount:
			amount = len(roleItemList)
		dropItems = random.sample( roleItemList, amount )
		tempItemDict = {}
		for dropItem in dropItems:
			tempItemDict[dropItem.id] = 1
		itemList = []
		for itemID, amount in tempItemDict.items():
			item = ItemFactory.ItemFactoryInst.createDynamicItem( itemID,amount,{} )
			itemList.append(item)
		for item in itemList:
			items = dieEntity.getItemInstsByID( item.id )
			if not len(items):
				continue
			dieEntity.removeItemByAmount( items[0], item.amount, csdefine.ITEM_REMOVE_BY_SPACE_EVENT )

		DBIDs = []
		for i in self._spaceRoles:
			DBIDs.append(i.playerDBID)
		dropBoxEntity = self.createEntityNear( "DropBox", dieEntity.position, Math.Vector3(0,0,0), {"modelNumber":"SM_DropBox", "modelScale":0.5,"allocationItems":{},"notAllocationItems":itemList,"ownershipIDs":DBIDs,"allocation": 1})
	
	def weedOutPlayerCampYCJMD(self, player):
		"""
		被淘汰玩家
		"""
		# 离开队伍
		if player.isInTeam():
			player.leaveTeamFC( player.id, player.id )

		# 退出副本
		player.reviveOnRturnPoint()

	def showCampYCJMDPopulationUI(self):
		"""
		显示双方阵营存活人数
		"""
		xAmount = 0
		mAmount = 0
		for i in self.memberDatas.values():
			if i["isLeave"]:
				continue
			if i["dead"] == 0 and i["camp"] == csdefine.CAMP_TAOSIM:
				xAmount += 1
			elif i["dead"] == 0 and i["camp"] == csdefine.CAMP_DEMON:
				mAmount += 1

		for player in self._spaceRoles:
			player.client.ShowCampYCJMDPopulationUI(xAmount, mAmount)

		winnerCamp = 0
		if xAmount==0:
			winnerCamp = csdefine.CAMP_DEMON
		elif mAmount == 0:
			winnerCamp = csdefine.CAMP_TAOSIM

		if not self.isEnd and self.hasBeKill and winnerCamp:
			self.isEnd = True
			#经验奖励
			self.addFinalExpReward(winnerCamp)
			#帮贡奖励
			self.addFinalContributionReward()
			#功勋奖励
			self.addFinalFeatsReward(winnerCamp)
			#军功奖励
			self.addFinalExploitReward(winnerCamp)
			#邮件奖励
			loserMailID = self.getScript().getLoserRewardMailID()
			winnerMailID = self.getScript().getWinnerRewardMailID()
			self.memberDatas.sendRewardMail(winnerCamp, loserMailID, winnerMailID)
			#出局者邮件奖励
			self.addOutMailReward(winnerCamp)

			#显示结算界面
			for player in self._spaceRoles:	
				if player.playerDBID in self.zyjjRewardDatas:
					player.client.ShowZYJJReward(self.zyjjRewardDatas.get(player.playerDBID))
				player.client.OnShowCampYCJMDCountdown(str(Functions.getTime()))
				#显示结算界面
				player.client.ShowYCJMDFinalUI()
			self.addTimerCallBack( 30.0 , "activityEnd", ())

	def activityStart( self ):
		"""
		活动开始
		"""
		pass

	def activityEnd( self ):
		"""
		活动结束
		""" 
		self.base.activityEnd()

#------------------------------------------------毒圈缩圈处理-------------------------------------------------------
	def setOriginCenterPos( self, originCenterPos ):
		"""
		设置起始中心点
		"""
		self.originCenterPos = originCenterPos

	def setOriginRadius( self, originRadius ):
		"""
		设置起始半径
		"""
		self.originRadius = originRadius

	def setEndCenterPos( self, endCenterPos ):
		"""
		设置终点圆心
		"""
		self.endCenterPos = endCenterPos

	def setEndRadius( self, endRadius ):
		"""
		设置终点半径
		"""
		self.endRadius = endRadius

	def getOriginCenterPos( self ):
		"""
		获得起始中心点
		"""
		return self.originCenterPos

	def getOriginRadius( self ):
		"""
		获得起始中心点圆的半径
		"""
		return self.originRadius

	def getEndCenterPos( self ):
		"""
		获得终点圆心
		"""
		return self.endCenterPos

	def getEndRadius( self ):
		"""
		获得终点圆的半径
		"""
		return self.endRadius

	def StartReduceYeZhanFengQiArea( self, totalUseTime ):
		"""
		开始缩小安全区域
		"""
		self.totalUseTime = totalUseTime
		self.startReduceTime = time.time()
		tickTime = 0.5
		totalTime = totalUseTime / tickTime
		centerVector = self.endCenterPos - self.originCenterPos
		#deltaVector = Math.Vector3( centerVector.x / totalTime, centerVector.y / totalTime, centerVector.z/totalTime )
		centerVector.normalise()

		centerLength = self.endCenterPos.flatDistTo( self.originCenterPos )
		centerSpeed = centerLength / totalTime #速度

		radiusLength = self.endRadius - self.originRadius
		radiusSpeed = radiusLength / totalTime

		self.reduceAreaTimer = self.addTimerRepeat( tickTime, "tickReduceYeZhanFengQiArea",( centerVector,centerSpeed,radiusSpeed) )
		self.addTimerCallBack( totalUseTime, "removeYeZhanFengQiAreaTimer",() )

	def tickReduceYeZhanFengQiArea( self,centerVector,centerSpeed,radiusSpeed ):
		"""
		"""
		self.originCenterPos = self.originCenterPos + centerVector * centerSpeed
		self.originRadius = self.originRadius + radiusSpeed

	def removeYeZhanFengQiAreaTimer( self ):
		"""
		清除缩毒timer
		"""
		self.startReduceTime = 0.0
		if self.reduceAreaTimer:
			self.popTimer( self.reduceAreaTimer )
			self.reduceAreaTimer = 0

	def checkPlayerIsInSaveArea( self, buffID ):
		"""
		检查玩家是否在安全区域里
		"""
		if self.checkAreaTimer:
			self.popTimer(self.checkAreaTimer)
		self.checkAreaTimer = self.addTimerRepeat(0.5, "tickCheckPlayerIsInSaveArea",(buffID,) )

	def tickCheckPlayerIsInSaveArea( self,buffID ):
		"""
		"""
		for player in self._spaceRoles:
			if player.position.flatDistTo( self.originCenterPos ) >  self.originRadius and not self.isEnd:
				if len(player.findBuffsByBuffID(buffID)):
					continue
				player.addBuff(player, buffID)
			else:
				player.removeBuffByID(buffID)


#------------------------------------------------随机事件 无所遁形-------------------------------------------------------
	def refreshCampYCJMDPostion(self, time, refreshTime):
		"""
		刷新敌对阵营玩家的位置
		"""
		self.showPosTimer = self.addTimerRepeat(refreshTime, "tickShowCampYCJMDPosition",() )
		self.endShowPosTimer = self.addTimerCallBack(time, "endTickShowCampYCJMDPosition",() )

	def tickShowCampYCJMDPosition(self):
		"""
		"""
		for player in self._spaceRoles:
			for i in self._spaceRoles:
				if player.camp != i.camp:
					player.client.showCampYCJMDPosition( i.id, KBEMath.KBEngine2UnrealPosition(i.position) )					

	def endTickShowCampYCJMDPosition(self):
		"""
		"""
		if self.showPosTimer:
			self.popTimer(self.showPosTimer)
			self.showPosTimer = 0
			
		for player in self._spaceRoles:
			player.client.HideCampYCJMDPosition()

	def tickShowSameCampYCJMDPosition(self):
		"""
		大地图显示同阵营位置
		"""
		for player in self._spaceRoles:
			for i in self._spaceRoles:
				if player.camp == i.camp:
					player.client.ShowSameCampYCJMDPos( i.id, KBEMath.KBEngine2UnrealPosition(i.position) )


#--------------------------------------------------随机出生点---------------------------------------------------------
	def setBirthInfos( self, birthInfos ):
		
		self.birthInfos.extend(birthInfos)
	
	def getBirthInfos( self ):
		"""
		获得出生点坐标
		"""
		infos = random.choice(self.birthInfos)
		self.birthInfos.remove( infos )
		return infos

#-------------------------阵营竞技结算奖励------------------------------------

	def addFinalContributionReward(self):
		#帮贡奖励 CST-13692
		#同一个帮会的成员分类
		tongDict = {}
		for player in self._spaceRoles:
			tongMB = player.tongMB
			if not tongMB:
				continue
			if tongMB.id not in tongDict:
				tongDict[tongMB.id] = []
			tongDict[tongMB.id].append(player)
		#同帮会成员人数达标后才可获得奖励
		for playerList in tongDict.values():
			amount = len(playerList)
			if amount in csconst.ZYJJ_REWARD_CONTRIBUTION:
				ctrbValue = csconst.ZYJJ_REWARD_CONTRIBUTION[amount]
				for player in playerList:
					player.addContribution(ctrbValue)
					self.zyjjRewardDatas.addContribution(player.playerDBID, ctrbValue)

	def addFinalExpReward(self, winnerCamp):
		"""
		副本结算经验奖励
		"""
		for player in self._spaceRoles:
			if player.getFinalCamp() == winnerCamp:
				value = self.getScript().getFinalExpDict(player.getLevel(), 1)
			else:
				value = self.getScript().getFinalExpDict(player.getLevel(), 0)
			if not value:
				continue
			player.addExp(value, csdefine.EXP_ADD_REASON_JMZC_FINAL_EXP)
			self.zyjjRewardDatas.addExp(player.playerDBID, value)


	def addFinalExploitReward(self, winnerCamp):
		"""
		副本结算军功奖励
		"""
		for player in self._spaceRoles:
			if player.getFinalCamp() == winnerCamp:
				value = self.getScript().getFinalWinExploits()
			else:
				value = self.getScript().getFinalLostExploits()
			if not value:
				continue
			player.addExploit(value)
			self.zyjjRewardDatas.addExploit(player.playerDBID, value)


	def addFinalFeatsReward(self, winnerCamp):
		"""
		副本结算功勋奖励
		"""
		for player in self._spaceRoles:
			if player.getFinalCamp() == winnerCamp:
				value = self.getScript().getFinalWinFeats()
			else:
				value = self.getScript().getFinalLostFeats()
			if not value:
				continue
			player.addFeats(value, csdefine.FEATS_ADD_REASON_JMZC)
			self.zyjjRewardDatas.addFeats(player.playerDBID, value)
			

	def addOutMailReward(self, winnerCamp):
		"""
		把数值奖励通过邮件发送给不在副本内的玩家
		"""
		for member in self.memberDatas.values():
			if member["isLeave"]:
				if member["camp"] == winnerCamp:
					mailID = self.getScript().getOutRewardMailID(member['level'], 1)
				else:
					mailID = self.getScript().getOutRewardMailID(member['level'], 0)
				g_mailContentDataLoader.sendSpaceReward(mailID, member["name"])
