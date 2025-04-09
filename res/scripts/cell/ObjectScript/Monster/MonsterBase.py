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
import Math
import math
import time
import Const
import csdefine
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

		self.attackRange = 0.0
		self.isServerAttackTrap = False							# 主动攻击陷阱类型：默认为客户端陷阱
		self.attackTrapShape = csdefine.TRAP_SHAPE_SQUARE		# 主动攻击陷阱形状：默认为方形（配为服务器端陷阱时可以减少消耗）
	
	def initData( self, data ):
		"""
		初始化数据
		@param data: dict
		"""
		NPCBaseScript.NPCBaseScript.initData( self, data )
		MonsterPropertyLoader.MonsterPropertyLoader.initData(self,data)
		
		self.minLv		= data["MinLevel"]
		self.maxLv		= data["MaxLevel"]
		self.ownership = int(data["ownership"])
#		self._xiuweiAtt= data.get( "XiuweiAttr", 0.0 )
		
		if data["attackRange"]:
			rangeParam = str(data["attackRange"]).split("|")
			self.attackRange = float(rangeParam[0])
			if len(rangeParam) > 1:
				self.isServerAttackTrap = False if int(rangeParam[1]) == 0 else True
			
			if self.attackRange > 0:
				if data["attackTrapShape"] not in csdefine.TRAP_SHAPE_LIST:
					KBEDebug.ERROR_MSG("Monster(%s) attack trap shape error! %i" % (self.scriptID, data["attackTrapShape"]))
				else:
					self.attackTrapShape = data["attackTrapShape"]
		
	def onClientReady(self, selfEntity):
		"""
		"""
		pass	
		
	def getEntityProperties( self, params ):
		return MonsterPropertyLoader.MonsterPropertyLoader.getEntityProperties( self, params )
		
	def initEntity( self, selfEntity ):
		"""
		virtual method.
		怪物初始化
		"""
		pass
	
	def getAttackTrapParams( self ,selfEntity):
		return ( selfEntity.isServerAttackTrap, selfEntity.attackTrapShape, str(selfEntity.attackRange) )
	
	def createEntity( self, spaceEntity, position, direction, params ) :
		"""
		创建entity
		"""
		if not 'level' in params:
			if spaceEntity.monsterUseSpaceLevel:		#使用副本等级赋值怪物等级（CST-2880）
				params["level"] = spaceEntity.spaceLevel
			else:
				params["level"] = random.randint( self.minLv, self.maxLv )
			
#		params["xiuwei"] = int( self._xiuweiAtt * g_XiuweiMgr.getMonsterXiuwei( params["level"] ) )
#		params["xiuweiLevel"] = g_XiuweiMgr.getMonsterXiuweiLevel( self._xiuweiAtt )
		return NPCBaseScript.NPCBaseScript.createEntity( self, spaceEntity, position, direction, params )
	
	def onAddEnemy( self, selfEntity, entityID ):
		"""
		"""
		pass
		
	def onRemoveEnemy( self, selfEntity, entityID ):
		"""
		"""
		pass
	
	def onHPChanged( self, selfEntity, oldValue ):
		"""
		virtual method
		血量改变
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
		
	def addBlow(self, selfEntity, windDirction, windSpeed, srcEntityID = None ):
		"""
		添加风效果
		"""
		if not selfEntity.hasTimer( selfEntity.windID ):
			yaw = windDirction[2] / 180 * math.pi
			selfEntity.blowTime = time.time()
			selfEntity.windID = selfEntity.addTimerRepeatForScript(Const.BLOW_WIND_TICK_TIME, "addBlowByTick", ( yaw, windSpeed ))
		if srcEntityID:
			srcEntity = KBEngine.entities.get( srcEntityID )
			if( srcEntity and srcEntity.client ):
				srcEntity.clientEntity( selfEntity.id ).CLIENT_addMonsterBlow( windDirction, windSpeed )
		else:
			selfEntity.allClients.CLIENT_addMonsterBlow( windDirction, windSpeed )

	def addBlowByTick(self, selfEntity, yaw, windSpeed ):
		""""""
		blowTime = time.time()
		delTime = blowTime - selfEntity.blowTime
		selfEntity.blowTime = blowTime
		dist = delTime * windSpeed
		distVecotr = Math.Vector3( dist * math.sin(yaw), 0, dist * math.cos(yaw) )
		selfEntity.position += distVecotr
		
	def endBlow( self, selfEntity ):
		"""
		结束风效果
		"""
		if selfEntity.hasTimer( selfEntity.windID ):
			selfEntity.popTimer( selfEntity.windID )
		selfEntity.windID = 0
		selfEntity.allClients.CLIENT_endMonsterBlow()