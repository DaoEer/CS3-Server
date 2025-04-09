# -*- coding: utf-8 -*-

import KBEngine
import Math
#script
import Singleton
import KBEDebug

from ObjectScript import Space
from ObjectScript import BunchSpace
from ObjectScript.NPC import NPCFactory
from ObjectScript.Monster import MonsterFactory
from ObjectScript.SpellBox import SpellBoxFactory
from ObjectScript.Trap import TrapFactory
from ObjectScript.Pet import PetFactory
from ObjectScript.Scene import SceneFactory
from ObjectScript import Stall

class ObjectScriptFactory( Singleton.Singleton ):
	"""
	游戏对象script工厂类
	"""
	def __init__( self ):
		Singleton.Singleton.__init__( self )
		Space.loadObject()
		BunchSpace.loadObject()
		Stall.loadObject()
		NPCFactory.g_NPCFactory.loadData( "GameObject/NPC.json" )
		MonsterFactory.g_monsterFactory.loadData( "GameObject/Monster.json" )
		SpellBoxFactory.g_spellBoxFactory.loadData( "GameObject/SpellBox.json", "GameObject/MultiAreaSpellBox.json" )
		TrapFactory.g_trapFactory.loadData( "GameObject/Trap.json" )
		PetFactory.g_petFactory.loadData( "GameObject/Pet.json" )
		SceneFactory.g_SceneFactory.loadData( "GameObject/SceneObject.json" )
		
	def reloadConfig( self ):
		"""
		热加载配置支持
		"""
		Space.loadObject()
		BunchSpace.loadObject()
		Stall.loadObject()
		NPCFactory.g_NPCFactory.loadData( "GameObject/NPC.json" )
		MonsterFactory.g_monsterFactory.loadData( "GameObject/Monster.json" )
		SpellBoxFactory.g_spellBoxFactory.loadData( "GameObject/SpellBox.json", "GameObject/MultiAreaSpellBox.json" )
		TrapFactory.g_trapFactory.loadData( "GameObject/Trap.json" )
		PetFactory.g_petFactory.loadData( "GameObject/Pet.json" )
		SceneFactory.g_SceneFactory.loadData( "GameObject/SceneObject.json" )
	
	def getSpaceObject( self, scriptID ):
		#获取Space 对象
		return Space.getObject( scriptID )
		
	def getAllNoBalanceCellAPPList(self):
		#获取不参与负载均衡的cellapp
		return Space.getAllNoBalanceCellAPP()
	
	def getBunchSpaceObject( self, scriptID ):
		#获取BunchSpace 对象
		return BunchSpace.getObject( scriptID )
	
	def getNPCObject( self, scriptID ):
		#获取Monster的对象
		return NPCFactory.g_NPCFactory.getObject( scriptID )
		
	def getMonsterObject( self, scriptID ):
		#获取Monster的对象
		return MonsterFactory.g_monsterFactory.getObject( scriptID )
	
	def getSpellBoxObject( self, scriptID ):
		#获取Monster的对象
		return SpellBoxFactory.g_spellBoxFactory.getObject( scriptID )

	def getTrapBoxObject( self, scriptID ):
		#获取Trap的对象
		return TrapFactory.g_trapFactory.getObject( scriptID )
		
	def getSceneObject( self, scriptID ):
		#获取场景物件的对象
		return SceneFactory.g_SceneFactory.getObject( scriptID )

	def getStallObject( self, scriptID ):
		#获得Stall的对象
		return Stall.getObject( scriptID )
	
	def getObject( self, scriptID ):
		"""
		搜索效率，做个简单优化
		"""
		if scriptID.startswith("1"):
			return self.getNPCObject( scriptID )
		elif scriptID.startswith("2"):
			return self.getMonsterObject( scriptID )
		elif scriptID.startswith("3"):
			return self.getTrapBoxObject( scriptID )
		elif scriptID.startswith("4"):
			return self.getSpellBoxObject( scriptID )
		elif scriptID.startswith("5"):
			return self.getSceneObject( scriptID )
			
	def createEntity( self, scriptID, spaceEntity, position, direction, params  ):
		"""
		"""
		KBEDebug.DEBUG_MSG("---------------ObjectScriptFactory::createEntity( scriptID:%s, spaceID:%d, position:%s )--------------------"%(scriptID,spaceEntity.spaceID, str(position)))
		object = self.getObject( scriptID )
		if object:
			entity = object.createEntity( spaceEntity, tuple(Math.Vector3(position)), direction, params  )
			return entity
		else:
			KBEDebug.ERROR_MSG( "Space(%s) Create Can not find scriptID(%s), please check!!" %( spaceEntity.getCurrentSpaceScriptID(),scriptID ) )
			return None
#-------global instance--------------------------------------------------
g_objFactory = ObjectScriptFactory()





