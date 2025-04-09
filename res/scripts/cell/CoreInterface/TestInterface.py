# -*- coding: utf-8 -*-

"""
测试示例
一些测试方法，都可以写在这里
"""
import KBEDebug
import KBEngine
import Functions
import SpaceStageDataType

class TestInterface:
	"""
	测试示例类
	"""
	def __init__(self):
		self._testitem = None
		self._testitemList = []
	
	#------------------------sample------------------------------------------------------------------
	#------------------------client call cellmethod -------------------------------------------------
	#-----------------------------bp call cellmethod-------------------------------------------------
	def testStringListBP(self, srcEntityID, stringList):
		"""
		<exposed method>
		客户端的蓝图中的testStringListBP并不调用服务器的此方法，
		而是调用testIntList和testStringList方法
		"""
		if not self.validateClientCall( srcEntityID ):
			return 
		KBEDebug.DEBUG_MSG("stringList[%s]"%str(stringList))

	def testCommonBP(self, srcEntityID, inta, floatb , stringc):
		"""
		<exposed method>
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		KBEDebug.DEBUG_MSG("inta[%s], floatb[%s], stringc[%s]!"%(inta, floatb, stringc))

	#-----------------------------c++ call cellmethod-------------------------------------------------
	def testIntList(self, srcEntityID, intList):
		"""
		<exposed method>
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		KBEDebug.DEBUG_MSG("intList[%s]"%str(intList))

	def testFloatList(self, srcEntityID, floatList):
		"""
		<exposed method>
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		KBEDebug.DEBUG_MSG("floatList[%s]"%str(floatList))

	def testDoubleList(self, srcEntityID, doubleList):
		"""
		<exposed method>
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		KBEDebug.DEBUG_MSG("doubleList[%s]"%str(doubleList))

	def testStringList(self, srcEntityID, stringList):
		"""
		<exposed method>
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		KBEDebug.DEBUG_MSG("stringList[%s]"%str(stringList))

	def testClientCall1(self, srcEntityID, inta, floatb, stringc, stringList):
		"""
		<exposed method>
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		KBEDebug.DEBUG_MSG("inta[%d], floatb[%f], stringc[%s], stringList[%s]!"%(inta, floatb, stringc, str(stringList)))

	def testComplex(self, srcEntityID,inta, floatb, stringc, testitem):
		"""
		<exposed method>
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		KBEDebug.DEBUG_MSG("inta[%d], floatb[%f], stringc[%s]!"%(inta, floatb, stringc))
		self._testitem = testitem


	def testComplex1(self, srcEntityID,inta, testitemList):
		"""
		<exposed method>
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		KBEDebug.DEBUG_MSG("inta[%d]!"%(inta))
		self._testitemList = testitemList


	#--------------------------cell call clientmethod, base similar -------------------------------------

	#----------------------------call client bp method---------------------------------------------------
	#-------------------------------------common-----------------------------------------------------------
	def testCellCommon1(self):
		"""
		一般调用
		"""
		inta = 1
		floatb = 2.0
		stringc = "aaaaaaaaaaaaa"
		self.client.TestCellCommon1(inta, floatb, stringc)

	def testCellCommon2(self):
		"""
		给客户端发送整形列表
		"""
		intlist = [1,2,3,4]
		self.client.TestCellCommon2(intlist)

	def testCellCommon3(self):
		"""
		给客户端发送float列表
		"""	
		floatlist = [1.1, 2.2, 3.3, 4.4 ]
		self.client.TestCellCommon3(floatlist)

	def testCellCommon4(self):
		"""
		给客户端发送string列表
		"""
		stringlist = ["aaa", "bbb", "ccc"]
		self.client.TestCellCommon4(stringlist)

	#======================================json---------------------------------------------------------
	def testJson1(self):
		"""
		result = {"ROOT":[{"aa":1, "bb":2.0, "cc":"fdsafdsfasdf"}, {"aa":2, "bb":3.0, "cc":"rewrttwq"}]}
		"""
		dict1 = {"aa":1, "bb":2.0, "cc":"fdsafdsfasdf"}
		dict2 = {"aa":2, "bb":3.0, "cc":"rewrttwq"}
		result = Functions.toJsonString([dict1, dict2])
		KBEDebug.DEBUG_MSG("result = %s"%result)
		self.client.testJson1(result)

	def testJson2(self):
		"""
		result = {"Root":{"aa":1, "bb":2.0, "cc":"fdsafdsf", "dd":["1111", "22222"]}}
		"""
		dict1 = {"aa":1, "bb":2.0, "cc":"fdsafdsf", "dd":["1111", "22222"]}
		result = Functions.toJsonString(dict1)
		KBEDebug.DEBUG_MSG("result = %s"%result)
		self.client.testJson2(result)

	#-------------------------------------------------call client c++ method--------------------------------
	#-----------------------------------------common--------------------------------------------------------
	def testCellCpp1(self):
		"""
		一般调用
		"""
		inta = 1
		floatb = 2.0
		stringc = "aaaaaaaaaaaaa"
		self.client.testCellCpp1(inta, floatb, stringc)

	def testCellCpp2(self):
		"""
		给客户端发送整形列表
		"""
		intlist = [1,2,3,4]
		self.client.testCellCpp2(intlist)

	def testCellCpp3(self):
		"""
		给客户端发送float列表
		"""	
		floatlist = [1.1, 2.2, 3.3, 4.4 ]
		self.client.testCellCpp3(floatlist)

	def testCellCpp4(self):
		"""
		给客户端发送string列表
		"""
		stringlist = ["aaa", "bbb", "ccc"]
		self.client.testCellCpp4(stringlist)

	def testCellCpp5(self):
		"""
		给客户端发复杂对象
		"""
		testdict = {"stageIndex":1,
			"title": "title",
			"comment": "none",
			"tasks": [{"implType":1,"taskIndex":0, "title":"task1", "reqVal":10, "val":5, "param1":"11","param2":"22","param3":"33"},
				{"implType":2,"taskIndex":1, "title":"task2", "reqVal":5, "val":2, "param1":"aa", "param2":"bb", "param3":"cc"},		
			 ],
			}
		obj = SpaceStageDataType.instance.createObjFromDict(testdict)
		self.client.testCellCpp5(obj)


	#------------------------------------------json----------------------------------------------------------
	def testJsonCpp1(self):
		"""
		result = {"ROOT":[{"aa":1, "bb":2.0, "cc":"fdsafdsfasdf"}, {"aa":2, "bb":3.0, "cc":"rewrttwq"}]}
		"""
		dict1 = {"aa":1, "bb":2.0, "cc":"fdsafdsfasdf"}
		dict2 = {"aa":2, "bb":3.0, "cc":"rewrttwq"}
		result = Functions.toJsonString([dict1, dict2])
		KBEDebug.DEBUG_MSG("result = %s"%result)
		self.client.testJsonCpp1(result)

	def testJsonCpp2(self):
		"""
		result = {"Root":{"aa":1, "bb":2.0, "cc":"fdsafdsf", "dd":["1111", "22222"]}}
		"""
		dict1 = {"aa":1, "bb":2.0, "cc":"fdsafdsf", "dd":["1111", "22222"]}
		result = Functions.toJsonString(dict1)
		KBEDebug.DEBUG_MSG("result = %s"%result)
		self.client.testJsonCpp2(result)

#------------------------------------------test uint64 and int64--------------------------------
	def test64(self):
		"""
		测试int64和uint64的传输
		"""
		self.testuint64 = 18446744073709087295
		self.testint64 = KBEngine.genUUID64()
		KBEDebug.DEBUG_MSG("testuint64[%s], testint64[%s]"%(str(self.testuint64), str(self.testint64)))
