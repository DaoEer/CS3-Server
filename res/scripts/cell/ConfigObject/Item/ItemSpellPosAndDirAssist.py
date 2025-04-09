# -*- coding: utf-8 -*-

#common
import KBEDebug
#cell
import ConfigObject.Item.ItemUse as ItemUse
#data
import csstatus


class ItemSpellPosAndDirAssist(ItemUse.ItemUse):
	"""
	玩家可以手动调整怪物刷出的 位置 和 朝向
	"""
	def __init__(self, srcData):
		"""
		"""
		ItemUse.ItemUse.__init__(self, srcData)
		# 参数1 模型ID，客户端使用！
		# 参数3 模型的偏移高度
		self.useSpaceList = srcData["Param2"].split("|")
		self.scriptID = srcData.get("Param4")

	def checkUseBySpace( self, owner ):
		"""
		检查地图是否可以使用
		"""
		if self.useSpaceList:
			if not owner.getCurrentSpaceScriptID() in self.useSpaceList:
				return False
		return ItemUse.ItemUse.checkUseBySpace(self, owner)
		
	def useToPosAndDir(self, owner, pos, dir):
		"""
		用客户端位置、朝向使用物品
		"""
		params = {}
		params["belongDBID"] = owner.playerDBID
		params["spawnPos"] = pos
		params["spawnDir"] = dir
		owner.createEntityByScriptID( self.scriptID, pos, dir, params )
		owner.removeItemByAmount(self, 1, csdefine.ITEM_REMOVE_BY_USE)