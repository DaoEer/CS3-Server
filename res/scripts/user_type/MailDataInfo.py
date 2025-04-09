# -*- coding: utf-8 -*-
import KBEDebug
import json
import ItemFactory
import Functions

class MailDataInfo( object ):
	"""
	邮件数据
	"""
	def __init__( self ):
		self.id = 0
		self.title = ""
		self.content = ""
		self.itemList = []
		self.money = 0
		self.senderName = ""
		self.receiverName = ""
		self.senderType = 0
		self.receiveTime = 0
		self.remainTime = 0
		self.isTaken = 0
		self.isUpper = 0
		self.isRead = 0
		self.lingshi = 0
		self.xianshi = 0
		self.bindMoney = 0

	def getDictFromObj( self, obj ):
		"""
		The method converts a wrapper instance to a FIXED_DICT instance.

		@param obj: The obj parameter is a wrapper instance.
		@return: This method should return a dictionary(or dictionary-like object) that contains the same set of keys as a FIXED_DICT instance.
		"""
		tempList= []
		for item in obj.itemList:
			itemDict = { "id":item.id,"uid":item.uid,"amount":item.amount,"bindType":item.bindType, "dynamicData": item.getDynamicDataForClient( None ) } 
			tempList.append( itemDict )
			
		data = {"id":obj.id,"title": obj.title,"content":obj.content,"itemList":tempList,"money":obj.money,"senderName":obj.senderName,"receiverName":obj.receiverName,
		"senderType":obj.senderType,"receiveTime":obj.receiveTime,"remainTime":obj.remainTime,"isTaken":obj.isTaken,"isRead":obj.isRead,"isUpper":obj.isUpper, 
		"lingshi":obj.lingshi, "xianshi":obj.xianshi, "bindMoney":obj.bindMoney}
		return data

	def createObjFromDict( self, dict ):
		"""
		This method converts a FIXED_DICT instance to a wrapper instance.

		@param dict: The dict parameter is a FIXED_DICT instance.
		@return: The method should return the wrapper instance constructed from the information in dict.
		"""
		obj = MailDataInfo()
		obj.id = dict["id"]
		obj.title = dict["title"]
		obj.content = dict["content"]
		for tempDict in dict["itemList"]:
			id = tempDict["id"]
			amount = tempDict["amount"]
			itemInst = ItemFactory.ItemFactoryInst.createDynamicItem( id, amount, tempDict )
			obj.itemList.append(itemInst)
		obj.money = dict["money"]
		obj.senderName = dict["senderName"]
		obj.receiverName = dict["receiverName"]
		obj.senderType = dict["senderType"]
		obj.receiveTime = dict["receiveTime"]
		obj.remainTime = dict["remainTime"]
		obj.isTaken = dict["isTaken"]
		obj.isRead = dict["isRead"]
		obj.isUpper = dict["isUpper"]
		obj.lingshi = dict["lingshi"]
		obj.xianshi = dict["xianshi"]
		obj.bindMoney = dict["bindMoney"]
		return obj

	def isSameType( self, obj ):
		"""
		This method check whether an object is of the wrapper type.

		@param obj: The obj parameter in an arbitrary Python object.
		@return: This method should return true if obj is a wrapper instance.
		"""
		return isinstance( obj, MailDataInfo )

class MailDataList( dict ):

	def getDictFromObj( self, obj ):
		"""
		The method converts a wrapper instance to a FIXED_DICT instance.

		@param obj: The obj parameter is a wrapper instance.
		@return: This method should return a dictionary(or dictionary-like object) that contains the same set of keys as a FIXED_DICT instance.
		"""
		data = {"mailDataList": []}
		for dat in obj[ "mailDataList" ]:
			#d = MailDataInfo().getDictFromObj(dat)
			data["mailDataList"].append( dat )
		return data	

	def createObjFromDict( self, dict ):
		obj = MailDataList()
		obj["mailDataList"] = []
		for dct in dict["mailDataList"]:
			obj["mailDataList"].append(dct)
		
		return obj

	def isSameType( self, obj ):
		if obj is None: return False
		return isinstance( obj, MailDataList )

# 自定义类型实现实例
g_mailDataInfo = MailDataInfo()

g_mailDataList = MailDataList()