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


class NPCSoulShopLBCPVP( NPC.NPC ):
	"""
	练兵场PVP NPC
	"""
	def __init__(self):
		NPC.NPC.__init__(self)
		self._guardSoulItem = {}
		self._guardSoulItem[csdefine.BELONG_SIDE_ATTACK] = {}
		self._guardSoulItem[csdefine.BELONG_SIDE_PROTECT] = {}
		self._pagodaSoulItem = {}
		self._pagodaSoulItem[csdefine.BELONG_SIDE_ATTACK] = {}
		self._pagodaSoulItem[csdefine.BELONG_SIDE_PROTECT] = {}
		
	def getGuardInfo( self, player ):
		"""获取魂卫商店数据"""
		space = self.getCurrentSpace()
		if space:
			passTime = (time.time() - space.lifeStartTime)/60
			belongSide = player.getBelongSide()
			camp = csdefine.CAMP_TAOSIM if belongSide == csdefine.BELONG_SIDE_ATTACK else csdefine.CAMP_DEMON
			guardInfos = g_tradeMgr.getAllGuardLevelByCamp(camp, passTime)
			for info in guardInfos:
				if info["scriptID"] in self._guardSoulItem[belongSide]:
					info.update( {"buyTime" : self.getGuardCallTime( player, info["scriptID"] ) })
				else:
					info.update( {"buyTime" : 0 })
					
			return guardInfos
		return {}
		
	def getGuardCallTime( self, player, scriptID ):
		"""获取魂卫次数"""
		belongSide = player.getBelongSide()
		if scriptID in self._guardSoulItem[belongSide]:
			return self._guardSoulItem[belongSide][scriptID]
		return 0
		
	def onCallGuard( self, player, scriptID ):
		"""召唤魂卫回调"""
		belongSide = player.getBelongSide()
		if scriptID in self._guardSoulItem[belongSide]:
			self._guardSoulItem[belongSide][scriptID] += 1
		else:
			self._guardSoulItem[belongSide][scriptID] = 1
		
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
			belongSide = player.getBelongSide()
			camp = csdefine.CAMP_TAOSIM if belongSide == csdefine.BELONG_SIDE_ATTACK else csdefine.CAMP_DEMON
			if belongSide== csdefine.BELONG_SIDE_ATTACK:
				destroyPa.extend( space.getXianDestroyBuildingData(wayType))
			else:
				destroyPa.extend( space.getMoDestrooyBuildingData(wayType) )
			sourcePaList = g_tradeMgr.getSourcePagoda( camp, wayType )
			for scriptID in list( sourcePaList ):
				if scriptID in self._pagodaSoulItem[belongSide] and wayType in self._pagodaSoulItem[belongSide][scriptID]:
					sourcePaList.remove( scriptID )
					sourcePaList.append( self._pagodaSoulItem[belongSide][scriptID][wayType] )
			return { "wayType": wayType ,"allPagoda" : sourcePaList, "deadPagoda" : destroyPa}
		return {}
		
	def canUpdateGradePagoda( self, player, oldScriptID, newScriptID, wayType ):
		"""能否升级魂塔"""
		belongSide = player.getBelongSide()
		camp = csdefine.CAMP_TAOSIM if belongSide == csdefine.BELONG_SIDE_ATTACK else csdefine.CAMP_DEMON
		scriptID = g_tradeMgr.getSourcePagodaByScriptID( camp, oldScriptID, wayType )
		if scriptID in self._pagodaSoulItem[belongSide] and wayType in self._pagodaSoulItem[belongSide][scriptID] and self._pagodaSoulItem[belongSide][scriptID][wayType] != oldScriptID:
			# 由于客户端不同步原因导致
			player.client.CLIENT_OnRequestUpdatePagodaSoul( oldScriptID, self._pagodaSoulItem[belongSide][scriptID][wayType], wayType )
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
		belongSide = player.getBelongSide()
		camp = csdefine.CAMP_TAOSIM if belongSide == csdefine.BELONG_SIDE_ATTACK else csdefine.CAMP_DEMON
		scriptID = g_tradeMgr.getSourcePagodaByScriptID( camp, oldScriptID, wayType )
		if scriptID not in self._pagodaSoulItem[belongSide]:
			self._pagodaSoulItem[belongSide][scriptID] = {}
		self._pagodaSoulItem[belongSide][scriptID][wayType] = newScriptID