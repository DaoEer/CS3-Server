# -*- coding: utf-8 -*-
import KBEngine
import csdefine
import Functions


class StoreGiftBoxData( dict ):
	"""
	礼品盒数据
	"""
	def __init__(self):
		self.goodsID 			= 0
		self.amount 			= 0
		self.receiverName 		= ""
		self.receiverDBID 		= ""
		self.senderName 		= ""
		self.senderDBID 		= ""
		self.endTime 			= ""
		self.giftState 			= csdefine.STORE_GIFT_STATE_NONE
		self.message			= ""
		self.uid				= str(KBEngine.genUUID64())
		self.overtime			= str(Functions.getTime(3*24*60*60))
		self.price 				= 0
		self.itemID 			= 0

	def getDictFromObj( self, obj ):
		data = {}
		data["goodsID"]			= obj.goodsID
		data["amount"]			= obj.amount
		data["receiverName"]	= obj.receiverName
		data["receiverDBID"] 	= obj.receiverDBID
		data["senderName"] 		= obj.senderName
		data["senderDBID"] 		= obj.senderDBID
		data["endTime"] 		= obj.endTime
		data["giftState"] 		= obj.giftState
		data["message"] 		= obj.message
		data["uid"] 			= obj.uid
		data["overtime"] 		= obj.overtime
		data["price"] 			= obj.price
		data["itemID"] 			= obj.itemID

		return data

	def createObjFromDict( self, data ):
		obj = StoreGiftBoxData()
		obj.goodsID 			= data["goodsID"]
		obj.amount 				= data["amount"]
		obj.receiverName 		= data["receiverName"]
		obj.receiverDBID 		= data["receiverDBID"]
		obj.senderName 			= data["senderName"]
		obj.senderDBID 			= data["senderDBID"]
		obj.endTime 			= data["endTime"]
		obj.giftState 			= data["giftState"]
		obj.message 			= data["message"]
		obj.uid 				= data["uid"]
		obj.overtime 			= data["overtime"]
		obj.price 				= data["price"]
		obj.itemID 				= data["itemID"]

		return obj

	def isSameType( self, obj ) :
		return isinstance( obj, StoreGiftBoxData )

class StoreGiftBoxSendDatas( dict ):
	"""
	"""

	def getDictFromObj( self, obj ):
		"""
		The method converts a wrapper instance to a FIXED_DICT instance.
		"""
		data = {}
		data["giftDatas"] = []
		for i in obj.values():
			for j in obj.values():
				data["giftDatas"].append( j )
		return data
		
	def createObjFromDict( self, data ):
		"""
		This method converts a FIXED_DICT instance to a wrapper instance. 
		"""
		obj = StoreGiftBoxSendDatas()
		giftDatas = data["giftDatas"]
		for i in giftDatas :
			if i.senderDBID not in obj:
				obj[ i.senderDBID ] = []
			obj[ i.senderDBID ].append(i)
		return obj
		
	def isSameType( self, obj ):
		"""
		This method check whether an object is of the wrapper type.
		"""
		return isinstance( obj, StoreGiftBoxSendDatas )

class StoreGiftBoxReceiveDatas( dict ):
	"""
	"""

	def getDictFromObj( self, obj ):
		"""
		The method converts a wrapper instance to a FIXED_DICT instance.
		"""
		data = {}
		data["giftDatas"] = []
		for i in obj.values():
			for j in obj.values():
				data["giftDatas"].append( j )
		return data
		
	def createObjFromDict( self, data ):
		"""
		This method converts a FIXED_DICT instance to a wrapper instance. 
		"""
		obj = StoreGiftBoxReceiveDatas()
		giftDatas = data["giftDatas"]
		for i in giftDatas :
			if i.receiverDBID not in obj:
				obj[ i.receiverDBID ] = []
			obj[ i.receiverDBID ].append(i)
		return obj
		
	def isSameType( self, obj ):
		"""
		This method check whether an object is of the wrapper type.
		"""
		return isinstance( obj, StoreGiftBoxReceiveDatas )

instance = StoreGiftBoxData()
g_storeGiftBoxSendDatas = StoreGiftBoxSendDatas()
g_storeGiftBoxReceiveDatas = StoreGiftBoxReceiveDatas()
