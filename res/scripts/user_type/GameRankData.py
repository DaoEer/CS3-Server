# -*- coding: utf-8 -*-

"""
cell/base部份的ItemTypeImpl实现模块.
"""
import Const
import KBEngine
import KBEDebug
import csdefine
import csconst
import math

class RankBase( dict ):
	""""""
	def __init__( self ):
		pass
		
	def insertRank( self, rankInfo ):
		"""插入数据"""
		camp = rankInfo["camp"]
		if camp not in self:
			self[camp] = {}
		globalKey = self.Global_Data_Key + "_" + str( camp )

		if rankInfo["playerDBID"] in self[camp]:
			self[camp][rankInfo["playerDBID"]] = rankInfo
			sortList = self.sortRank(camp)
			KBEngine.globalData[globalKey] = sortList[-1][1][self.Rank_Key]
			return
		else:
			if len( self[camp] ) < Const.GAME_RANK_MAX_RANKING:
				self[camp].update({rankInfo["playerDBID"]: rankInfo})
				sortList = self.sortRank(camp)
				KBEngine.globalData[globalKey] = sortList[-1][1][self.Rank_Key]
				return
			else:
				sortList = self.sortRank(camp)
				self[camp].pop(sortList[-1][0])
				self[camp].update({rankInfo["playerDBID"]: rankInfo})
				sortList = self.sortRank(camp)
				KBEngine.globalData[globalKey] = sortList[-1][1][self.Rank_Key]

	
	def sortRank( self, camp ):
		"""排序排行榜"""
		if camp in self and len(self[camp]):
			return sorted(self[camp].items(), key = lambda x:x[1][self.Rank_Key], reverse=1)
		return []
		
	def getPlayerRanking( self, campRank, playerDBID ):
		"""获取玩家的排名"""
		if campRank == 0:				# 全服排名
			for rank in self.values():
				if playerDBID in rank:
					playerRank = rank[playerDBID]
					temp = {}
					for camp, rank in self.items():
						temp.update(rank)
					sRank = sorted(temp.items(), key = lambda x:x[1][self.Rank_Key], reverse=1)
					rankNum = sRank.index((playerDBID, playerRank)) + 1
					if rankNum > Const.GAME_RANK_MAX_RANKING:
						return -1
					return rankNum
		else:							# 阵营排名
			if campRank in self and playerDBID in self[campRank]:
				playerRank = self[campRank][playerDBID]
				sRank = self.sortRank( campRank )
				return sRank.index((playerDBID, playerRank)) + 1
		return -1
	
	def getPage( self, camp ):
		"""获取客户端显示页数"""
		if camp == 0:			# 全服
			num = 0
			for camp, rank in self.items():
				num += len(rank)
				if num >= Const.GAME_RANK_MAX_RANKING:
					return csconst.GAME_RANKING_NUM_MAX_PAGE
			return max( math.ceil( num / csconst.GAME_RANKING_NUM_PER_PAGE ), 1)
		if camp in self:
			return max( math.ceil( len(self[camp]) / csconst.GAME_RANKING_NUM_PER_PAGE ), 1)
		return 1
		
	def getRankInfoByPage( self, camp, page ):
		"""
		获取某一页排行榜数据
		服务器的page 由0开始计算，客户端显示从1开始
		"""
		begin = ( page - 1 ) * csconst.GAME_RANKING_NUM_PER_PAGE
		end = begin + csconst.GAME_RANKING_NUM_PER_PAGE

		if camp == 0:				# 全服数据
			temp = {}
			for rank in self.values():
				temp.update(rank)
			sRank = sorted(temp.items(), key = lambda x: x[1][self.Rank_Key], reverse=1)
		else:						# 阵营数据
			sRank = self.sortRank( camp )
		rankInfo = sRank[begin:end]
		temp = {}
		temp[camp] = {}
		for dbid, rank in rankInfo:
			temp[camp][dbid] = rank
		return temp

	def getRankInfoByCamp(self,camp):
		if camp == 0:
			temp = {}
			for rank in self.values():
				temp.update(rank)
			sRank = sorted(temp.items(), key=lambda x: x[1][self.Rank_Key], reverse=1)
		else:						# 阵营数据
			sRank = self.sortRank( camp )
		rankInfo = sRank[:Const.GAME_RANK_MAX_RANKING]
		temp = {}
		temp[camp] = {}
		for dbid, rank in rankInfo:
			temp[camp][dbid] = rank
		return temp

	def getDictFromObj( self, obj):
		"""
		The method converts a wrapper instance to a FIXED_DICT instance.

		@param obj: The obj parameter is a wrapper instance.
		@return: This method should return a dictionary(or dictionary-like object) that contains the same set of keys as a FIXED_DICT instance.
		"""
		temp = []
		for rankInfo in obj.values():
			for dbid, info in rankInfo.items():
				if "ascend" not in info:
					info["ascend"] = 0
				temp.append( info )
		return {"datas": temp}

	def createObjFromDict(self, dict):
		"""
		This method converts a FIXED_DICT instance to a wrapper instance.

		@param dict: The dict parameter is a FIXED_DICT instance.
		@return: The method should return the wrapper instance constructed from the information in dict.
		"""
		obj = self.__class__()
		obj[csdefine.CAMP_TAOSIM] = {}
		obj[csdefine.CAMP_DEMON] = {}
		for rankData in dict["datas"]:
			if "ascend" not in rankData:
				rankData["ascend"] = 0
			obj[rankData["camp"]][rankData["playerDBID"]] = rankData
		return obj
		
	def isSameType( self, obj):
		"""
		This method check whether an object is of the wrapper type.

		@param obj: The obj parameter in an arbitrary Python object.
		@return: This method should return true if obj is a wrapper instance.
		"""
		return isinstance( obj, dict )

class LevelRank( RankBase ):
	"""
	等级排行榜
	"""
	Rank_Key = "level"
	Global_Data_Key = "Rank_Level"

class MoneyRank( RankBase ):
	"""
	金钱排行榜
	"""
	Rank_Key = "money"
	Global_Data_Key = "Rank_Money"

		
class CombatRank( RankBase ):
	"""
	战斗力排行榜
	"""
	Rank_Key = "combatPower"
	Global_Data_Key = "Rank_CombatPower"
	

class WeaponCombatRank( RankBase ):
	"""
	神器排行榜
	"""
	Rank_Key = "combatPower"
	Global_Data_Key = "Rank_WeaponCombatPower"
	
		
# 自定义类型实现实例
LevelRankInst = LevelRank()
MoneyRankInst = MoneyRank()
CombatRankInst = CombatRank()
WeaponCmbatRankInst = WeaponCombatRank()

