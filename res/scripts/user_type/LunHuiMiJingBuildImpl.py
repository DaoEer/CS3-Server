# -*- coding: utf-8 -*-

import KBEDebug
import csdefine

class LunHuiMiJingBuildImpl(dict):

	def __int__(self):
		dict.__init__(self)
		self.ownSpaceType = csdefine.SPACE_TYPE_NONE			# 占领地图类型
		self.builds = {}
		
	def occupySpace( self, spaceType ):
		"""占领地图"""
		self.ownSpaceType = spaceType
		
	def isOccupySpaceType( self, spaceType ):
		"""是否占据 地图"""
		return self.ownSpaceType == spaceType
		
	def resetBuilds(self, buildDict):
		"""重新设置建筑等级"""
		self.builds = buildDict
		
	def getBuildLevel(self, buildType):
		"""
		获取建筑等级
		"""
		if self.isOccupySpaceType( csdefine.SPACE_TYPE_PUBLIC ):
			return self.builds.get( csdefine.LHMJ_BUIILD_LING_QUAN, 1)
		return self.builds.get(buildType, 1)
		
	def addBuildLevel(self, player, buildType):
		"""升级建筑"""
		if not buildType in self.builds:
			self.builds[buildType] = 1
		self.builds[buildType] += 1
		self.onBuildLevelChange(player, buildType, self.builds[buildType])
		
	def setBuildLevel(self, player, buildType, level):
		"""设置建筑"""
		if not buildType in self.builds:
			self.builds[buildType] = 1
		self.builds[buildType] = level
		self.onBuildLevelChange(player, buildType, level)
		
	def onBuildLevelChange(self, player, buildType, newLevel):
		"""建筑等级改变"""
		if self.isOccupySpaceType( csdefine.SPACE_TYPE_PRIVATE ):
			player.client.CLIENT_OnLHMJBuildLevelChange(buildType, newLevel)
		
	def getPetFenceMax( self ):
		"""获取 兽栏最大容量"""
		return self.getBuildLevel(csdefine.LHMJ_BUIILD_SHOU_LAN) + 1
		
	def onJadeUpgrade(self, level):
		"""玲珑玉令升级"""
		# 用灵泉的等级代表 玲珑玉令的等级
		self.builds[csdefine.LHMJ_BUIILD_LING_QUAN] = level

	def getDictFromObj(self, obj):
		"""
		The method converts a wrapper instance to a FIXED_DICT instance.

		@param obj: The obj parameter is a wrapper instance.
		@return: This method should return a dictionary(or dictionary-like object) that contains the same set of keys as a FIXED_DICT instance.
		"""
		return {"ownSpaceType" : obj.ownSpaceType, "builds" : obj.builds}

	def createObjFromDict(self, dict):
		"""
		his method converts a FIXED_DICT instance to a wrapper instance.

		@param dict: The dict parameter is a FIXED_DICT instance.
		@return: The method should return the wrapper instance constructed from the information in dict.
		"""
		obj=self.__class__()
		obj.ownSpaceType=dict["ownSpaceType"]
		obj.builds=dict["builds"]
		return obj

	def isSameType(self, obj):
		"""
		This method check whether an object is of the wrapper type.

		@param obj: The obj parameter in an arbitrary Python object.
		@return: This method should return true if obj is a wrapper instance.
		"""
		if obj is None: return False
		return isinstance(obj, LunHuiMiJingBuildImpl)


instance = LunHuiMiJingBuildImpl()
