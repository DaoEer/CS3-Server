import KBEngine

#common
import Singleton
import KBEDebug
import csconst
import json
from LoadModule import *
from ConfigObject.SpaceEffect import SpaceEffectObject


class SpaceEffectLoader(Singleton.Singleton):
	"""
	空间动态效果配置加载
	"""
	def __init__( self ):
		self._effectDict = {}
		self.effectObjDict = {}

	def init( self, configData ):
		"""
		读取配置
		"""
		for effectID, datas in configData.items():
			effectObj = SpaceEffectObject.SpaceEffectObjectBase.getEffectObject( datas )
			self.effectObjDict[effectID] = effectObj
			scriptIDList = datas["spaceScriptID"].split("|")
			self._effectDict[effectID] = scriptIDList
	
	def reloadConfig( self ):
		"""
		配置热更新
		"""
		pass

	def getSpaceEffectList( self, playerEntity):
		"""
		获取玩家所在地图所有效果
		"""
		spaceEffectList = []
		spaceScriptID = playerEntity.getCurrentSpaceScriptID()
		for key, value in self._effectDict.items():
			if spaceScriptID in value:
				spaceEffectList.append( key )
		return spaceEffectList

	def getSpaceEffectCheck( self, playerEntity ):
		"""
		获取玩家所在地图满足条件的所有效果
		"""
		effectCndList = []
		effectList = self.getSpaceEffectList( playerEntity )
		for effectID in effectList:
			effectObj = self.effectObjDict[effectID]
			if effectObj.doEnterSpaceCheck( None, playerEntity ):
				effectCndList.append( int(effectID) )

		return effectCndList

	def checkSpaceEffect( self, spaceEntity, playerEntity, effectID ):
		"""
		获取空间效果刷新后满足条件的效果
		"""
		effectObj = self.effectObjDict[ str(effectID) ]
		if effectObj:
			return effectObj.doEnterSpaceCheck( spaceEntity, playerEntity )


g_spaceEffectLoader = SpaceEffectLoader()