# -*- coding: utf-8 -*-

import KBEDebug
from Singleton import Singleton
import ItemFactory
from ConfigObject.Reward.ActivityRewardMgr import g_activityRewardMgr
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
	
		self.sendMail(mailID, playerName)

	def sendMail(self, mailID, playerName, extraData = {}):
		"""
		"""
		if not self.isMailIDInMailData( mailID ):
			KBEDebug.ERROR_MSG("MailID = %s is not in MailContentData.json"%mailID)
			return

		extraMoney = extraData.get("money", 0)
		extraItems = extraData.get("itemList", [])
		
		senderName = self.getMailDataSenderNameByMailID(mailID)
		title = self.getMailDataTitleByMailID(mailID)
		content = self.getMailDataContentByMailID(mailID)
		money = self.getMailDataMoneyByMailID(mailID) + extraMoney
		itemDatas = self.getMailDataItemDatasByMailID(mailID)
		itemDatas.extend(extraItems)
		lingshi = self.getMailDataLingShiByMailID(mailID)
		xianshi = self.getMailDataxianShiByMailID(mailID)
		KBEngine.globalData["MailManager"].send( None, playerName,csdefine.MAIL_SENDER_TYPE_SYS,senderName,title,content,money, 0, itemDatas, lingshi, xianshi )
		
	def sendMailByContentArgs( self, mailID, playerName, arg = (), extraData = {}):
		"""
		发送内容带有参数的邮件
		"""
		if not self.isMailIDInMailData( mailID ):
			KBEDebug.ERROR_MSG("MailID = %s is not in MailContentData.json"%mailID)
			return
		extraMoney = extraData.get("money", 0)
		extraItems = extraData.get("itemList", [])
		
		senderName = self.getMailDataSenderNameByMailID(mailID)
		title = self.getMailDataTitleByMailID(mailID)
		content = self.getMailDataContentByMailID(mailID).format( *arg )
		money = self.getMailDataMoneyByMailID(mailID) + extraMoney
		itemDatas = self.getMailDataItemDatasByMailID(mailID)
		itemDatas.extend(extraItems)
		lingshi = self.getMailDataLingShiByMailID(mailID)
		xianshi = self.getMailDataxianShiByMailID(mailID)
		KBEngine.globalData["MailManager"].send( None, playerName,csdefine.MAIL_SENDER_TYPE_SYS,senderName,title,content,money, 0, itemDatas, lingshi, xianshi )

g_mailContentDataLoader = MailContentDataLoader()