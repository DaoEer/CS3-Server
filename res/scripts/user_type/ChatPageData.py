import KBEDebug
import Functions

class ChatPageSettings( dict ):

	def __init__(self):
		dict.__init__(self)

	def getDictFromObj( self, obj ):
		data = {}
		data = {"pageType": obj["pageType"], "isDeletable": obj["isDeletable"], "isDraggable": obj["isDraggable"], "pageName": obj["pageName"],"channelList": []}
		
		for ch in obj["channelList"]:
			data["channelList"].append( ch )

		return data
	def createObjFromDict( self, dict ):
		obj  = ChatPageSettings()
		obj["pageType"] = dict["pageType"]
		obj["isDeletable"] = dict["isDeletable"]
		obj["isDraggable"] = dict["isDraggable"]
		obj["pageName"] = dict["pageName"]
		obj["channelList"] = []

		for ch in dict["channelList"]:
			obj["channelList"].append( ch )

		return obj

	def isSameType( self, obj ):

		if obj is None: return True
		return isinstance( obj, ChatPageSettings )

class ChatPageSettingsList( dict ):

	def __init__(self):
		dict.__init__(self)

	def getDictFromObj( self, obj ):
		data = {"datas" : []}
		for o in obj[ "datas" ]:
			data["datas"].append( o )

		return data

	def createObjFromDict( self, dict ):
		obj  = ChatPageSettingsList()
		obj["datas"] = []

		for dct in dict["datas"]:
			obj["datas"].append( dct )

		return obj

	def isSameType( self, obj ):

		if obj is None: return True
		return isinstance( obj, ChatPageSettingsList )

class ChatQuickseTTings( dict ):

	def __init__(self):
		dict.__init__(self)

	def getDictFromObj( self, obj ):
		data = {}
		data = {"channelType": obj["channelType"], "isCanModify": obj["isCanModify"], "shortcutKey": obj["shortcutKey"]}

		return data

	def createObjFromDict( self, dict ):
		obj  = ChatQuickseTTings()
		
		obj["channelType"] = dict["channelType"]
		obj["isCanModify"] = dict["isCanModify"]
		obj["shortcutKey"] = dict["shortcutKey"]

		return obj

	def isSameType( self, obj ):

		if obj is None: return True
		return isinstance( obj, ChatQuickseTTings )

class ChatQuickseTTingsList( dict ):

	def __init__(self):
		dict.__init__(self)

	def getDictFromObj( self, obj ):
		data = {"datas" : []}
		for o in obj[ "datas" ]:
			data["datas"].append( o )

		return data

	def createObjFromDict( self, dict ):
		obj  = ChatQuickseTTingsList()
		obj["datas"] = []

		for dct in dict["datas"]:
			obj["datas"].append( dct )

		return obj

	def isSameType( self, obj ):

		if obj is None: return True
		return isinstance( obj, ChatQuickseTTingsList )
# 自定义类型实现实例
ChatPageDict 	= ChatPageSettings()

ChatPageList 	= ChatPageSettingsList()

ChatQuickDict   = ChatQuickseTTings()

ChatQuickList   = ChatQuickseTTingsList()

