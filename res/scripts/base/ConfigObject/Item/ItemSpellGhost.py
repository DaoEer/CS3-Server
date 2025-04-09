# -*- coding: utf-8 -*-

#common
import KBEDebug
#cell
import ConfigObject.Item.ItemSpellPosAndDirAssist as ItemSpellPosAndDirAssist
#data
import csstatus
import csdefine


class ItemSpellGhost(ItemSpellPosAndDirAssist.ItemSpellPosAndDirAssist):
	"""
	放置傀儡(洞府)
	玩家可以手动调整怪物刷出的 位置 和 朝向
	"""
	def __init__(self, srcData):
		"""
		"""
		ItemSpellPosAndDirAssist.ItemSpellPosAndDirAssist.__init__(self, srcData)
		self.sumeDatas = {}
		strSume = srcData["Param5"].split("|")
		for sume in strSume:
			dataStr = sume.split(":")
			if len(dataStr) >= 2:
				self.sumeDatas[dataStr[0]] = dataStr[1]

	def checkUse(self, owner):
		"""
		使用前检测
		"""
		num = owner.queryTemp("ItemSpellGhost", 0)
		buildlevel = owner.secretBuilds.getBuildLevel( csdefine.LHMJ_BUIILD_LING_QUAN )
		if num >= self.sumeDatas.get(buildlevel, 1):
			return csstatus.LHMJ_CALL_MAX_GHOST
		space = owner.getCurrentSpace()
		if space.__class__.__name__ == "SpaceDongFu" and space.belongDBID == owner.playerDBID:		# 守方玩家不能使用傀儡
			return csstatus.LHMJ_CANNOT_CALL_GHOST_IN_SELF_SPACE
		return ItemSpellPosAndDirAssist.ItemSpellPosAndDirAssist.checkUse(self, owner)
		
		
	def useToPosAndDir(self, owner, pos, dir):
		"""
		用客户端位置、朝向使用物品
		"""
		owner.createEntityByScriptID( self.scriptID, pos, dir, {"playerDBID" : owner.playerDBID} )
		num = owner.queryTemp("ItemSpellGhost", 0)
		owner.setTemp("ItemSpellGhost", num + 1)
		self.onUseResult( owner, True)