# -*- coding: utf-8 -*-

"""
用于服务器entity类型派生基类
"""


import KBEngine
#script
import CoreInterface.ECBProximityInterface as ECBProximityInterface
import CoreInterface.EntityDataValidateInterface as EntityDataValidateInterface
import CoreInterface.EntitiesInRangeInterface as EntitiesInRangeInterface
import csdefine

import KBEDebug

class EntityObject( KBEngine.Entity, ECBProximityInterface.ECBProximityInterface, EntityDataValidateInterface.EntityDataValidateInterface, EntitiesInRangeInterface.EntitiesInRangeInterface ):
	"""
	引擎Entity封装类
	"""
	def __init__( self ):
		self.setSelfEntityFlag()
		self.setSelfEntityFlagExt()
		ECBProximityInterface.ECBProximityInterface.__init__( self )
		EntityDataValidateInterface.EntityDataValidateInterface.__init__( self )
		EntitiesInRangeInterface.EntitiesInRangeInterface.__init__( self )
		self.isSpaceGone = False


	def setSelfEntityFlag(self):
		"""
		virtual method
		"""
		self.setEntityFlag(csdefine.ENTITY_FLAG_UNKNOWN)

	def setSelfEntityFlagExt(self):
		"""
		virtual method
		"""
		self.setEntityFlagExt(csdefine.ENTITY_FLAG_EXT_UNKNOWN)

	def getClient( self ):
		"""
		获取client
		"""
		if hasattr(self, "client") and self.client:
			return self.client
		return None
		
	def getAllClients( self ):
		"""
		获取allClients
		"""
		if hasattr(self, "allClients") and self.allClients:
			return self.allClients
		return None
	
	def setEntityFlag( self, entityFlag ):
		"""
		设置entity的类型
		"""
		self.entityFlag = entityFlag
	
	def getEntityFlag( self ):
		return self.entityFlag
		
	def isEntityFlag( self, entityFlag ):
		return self.entityFlag == entityFlag

	#二级标识
	def setEntityFlagExt( self, entityFlagExt ):
		"""
		设置entity的类型
		"""
		self.entityFlagExt = entityFlagExt

	def getEntityFlagExt(self):
		return self.entityFlagExt

	def isEntityFlagExt( self, entityFlagExt ):
		return self.entityFlagExt == entityFlagExt
	
	def onSpaceGone( self ):
		"""
		KBEngine callback
		副本销毁
		"""
		self.isSpaceGone = True
		self.destroy()
	
	def isOutOwnerAOI( self, entity ):
		"""
		判断一个entity是否在我的AOI之外
		entity必需是玩家，只有玩家才AOI
		"""
		if entity is None:
			return True
		elif not entity.isReal() or entity.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
			return True
		elif self.spaceID != entity.spaceID:
			return True
		elif not self in entity.entitiesInView():
			return True
		return False
		
	def navmeshRaycast( self, srcPosition, dstPosition ):
		"""
		由源坐标向目的坐标射出一道射线，返回碰撞到的坐标点。 
		"""
		if self.hasParent(): 				# CST-7959
			srcLocalPos = self.parent.positionWorldToLocal( srcPosition )
			dstLocalPos = self.parent.positionWorldToLocal( dstPosition )
			posList = KBEngine.navmeshRaycast( self.parent.getNavmeshPath(), self.layer, 0xffff, srcLocalPos, dstLocalPos )
			if posList:
				posList = [ self.parent.positionLocalToWorld(posList[0]) ]
			return posList
			
		else:
			return KBEngine.raycast( self.spaceID, self.layer, srcPosition, dstPosition )
