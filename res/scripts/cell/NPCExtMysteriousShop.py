# -*- coding: utf-8 -*-
#
import random
import KBEngine
import KBEDebug
import NPC
import Const
import csdefine
import csstatus
import Functions
import KST
from ConfigObject.Trade.TradeMgr import g_tradeMgr

class NPCExtMysteriousShop(NPC.NPC):
	"""
	神秘商人
	"""
	def __init__(self):
		NPC.NPC.__init__( self )
		
		self.shopItems = {}
		self.initShopData()
		self.addTimerDestroyShop()
		
	def initShopData(self):
		"""
		"""
		datas = g_tradeMgr.getMysteriousMerchantConfig()
		for slotID in list(datas.keys()):
			_probability = 0
			probability = random.uniform(0, 100)
			slotDatas = datas[slotID]	
			for k,v in slotDatas.items():
				_probability += v["probability"]
				if _probability >= probability:
					self.shopItems[slotID] = [v["id"], v["buyLimit"]]
					break
					
	def addTimerDestroyShop(self):
		"""
		"""
		self.destroyTimeID = 0
		lifeTime = self.getScript().lifeTime
		if lifeTime: 
			self.destroyTimeID = self.addTimerCallBack(lifeTime, "onDestroyShop", ())
		
	def onDestroyShop(self):
		"""
		"""
		self.destroyTimeID = 0
		spaceEntity = self.getCurrentSpace()
		spaceEntity.globalWorld(csstatus.MYSTERIOUS_SHOP_TIMES_UP, "")
		if spaceEntity:
			for role in spaceEntity._spaceRoles:
				if role.playerDBID == self.ownerDBID:
					pass
		self._onDestroyShop()
			
	def _onDestroyShop(self):
		if self.destroyTimeID:
			self.popTimer(self.destroyTimeID)
		self.destroy()
		
	def isValidatePlayer(self, player):
		"""
		"""
		if player and player.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ):
			if player.playerDBID == self.ownerDBID:
				return True
		return False
		
	def requestShopData(self, srcEntityID):
		"""
		Exposed method
		请求获取商店数据
		"""
		if srcEntityID == self.id:
			return
		
		player = KBEngine.entities.get(srcEntityID)
		if not self.isValidatePlayer(player):
			return
		
		params = []
		for k,v in self.shopItems.items():
			dct = {"slotID" : k, "id" : v[0], "amount" : v[1]}
			params.append(dct)
		
		player.clientEntity(self.id).recvMysteriousShopData(params)
		
	def requestBuyShopItem(self, srcEntityID, slotID, amount):
		"""
		Exposed method
		请求购买商店物品
		"""
		if srcEntityID == self.id:
			return
			
		player = KBEngine.entities.get(srcEntityID)
		if not self.isValidatePlayer(player):
			return
		
		if slotID not in self.shopItems:
			return
		
		if self.shopItems[slotID][1] < amount:
			player.statusMessage(csstatus.NPCSHOP_SHOP_AMOUNT_ERROR)
			return
		
		player.requestBuyMysteriousShopItem(self.id, slotID, self.shopItems[slotID][0], amount)
		
	def onSuccessBuyShopItem(self, srcEntityID, slotID, amount):
		"""
		"""
		if slotID not in self.shopItems:
			return
		
		self.shopItems[slotID][1] -= amount
		player = KBEngine.entities.get(srcEntityID)
		if player and player.getClient():
			player.clientEntity(self.id).OnSuccessBuyShopItem( slotID, amount )
		
		#判断一下是否已经全部出售完毕
		for k,v in self.shopItems.items():
			if v[1] > 0:
				return
		
		self._onDestroyShop()
		