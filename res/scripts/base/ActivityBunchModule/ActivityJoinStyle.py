# -*- coding: utf-8 -*-
import KBEMath
import Functions
import KBEngine
import Math
from ObjectScript.ObjectScriptFactory import g_objFactory
import KBEDebug
import csdefine

class JoinStyleBase( object ):
	objects_ = {}
	def __init__( self, section ):
		pass

	@classmethod
	def getObject( SELF, section ):
		"""
		获得Object对象
		"""
		scriptStr = section["script"]
		scriptObj = SELF.objects_.get(scriptStr,None)
		if scriptObj:
			return scriptObj(section)
		return None

	@classmethod
	def register( SELF, className, instance ):
		"""
		注册一个实例到全局列表中
		"""
		SELF.objects_[ className ] = instance

	def join( self, actMgr, joinObj, params ):
		"""
		"""
		pass

class JoinGotoShiFangCheng( JoinStyleBase ):
	#十方城专用
	def __init__( self, section ):
		JoinStyleBase.__init__( self, section )
		self.spaceClassNameDict = {}  #等级对应space文件
		if section["param1"]:
			spaceClassNameList = section["param1"].split("|")
			for item in spaceClassNameList:
				itemList = item.split(":")
				self.spaceClassNameDict[ int(int(itemList[0]) / 10) ] = itemList[1]

		pos = Functions.vector3TypeConvert( section["param2"] )
		self.enterPosition = Math.Vector3(KBEMath.Unreal2KBEnginePosition(pos))
		direction = Functions.vector3TypeConvert( section["param3"] )
		self.enterDirection = Math.Vector3(KBEMath.Unreal2KBEnginePosition(direction))
	
	def join( self, mgr, joinObj, params ):
		activityKey = params[ "activityKey" ]
		joinObj.cell.gotoSpace( self.spaceClassNameDict[ activityKey ], self.enterPosition, self.enterDirection )
	
	def requestPrepareSpace( self, joinObj, params ):
		"""
		请求预创建十方城空间
		"""
		spaceParams = {}
		activityKey = params[ "activityKey" ]
		spaceClassName = self.spaceClassNameDict[ activityKey ]
		spaceParams[ "spaceKey" ] = str(params[ "playerDBID" ])
		spaceParams["belongType"] = csdefine.SPACE_BELONG_PERSON
		KBEngine.globalData["SpaceManager"].remoteCallDomain(  spaceClassName, "createSpaceItem", (spaceParams,) )
	
	def getAllSpace( self ):
		"""
		获取所有副本className
		"""
		return self.spaceClassNameDict.values()

class JoinGotoRandomPos( JoinStyleBase ):
	"""
	传送到随机位置
	"""
	def __init__( self, section ):
		JoinStyleBase.__init__( self, section )
		self.spaceClassNameDict = {}  #等级对应space文件
		if section["param1"]:
			spaceClassNameList = section["param1"].split("|")
			for item in spaceClassNameList:
				itemList = item.split(":")
				self.spaceClassNameDict[ int(int(itemList[0]) / 10) ] = itemList[1]

	def join( self, mgr, joinObj, params ):
		activityKey = params[ "activityKey" ]
		spaceClassName = self.spaceClassNameDict[activityKey]
		spaceObject = g_objFactory.getSpaceObject( spaceClassName )
		enterPos,enterDir = spaceObject.getEnterInfo()
		joinObj.cell.gotoSpaceUseArg( spaceClassName, enterPos, enterDir, params )

JoinStyleBase.register( "JoinGotoShiFangCheng", JoinGotoShiFangCheng )
JoinStyleBase.register( "JoinGotoRandomPos", JoinGotoRandomPos )
