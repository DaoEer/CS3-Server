# -*- coding: utf-8 -*-

import ConfigObject.Item.ItemBase as ItemBase

class ItemOriginPetEgg(ItemBase.ItemBase):
	"""
	原兽蛋
	"""
	def __init__(self, srcData):
		ItemBase.ItemBase.__init__(self, srcData)
		self._scriptID = int( srcData.get( "Param1", 0 ) )		# 幻兽ScriptID
		self._eggQuality = int( srcData.get( "Quality", 1 ) )	# 幻兽蛋品质
		self._abilityRoll = int( srcData.get( "Param2", 1 ) )	# 品质

	def getOriginPetData( self ):
		""""""
		return ( self._scriptID, self._eggQuality, self._abilityRoll )