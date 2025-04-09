# -*- coding: utf-8 -*-



import KBEDebug
import csdefine
import csstatus
import ItemFactory
import time

class RoleGiftInterface:
	"""
	礼包奖励
	"""
	def __init__( self ):
		pass
		
	def onReceiveNewPlayerGift( self, giftStr, bindType ):
		"""
		define method
		获取新手在线奖励
		"""
		if self._addGiftStr( [giftStr], [bindType], csdefine.ITEM_ADD_BY_NEW_PLAYER_GIFT):
			self.base.onReceiveNewPlayerGiftSuccess()

	def onSignInOnline( self, giftStr, bindType ):
		"""
		define method
		获取签到奖励
		"""
		if self._addGiftStr( [giftStr], [bindType], csdefine.ITEM_ADD_BY_SIGN_IN_GIFT):
			self.base.onSignInOnlineSuccess()
			
	def onAugmentSignIn( self, giftStr, bindType, key, day ):
		"""
		define method
		补签奖励
		"""
		if self._addGiftStr( [giftStr], [bindType], csdefine.ITEM_ADD_BY_SIGN_IN_GIFT):
			self.base.onAugmentSignInSuccess( key, day )
		
	def onAugmentSignInMonth( self, giftStrList, bindTypeList, key ):
		"""
		define method
		补签一个月奖励
		"""
		if self._addGiftStr( giftStr, csdefine.ITEM_ADD_BY_SIGN_IN_GIFT):
			self.base.onAugmentSignInMonthSuccess( key )
			
	def onReceiveTotalSignReward( self, giftStr, bindType, accumulateNum ):
		"""
		define method
		领取 累计签到奖励
		"""
		if self._addGiftStr( [giftStr], [bindType], csdefine.ITEM_ADD_BY_SIGN_IN_GIFT):
			self.base.onReceiveTotalSignRewardSuccess( accumulateNum )
		
	def _addGiftStr( self, giftStrList, bindTypeList, reason ):
		""""""
		if len(giftStrList) != len(bindTypeList):
			KBEDebug.ERROR_MSG("add gift error")
			return False

		itemInstList = []
		for index, giftStr in enumerate(giftStrList):
			bindType = bindTypeList[index]
			giftList = giftStr.split(";")

			for giftS in giftList:
				if not giftS: continue
				itemList = giftS.split(":")
				itemID = int( itemList[0] )
				amount = 1
				if len(itemList) > 1:
					amount = int( itemList[1] )
				itemInst = ItemFactory.ItemFactoryInst.createDynamicItem(itemID, amount, {})
				if itemInst is None:return False
				if bindType: itemInst.setBindType(None)	#设置绑定
				itemInstList.append( itemInst )
		
		result = self.addItemList( itemInstList, reason )
		if result != csstatus.ITEM_GO_ON:
			self.statusMessage(result,"")
			return False
		return True

	def onNewDayLogin( self ):
		"""玩家在新的一天登录, 更新在线礼包数据"""
		self.base.onNewDayLoginSuccess()