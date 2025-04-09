# -*- coding: utf-8 -*-

import KBEngine
import Functions
import csdefine

class StoreBuyRecordData(dict):
	"""
	购买记录
	"""
	def __init__(self):
		self.goodsID 		= 0
		self.amount 		= 0
		self.buyTime 		= str(Functions.getTime())
		self.uid 			= str(KBEngine.genUUID64())
		self.price 			= 0
		self.goodsType 		= 0
		self.itemID 		= 0

	def getDictFromObj( self, obj ):
		data 				= {}
		data["goodsID"] 	= obj.goodsID
		data["amount"] 		= obj.amount
		data["buyTime"] 	= obj.buyTime
		data["uid"] 		= obj.uid
		data["price"] 		= obj.price
		data["goodsType"] 	= obj.goodsType
		data["itemID"] 		= obj.itemID

		return data

	def createObjFromDict( self, data ):
		obj 				= self.__class__()
		obj.goodsID 		= data["goodsID"]
		obj.amount 			= data["amount"]
		obj.buyTime 		= data["buyTime"]
		obj.uid 			= data["uid"]
		obj.price 			= data["price"]
		obj.goodsType 		= data["goodsType"]
		obj.itemID 			= data["itemID"]

		return obj

	def isSameType( self, obj ) :
		return isinstance( obj, StoreBuyRecordData )

class StorePresentRecordData(dict):
	"""
	赠送记录
	"""
	def __init__(self):
		self.goodsID 			= 0
		self.amount 			= 0
		self.buyTime			= str(Functions.getTime())
		self.sender 			= ""
		self.receiver			= ""
		self.uid 				= str(KBEngine.genUUID64())
		self.price 				= 0
		self.receiverDBID 		= ""
		self.senderDBID 		= ""
		self.itemID 			= 0

	def getDictFromObj( self, obj ):
		data 					= {}
		data["goodsID"] 		= obj.goodsID
		data["amount"] 			= obj.amount
		data["buyTime"] 		= obj.buyTime
		data["sender"] 			= obj.sender
		data["receiver"] 		= obj.receiver
		data["uid"] 			= obj.uid
		data["price"] 			= obj.price
		data["receiverDBID"] 	= obj.receiverDBID
		data["senderDBID"] 		= obj.senderDBID
		data["itemID"] 			= obj.itemID


		return data

	def createObjFromDict( self, data ):
		obj 					= self.__class__()
		obj.goodsID 			= data["goodsID"]
		obj.amount 				= data["amount"]
		obj.buyTime 			= data["buyTime"]
		obj.sender 				= data["sender"]
		obj.receiver 			= data["receiver"]
		obj.uid 				= data["uid"]
		obj.price 				= data["price"]
		obj.receiverDBID 		= data["receiverDBID"]
		obj.senderDBID 			= data["senderDBID"]
		obj.itemID 				= data["itemID"]

		return obj

	def isSameType( self, obj ) :
		return isinstance( obj, StorePresentRecordData )

class StoreSPresentRecordDatas( dict ) :
	"""
	赠送方赠送记录
	"""
	def getDictFromObj( self, obj ):
		"""
		The method converts a wrapper instance to a FIXED_DICT instance.
		
		"""
		datas = {}
		datas["recordsDatas"] = []
		for i in obj.values() :
			datas["recordsDatas"].append(i)
		return datas
		
	def createObjFromDict( self, dict ):
		"""
		This method converts a FIXED_DICT instance to a wrapper instance.
		"""
		obj = StoreSPresentRecordDatas()
		datas = dict["recordsDatas"]
		for i in datas :
			if i.senderDBID not in obj:
				obj[ i.senderDBID ] = []
			obj[ i.senderDBID ].append(i)
			
		return obj
		
	def isSameType( self, obj ):
		"""
		This method check whether an object is of the wrapper type.
		"""
		return isinstance( obj, StoreSPresentRecordDatas )

class StoreRPresentRecordDatas( dict ) :
	"""
	收礼方赠送记录
	"""
	def getDictFromObj( self, obj ):
		"""
		The method converts a wrapper instance to a FIXED_DICT instance.
		
		"""
		datas = {}
		datas["recordsDatas"] = []
		for i in obj.values() :
			datas["recordsDatas"].append(i)
		return datas
		
	def createObjFromDict( self, dict ):
		"""
		This method converts a FIXED_DICT instance to a wrapper instance.
		"""
		obj = StoreRPresentRecordDatas()
		datas = dict["recordsDatas"]
		for i in datas :
			if i.receiverDBID not in obj:
				obj[ i.receiverDBID ] = []
			obj[ i.receiverDBID ].append(i)
			
		return obj
		
	def isSameType( self, obj ):
		"""
		This method check whether an object is of the wrapper type.
		"""
		return isinstance( obj, StoreRPresentRecordDatas )

g_StoreBuyRecord = StoreBuyRecordData()
g_StorePresentRecord = StorePresentRecordData()
g_StoreSPresentRecords = StoreSPresentRecordDatas()
g_StoreRPresentRecords = StoreRPresentRecordDatas()