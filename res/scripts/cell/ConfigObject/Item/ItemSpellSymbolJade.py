# -*- coding: utf-8 -*-

#common
import KBEDebug
#cell
import time
import ConfigObject.Item.ItemSpellPosAndDirAssist as ItemSpellPosAndDirAssist
#data
import csstatus
import Const
import csdefine

class ItemSpellSymbolJade(ItemSpellPosAndDirAssist.ItemSpellPosAndDirAssist):
	"""
	放置 陷阱符玉(洞府)
	玩家可以手动调整怪物刷出的 位置 和 朝向
	"""
	def __init__(self, srcData):
		"""
		"""
		ItemSpellPosAndDirAssist.ItemSpellPosAndDirAssist.__init__(self, srcData)
		self.maxNum = 8
		self.lifeTime = 5 * 60
		strList = srcData["Param5"].split("|")
		if len(strList) >= 2:
			self.maxNum = int(strList[0])
			self.lifeTime = int(strList[1])

	def checkUse(self, owner):
		"""
		使用前检测
		"""
		space = owner.getCurrentSpace()
		if space.__class__.__name__ == "SpaceCopyDongFu":
			if space.belongDBID != owner.playerDBID:		# 只有守方玩家能使用符玉
				return csstatus.LHMJ_SYMBOL_JADE_ONLY_USE_SELF_SPACE
			if space.getTrapNum() >= self.maxNum:
				return csstatus.LHMJ_SYMBOL_JADE_HAS_EMOUGH
		return ItemSpellPosAndDirAssist.ItemSpellPosAndDirAssist.checkUse(self, owner)
		
		
	def useToPosAndDir(self, owner, pos, dir):
		"""
		用客户端位置、朝向使用物品
		"""
		owner.createEntityByScriptID( self.scriptID, pos, dir, {"belongDBID" : owner.playerDBID, "playerID" : owner.id, "lifeTime" : time.time() + self.lifeTime} )			# 因为洞府是个 副本，出副本就销毁了！所以，直接保存entityID
		owner.removeItemByAmount(self, 1, csdefine.ITEM_REMOVE_BY_USE)