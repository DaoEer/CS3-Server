"""
cell/base部份的RelationDataImpl实现模块.
"""
import KBEDebug
import Functions

class RelationCatalogDict(dict):
	
	def __init__( self ):
		dict.__init__( self )

	def getDictFromObj( self, obj ):
		dict = {"relationIndex": obj["relationIndex"], "catalogName": obj["catalogName"], "catalogList": [] }

		for uid in obj["catalogList"]:
			dict["catalogList"].append(uid)

		return dict

	def createObjFromDict( self, dict ):

		obj = RelationCatalogDict()

		obj["relationIndex"] = dict["relationIndex"]

		obj["catalogName"] = dict["catalogName"]

		obj["catalogList"] = []

		for uid in dict["catalogList"]:
			obj["catalogList"].append( uid )

		return obj

	def isSameType( self, obj ):
		if obj is None: return False
		return isinstance( obj, RelationCatalogDict )


class RelationCatalogList( dict ):
	
	def __init__( self ):
		dict.__init__( self )

	def getDictFromObj( self, obj ):

		dict = { "RelationCatalogDatas" :[] }

		for i in obj["RelationCatalogDatas"]:
			j = RelationCatalogDict().getDictFromObj( i )
			dict["RelationCatalogDatas"].append( j )

		return dict

	def createObjFromDict( self, dict ):

		obj = RelationCatalogList()

		obj["RelationCatalogDatas"] = []

		for i in dict["RelationCatalogDatas"]:
			j = RelationCatalogDict().createObjFromDict( i )
			obj["RelationCatalogDatas"].append( j )

		return obj

	def isSameType( self, obj ):
		if obj is None: return False
		return isinstance( obj, RelationCatalogList )
		
# 自定义类型实现实例
relationCatalogDict = RelationCatalogDict()

relationCatalogList = RelationCatalogList()