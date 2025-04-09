# -*- coding: utf-8 -*-

import csdefine
import csconst
import TongLoader
from Tong.TongBuildFunc import Datas as tongBuildFunc

class TongBuildBase( object ):
	"""
	帮会建筑基类
	"""
	BUILD_TYPE = 0
	def __init__( self ):
		object.__init__( self )
		self.buildLevel = 1
	
	@classmethod
	def getBuildType( SELF ):
		return SELF.BUILD_TYPE
		
	def init( self, tongEntity ):
		pass
	
	def setLevel( self, tongEntity, newLevel ):
		"""
		设置建筑等级
		"""
		self.buildLevel = newLevel
		self.onLevelChange( tongEntity )
	
	def onTongLevelDown( self, tongEntity ):
		"""帮会降级"""
		pass
	
	def onLevelChange( self, tongEntity ):
		tongEntity.addRecord( csdefine.TONG_EVENT_UPGRADE_BUILD, self.BUILD_TYPE, self.buildLevel )
		for member in tongEntity.members.values():
			member.onBuildLevelChange( tongEntity, self.getBuildType(), self.buildLevel )
		
	def getMaxLevel( self, tongEntity ):		# 因为 帮会等级会降，建筑等级不会。功能按最小等级算
		maxLevel = TongLoader.getBuildMaxLevelByTongLevel( self.getBuildType(), tongEntity.level )
		return min( maxLevel, self.buildLevel )
		
	@classmethod
	def getDictFromObj( self, obj ):
		"""
		打包
		"""
		tempDict = {}
		tempDict[ "buildLevel" ] = obj.buildLevel
		tempDict[ "buildType" ] = obj.BUILD_TYPE
			
		return  tempDict
	
	@classmethod
	def createObjFromDict( self, proDict ):
		"""
		解包
		"""
		type = proDict["buildType"]
		if type in TONG_BUILD_TYPES:
			buildObj = copy.deepcopy( TONG_BUILD_TYPES[type] )
			buildObj.buildLevel = proDict["buildLevel"]
			return buildObj
		return TongBuildBase()
	
	@classmethod
	def isSameType( self, obj ):
		"""
		比较
		"""
		return isinstance( obj, TongBuildBase )

g_TongBuildBase = TongBuildBase()
		
class TongBuildYSDT( TongBuildBase ):
	"""
	议事大厅
	"""
	BUILD_TYPE = csdefine.TONG_BUILDING_TYPE_YSDT
	def __init__( self ):
		TongBuildBase.__init__( self )
		
	def onTongLevelDown( self, tongEntity ):
		"""帮会降级"""
		maxLevel = self.getMaxLevel(tongEntity)
		if self.buildLevel != maxLevel:
			for member in tongEntity.members.values():
					member.onConferenceHallLevelChange( self.getTongLimitNum(tongEntity) )
		
	def onLevelChange( self, tongEntity ):
		"""建筑等级改变时"""
		TongBuildBase.onLevelChange( self, tongEntity )
		maxLevel = self.getMaxLevel(tongEntity)
		if self.buildLevel == maxLevel:
			for member in tongEntity.members.values():
					member.onConferenceHallLevelChange( self.getTongLimitNum(tongEntity) )
		
	def getTongLimitNum( self, tong ):
		"""帮会人数上限"""
		return tongBuildFunc[self.getMaxLevel(tong)]["limitNum"]
		
	def getTongLimitGrow( self, tong ):
		"""帮会成长度上限"""
		return tongBuildFunc[self.getMaxLevel(tong)]["limitGrow"]
		
	def getSalary( self, tong, titleID ):
		"""每日俸禄，一个礼包"""
		gift = tongBuildFunc[self.getMaxLevel(tong)]["gift"]
		gifts = gift.split("|")
		if len( gifts ) == 5:
			index = max( titleID - 4, 0 )		# 前面四个管理层，领第一个礼包
			return int( gifts[index] )
		else:
			return int( gifts[titleID-1] )

class TongBuildSSD( TongBuildBase ):
	"""
	神兽殿
	"""
	BUILD_TYPE = csdefine.TONG_BUILDING_TYPE_SSD
	def __init__( self ):
		TongBuildBase.__init__( self )
		
	def getShenShouScriptID( self, tong, shenshouType ):
		"""帮会神兽ScriptID"""
		type = "shenshou_" + str( shenshouType )
		return tongBuildFunc[self.getMaxLevel(tong)][type]


class TongBuildCK( TongBuildBase ):
	"""
	仓库
	"""
	BUILD_TYPE = csdefine.TONG_BUILDING_TYPE_CK
	def __init__( self ):
		TongBuildBase.__init__( self )
		
	def init( self, tongEntity ):
		bag = self.getTongStoreBag( tongEntity )
		if bag:
			tongEntity.addTongStoreCapacity(bag * csconst.TONG_STORE_BAG_CAPACITY)
		
	def onLevelChange( self, tongEntity ):
		"""建筑等级改变时"""
		TongBuildBase.onLevelChange( self, tongEntity )
		bag = self.getTongStoreBag( tongEntity )
		if bag:
			tongEntity.addTongStoreCapacity(bag * csconst.TONG_STORE_BAG_CAPACITY)
		
	def getTongMoneyLimit( self, tong ):
		"""帮会资金上限"""
		return tongBuildFunc[self.getMaxLevel(tong)]["moneyLimit"]

	def getTongStoreBag( self, tong ):
		"""仓库解锁包裹"""
		return tongBuildFunc[self.getMaxLevel(tong)]["bag"]

class TongBuildTJP( TongBuildBase ):
	"""
	铁匠铺
	"""
	BUILD_TYPE = csdefine.TONG_BUILDING_TYPE_TJP
	def __init__( self ):
		TongBuildBase.__init__( self )
		
	def onTongLevelDown( self, tongEntity ):
		"""帮会降级"""
		maxLevel = self.getMaxLevel(tongEntity)
		if self.buildLevel != maxLevel:
			for member in tongEntity.members.values():
				member.onBuildSmithyLevelChange( maxLevel )
				
	def onLevelChange( self, tongEntity ):
		TongBuildBase.onLevelChange( self, tongEntity )
		maxLevel = self.getMaxLevel(tongEntity)
		if self.buildLevel == maxLevel:
			for member in tongEntity.members.values():
				member.onBuildSmithyLevelChange( maxLevel )
		
	def getTongDiscount( self, tong ):
		"""铁匠铺折扣"""
		return tongBuildFunc[self.getMaxLevel(tong)]["discount"]

class TongBuildSD( TongBuildBase ):
	"""
	 商店
	"""
	BUILD_TYPE = csdefine.TONG_BUILDING_TYPE_SD
	def __init__( self ):
		TongBuildBase.__init__( self )
		
	def onLevelChange( self, tongEntity ):
		TongBuildBase.onLevelChange( self, tongEntity )
		maxLevel = self.getMaxLevel(tongEntity)
		if self.buildLevel == maxLevel:
			for member in tongEntity.members.values():
				member.onBuildShopLevelChange( maxLevel )
		
	def onTongLevelDown( self, tongEntity ):
		"""帮会降级"""
		maxLevel = self.getMaxLevel(tongEntity)
		if self.buildLevel != maxLevel:
			for member in tongEntity.members.values():
				member.onBuildShopLevelChange( maxLevel )
		
class TongBuildYJY( TongBuildBase ):
	"""
	研究院
	"""
	BUILD_TYPE = csdefine.TONG_BUILDING_TYPE_YJY
	def __init__( self ):
		TongBuildBase.__init__( self )

TONG_BUILD_TYPES = {}
TONG_BUILD_TYPES[ TongBuildYSDT.getBuildType() ] = TongBuildYSDT()
TONG_BUILD_TYPES[ TongBuildSSD.getBuildType() ] = TongBuildSSD()
TONG_BUILD_TYPES[ TongBuildCK.getBuildType() ] = TongBuildCK()
TONG_BUILD_TYPES[ TongBuildTJP.getBuildType() ] = TongBuildTJP()
TONG_BUILD_TYPES[ TongBuildSD.getBuildType() ] = TongBuildSD()
TONG_BUILD_TYPES[ TongBuildYJY.getBuildType() ] = TongBuildYJY()


import copy
class TongBuildingDict( dict ):
	"""
	帮会建筑
	"""
	def __init__( self ):
		dict.__init__( self )
		
	def init( self, tongEntity ):
		self.update( copy.deepcopy( TONG_BUILD_TYPES ) )
		for build in self.values():
			build.init( tongEntity )
	
	def setLevel( self, tongEntity, buildType, newLevel ):
		self[ buildType ].setLevel( tongEntity,  newLevel )
		
	@classmethod
	def getDictFromObj( self, obj ):
		"""
		打包
		"""
		tempDict = {}
		tempDict[ "builds" ] = []
		
		for mObj in obj.values():
			tempDict[ "builds" ].append( mObj )
			
		return  tempDict
	
	@classmethod
	def createObjFromDict( self, proDict ):
		"""
		解包
		"""
		obj = TongBuildingDict()
		for mObj in proDict[ "builds" ]:
			obj[ mObj.getBuildType() ] = mObj
			
		return obj
	
	@classmethod
	def isSameType( self, obj ):
		"""
		比较
		"""
		return isinstance( obj, TongBuildingDict )
		
	def getBuildLevel(self):
		levelDict = []
		levelDict.append( self[csdefine.TONG_BUILDING_TYPE_YSDT].buildLevel )
		levelDict.append( self[csdefine.TONG_BUILDING_TYPE_SSD].buildLevel )
		levelDict.append( self[csdefine.TONG_BUILDING_TYPE_CK].buildLevel )
		levelDict.append( self[csdefine.TONG_BUILDING_TYPE_TJP].buildLevel )
		levelDict.append( self[csdefine.TONG_BUILDING_TYPE_SD].buildLevel )
		levelDict.append( self[csdefine.TONG_BUILDING_TYPE_YJY].buildLevel )
		return levelDict
		
	def onTongLevelDown( self, tongEntity ):
		"""帮会降级"""
		for build in self.values():
			build.onTongLevelDown( tongEntity )

g_TongBuildingDict = TongBuildingDict()
	
	
	