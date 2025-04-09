# -*- coding: utf-8 -*-
import csdefine
import KBEDebug
import KBEngine
import Const
import KST
import csstatus
from CoreObject import MgrPersistentObject

from ConfigObject.Crond.CrondDatas import CrondDatas
g_CrondDatas = CrondDatas.instance()


class CampActivityFrozenFightMgr( MgrPersistentObject.MgrPersistentObject ):
	"""
	冰雪之战管理器
	"""
	def __init__( self ):
		MgrPersistentObject.MgrPersistentObject.__init__( self )
		self.register()
		self._key = 0
		self._timer = {}
		# 仙魔阵营匹配队列
		self._taosimMatchQueue = {}			# { level : [playerMB,...]}
		self._demonMatchQueue = {}			
		self._matchQueue = {}
		self._matchQueue.update( { csdefine.CAMP_TAOSIM : self._taosimMatchQueue } )
		self._matchQueue.update( { csdefine.CAMP_DEMON : self._demonMatchQueue } )
		# 准备队列
		self._taosimReadyQueue = {}			# { level : [[playerMB,...],...]}
		self._demonReadyQueue = {}
		self._readyQueue = {}
		self._readyQueue.update( { csdefine.CAMP_TAOSIM : self._taosimReadyQueue } )
		self._readyQueue.update( { csdefine.CAMP_DEMON : self._demonReadyQueue } )
		# 传送队列
		self._teleportQueue = {}			# { key: [playerMB...] }
		self.onCompleteInit()
		
	def register( self ):
		"""
		注册
		"""
		taskEvents = { "CampFrozenFightCopyMgr_Notice":"onActiveNotice",
						"CampFrozenFightCopyMgr_Start":"onActiveStart",
						"CampFrozenFightCopyMgr_End":"onActiveEnd"
		 }
		for taskName, callbackName in taskEvents.items():
			for scriptID, cmd in g_CrondDatas.getCrondTaskCmds(taskName):
		 		KBEngine.globalData["CrondManager"].addScheme( scriptID, cmd, self, callbackName, -1,() )

	def onActiveNotice( self, cmd ):
		"""
		活动公告
		"""
		KST.g_baseAppEntity.globalWold( csstatus.ACTIVITY_CAMP_FROZEN_FIGHT_NOTICE, "" )

	def onActiveStart( self, cmd ):
		"""
		define method
		活动开始
		"""
		KBEngine.globalData["FrozenFight"] = 1
		KST.g_baseAppEntity.globalWold( csstatus.ACTIVITY_CAMP_FROZEN_FIGHT_START, "" )

	def onActiveEnd( self, cmd ):
		"""
		define method
		活动结束
		"""
		KBEngine.globalData["FrozenFight"] = 0
		self._key = 0
		for queue in self._matchQueue.values():
			for mb in queue.values():
				mb.client.CLIENT_OnFrozenFightActivityEnd()
		for queue in self._readyQueue.values():
			for allMbList in queue.values():
				for sameMbList in allMbList:
					for mb in sameMbList:
						mb.onFrozenFightActivityEnd()
		self._taosimMatchQueue.clear()
		self._demonMatchQueue.clear()
		self._taosimReadyQueue.clear()
		self._demonReadyQueue.clear()
		self._teleportQueue.clear()
		for timer in self._timer:
			self.popTimer( timer )
		self._timer.clear()
		KST.g_baseAppEntity.globalWold( csstatus.ACTIVITY_CAMP_FROZEN_FIGHT_END, "" )

	def signIn( self, playerMB, camp, level ):
		"""
		define method
		登记报名
		"""
		if not KBEngine.globalData.get( "FrozenFight", 0 ):return
		levelSec = level//10
		
		queueDict = self._matchQueue[camp]
		if not levelSec in queueDict:
			queueDict[levelSec] = []
		queueDict[levelSec].append( playerMB )
		playerMB.client.CLIENT_OnEnterFrozenFightMatchQueue()
		if len( queueDict[levelSec] ) >= Const.CAMP_FROZEN_FIGHT_MATCH_NUM:
			self._enterReadyQueue( camp, levelSec )
		
	def cancelMatching( self, playerMB, camp, level ):
		"""
		define method
		取消匹配
		"""
		levelSec = level//10
		if levelSec in self._matchQueue[camp]:
			for mb in self._matchQueue[camp][levelSec]:
				if mb.id == playerMB.id:
					self._matchQueue[camp][levelSec].remove( mb )
					return
					
		if levelSec in self._readyQueue[camp]:
			for mbList in self._readyQueue[camp][levelSec]:
				for mb in mbList:
					if mb.id == playerMB.id:
						self._readyQueue[camp][levelSec].remove( mbList )
						mbList.remove( mb )
						for mb in mbList:
							self.signIn( mb, camp, levelSec )
		
		
	def frozenFight_onPlayerLoginOff( self, playerMB, camp, level ):
		"""
		define method
		玩家下线
		"""
		self.cancelMatching( playerMB, camp, level )
		
	def _enterReadyQueue( self, camp, levelSec ):
		"""
		进入准备阶段
		开始匹配敌方
		"""
		if not levelSec in self._readyQueue[camp]:
			self._readyQueue[camp][levelSec] = []
			
		queue = self._matchQueue[camp].pop( levelSec )
		for playerMB in queue:
			playerMB.client.CLIENT_OnEnterFrozenFightReadyQueue()
		
		oppiseCamp = self._getOpposeCamp( camp )
		if levelSec in self._readyQueue[oppiseCamp] and len(self._readyQueue[oppiseCamp][levelSec] ) > 0:
			queue.extend( self._readyQueue[oppiseCamp][levelSec].pop(0) )
			self._enterTelPortQueue( queue )
		else:
			self._readyQueue[camp][levelSec].append( queue )
		
	def _enterTelPortQueue( self, queue ):
		"""
		匹配成功
		准备进入
		"""
		self._key += 1
		for playerMB in queue:
			playerMB.client.CLIENT_OnEnterFrozenFightTelPortQueue( self._key )
		self._teleportQueue[self._key] = queue
		self._addTeleportTimer()
		
	def _getOpposeCamp( self, camp ):
		"""获取对立阵营"""
		if camp == csdefine.CAMP_TAOSIM:
			return csdefine.CAMP_DEMON
		else:
			return csdefine.CAMP_TAOSIM
		
	def beginEnterFrozenFight( self, playerMB, key ):
		"""
		define method
		开始进入战场
		"""
		if key in self._teleportQueue:
			for mb in self._teleportQueue[key]:
				if mb.id == playerMB.id:
					self._teleportQueue[key].remove( mb )
		
	def _addTeleportTimer( self ):
		"""添加准备阶段timer"""
		timer = self.addTimerCallBack( Const.FROZEN_FIGHT_READY_STAGE_TIMER_SECOND, "_teleportTimeOver", ( self._key, ) )
		self._timer[self._key] = timer
		
	def _teleportTimeOver( self, key ):
		"""
		传送阶段结束
		"""
		self._timer.pop( key )
		if key in self._teleportQueue:
			for mb in self._teleportQueue[key]:
				mb.telportFrozenFightActivity( key )
			self._teleportQueue.pop(key)
