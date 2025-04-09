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
				self.sumeDatas[int(dataStr[0])] = int( dataStr[1] )

	def checkUse(self, owner):
		"""
		使用前检测
		"""
		space = owner.getCurrentSpace()
		if not space or space.getScript().getSpaceType() != csdefine.SPACE_TYPE_DONG_FU:
			return csstatus.CAN_NOT_USE_KUILEI_IN_SPACE
		if space.belongDBID == owner.playerDBID:
			return csstatus.CAN_NOT_USE_KUILEI_IN_SELF_DONGFU
		
		num = len( space.ghostList )
		buildlevel = owner.getLHMJBuildLevel( csdefine.LHMJ_BUIILD_LING_QUAN )
		if num >= self.sumeDatas.get(buildlevel, 1):
			return csstatus.LHMJ_CALL_MAX_GHOST
			
		return ItemSpellPosAndDirAssist.ItemSpellPosAndDirAssist.checkUse(self, owner)
		
		
	def useToPosAndDir(self, owner, pos, dir):
		"""
		用客户端位置、朝向使用物品
		"""
		params = {}
		params["belongDBID"] = owner.playerDBID
		params["spawnPos"] = pos
		params["spawnDir"] = dir
		ent = owner.createEntityByScriptID( self.scriptID, pos, dir, params )
		owner.removeItemByAmount(self, 1, csdefine.ITEM_REMOVE_BY_USE)
		owner.client.addDFMonsterInfo(ent.id)