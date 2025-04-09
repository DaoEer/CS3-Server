
import ConfigObject.Item.ItemSpell as ItemSpell
import KBEDebug

class ItemTeleportStone(ItemSpell.ItemSpell):
	"""
	神行石
	"""
	def __init__(self, srcData):
		ItemSpell.ItemSpell.__init__(self, srcData)
