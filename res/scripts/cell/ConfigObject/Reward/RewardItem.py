# -*- coding- : utf-8 -*-

import ItemFactory
import KBEngine
import Define
import csstatus
import csdefine
from ConfigObject.Reward.RewardBase import RewardBase

class RewardItemBase( RewardBase.RewardBase ):
	"""
	掉落物品类
	"""
	def __init__( self, configSection ):
		self._itemID = configSection[ "goodsid" ]
		self._amount = configSection[ "amount" ]

class RewardItem( RewardItemBase ):
	"""
	物品
	"""
	def __init__( self, configSection ):
		RewardItemBase.__init__( self, configSection )
	
	def getItem( self ):
		return ItemFactory.ItemFactoryInst.createDynamicItem( self._itemID, self._amount )
		
	def addReward( self, rewarderID, reason ):
		
		rewarder = KBEngine.entities.get( rewarderID, None )
		if rewarder:
			item = self.getItem()
			result = rewarder.addItem( item, reason )
			if result != csstatus.ITEM_GO_ON:
				return item
		return None
		
