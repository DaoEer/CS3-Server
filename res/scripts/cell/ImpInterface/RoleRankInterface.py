# -*- coding: utf-8 -*-


import csconst
import KBEDebug
import KBEngine
import csdefine
import csstatus
import ItemFactory
import time
import ItemTypeEnum

class RoleRankInterface:
	"""
	排行榜
	"""
	def __init__( self ):
		pass
		
	def beforeDestroy( self ):
		"""
		virtual method
		销毁前做一些事
		"""
		self.updateLevelRank( True )
		self.updateCombatRank( True )
		self.updateMoneyRank( True )
		self.updateWeaponRank( True )
		
	def updateGameRank( self, rankType ):
		"""
		define method
		获取新手在线奖励
		"""
		if rankType == csdefine.GAME_RANKING_TYPE_LEVEL:
			self.updateLevelRank( False )
		elif rankType == csdefine.GAME_RANKING_TYPE_COMBAT:
			self.updateCombatRank( False )
		elif rankType == csdefine.GAME_RANKING_TYPE_MONEY:
			self.updateMoneyRank( False )
		elif rankType == csdefine.GAME_RANKING_TYPE_WEAPON:
			self.updateWeaponRank( False )
			
	def updateLevelRank( self, bOffline ):
		"""更新等级排行榜"""
		key = "Rank_Level_" + str(self.camp)
		if self.level >= csconst.GAME_LEVEL_RANK_LOWER_LEVEL and self.level > KBEngine.globalData.get(key, 0):
			levelRank = {}
			levelRank.update( {"playerDBID" : self.playerDBID } )
			levelRank.update( {"playerName" : self.playerName } )
			levelRank.update( {"camp" : self.camp } )
			levelRank.update( {"profession" : self.profession } )
			levelRank.update( {"combatPower" : self.combatPower } )
			levelRank.update( {"level" : self.level } )
			levelRank.update( {"ascend" : 0 } )
			KBEngine.globalData["GameRankingManager"].updatePlayerLevelRank( levelRank, bOffline )
		
	def updateMoneyRank( self, bOffline ):
		"""更新财富排行榜"""
		self.base.updateMoneyRank( self.money, bOffline )
		
	def updateCombatRank( self, bOffline ):
		"""更新战斗力排行榜"""
		key = "Rank_CombatPower_" + str(self.camp)
		if self.level >= csconst.GAME_COMBAT_RANK_LOWER_LEVEL and self.combatPower > KBEngine.globalData.get(key, 0):
			combatRank = {}
			combatRank.update( {"playerDBID" : self.playerDBID } )
			combatRank.update( {"playerName" : self.playerName } )
			combatRank.update( {"camp" : self.camp } )
			combatRank.update( {"profession" : self.profession } )
			combatRank.update( {"combatPower" : self.combatPower } )
			combatRank.update( {"level" : self.level } )
			combatRank.update( {"ascend" : 0 } )
			KBEngine.globalData["GameRankingManager"].updatePlayerCombatRank( combatRank, bOffline )

	def updateWeaponRank( self, bOffline ):
		"""更新神器排行榜"""
		key = "Rank_WeaponCombatPower_" + str(self.camp)
		weapon = self.getItemInstByOrder( ItemTypeEnum.EQUIP_WEAPON )
		if weapon == None:
			return
		if weapon.getQuality() <= ItemTypeEnum.QUALITY_GREEN:
			return

		combatPower = weapon.dynamicData.get( "combatPower" )
		if combatPower and combatPower > KBEngine.globalData.get(key, 0):
			combatRank = {}
			combatRank.update( {"playerDBID" : self.playerDBID } )
			combatRank.update( {"playerName" : self.playerName } )
			combatRank.update( {"camp" : self.camp } )
			combatRank.update( {"weaponUID" : weapon.uid } )
			combatRank.update( {"weaponID" : weapon.id } )
			combatRank.update( {"quality" : weapon.getQuality() } )
			combatRank.update( {"combatPower" : weapon.dynamicData["combatPower"] } )
			combatRank.update( {"attackProperties" : weapon.dynamicData["attackPropertiesStr"] } )
			combatRank.update( {"attachProperties" : weapon.dynamicData["attachPropertiesStr"] } )
			combatRank.update( {"intensifyProperties" : weapon.dynamicData["intensifyDataStr"] } )
			combatRank.update( {"ascend" : 0 } )
			KBEngine.globalData["GameRankingManager"].updatePlayerWeaponCombatRank( combatRank, bOffline )