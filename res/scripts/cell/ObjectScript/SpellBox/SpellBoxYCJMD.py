# -*- coding: utf-8 -*-

import random

import KBEngine
import Math
import KBEDebug
import csstatus
import csdefine
import csconst

from ObjectScript.SpellBox import SpellBoxPickItem


class SpellBoxYCJMD( SpellBoxPickItem.SpellBoxPickItem ):
	"""
	勇闯绝命岛 专属SpellBox
	"""
	def __init__( self ):
		SpellBoxPickItem.SpellBoxPickItem.__init__( self )

	def initData( self, data ):
		SpellBoxPickItem.SpellBoxPickItem.initData(self, data)
		self.reviveTime = (csconst.DHZC_BOX_REVIVER_TIME_MIN,csconst.DHZC_BOX_REVIVER_TIME_MAX)


	def randomSpawn(self, selfEntity):
		"""
		#复活时间随机
		"""
		spaceEntity = selfEntity.getCurrentSpace()
		if not spaceEntity:
			return

		spaceEntity.addTimerCallBack(random.randint(self.reviveTime[0], self.reviveTime[1]),"createSpellBox",( selfEntity.scriptID,selfEntity.position,selfEntity.direction,{}))
		selfEntity.destroySelf()


	def onDestroyTimeCB( self, selfEntity, srcEntityID ):
		"""
		销毁timer到达
		"""
		self.randomSpawn(selfEntity)
		
	
	def onLifeTimeCB( self, selfEntity ):
		"""
		virtual method
		生存时间到达
		"""
		selfEntity.lifeTimerID = 0
		self.randomSpawn(selfEntity)

	def pickUpItem( self, selfEntity, player, itemUIDs ):
		"""
		拾取物品
		"""
		for itemUID in itemUIDs:
			for itemInst in selfEntity.spellBoxItemList:
				if itemInst.uid != int(itemUID):
					continue
				status = player.addItemCheck( itemInst )
				if status == csstatus.ITEM_GO_ON:
					player.addItem( itemInst, csdefine.ITEM_ADD_BY_PICKUP )
					if player.getClient():
						player.client.OnPickUpSpellBoxItem( selfEntity.id,itemUID )
					selfEntity.spellBoxItemList.remove(itemInst)
					break

		if not len(selfEntity.spellBoxItemList):
			player.clearInteractiveSpellBox()
			#重刷
			self.randomSpawn(selfEntity)

			