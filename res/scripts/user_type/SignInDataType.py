import KBEDebug
import Functions


class SignData( dict ):

	def __init__( self ):
		dict.__init__( self )

	def getDictFromObj( self, obj ):

		dict = {"yearMonth": obj["yearMonth"] ,"dayList": []}

		for o in obj["dayList"]:
			dict["dayList"].append( o )

		return dict

	def createObjFromDict( self, dict ):

		obj = SignData()
		obj["yearMonth"] = dict["yearMonth"]

		obj["dayList"] = []
		
		for dct in dict[ "dayList" ]:
			obj["dayList"].append(dct)

		return obj

	def isSameType( self, obj ):
		if obj is None: return False
		return isinstance( obj, SignData )

class SignDataList( dict ):

	def __init__( self ):
		dict.__init__( self )

	def getDictFromObj( self, obj ):

		dict = { "signDatas":[] }

		for o in obj["signDatas"]:

			dict["signDatas"].append( o )

		return dict

	def createObjFromDict( self, dict ):

		obj = SignDataList()

		obj["signDatas"] = []

		for dct in dict["signDatas"]:
			d = SignData().createObjFromDict( dct )
			obj["signDatas"].append( d )

		return obj

	def isSameType( self, obj ):
		if obj is None: return False
		return isinstance( obj, SignDataList )

# 自定义类型实现实例
signData = SignData()

signDataList = SignDataList()
