# -*- coding: utf-8 -*-


"""
usage:
	效果

attribute:
	pass

member function:
	pass

callback:
	pass

"""


#cell
from ConfigObject.Skill.Effect.EffectSkillBase import EffectSkillBase
import KBEDebug
#common
import csdefine

class EffectRemoveYCJMDBossItemData( EffectSkillBase ):
	"""
	CST-8727 移除勇闯夺命岛Boss物品数据
	"""
	def __init__( self ):
		EffectSkillBase.__init__( self )
		self.itemID = 0
		self.amount = 0

	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		EffectSkillBase.init( self, dictDat, skill )
		self.itemID = int(dictDat["Param1"])
		self.amount = 1
		if dictDat["Param2"]:
			self.amount = int( dictDat["Param2"] )

	def onReceive( self, skill, caster, receiver ):
		"""
		效果开始
		"""
		if caster.getEntityFlagExt() == csdefine.ENTITY_FLAG_EXT_MONSTER_EXT_YCJMD:
			caster.reduceBossItemData( self.itemID, self.amount )



