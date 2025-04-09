# -*- coding: utf-8 -*-
#import KBEngine


"""
usage:
	怪物对象script类

attribute:
	objectType

member function:
	getObjectType
	getName

callback:
	pass

"""


#python
import random
#engine
import KBEngine
#script

import KBEDebug
from XiuweiLoader import g_XiuweiMgr
import ObjectScript.ObjectScriptBase.NPCBaseScript as NPCBaseScript
from ObjectScript.Monster import MonsterPropertyLoader

class MonsterBase( NPCBaseScript.NPCBaseScript, MonsterPropertyLoader.MonsterPropertyLoader ):
	"""
	怪物对象script类
	"""
	def __init__( self ):
		NPCBaseScript.NPCBaseScript.__init__( self )
		MonsterPropertyLoader.MonsterPropertyLoader.__init__( self )
		
		self.minLv			= 0
		self.maxLv			= 0
#		self._xiuweiAtt	= 0.0					# 怪物修为属性比率的计算
	
	def initData( self, data ):
		"""
		初始化数据
		@param data: dict
		"""
		NPCBaseScript.NPCBaseScript.initData( self, data )
		MonsterPropertyLoader.MonsterPropertyLoader.initData(self,data)
		
		self.minLv		= data["MinLevel"]
		self.maxLv		= data["MaxLevel"]
#		self._xiuweiAtt= data.get( "XiuweiAttr", 0.0 )
	
	def getEntityProperties( self, params ):
		return MonsterPropertyLoader.MonsterPropertyLoader.getEntityProperties( self, params )
		
	def createLocalEntity( self, params ) :
		"""
		创建entity
		"""
		if not 'level' in params:
			params["level"] = random.randint( self.minLv, self.maxLv )
			
#		params["xiuwei"] = int( self._xiuweiAtt * g_XiuweiMgr.getMonsterXiuwei( params["level"] ) )
#		params["xiuweiLevel"] = g_XiuweiMgr.getMonsterXiuweiLevel( self._xiuweiAtt )
#		
		return NPCBaseScript.NPCBaseScript.createLocalEntity( self, params )
	
	def onAddEnemy( self, selfEntity, entityID ):
		"""
		"""
		pass
		
	def onRemoveEnemy( self, selfEntity, entityID ):
		"""
		"""
		pass
	
	def onEnterFree( self, selfEntity ):
		"""
		virtual method
		进入自由状态
		"""
		pass
		
	def onLeaveFree( self, selfEntity ):
		"""
		virtual method
		离开自由状态
		"""
		pass
	
	def onEnterFight( self, selfEntity ):
		"""
		virtual method
		进入战斗
		"""
		pass
		
	def onLeaveFight( self, selfEntity ):
		"""
		virtual method
		离开战斗
		"""
		pass
	
	def onEnterDead( self, selfEntity ):
		"""
		virtual method
		进入死亡状态
		"""
		pass
		
	def onLeaveDead( self, selfEntity ):
		"""
		virtual method
		离开死亡状态
		"""
		pass
		
	def onEnterPead( self, selfEntity ):
		"""
		virtual method
		进入未决状态
		"""
		pass
		
	def onLeavePead( self, selfEntity ):
		"""
		virtual method
		离开未决状态
		"""
		pass
		
	def onEnterWarn( self, selfEntity ):
		"""
		virtual method
		进入警戒状态
		"""
		pass
		
	def onLeaveWarn( self, selfEntity ):
		"""
		virtual method
		离开警戒状态
		"""
		pass
		
	def onEnterReset( self, selfEntity ):
		"""
		virtual method
		进入重置状态
		"""
		pass
		
	def onLeaveReset( self, selfEntity ):
		"""
		virtual method
		离开重置状态
		"""
		pass