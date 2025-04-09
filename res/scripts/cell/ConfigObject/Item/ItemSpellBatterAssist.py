# -*- coding: utf-8 -*-

#common
import KBEDebug
import KBEngine
#cell
import ConfigObject.Item.ItemSpellAssist as ItemSpellAssist
#data
import csstatus
import KBEMath
import Functions
import csdefine
import Math


class ItemSpellBatterAssist(ItemSpellAssist.ItemSpellAssist):
	"""
	"""
	def __init__(self, srcData):
		"""
		"""
		ItemSpellAssist.ItemSpellAssist.__init__(self, srcData)
		self.posList = []
		for strPos in srcData["Param4"].split("|"):
			strPosList = strPos.split(" ")
			if len( strPosList )>= 3:
				self.posList.append( Math.Vector3( KBEMath.Unreal2KBEnginePosition( Functions.vector3TypeConvert( strPos ) ) ))
		

	def checkUse(self, owner):
		"""
		使用物品检测
		"""
		if KBEngine.globalData.get( "LHMJ_ChallengeActive") or KBEngine.globalData.get( "LHMJ_PlunderActive" ):
			return csstatus.CAN_NOT_SET_BATTERY_CUR_STATE
		
		return ItemSpellAssist.ItemSpellAssist.checkUse( self, owner )

	def useToPos( self, owner, pos ):
		"""
		对位置使用物品
		"""
		for _pos in self.posList:
			if _pos.distTo( pos ) <= 2:					# 使用策划配置的pos，而不是 玩家选取的位置
				pos = _pos
				break
		space = owner.getCurrentSpace()
		if space.getScript().getSpaceType() == csdefine.SPACE_TYPE_DONG_FU:
			isFind = 0
			for scriptID in space.batteryScriptIDList:
				for entBatter in space.getEntityMailBoxRecord( scriptID ):
					if entBatter.position.distTo( pos ) <= 2:
						isFind = 1
						entBatter.destroySelf()
						break
				if isFind:
					break
		
		statusID = owner.useSkillToEntityForItemPos( self.getSkillID(), pos, self.getUid() )
		if statusID != csstatus.SKILL_GO_ON:
			return statusID
		
		return csstatus.ITEM_USE_GO_ON_MSG

