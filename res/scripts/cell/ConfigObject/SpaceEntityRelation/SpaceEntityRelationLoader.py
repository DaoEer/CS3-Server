# -*- coding: utf-8 -*-

import KBEDebug
import SpaceEntityRelationCfg

from Singleton import Singleton
from SmartImport import smartImport


DEFAULT_RELATION_MODE = "RelationDefault"		#通用关系模式

class SpaceEntityRelationLoader( Singleton ):
	"""
	地图entity关系判断实例加载类
	"""
	def __init__( self ):
		self._datas = {}
		self._clsToObj = {}

	def init( self ):
		"""
		"""
		for relationMode, relationDict in SpaceEntityRelationCfg.Datas.items():
			self._datas[ relationMode ] = {}
			
			for entityFlagExt, relClass in relationDict.items():
				try:
					relClassObj = smartImport( "ConfigObject.SpaceEntityRelation.SpaceEntityRelation:" + relClass )
				except ImportError:
					KBEDebug.ERROR_MSG( "SpaceEntityRelation class(%s) not exist!"%relClass )
					continue
				
				self._datas[ relationMode ][entityFlagExt] = relClassObj
				if entityFlagExt not in self._clsToObj:
					self._clsToObj[entityFlagExt] = relClassObj
		
		if DEFAULT_RELATION_MODE not in self._datas:	#确保配置了通用关系模式
			KBEDebug.ERROR_MSG( "SpaceEntityRelation defaultMode config lack!" )
	
	def getRelationIns( self, relationMode, entityFlagExt ):
		"""
		根据关系模式和entityFlagExt获取关系判断实例
		"""
		if relationMode not in self._datas:
			KBEDebug.ERROR_MSG( "SpaceEntityRelation config error!", relationMode )
			return None
		
		if entityFlagExt in self._datas[ relationMode ]:
			return self._datas[ relationMode ].get( entityFlagExt, None )
		else:
			return self._datas[ DEFAULT_RELATION_MODE ].get( entityFlagExt, None )	#指定模式下没有此entity的关系判断实例，则取通用模式下的实例
	
	def getRelationInsByCls( self, relClass ):
		"""
		根据类名获取关系实例
		"""
		if relClass not in self._clsToObj:
			try:
				relClassObj = smartImport( "ConfigObject.SpaceEntityRelation.SpaceEntityRelation:" + relClass )
			except ImportError:
				KBEDebug.ERROR_MSG( "SpaceEntityRelation class(%s) not exist!"%relClass )
				return None
			self._clsToObj[relClass] = relClassObj
		
		return self._clsToObj.get( relClass, None )
	
	def reloadConfig( self ):
		"""
		热加载配置
		"""
		pass	#因为此配置是程序维护，暂不做热更新支持


g_spaceEntityRelationLoader = SpaceEntityRelationLoader()