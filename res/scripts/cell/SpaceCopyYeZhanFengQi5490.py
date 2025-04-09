# -*- coding: utf-8 -*-

import KBEDebug
from SpaceCopy import SpaceCopy
import csdefine
from YeZhanFengQiDataInfo5490 import g_yeZhanFengQiDataInfo
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

class SpaceCopyYeZhanFengQi5490( SpaceCopy ):
	"""
	血斗凤栖镇 JIRA CST-5490
	"""
	def __init__( self ) :
		SpaceCopy.__init__( self )
		self.memberDict = {}
		self.startReduceTime = 0.0
		self.kickOutMember = {}

	def getDynamicReviverInfo( self, camp = csdefine.CMAP_NONE ):
		"""
		<Define method>
		获取副本动态复活点
		"""
		random.shuffle(self.getScript().getRevivePosList())
		dstPos = None
		for revivePos in self.getScript().getRevivePosList():
			if Math.Vector3(revivePos).flatDistTo( self.originCenterPos ) < self.originRadius:
				dstPos = revivePos
				break
		if dstPos == None:
			time = 10
			pos = Math.Vector3(self.originCenterPos.x, self.originCenterPos.y + 50.0, self.originCenterPos.z)
			while dstPos == None and time > 0:
				time -= 1
				posList = KBEngine.collideVertical(self.spaceID, self.layer, pos, 100, -100)
				if len(posList):
					dstPos = posList[0]
				else:
					pos = csarithmetic.getPositionByCircular( pos, self.originRadius )
		return dstPos,Math.Vector3(0,0,0)

	
	def addYeZhanFengQiMember( self, player, initIntegral ):
		"""
		增加血斗凤栖镇的成员
		"""
		memberInfo = self.findYeZhanFengQiMemeberByPlayerDBID(player.playerDBID)
		if memberInfo != None:
			member = self.memberDict.pop(memberInfo.roleID)
			scrMemberID = member.roleID
			member.roleID = player.id
			member.roleMB = player
			member.isLogoOut = False
			member.logoOutPos = Math.Vector3(0,0,0)
			self.memberDict[player.id] = member
			self.updateMemberDataToOtherMemberOnLogin( scrMemberID, member.roleID )
			self.updateYeZhanFengQiMemberNumber()
			self.receiveYeZhanFengQiMemberData( player )
			self.updateYeZhanFengQiIntegralToOtherClient( player )
			self.updateYeZhanFengQiKillDataToOtherClient( player )
			return
		if player.id not in self.memberDict:
			tempDict = { "roleID":player.id,"roleMB":player,"roleName":player.getName(),"kill":0,"integral":initIntegral,"killNum":0,"roleDBID":player.playerDBID,"isLogoOut":False,"logoOutPos":Math.Vector3(0,0,0),"logoOutItemList":[],"isDead":False }
			yeZhanFengQiData = g_yeZhanFengQiDataInfo.createObjFromDict(tempDict)
			self.memberDict[player.id] = yeZhanFengQiData
			self.updateYeZhanFengQiMemberNumber()
			self.updateYeZhanFengQiMyKillNumber(player)
			self.updateYeZhanFengQiMemberDataToOtherClient( player )
			self.receiveYeZhanFengQiMemberData( player )
			self.updateYeZhanFengQiIntegralToOtherClient(player)
			self.updateYeZhanFengQiKillDataToOtherClient( player )

	def findYeZhanFengQiMemeberByPlayerDBID( self, playerDBID ):
		"""
		找血斗凤栖镇成员
		"""
		tempMemberInfo = None
		for memberInfo in self.memberDict.values():
			if memberInfo.roleDBID == playerDBID:
				tempMemberInfo = memberInfo
				break
		return tempMemberInfo

	def reduceYeZhanFengQiMember( self, player ):
		"""
		减少血斗凤栖镇的成员
		"""
		if player.id in self.memberDict:
			memberData = self.memberDict.pop(player.id)
			self.updateYeZhanFengQiMemberNumber()
			#self.checkYeZhanFengQiMemberNum()
			for memberInfo in self.memberDict.values():
				if memberInfo.roleMB and memberInfo.roleMB.getClient():
					memberInfo.roleMB.client.CLIENT_FengQiMemberLeave(player.id)
			if player.id not in self.kickOutMember:
				self.kickOutMember[player.id] = memberData
	
	def updateYeZhanFengQiMemberNumber( self ):
		"""
		更新血斗凤栖镇的参与人员数
		"""
		for memberInfo in self.memberDict.values():
			if memberInfo.roleMB and memberInfo.roleMB.getClient():
				memberInfo.roleMB.client.CLIENT_UpdateYeZhanFengQiMemberNumber( len(self.memberDict) )

	def updateYeZhanFengQiMyKillNumber( self, player ):
		"""
		更新自己击杀数
		"""
		if player.id in self.memberDict:
			killNum = self.memberDict[player.id].kill
			if player.getClient():
				player.client.CLIENT_UpdateYeZhanFengQiMyKillNumber( killNum )

	def updateYeZhanFengQiMemberDataToOtherClient( self, player ):
		"""
		更新自己成员数据到其他客户端
		"""
		if player.id not in self.memberDict:
			return
		playerInfo = self.memberDict[player.id]
		for memberInfo in self.memberDict.values():
			if memberInfo.roleMB and memberInfo.roleMB.getClient():
				memberInfo.roleMB.client.CLIENT_UpdateFengQiMemberDataToOtherClient( playerInfo.roleID, playerInfo.integral,playerInfo.roleName,playerInfo.roleMB.getProfession(),playerInfo.kill )

	def receiveYeZhanFengQiMemberData( self, player ):
		"""
		接收其他玩家的成员数据
		"""
		if player.id not in self.memberDict:
			return
		for memberInfo in self.memberDict.values():
			if player.getClient():
				player.client.CLIENT_ReceiveFengQiOtherMemberData( memberInfo.roleID,memberInfo.integral,memberInfo.roleName,memberInfo.roleMB.getProfession(),memberInfo.kill )

	def updateYeZhanFengQiIntegralToOtherClient( self, player ):
		"""
		更新积分数据到客户端(包括自己)
		"""
		if player.id not in self.memberDict:
			return
		playerInfo = self.memberDict[player.id]
		for memberInfo in self.memberDict.values():
			if memberInfo.roleMB and memberInfo.roleMB.getClient():
				memberInfo.roleMB.client.CLIENT_UpdateFengQiIntegralToOtherClient( playerInfo.roleID,playerInfo.integral )

	def updateYeZhanFengQiKillDataToOtherClient( self, player ):
		"""
		更新其他玩家击杀的数据到客户端( 包括自己 )
		"""
		if player.id not in self.memberDict:
			return
		playerInfo = self.memberDict[player.id]
		for memberInfo in self.memberDict.values():
			if memberInfo.roleMB and memberInfo.roleMB.getClient():
				memberInfo.roleMB.client.UpdateFengQiKillDataToOtherClient( playerInfo.roleID,playerInfo.kill )

	def updateMemberDataToOtherMemberOnLogin( self, srcMemberID, dstMemberID ):
		"""
		"""
		for memberInfo in self.memberDict.values():
			if memberInfo.roleMB and memberInfo.roleID != dstMemberID and memberInfo.roleMB.getClient():
				memberInfo.roleMB.client.CLIENT_UpdateFengQiMemberDataToOtherOnLogin( srcMemberID, dstMemberID )

	def yeZhanFengQiMemberLogOut( self, player ):
		"""
		某成员掉线
		"""
		if player.id in self.memberDict:
			self.memberDict[player.id].isLogoOut = 1
			self.memberDict[player.id].logoOutPos = Math.Vector3(player.position)
			spaceCopyItemList = player.getItemListByKBType(ItemTypeEnum.BAG_SPACE_COPY)
			tempArray = []
			for itemInst in spaceCopyItemList:
				tempArray.append( itemInst.getDictFromObj() )
			self.memberDict[player.id].logoOutItemList = tempArray

	def addPlayerIntegral( self, roleMB, integral ):
		"""
		增加积分
		"""
		if roleMB.id not in self.memberDict:
			return
		self.memberDict[roleMB.id].integral += integral
		self.updateYeZhanFengQiIntegralToOtherClient(roleMB)

	def reducePlayerIntegral( self, roleMB, integral ):
		"""
		减少积分
		"""
		if roleMB.id not in self.memberDict:
			return
		self.memberDict[roleMB.id].integral -= integral
		self.updateYeZhanFengQiIntegralToOtherClient(roleMB)
		if self.memberDict[roleMB.id].integral == 0:
			roleMB.fengQiMemberOut()
		else:
			roleMB.addTimerCallBack(10.0,"reviveOnSpaceCopy",())

	def getMemberKill( self, player ):
		"""
		获得成员击杀数
		"""
		if player.id in self.memberDict:
			return self.memberDict[player.id].kill
		return 0

	def getMemberIntegral( self, player ):
		"""
		获得成员的积分
		"""
		if player.id in self.memberDict:
			return self.memberDict[player.id].integral
		return None

	def addYeZhanFengQiMemberKillNum( self, player, diePlayer ):
		"""
		增加某成员的击杀数
		"""
		if player.id in self.memberDict and diePlayer.id in self.memberDict:
			dieMemberInfo = self.memberDict[diePlayer.id]
			killMemberInfo = self.memberDict[player.id]
			if player.id != diePlayer.id:
				killMemberInfo.kill += 1
				killMemberInfo.killNum += 1
				self.updateYeZhanFengQiMyKillNumber(player)
				self.updateYeZhanFengQiKillDataToOtherClient(player)
			# rank = self.getYeZhanFengQiMemberRankByMemNum()
			# if rank:
			# 	self.addTimerCallBack(4.0,"showYeZhanFengQiMemberRank",( diePlayer, rank,dieMemberInfo.kill )) #这里加四秒延迟  是由于客户端播完死亡动作后会弹出复活框会将改提示框覆盖掉
			if player.id != diePlayer.id:
				self.checkFirstKill( killMemberInfo )
				self.checkKillNum( killMemberInfo )
				self.checkKillGodPlayer( killMemberInfo, dieMemberInfo )
			dieMemberInfo.killNum = 0
			# self.reduceYeZhanFengQiMember(diePlayer)
			# offsetTime = time.time() - self.lifeStartTime
			# if offsetTime > 180.0 and len( self.memberDict ) <= 15 and player.id != diePlayer.id: #3分钟之后，剩余15个人，没击杀一个，提示一次 “XX玩家被YY玩家一招毙命淘汰出局”
			# 	for m in self.memberDict.values():
			# 		m.roleMB.statusMessage( csstatus.YE_ZHAN_FENG_QI_MEMBER_BE_KILL, dieMemberInfo.roleName,killMemberInfo.roleName)
			# self.checkYeZhanFengQiMemberNum()
			# self.yeZhanFengQiDropBox( dieMemberInfo, diePlayer.position )

	def checkYeZhanFengQiMemberNum( self ):
		"""
		检查下副本人数
		"""
		if len(self.memberDict) == 1:
			self.golbalYeZhanFengQiChampion( list(self.memberDict.values())[0] )
			# rank = self.getYeZhanFengQiMemberRankByMemNum()
			# self.showYeZhanFengQiMemberRank(list(self.memberDict.values())[0].roleMB,rank,list(self.memberDict.values())[0].kill)

	def golbalYeZhanFengQiChampion(self, memberInfo ):
		"""
		全局广播血斗凤栖镇冠军
		"""
		KBEngine.globalData["PersonStarcraftMgr"].sendWoldMsg( csstatus.ZHIZUNZHENBA_THE_FIRST,memberInfo.roleName)
		if self.checkAreaTimer:
			self.popTimer( self.checkAreaTimer )
			self.checkAreaTimer = 0
		self.addTimerCallBack(30.0,"closeSpace",())

	def checkFirstKill( self, memberInfo ):
		"""
		检查是否为首杀
		"""
		isFirstKill = True
		if memberInfo.kill == 1:
			for m in self.memberDict.values():
				if memberInfo.roleID != m.roleID and m.kill != 0:
					isFirstKill = False
		else:
			isFirstKill = False
		if isFirstKill:
			for m in self.memberDict.values():
				if m.roleMB and m.roleMB.getClient():
					m.roleMB.client.CLIENT_OnFirstKill( memberInfo.roleName )

	def checkKillNum( self, memberInfo ):
		"""
		检查是否连续击杀次数
		"""
		num = memberInfo.killNum
		if num < 10:
			return
		for m in self.memberDict.values():
			if m.roleMB and m.roleMB.getClient():
				m.roleMB.client.CLIENT_OnGodLike( memberInfo.roleName )

	def checkKillGodPlayer( self, killMemberInfo, dieMemberInfo ):
		"""
		检查是否击杀超神玩家
		"""
		if dieMemberInfo.killNum >= 10:
			for m in self.memberDict.values():
				if m.roleMB and m.roleMB.getClient():
					m.roleMB.client.CLIENT_OnEndLegendary( killMemberInfo.roleName )
	
	def getYeZhanFengQiMemberRankByMemNum( self ):
		"""
		通过人数获得成员排名
		"""
		return len(self.memberDict)

	def getYeZhanFengQiMemberRankByKill( self, player ):
		"""
		通过击杀数获得成员排名
		"""
		rank = 0
		if player.id in self.memberDict:
			memberInfo = self.memberDict[player.id]
			memberInfos = self.memberDict.values()
			memberInfos = sorted( memberInfos ,key = lambda m : m.kill, reverse = True )
			memberIDs = [member.roleID for member in memberInfos]
			rank = memberIDs.index( player.id ) + 1
		return rank

	def showYeZhanFengQiMemberRank( self, player,rank,kill ):
		"""
		显示成员的排名
		"""
		player.addTimerCallBack(10.0,"CELL_leaveYeZhanFengQi",(player.id,))
		if player.getClient():
			player.client.CLIENT_ShowYeZhanFengQiMemberRank( rank, kill )

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
		获得起始中心点
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
		self.checkAreaTimer = self.addTimerRepeat(0.1, "tickCheckPlayerIsInSaveArea",(buffID,) )

	def getAllMemberDBID( self ):
		"""
		获得所有成员列表
		"""
		temp = []
		for member in self.memberDict.values():
			temp.append( member.roleDBID )
		return temp

	def getMemberInfoByID( self, playerID ):
		"""
		"""
		if playerID in self.memberDict:
			return self.memberDict[playerID]
		return None

	def tickCheckPlayerIsInSaveArea( self,buffID ):
		"""
		"""
		needToRemoveRoleIDs = []		
		for member in self.memberDict.values():
			if member.isLogoOut:
				if not member.isDead:
					dis = member.logoOutPos.flatDistTo( self.originCenterPos )
					if dis > self.originRadius:
						self.yeZhanFengQiDropBox( member, member.logoOutPos )
						needToRemoveRoleIDs.append(member.roleID)
			else:		
				dis = member.roleMB.position.flatDistTo( self.originCenterPos )
				if dis > self.originRadius:
					if len(member.roleMB.findBuffsByBuffID(buffID)) > 0:
						continue
					member.roleMB.addBuff(member.roleMB,buffID)
				else:
					member.roleMB.removeBuffByID(buffID)
		# for needToRemoveRoleID in needToRemoveRoleIDs:
		# 	self.memberDict.pop(needToRemoveRoleID)
		# if len(needToRemoveRoleIDs):
		# 	self.updateYeZhanFengQiMemberNumber()
			#self.checkYeZhanFengQiMemberNum()

	def yeZhanFengQiDropBox( self, memberInfo, position ):
		"""
		玩家死亡 掉落箱子
		"""
		itemList = []
		if memberInfo.isLogoOut:
			memberInfo.isDead = True
			self.yeZhanFengQiKickOutMember( memberInfo.roleDBID )
			for itemDict in memberInfo.logoOutItemList:
				id = itemDict["id"]
				amount = itemDict["amount"]
				item = ItemFactory.ItemFactoryInst.createDynamicItem( id,amount,itemDict )
				itemList.append(item)
		else:
			spaceCopyItemList = memberInfo.roleMB.getItemListByKBType(ItemTypeEnum.BAG_SPACE_COPY)
			dropItem = random.sample(spaceCopyItemList,math.ceil(len(spaceCopyItemList) / 2))
			for item in dropItem:
				id = item.id
				amount = item.amount
				item = ItemFactory.ItemFactoryInst.createDynamicItem( id,amount,item.getDictFromObj() )
				itemList.append(item)
			for item in itemList:
				items = memberInfo.roleMB.getItemInstsByID( item.id )
				for needDelItem in items:
					memberInfo.roleMB.removeItemByAmount( needDelItem, needDelItem.amount, csdefine.ITEM_REMOVE_BY_SPACE_EVENT )
		if not len(itemList):
			return
		memberList = self.getAllMemberDBID()
		# if memberInfo.roleDBID in memberList:
		# 	memberList.remove(memberInfo.roleDBID)
		dropBoxEntity = self.createEntityNear( "DropBox",position,Math.Vector3(0,0,0),{"modelNumber":"SM_DropBox", "modelScale":1.0,"allocationItems":{},"notAllocationItems":itemList,"ownershipIDs":memberList,"allocation": 1})

	def yeZhanFengQiKickOutMember( self, playerDBID ):
		"""
		玩家淘汰
		"""
		KBEngine.globalData["PersonStarcraftMgr"].yeZhanFengQiKickOutMember( playerDBID )
			
	def isMemberKickOut( self, player ):
		"""
		玩家是否被淘汰
		"""
		memberInfo = self.findYeZhanFengQiMemeberByPlayerDBID(player.playerDBID)
		if memberInfo != None:
			if memberInfo.isDead:
				return True
		return False

	def checkSpaceRoleNumber( self ):
		"""
		3分钟之后检查一下副本人数 只剩一名玩家时决出第一名
		"""
		if len(self.memberDict) == 1:
			memberInfos = list(self.memberDict.values())
			# firstPlayerMB = memberInfos[0].roleMB
			# rank = self.getYeZhanFengQiMemberRankByKill( firstPlayerMB )
			# self.showYeZhanFengQiMemberRank(firstPlayerMB,rank, memberInfos[0].kill )
			self.golbalYeZhanFengQiChampion( memberInfos[0] )

