# -*- coding: utf-8 -*-

import KBEDebug
import KBEngine
import Const
import copy
import time
import KST
import csdefine
import Functions
from GameRankData import *
from CoreObject import MgrPersistentObject

from ConfigObject.Crond.CrondDatas import CrondDatas
g_CrondDatas = CrondDatas.instance()

class GameRankingManager( MgrPersistentObject.MgrPersistentObject ):
	"""
	游戏排行榜管理器
	"""
	def  __init__( self ):
		"""
		"""
		MgrPersistentObject.MgrPersistentObject.__init__( self )
		self.register()
		self._oldLevelRank = {}
		self._oldMoneyRank = {}
		self._oldCombatRank = {}
		self._oldWeaponRank = {}
		self.rankInfo = {}
		self.lastLevelTime = 0
		self.lastMoneyTime = 0
		self.lastCombatTime = 0
		self.lastWeaponTime = 0
		self.rankInfo[csdefine.GAME_RANKING_TYPE_LEVEL] = self.levelRank
		self.rankInfo[csdefine.GAME_RANKING_TYPE_COMBAT] = self.combatRank
		self.rankInfo[csdefine.GAME_RANKING_TYPE_MONEY] = self.moneyRank
		self.rankInfo[csdefine.GAME_RANKING_TYPE_WEAPON] = self.weaponRank
		self.onCompleteInit()
		
	def register( self ):
		""""""
		task = { "GameRank_UpdateLevel" : "broadUpdatePlayerLevelRank",
				"GameRank_UpdateMoney" : "broadUpdatePlayerMoneyRank",
				"GameRank_UpdateCombat" : "broadUpdatePlayerCombatRank",
				"GameRank_UpdateWeapon" : "broadUpdatePlayerWeaponRank", 
			}
		for taskName, callback in task.items():
			for scriptID, cmd in g_CrondDatas.getCrondTaskCmds(taskName):
				KBEngine.globalData["CrondManager"].addScheme( scriptID, cmd, self, callback, -1, ())
		
	def broadUpdatePlayerLevelRank( self, cmd, *callbackArgs):
		"""广播通知更新等级排行榜"""
		KST.g_baseAppEntity.broadUpdateRank( csdefine.GAME_RANKING_TYPE_LEVEL )
		
	def broadUpdatePlayerMoneyRank( self, cmd, *callbackArgs):
		"""广播通知更新财富排行榜"""
		KST.g_baseAppEntity.broadUpdateRank( csdefine.GAME_RANKING_TYPE_MONEY )
		
	def broadUpdatePlayerCombatRank( self, cmd, *callbackArgs):
		"""广播通知更新战斗力排行榜"""
		KST.g_baseAppEntity.broadUpdateRank( csdefine.GAME_RANKING_TYPE_COMBAT )
		
	def broadUpdatePlayerWeaponRank( self, cmd, *callbackArgs):
		"""广播通知更新神器排行榜"""
		KST.g_baseAppEntity.broadUpdateRank( csdefine.GAME_RANKING_TYPE_WEAPON )
		
	def updatePlayerLevelRank( self, levelRank, bOffline ):
		"""
		define method
		更新玩家等级排行
		"""
		if not bOffline:
			curTime = int( time.time() )
			if curTime - self.lastLevelTime >= Const.GAME_RANK_MIN_UPDATE_TIME:
				self.lastLevelTime = curTime
				self._oldLevelRank = copy.deepcopy( self.levelRank )
				self.addTimerCallBack( 5.0, "calculateLevelRank", () )
		self.levelRank.insertRank( levelRank )

		
	def calculateLevelRank( self ):
		"""计算等级排行的名次升降"""
		self._calculateRank( self.levelRank, self._oldLevelRank )
		KST.g_baseAppEntity.broadRankUpdateMessage(csdefine.GAME_RANKING_TYPE_LEVEL)

	def updatePlayerMoneyRank( self, moneyRank, bOffline ):
		"""
		define method
		更新玩家财富排行
		"""
		if not bOffline:
			curTime = int( time.time() )
			if curTime - self.lastMoneyTime >= Const.GAME_RANK_MIN_UPDATE_TIME:
				self.lastMoneyTime = curTime
				self._oldMoneyRank = copy.deepcopy( self.moneyRank )
				self.addTimerCallBack( 5.0, "calculateMoneyRank", () )
		self.moneyRank.insertRank( moneyRank )

		
	def calculateMoneyRank( self ):
		"""计算等级财富的名次升降"""
		self._calculateRank( self.moneyRank, self._oldMoneyRank )
		KST.g_baseAppEntity.broadRankUpdateMessage(csdefine.GAME_RANKING_TYPE_MONEY)
		
	def updatePlayerCombatRank( self, combatRank, bOffline ):
		"""
		define method
		更新玩家战斗力排行
		"""
		if not bOffline:
			curTime = int( time.time() )
			if curTime - self.lastCombatTime >= Const.GAME_RANK_MIN_UPDATE_TIME:
				self.lastCombatTime = curTime
				self._oldCombatRank = copy.deepcopy( self.combatRank )
				self.addTimerCallBack( 5.0, "calculateCombatRank", () )
		self.combatRank.insertRank( combatRank )


	def calculateCombatRank( self ):
		"""计算战斗力排行的名次升降"""
		self._calculateRank( self.combatRank, self._oldCombatRank )
		KST.g_baseAppEntity.broadRankUpdateMessage(csdefine.GAME_RANKING_TYPE_COMBAT)
		
	def updatePlayerWeaponCombatRank( self, weaponRank, bOffline ):
		"""
		define method
		更新玩家神器排行
		"""
		if not bOffline:
			curTime = int( time.time() )
			if curTime - self.lastWeaponTime >= Const.GAME_RANK_MIN_UPDATE_TIME:
				self.lastWeaponTime = curTime
				self._oldWeaponRank = copy.deepcopy( self.weaponRank )
				self.addTimerCallBack( 5.0, "calculateWeaponRank", () )
		self.weaponRank.insertRank( weaponRank )

		
	def calculateWeaponRank( self ):
		"""计算神器排行的名次升降"""
		self._calculateRank( self.weaponRank, self._oldWeaponRank )
		KST.g_baseAppEntity.broadRankUpdateMessage(csdefine.GAME_RANKING_TYPE_WEAPON)
		
	def _calculateRank( self,newRank, oldRank ):
		"""计算排行榜名次升降"""
		for camp, newRankInfo in newRank.items():
			oldList = oldRank.sortRank( camp )
			newList = newRank.sortRank( camp )
			for nIndex, NInfo in enumerate( newList ):
				dbid = NInfo[1]["playerDBID"]
				if dbid not in oldRank[camp]:					# 玩家还没有进入过排行榜
					newRank[camp][NInfo[1]["playerDBID"]]["ascend"] = len( newRank[camp].values()) - nIndex
					continue
				for oIndex, OInfo in enumerate( oldList ):
					if OInfo[1]["playerDBID"] == dbid:
						newRank[camp][NInfo[1]["playerDBID"]]["ascend"] = oIndex - nIndex
						break
					
	def openGameRank( self, roleCell, roleDBID, npcID ):
		"""
		define method
		打开排行榜
		"""
		lRInAll = self.levelRank.getPlayerRanking( 0, roleDBID )
		totalPage = self.levelRank.getPage(0)
		rankInfo = self.levelRank.getRankInfoByPage(0,1)
		roleCell.client.OpenGameRank( npcID, lRInAll, totalPage, rankInfo )
		
	def requestGameRankFirstTime( self, roleBase, roleDBID, rankType, camp ):
		"""
		define method
		请求排行榜数据
		camp 为0，表示全阵营
		"""
		rankInfo = self.rankInfo[rankType]
		rankNum = rankInfo.getPlayerRanking( camp, roleDBID )
		totalPage = rankInfo.getPage(camp)
		rankData = rankInfo.getRankInfoByCamp(camp)

		if rankType == csdefine.GAME_RANKING_TYPE_LEVEL:
			roleBase.client.OnRequestLevelRankFirstTime(camp, rankNum, totalPage, rankData )
		elif rankType == csdefine.GAME_RANKING_TYPE_COMBAT:
			roleBase.client.OnRequestCombatRankFirstTime(camp, rankNum, totalPage, rankData )
		elif rankType == csdefine.GAME_RANKING_TYPE_MONEY:
			roleBase.client.OnRequestMoneyRankFirstTime(camp, rankNum, totalPage, rankData )
		elif rankType == csdefine.GAME_RANKING_TYPE_WEAPON:
			roleBase.client.OnRequestWeaponRankFirstTime(camp, rankNum, totalPage, rankData )
