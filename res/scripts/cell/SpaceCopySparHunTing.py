# -*- coding: utf-8 -*-

import random
import KBEDebug
from SpaceCopy import SpaceCopy
import Math
import KBEngine
import csdefine
import csstatus
import Const

class SpaceCopySparHunTing( SpaceCopy ):
	"""
	晶石狩猎场副本
	"""
	def __init__( self ) :
		SpaceCopy.__init__( self )
		
		#记录从当前副本进入其他副本的玩家
		self.luckySpaceRoles = {}

	def activeStart( self ):
		"""
		活动开始 触发条件改变
		"""
		self.getScript().activeStart(self)

	def activeEnd( self ):
		"""
		活动结束
		"""
		allMembers = self.memberDatas.getAllMembers()
		for member in allMembers:
			if member.roleMB:
				if member.roleMB not in self.luckySpaceRoles:
					self.playerExchangeToMoney(member.roleMB)
		nameList = self.memberDatas.getThreeTopMemberNamesByMoney()
		tempStr = ""
		length = ""
		if len(nameList) == 3:
			tempStr = nameList[0] + "、" + nameList[1] + "、" + nameList[2]
			length = Const.SPAR_HUNTING_MONEY_RANK_THIRD
		if len(nameList) == 2:
			tempStr = nameList[0] + "、" + nameList[1]
			length = Const.SPAR_HUNTING_MONEY_RANK_SECOND
		if len(nameList) == 1:
			tempStr = nameList[0]
			length = Const.SPAR_HUNTING_MONEY_RANK_FIRST
		msg = tempStr + "|" + length
		for member in allMembers:
			if member.roleMB:
				member.roleMB.client.CLIENT_ShowRankList()
				member.roleMB.statusMessage( csstatus.SPARHUNTING_ACTIVITY_END, msg )
		
		self.addTimerCallBack(10,"clearData",()) #通知客户端清除数据
		self.addTimerCallBack(10,"closeSpace",()) #跟策划商议暂停10秒关闭副本

	def addSparHunTingMemberData( self, roleMB ):
		"""
		增加副本玩家数据
		"""
		self.memberDatas.add( roleMB )

	def removeSparHunTingMemberData( self, roleMB ):
		"""
		减少副本玩家数据
		"""
		#如果是进入机缘副本，不要移除相关的数据
		flag = roleMB.playerDBID not in self.luckySpaceRoles
		self.memberDatas.remove( roleMB, flag )

	def setIntegralMax( self, integralMax ):
		"""
		设置积分上限
		"""
		self.integralMax = integralMax
		for m in self.memberDatas.getAllMembers():
			if m.roleMB:
				m.roleMB.client.CLIENT_SetIntegralMax( self.integralMax )

	def setExchMoneyScale( self, exchScale ):
		"""
		设置兑换比例
		"""
		self.exchMoneyScale = exchScale
		
	def setIntegralOverflowBuffID(self, buffID):
		"""
		设置金精溢出是玩家身上添加的BuffID
		"""
		self.buffID = buffID

	def addSparHunTingMoney( self, roleMB, money ):
		"""
		金钱增加
		"""
		self.memberDatas.addMoney( roleMB.id,money )

	def addPlayerIntegral( self, roleMB, integral, isCanOverFlow = False ):
		"""
		增加玩家积分(可能需要根据玩家身上加成buff去计算积分)
		"""
		if not isCanOverFlow:
			playerIntegral = self.memberDatas.getIntegral( roleMB.id )
			if playerIntegral >= self.integralMax:
				roleMB.statusMessage( csstatus.SPARHUNTING_INTEGRAL_MAX,"" )
				return
		roleMB.addPlayerIntegral( integral, isCanOverFlow )

	def onAddPlayerIntegral( self, roleMB, integral, isCanOverFlow = False ):
		"""
		添加玩家积分
		"""
		playerIntegral = self.memberDatas.getIntegral( roleMB.id )
		if playerIntegral + integral > self.integralMax:
			roleMB.addBuff(roleMB, self.buffID)
			if not isCanOverFlow:
				integral = self.integralMax - playerIntegral
		#	roleMB.statusMessage( csstatus.SPARHUNTING_INTEGRAL_MAX,"" )
		self.memberDatas.addIntegral( roleMB.id,integral )
		roleMB.addSparHunTingTotalIntegral(integral)
		
	
	def reducePlayerIntegral( self, roleMB, integral ):
		"""
		减少玩家积分(直接减少)
		"""
		playerIntegral = self.memberDatas.getIntegral( roleMB.id )
		if playerIntegral - integral < 0:
			integral = playerIntegral
		self.memberDatas.decIntegral( roleMB.id, integral )
		roleMB.reduceSparHunTingTotalIntegral(integral)
		
		if playerIntegral - integral <= self.integralMax:
			roleMB.removeBuffByID(self.buffID)

	def playerExchangeToMoney( self,roleMB ):
		"""
		玩家积分兑换成金钱
		"""
		playerIntegral = self.memberDatas.getIntegral(roleMB.id)
		if playerIntegral > 0:
			roleMB.playerExchangeToMoney(self.exchMoneyScale, playerIntegral)
		
	def onPlayerExchangeToMoney(self, roleMB, playerIntegral, money):
		self.reducePlayerIntegral( roleMB, playerIntegral)
		self.addSparHunTingMoney( roleMB, money )

	def addCampMoney( self, camp, money ):
		"""
		阵营增加金钱
		"""
		members = self.memberDatas.getCampMembers( camp )
		for m in members:
			if m.roleMB:
				self.addSparHunTingMoney( m.roleMB, money )

	def campTotalMoney( self, camp, money ):
		"""
		阵营总共增加的金钱
		"""
		members = self.memberDatas.getCampMembers( camp )
		for m in members:
			if m.roleMB:
				m.roleMB.statusMessage( csstatus.SPARHUNTING_TOTAL_REWARD_MONEY,money )

	def clearData( self ):
		"""
		通知客户端清除数据
		"""
		allMembers = self.memberDatas.getAllMembers()
		for member in allMembers:
			if member.roleMB:
				member.roleMB.client.CLIENT_OnClearData()