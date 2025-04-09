# -*- coding: utf-8 -*-
import os
import platform
import KBEngine
import Singleton
import Const
import KBEDebug

PLATFORM_NAVMESH_PATH = "res/space/A_PLATFORM_NAVIMESH"


class NavmeshLoader( Singleton.Singleton ):
	"""
	寻路网格数据加载类
	"""
	def __init__( self ):
		"""
		要初始化的配置放在这行进行加载
		"""
		self.currentLoadSpaceMapping = 0
		self.loadMappingList = []
	
	def init( self ):
		"""
		初始化
		"""
		self.loadAllPlatformNavmesh()
	
	def loadAllPlatformNavmesh( self ):
		"""
		加载所有移动平台的寻路数据
		"""
		for filename in os.listdir( PLATFORM_NAVMESH_PATH ):
			if not os.path.isfile( PLATFORM_NAVMESH_PATH + "/" + filename ):
				KBEngine.loadGeometryMapping( None, "space/A_PLATFORM_NAVIMESH/" + filename, {} )
	
	def loadSpaceNavmesh( self, spaceID, navmeshPath ):
		"""
		添加要加载地图资源
		"""
		self.loadMappingList.append( ( spaceID, navmeshPath ) )
		if self.currentLoadSpaceMapping == 0 and len( self.loadMappingList ):
			self.loadNavmesh()
	
	def loadNavmesh( self ):
		"""
		加载地图网格
		"""
		if len( self.loadMappingList ):
			spaceID, navmeshPath = self.loadMappingList.pop( 0 )
			self.currentLoadSpaceMapping = spaceID
			KBEDebug.INFO_MSG("spaceID = %i, navmeshPath = %s" %(spaceID, navmeshPath))
			try:
				KBEngine.addSpaceGeometryMapping( spaceID, None, navmeshPath, True, {} )
			except:
				#到这里，最大的可能就是地图已经销毁了
				KBEDebug.INFO_MSG( "loader Navmesh failure! spaceID = %i, navmeshPath = %s" %(spaceID, navmeshPath) )
				self.loadNavmeshOver() #继续加载下一个

	def loadNavmeshOver( self, spaceID ):
		"""
		加载完一个地图的寻路数据
		"""
		if spaceID != self.currentLoadSpaceMapping:
			return
		
		spaceBaseKey = Const.GET_SPACE_CELLAPP_KEY( spaceID )
		if spaceBaseKey in KBEngine.cellAppData:
			KBEngine.cellAppData[ spaceBaseKey ].cell.spawnPointStartLoader()
			KBEngine.cellAppData[ spaceBaseKey ].cell.onSpaceInitLoadOver()
			
		self.currentLoadSpaceMapping = 0
		self.loadNavmesh()
		
	def stopLoadNavmeshOver( self, spaceID ):
		"""
		space的导航数据未加载完毕的情况下直接关闭走这里
		"""
		#有可能还没开始加载导航数据
		for loadMapping in self.loadMappingList:
			if loadMapping[0] == spaceID:
				self.loadMappingList.remove(loadMapping)
				break
		
		if spaceID != self.currentLoadSpaceMapping:
			return
		
		self.currentLoadSpaceMapping = 0
		self.loadNavmesh()
		
	def reloadConfig( self ):
		"""
		配置支持热更新
		"""
		self.loadAllPlatformNavmesh()

	def calcNavmeshLayers(self, navmeshPath):
		"""
		计算导航层数
		"""
		fileStr = "res/" + navmeshPath
		if platform.system() != "Windows":
			fileStr = fileStr.replace("\\", "/")
			
		count = 0
		for filename in os.listdir( fileStr ):
			if filename.endswith(".navmesh"):
				count += 1
		return count

#-------global instance--------------------------------------------------
g_navmeshLoader = NavmeshLoader()