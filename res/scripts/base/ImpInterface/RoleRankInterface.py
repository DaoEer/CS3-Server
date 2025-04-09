# -*- coding: utf-8 -*-

import time
import KBEDebug
import KBEngine
import csconst
import csdefine
import csstatus
import Functions

class RoleRankInterface:
	"""
	游戏排行榜
	"""
	def __init__( self ):
		""""""
		pass
		
	def updateMoneyRank( self, money, bOffline ):
		"""
		define method
		更新排行榜
		"""
		totalMoney = money + self.storeMoney
		key = "Rank_Money_" + str(self.camp)
		if totalMoney >= csconst.GAME_MONEY_RANK_LOWER_MONEY and totalMoney > KBEngine.globalData.get(key, 0):
			moneyRank = {}
			moneyRank.update( {"playerDBID" : self.databaseID } )
			moneyRank.update( {"playerName" : self.playerName } )
			moneyRank.update( {"camp" : self.camp } )
			moneyRank.update( {"profession" : self.profession } )
			moneyRank.update( {"money" : totalMoney } )
			moneyRank.update( {"level" : self.level } )
			moneyRank.update( {"ascend" : 0 } )
			KBEngine.globalData["GameRankingManager"].updatePlayerMoneyRank( moneyRank, bOffline )

	def requestGameRankFirstTime( self, rankType, camp ):
		"""
		exposed method
		请求排行榜数据
		"""
		if rankType == csdefine.GAME_RANKING_TYPE_MONEY:
			self.client.OnRequestRankStoreMoney( str(self.storeMoney ))
		KBEngine.globalData["GameRankingManager"].requestGameRankFirstTime( self, self.databaseID, rankType, camp )
