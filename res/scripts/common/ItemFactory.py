
import KBEDebug
import Singleton
import SmartImport
import LoadModule
from MsgLogger import g_logger

PATH = "Item/ItemData.json"

class ItemFactory(Singleton.Singleton):
	def __init__(self):
		self._datas = {}
		self.initData()


	def initData(self):
		self._datas = LoadModule.openJsonCfg(PATH)

		
	def getItemData(self, id):
		try:
			return self._datas[str(id)]
		except:
			KBEDebug.WARNING_MSG( "ItemDataDict can't not find item[%s] config"%str(id) )
			return {}

	def createDynamicItem( self, id, amount = 1, params = {} ):
		"""
		"""
		itemDict = self.getItemData(id)
		if not itemDict:
			KBEDebug.WARNING_MSG( "ItemDataDict can't not find item[%s] config"%str(id) )
			g_logger.ItemLoadLog(id)
			return None
		script = itemDict["Script"]
		try:
			itemClass = SmartImport.smartImport("ConfigObject.Item." + script + ":" + script)
		except TypeError:
			KBEDebug.EXCEHOOK_MSG( "item which id is %s has no script!" % str(id) )
			g_logger.ItemLoadLog(id)
			return None
		item = itemClass(itemDict)
		item.loadDynamicData( params )
		if amount > 1:
			item.amount = amount
		return item

ItemFactoryInst = ItemFactory()