
import ConfigObject.Item.ItemUse as ItemUse
import KBEDebug

class ItemSpell(ItemUse.ItemUse):
	def __init__(self, srcData):
		ItemUse.ItemUse.__init__(self, srcData)
		#----------------------静态属性，不会通过网络传输-------------
		self.skillID = srcData.get("skillID")		#技能ID
		self.limitCD = srcData.get("limitCD")		#技能CD
		#----------------------静态属性，不会通过网络传输-------------
