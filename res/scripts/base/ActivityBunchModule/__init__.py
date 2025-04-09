#-*-coding:utf-8-*-

import LoadModule
from SmartImport import smartImport

PATH = "ActivityBunch"
"""
整个模块的设计
base：
1、负责活动的开启，关闭等活动状态切换；
2、负责活动的操作，报名等
3、负责活动的串联。

cell：
1、负责活动数据的打包；
2、负责基本参与条件的检查；
3、负责参与活动的响应（例如进行传送，进行弹框等操作）。

数据的初始化：
base上的数据只能初始化一次，和ActivityBunchMgr绑定在一个base; 
cell数据在每个cellapp都进行初始化。
"""
class ActObj( object ):
	__instance = None
	__bunchObj = {}
	__eventToFunc = {}
	def __init__( self ) :
		assert ActObj.__instance is None
	
	@classmethod
	def instance( SELF ) :
		if SELF.__instance is None :
			SELF.__instance = ActObj()
		return SELF.__instance
	
	@classmethod
	def registerEventFunc( SELF, key, func ):
		SELF.__eventToFunc[ key ] = func
	
	@classmethod
	def doEventFunc( SELF, key ):
		SELF.__eventToFunc[ key ]()
	
	@classmethod
	def getEventKeys( SELF ):
		return SELF.__eventToFunc.keys()
	
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
		if not self.__bunchObj.get(actBunchName,None):
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

	def signUp( self, actMgr, bunchName, signUpEntityMB, params ):
		"""
		报名某个活动串
		"""
		bunchObj = self.getActBunch( bunchName )
		bunchObj.signUp( actMgr, signUpEntityMB, params )

	def join( self, actMgr, bunchName, actName, joinEntityMB, params ):
		"""
		参加某个活动串中的某个活动
		"""
		bunchObj = self.getActBunch( bunchName )
		bunchObj.join( actMgr, actName, joinEntityMB, params )

	def joinNext( self, actMgr, bunchName, actName, joinEntityMB, params ):
		"""
		参加下轮活动
		"""
		bunchObj = self.getActBunch( bunchName )
		bunchObj.joinNext( actMgr, actName, joinEntityMB, params )

	def abandon( self, actMgr, bunchName, actName, abandonEntityMB, activityKey, playerDBID ):
		"""
		放弃活动
		"""
		bunchObj = self.getActBunch( bunchName )
		bunchObj.abandon( actMgr, actName, abandonEntityMB, activityKey, playerDBID )

	def onCompleteActivityStage( self, bunchName, actName, joinEntityMB,playerDBID,playerName,completeStage, useTime ):
		"""
		"""
		bunchObj = self.getActBunch( bunchName )
		bunchObj.onCompleteActivityStage(actName, joinEntityMB,playerDBID,playerName,completeStage, useTime )


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

def signUp( actMgr, bunchName, signUpEntityMB, params ):
	"""
	报名某个活动串
	"""
	global g_actObj
	g_actObj.signUp( actMgr, bunchName, signUpEntityMB, params )

def join( actMgr, bunchName, actName, joinEntityMB, params ):
	"""
	参加某个活动串中某个活动
	"""
	global g_actObj
	g_actObj.join( actMgr, bunchName, actName, joinEntityMB, params )

def joinNext( actMgr, bunchName, actName, joinEntityMB, params ):
	"""
	参加下轮活动
	"""
	global g_actObj
	g_actObj.joinNext( actMgr, bunchName, actName, joinEntityMB, params )

def abandon( actMgr, bunchName, actName, abandonEntityMB, activityKey, playerDBID ):
	"""
	放弃活动
	"""
	global g_actObj
	g_actObj.abandon( actMgr, bunchName, actName, abandonEntityMB, activityKey, playerDBID )

def onCompleteActivityStage(bunchName, actName, joinEntityMB,playerDBID,playerName,completeStage, useTime ):
	"""
	完成某个活动的某阶段
	"""
	global g_actObj
	g_actObj.onCompleteActivityStage(bunchName, actName, joinEntityMB,playerDBID,playerName,completeStage, useTime )

