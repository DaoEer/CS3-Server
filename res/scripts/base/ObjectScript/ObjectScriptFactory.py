# -*- coding: utf-8 -*-

import KBEngine
#script
import Singleton
import KBEDebug

from ObjectScript import Space
from ObjectScript import SpaceDomain
from ObjectScript import BunchSpace
from ObjectScript import BunchSpaceDomain

from ObjectScript.NPC import NPCFactory
from ObjectScript.Monster import MonsterFactory
from ObjectScript.Pet import PetFactory

class ObjectScriptFactory( Singleton.Singleton ):
	"""
	游戏对象script工厂类
	"""
	def __init__( self ):
		SpaceDomain.loadObject()
		Space.loadObject()
		BunchSpaceDomain.loadObject()
		BunchSpace.loadObject()
		
		NPCFactory.g_NPCFactory.loadData( "GameObject/NPC.json" )
		MonsterFactory.g_monsterFactory.loadData( "GameObject/Monster.json" )
		PetFactory.g_petFactory.loadData( "GameObject/Pet.json" )

	def getSpaceDomainObject( self, scriptID ):
		#获取SpaceDomain 对象
		return SpaceDomain.getObect( scriptID )

	def getAllSpaceDomian( self ):
		#获取所有SpaceDomain
		return SpaceDomain.getAllSpaceDomian()

	def getSpaceObject( self, scriptID ):
		#获取SpaceObject 对象
		return Space.getObect( scriptID )
		
	def getSpaceConsume(self, scriptID):
		#获取地图消耗
		return Space.getSpaceConsume(scriptID)
		
	def getAllNoBalanceSpace(self):
		#获取不参与负载均衡的space集合
		return Space.getAllNoBalanceSpace()
		
	def getAllNoBalanceCellAPPList(self):
		#获取不参与负载均衡的cellapp
		return Space.getAllNoBalanceCellAPP()

	def getBunchSpaceDomainObject( self, scriptID ):
		#获取副本串domain对象
		return BunchSpaceDomain.getObect( scriptID )

	def getAllBunchSpaceDomian( self ):
		#获取所有BunchSpaceDomain
		return BunchSpaceDomain.getAllBunchSpaceDomian()

	def getBunchSpaceObject( self, scriptID ):
		#获取SpaceDomain 对象
		return BunchSpace.getObect( scriptID )
	
	def getNPCObject( self, scriptID ):
		#获取Monster的对象
		return NPCFactory.g_NPCFactory.getObject( scriptID )
		
	def getMonsterObject( self, scriptID ):
		#获取Monster的对象
		return MonsterFactory.g_monsterFactory.getObject( scriptID )
			
	def createNPC( self, scriptID, spaceCell, position, direction, params  ):
		"""
		创建NPC,必需有base
		"""
		KBEDebug.DEBUG_MSG("---------------ObjectScriptFactory::createNPC( scriptID:%s, spaceEntityID:%d, position:%s )--------------------"%(scriptID,spaceCell.id, str(position)))
		params[ "spaceCell" ] = spaceCell
		params[ "position" ] = position
		params[ "direction" ] = direction
		npcObject = self.getNPCObject( scriptID )
		if npcObject:
			entity = npcObject.createLocalEntity( params  )
			return entity
		else:
			KBEDebug.ERROR_MSG( "Can not find scriptID(%s), please check!!" %scriptID )
			return None
			
	def createMonster( self, scriptID, spaceCell, position, direction, params  ):
		"""
		创建Monster,必需有base
		"""
		KBEDebug.DEBUG_MSG("---------------ObjectScriptFactory::createMonster( scriptID:%s, spaceEntityID:%d, position:%s )--------------------"%(scriptID,spaceCell.id, str(position)))
		params[ "spaceCell" ] = spaceCell
		params[ "position" ] = position
		params[ "direction" ] = direction
		monsterObject = self.getMonsterObject( scriptID )
		if monsterObject:
			entity = monsterObject.createLocalEntity( params  )
			return entity
		else:
			KBEDebug.ERROR_MSG( "Can not find scriptID(%s), please check!!" %scriptID )
			return None
	
#global instance
g_objFactory = ObjectScriptFactory()
