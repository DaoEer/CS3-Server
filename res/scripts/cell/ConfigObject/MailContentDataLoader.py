# -*- coding: utf-8 -*-

import KBEDebug
from Singleton import Singleton
import ItemFactory
from ConfigObject.ActivityReward.ActivityRewardMgr import g_activityRewardMgr
import KBEngine
import csdefine

class MailContentDataLoader( Singleton ):
	"""
	邮件内容数据类
	"""
	def __init__( self ):
		Singleton.__init__( self )
		self.mailDatas = {}

	def init( self, mailConfigDatas ):
		"""
		读取配置
		"""
		self.mailDatas.clear()
		for mailID, mailData in mailConfigDatas.items():
			self.mailDatas[mailID] = mailData

	def isMailIDInMailData( self, mailID ):
		"""
		mailID 是否在邮件数据内中
		"""
		if mailID in self.mailDatas.keys():
			return True

		return False

	def getMailDataSenderNameByMailID( self, mailID ):
		"""
		获得发送者的名字
		"""
		if mailID in self.mailDatas:
			return self.mailDatas[mailID]["senderName"]
		return ""

	def getMailDataTitleByMailID( self, mailID ):
		"""
		获得邮件的标题
		"""
		if mailID in self.mailDatas:
			return self.mailDatas[mailID]["title"]
		return ""

	def getMailDataContentByMailID( self, mailID ):
		"""
		获得邮件内容
		"""
		if mailID in self.mailDatas:
			return self.mailDatas[mailID]["content"]
		return ""

	def getMailDataMoneyByMailID( self, mailID ):
		"""
		获得邮件的金币
		"""
		if mailID in self.mailDatas:
			return self.mailDatas[mailID]["money"]
		return ""

	def getMailDataItemDatasByMailID( self, mailID ):
		"""
		获得邮件的物品数据
		"""
		if mailID not in self.mailDatas:
			return []
		
		bindType = int(self.mailDatas[mailID].get("bindType", 0))
		return self._getItemDatasByItemIDs(self.mailDatas[mailID]["itemIDs"], bindType)
		
	def _getItemDatasByItemIDs( self, itemsIDs, bindType ):
		"""
		"""
		tempItemDatas = []
		itemIDs = [itemID for itemID in itemsIDs.split("|")]
		for itemID in itemIDs:
			if not itemID: continue
			itemID = int(itemID)
			itemInst = ItemFactory.ItemFactoryInst.createDynamicItem(itemID, 1, {})
			if not itemInst:
				KBEDebug.ERROR_MSG("MailContentData.json has not item=%i"%(itemID))
				continue
			
			if bindType: itemInst.setBindType(None)
			tempItemDatas.append(itemInst)
		return tempItemDatas

	def getMailDataLingShiByMailID( self, mailID ):
		"""
		获得邮件的灵石
		"""
		if mailID in self.mailDatas:
			return self.mailDatas[mailID]["lingshi"]
		return 0

	def getMailDataxianShiByMailID( self, mailID ):
		"""
		获得邮件的灵石
		"""
		if mailID in self.mailDatas:
			return self.mailDatas[mailID]["xianshi"]
		return 0

	def sendActivityReward( self, spaceScriptID, rank, playerName ):
		"""
		发送活动奖励
		"""
		mailID = g_activityRewardMgr.getRewardMailIDByRank( spaceScriptID, rank )
		if mailID == "":
			return
	
		self._sendMail(mailID, playerName)

	def _sendMail(self, mailID, playerName):
		"""
		"""
		if not self.isMailIDInMailData( mailID ):
			KBEDebug.ERROR_MSG("MailID = %s is not in MailContentData.json"%mailID)
			return
		
		senderName = self.getMailDataSenderNameByMailID(mailID)
		title = self.getMailDataTitleByMailID(mailID)
		content = self.getMailDataContentByMailID(mailID)
		money = self.getMailDataMoneyByMailID(mailID)
		itemDatas = self.getMailDataItemDatasByMailID(mailID)
		lingshi = self.getMailDataLingShiByMailID(mailID)
		xianshi = self.getMailDataxianShiByMailID(mailID)
		bindMoney = 0
		KBEngine.globalData["MailManager"].send( None, playerName,csdefine.MAIL_SENDER_TYPE_SYS,senderName,title,content,money, bindMoney,itemDatas, lingshi, xianshi )
		
	def sendSpaceReward( self, mailID, playerName ):
		"""
		发送副本奖励邮件
		"""
		self._sendMail(mailID, playerName)
	
g_mailContentDataLoader = MailContentDataLoader()