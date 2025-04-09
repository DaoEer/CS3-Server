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
#common
import csdefine



class EffectItem( EffectSkillBase ):
	"""
	添加物品
	"""
	def __init__( self ):
		EffectSkillBase.__init__( self )
		self._itemID = ""
		self._number = ""
	
	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		EffectSkillBase.init( self, dictDat, skill )
		self._itemID = int( dictDat["Param1"] )
		self._number = int( dictDat["Param2"] )

	def onReceive( self, skill, caster, receiver ):
		"""
		效果开始
		"""
		receiver.addItemByID( self._itemID, self._number, csdefine.ITEM_ADD_BY_SKILL )



