# -*- coding: utf-8 -*-

"""帮会事件"""

import Const
import Functions
class TongRecordInterface( object ):
	def __init__( self ):
		pass
		
	def addRecord( self, eventType, *param ):
		"""添加记录"""
		if len( self.tongRecords ) >= Const.TONG_RECORD_MAX_NUM:
			self.tongRecords.pop(0)
		time = str( Functions.getTime() )
		self.tongRecords.append( ( time, eventType, param ) )
		
	def requestTongEvent( self, baseMB ):
		"""
		define method
		请求帮会事件
		"""
		eventList = {"eventDatas":[]}
		for record in self.tongRecords:
			temp = {"param" : []}
			for index, arg in enumerate( record ):
				if index == 0:
					temp["time"] = str(arg)
				elif index == 1:
					temp["type"] = arg
				elif index == 2:
					for i in arg:
						temp["param"].append(str(i ))
			eventList["eventDatas"].append( temp )
		baseMB.client.CLIENT_OnRequireTongEvent(  eventList ) 
		
	def addStoreRecord( self, eventType, *param ):
		"""仓库记录"""
		if len( self.tongStoreRecords ) >= Const.TONG_RECORD_MAX_NUM:
			self.tongStoreRecords.pop(0)
		time = str( Functions.getTime() )
		self.tongStoreRecords.append( ( time, eventType, param ) )
		
	def requestTongStoreEvent( self, baseMB ):
		"""
		define method
		请求帮会仓库事件
		"""
		eventList = {"eventDatas":[]}
		for record in self.tongStoreRecords:
			temp = {}
			for index, arg in enumerate( record ):
				if index == 0:
					temp["time"] = str(arg)
				elif index == 1:
					temp["type"] = arg
				elif index == 2:
					arg_temp = []
					for i in arg:
						arg_temp.append(str(i))
					temp["param"] = tuple(arg_temp)
			eventList["eventDatas"].append( temp )
		baseMB.client.CLIENT_OnRequireTongStoreEvent(  eventList ) 