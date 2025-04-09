# -*- coding: utf-8 -*-

import LoadModule
from SmartImport import smartImport

PATH = "ActivityBunch"

class ActObj( object ):
	__instance = None
	__bunchObj = {}
	def __init__( self ) :
		assert ActObj.__instance is None

	@classmethod
	def instance( SELF ) :
		if SELF.__instance is None :
			SELF.__instance = ActObj()
		return SELF.__instance
	
	def loadConfig( self, actBunchName ):
		"""
		加载某个活动串的数据
		"""
		config = LoadModule.openJsonCfg( actBunchName )
		self.__initBunch( config )

	def loadAll( self ) :
		"""
		加载所有活动串的数据
		"""
		objConfigs = LoadModule.openJsonPathCfg( PATH )
		for config in objConfigs:
			self.__initBunch( config )
			
	def getActBunch( self, actBunchName ):
		"""
		获得某个活动串对象
		"""
		if not self.__bunchObj.get( actBunchName,None ):
			self.loadConfig( actBunchName )
		
		return self.__bunchObj[ actBunchName ]
	
	def __initBunch( self, config ):
		"""
		初始化数据
		"""
		bunchName = config["BunchName"]
		scriptName = config["Script"]
		if scriptName:
			ObjClass = smartImport( "ActivityBunchModule." + scriptName + ":" + scriptName )
			obj = ObjClass( self, bunchName )
			obj.loadConfig( config )
			self.__bunchObj[bunchName] = obj

	def signUp( self, bunchName, signUpEntity ):
		"""
		报名某个活动串
		"""
		if self.__bunchObj.get(bunchName,None):
			self.__bunchObj[bunchName].signUp(signUpEntity)

	def join( self, bunchName, actName, joinEntity, params ):
		"""
		参加某个活动串
		"""
		if self.__bunchObj.get(bunchName,None):
			self.__bunchObj[bunchName].join( actName, joinEntity, params )

	def joinNext( self, bunchName, actName, joinEntity, params ):
		"""
		参加下个活动
		"""
		if self.__bunchObj.get(bunchName,None):
			self.__bunchObj[bunchName].joinNext( actName, joinEntity, params )

	def onAddJoinner( self, bunchName, actName, joinEntity, result ):
		"""
		添加参与者回调
		"""
		if self.__bunchObj.get(bunchName,None):
			self.__bunchObj[bunchName].onAddJoinner( actName, joinEntity, result )

	def getNextJoinMembers( self, bunchName, actName ):
		"""
		获得允许参与该活动的人数
		"""
		if self.__bunchObj.get( bunchName, None ):
			self.__bunchObj[bunchName].getNextJoinMembers( actName )

g_actObj = ActObj.instance()


def loadAllBunch():
	"""
	加载所有活动串数据
	"""
	global g_actObj
	g_actObj.loadAll()

def getEventKeys():
	"""
	获得所有活动串事件key
	"""
	global g_actObj
	g_actObj.getEventKeys()

def doEventFunc( key ):
	"""
	执行活动串某事件
	"""
	global g_actObj
	g_actObj.doEventFunc( key )

def signUp( bunchName, signUpEntity ):
	"""
	报名某个活动串
	"""
	global g_actObj
	g_actObj.signUp( bunchName, signUpEntity )

def join( bunchName, actName, joinEntity, params ):
	"""
	参加某个活动串
	"""
	global g_actObj
	g_actObj.join( bunchName, actName, joinEntity, params )

def joinNext( bunchName, actName, joinEntity, params ):
	"""
	参加某个活动串下个活动
	"""
	global g_actObj
	g_actObj.joinNext( bunchName, actName, joinEntity, params )

def onAddJoinner( bunchName, actName, joinEntity, result ):
	global g_actObj
	g_actObj.onAddJoinner( bunchName, actName, joinEntity, result )

def getNextJoinMembers( bunchName, actName ):
	global g_actObj
	return g_actObj.getNextJoinMembers( bunchName, actName )
