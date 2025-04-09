# -*- coding: utf-8 -*-

#common
import KBEDebug
#cell
import ConfigObject.Item.ItemSpell as ItemSpell
#data
import csstatus


class ItemTeleportStone(ItemSpell.ItemSpell):
	"""
	CST-4305
	神行石
	1、直接点击使用的话，打开地图界面
	2、点击地图界面传送点，通过传送石传送到相应位置
	"""
	def __init__(self, srcData):
		"""
		"""
		ItemSpell.ItemSpell.__init__(self, srcData)

	def use(self, owner, target):
		"""
		使用物品
		"""
		owner.onOpenMapWin()
		return csstatus.ITEM_USE_GO_ON_MSG
		
	def onUseResult(self, owner, useResult ):
		"""
		使用后给玩家回调
		"""
		pass

	def useToTeleport( self, owner, point ):
		"""
		传送
		"""
		owner.setCurrentTeleportPoint(point)
		statusID = owner.useSkillToEntity( self.getSkillID(), owner.id )
		if statusID == csstatus.SKILL_NOT_READY:
			return csstatus.ITEM_INCD
		elif statusID != csstatus.SKILL_GO_ON:
			return statusID
		
		return csstatus.ITEM_USE_GO_ON_MSG

