# -*- coding- : utf-8 -*-

from ConfigObject.Drop.DropBase.DropItemBase import DropItemBase
import ItemFactory

import Define
import csdefine

class DItem( DropItemBase ):
	"""
	物品
	"""
	def __init__( self, configSection ):
		DropItemBase.__init__( self, configSection )
	
	def getItem( self, dieEntity, killer, args ):
		return ItemFactory.ItemFactoryInst.createDynamicItem( self._itemID, self._amount )

DropItemBase.registerOjbect( Define.DROP_ITEM_DEFAULT, DItem )