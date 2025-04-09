# -*- coding: utf-8 -*-
#
import random
import time
import KBEngine
import Const
import csdefine
import QuestEventDefine
from KBEDebug import *
import NPC

from ConfigObject.Trade.TradeMgr import g_tradeMgr


class NPCSoulShop( NPC.NPC ):
	"""
	英雄联盟商店NPC
	"""
	def __init__(self):
		NPC.NPC.__init__(self)
		self._guardSoulItem = {}
		self._guardSoulItem[csdefine.CAMP_TAOSIM] = {}
		self._guardSoulItem[csdefine.CAMP_DEMON] = {}
		self._pagodaSoulItem = {}
		self._pagodaSoulItem[csdefine.CAMP_TAOSIM] = {}
		self._pagodaSoulItem[csdefine.CAMP_DEMON] = {}
		
	def getGuardInfo( self, player ):
		"""获取魂卫商店数据"""
		space = self.getCurrentSpace()
		if space:
			passTime =  (time.time() - space.lifeStartTime)/60 
			guardInfos = g_tradeMgr.getAllGuardLevelByCamp(player.camp, passTime )
			for info in guardInfos:
				if info["scriptID"] in self._guardSoulItem[player.camp]:
					info.update( {"buyTime" : self.getGuardCallTime( player, info["scriptID"] ) })
				else:
					info.update( {"buyTime" : 0 })
					
			return guardInfos
		return {}
		
	def getGuardCallTime( self, player, scriptID ):
		"""获取魂卫次数"""
		cmap = player.camp
		if scriptID in self._guardSoulItem[camp]:
			return self._guardSoulItem[camp][scriptID]
		return 0
		
	def onCallGuard( self, player, scriptID ):
		"""召唤魂卫回调"""
		camp = player.camp
		if scriptID in self._guardSoulItem[camp]:
			self._guardSoulItem[camp][scriptID] += 1
		else:
			self._guardSoulItem[camp][scriptID] = 1
		
	def getPagodaInfos( self, player ):
		"""获取魂塔商店数据"""
		pagodaInfos = []
		pagodaInfos.append( self.getWayPagodaInfo( player, csdefine.YXLM_TOWER_UP ) )
		pagodaInfos.append( self.getWayPagodaInfo( player, csdefine.YXLM_TOWER_CENTER ) )
		pagodaInfos.append( self.getWayPagodaInfo( player, csdefine.YXLM_TOWER_DOWN ) )
		pagodaInfos.append( self.getWayPagodaInfo( player, csdefine.YXLM_TOWER_BASE ) )
		return pagodaInfos

	def getWayPagodaInfo( self, player, wayType ):
		"""
		获得某一路魂塔的数据
		"""
		space = self.getCurrentSpace()
		if space:
			destroyPa = []
			if player.camp == csdefine.CAMP_TAOSIM:
				destroyPa.extend( space.getXianDestroyBuildingData(wayType))
			else:
				destroyPa.extend( space.getMoDestrooyBuildingData(wayType) )
			sourcePaList = g_tradeMgr.getSourcePagoda( player.camp, wayType )
			for scriptID in list( sourcePaList ):
				if scriptID in self._pagodaSoulItem[player.camp] and wayType in self._pagodaSoulItem[player.camp][scriptID]:
					sourcePaList.remove( scriptID )
					sourcePaList.append( self._pagodaSoulItem[player.camp][scriptID][wayType] )
			return { "wayType": wayType ,"allPagoda" : sourcePaList, "deadPagoda" : destroyPa}
		return {}
		
	def canUpdateGradePagoda( self, player, oldScriptID, newScriptID, wayType ):
		"""能否升级魂塔"""
		camp = player.camp
		scriptID = g_tradeMgr.getSourcePagodaByScriptID( camp, oldScriptID, wayType )
		if scriptID in self._pagodaSoulItem[camp] and wayType in self._pagodaSoulItem[camp][scriptID] and self._pagodaSoulItem[camp][scriptID][wayType] != oldScriptID:
			# 由于客户端不同步原因导致
			player.client.CLIENT_OnRequestUpdatePagodaSoul( oldScriptID, self._pagodaSoulItem[camp][scriptID][wayType], wayType )
			return False
		
		space = self.getCurrentSpace()
		if space is None:
			return False
		idList = space.getEntityRecord( oldScriptID )
		if len(idList) == 0:				# 相关的塔，已经被摧毁
			ERROR_MSG("Can not find srcptID(%s) in the space(%s)"%(oldScriptID, space.scriptID))
			return False
			
		return True
		
	def onUpdateGradePagoda( self, player, oldScriptID, newScriptID, wayType ):
		"""升级魂塔回调"""
		camp = player.camp
		scriptID = g_tradeMgr.getSourcePagodaByScriptID( camp, oldScriptID, wayType )
		if scriptID not in self._pagodaSoulItem[camp]:
			self._pagodaSoulItem[camp][scriptID] = {}
		self._pagodaSoulItem[camp][scriptID][wayType] = newScriptID