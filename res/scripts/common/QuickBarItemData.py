import csdefine

class QuickBarItemData(dict):
	def __init__( self ):
		self.index = 0
		self.qbtype = csdefine.QB_ITEM_NONE
		self.id = 0
		self.bindType = 0
		self.quickID = 0
		self.page = 0
		self.petUid = 0

	def getDictFromObj( self, obj ):

		itemDict = { "index":obj.index, "qbtype":obj.qbtype, "id":obj.id, "bindType":obj.bindType, "quickID":obj.quickID, "page":obj.page, "petUid":obj.petUid}
		return itemDict
	
	def createObjFromDict( self, dict ):

		obj = QuickBarItemData()
		obj.index = dict["index"]
		obj.qbtype = dict["qbtype"]
		obj.id = dict["id"]
		obj.bindType = dict["bindType"]
		obj.quickID = dict["quickID"]
		obj.page = dict["page"]
		obj.petUid = dict["petUid"]
		
		return obj

	def isSameType( self, obj ) :
		return isinstance( obj, QuickBarItemData )

instance = QuickBarItemData()
