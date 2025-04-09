# -*- coding: utf-8 -*-

import KBEDebug
import KBEngine
import csdefine
import csstatus
import ConfigObject.Reward.RewardBase.RewardMgr as RewardMgr
from CampMoraleConfigLoader import g_campMoraleConfig

VEN_LIST = [csdefine.CAMP_TAOISM_VEV_TITLE, csdefine.CAMP_DEMON_VEV_TITLE, csdefine.CAMP_FENG_MING_VEV_TITLE]

class RoleCampInterface:
	def __init__( self ):
		if self.title in VEN_LIST:
			self.campVenOline()

	def campVenOline(self):
		KBEngine.globalData["CampMgr"].onCampVenOline(self.playerName, self.title, self.camp )

	def onCampVenOlineMessage(self, venName, title):
		"""
		define method
		阵营尊者上线提示消息
		"""
		if title == self.title:
			return

		if title == csdefine.CAMP_TAOISM_VEV_TITLE:
			self.statusMessage(csstatus.CAMP_TAOISM_VEV_ONLINE, venName)
		elif title == csdefine.CAMP_DEMON_VEV_TITLE:
			self.statusMessage(csstatus.CAMP_DEMON_VEV_ONLINE, venName)
		elif title == csdefine.CAMP_FENG_MING_VEV_TITLE:
			self.statusMessage(csstatus.CAMP_FENG_MING_VEV_ONLINE, venName)

	def campBeKilled( self, killer ):
		"""
		被阵营击杀
		"""
		if killer.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE or killer.getCamp() == self.getCamp():
			# 只有被敌对阵营的玩家击杀才能获得奖励
			return
		beKTimes = self.getBeKillTimes(killer)
		killer.campKillFeatsReward( self, beKTimes )
		KBEngine.globalData["CampMgr"].onCampBeKilled( self.base, killer.id )

	def onCampBeKilled( self, killerID ):
		"""
		define method
		被敌对阵营玩家击杀
		"""	
		killer = KBEngine.entities.get( killerID, None )
		if not killer:
			return
		beKTimes = self.getBeKillTimes(killer)
		killer.campKillMoraleReward( self, beKTimes )	

	def getBeKillTimes(self, killer):
		"""
		获得被同一个人杀的次数
		"""
		beKTimes = 0
		if killer.playerDBID not in self.camp_killerList:
			self.camp_killerList.append(killer.playerDBID)
		else:
			for DBID in self.camp_killerList:
				if killer.playerDBID == DBID:
					if beKTimes >= 3:
						break
					beKTimes += 1
					self.camp_killerList.append(killer.playerDBID)
		return beKTimes

	def campKillMoraleReward( self, beKiller, beKTimes ):
		"""
		define method
		阵营击杀气运奖励
		"""
		if self.dayCampMorale > 20:
			self.statusMessage(csstatus.CAMP_MORALE_ROLE_LIMIT)
		if beKTimes >= 3:
			if beKiller.getCamp() == csdefine.CAMP_TAOSIM:
				self.statusMessage(csstatus.CAMP_MORALE_KILL_TAOISM_LIMIT, beKiller.playerName)
			elif beKiller.getCamp() == csdefine.CAMP_DEMON:
				self.statusMessage(csstatus.CAMP_MORALE_KILL_DEMON_LIMIT, beKiller.playerName)
			return

		if beKiller.getCamp() == csdefine.CAMP_TAOSIM:
			self.statusMessage(csstatus.CAMP_MORALE_KILL_TAOISM, beKiller.playerName, 3 -beKTimes)
		elif beKiller.getCamp() == csdefine.CAMP_DEMON:
			self.statusMessage(csstatus.CAMP_MORALE_KILL_DEMON, beKiller.playerName, 3 -beKTimes)		
		self.dayCampMorale += 3 -beKTimes
		KBEngine.globalData["CampMgr"].addMorale( self.getCamp(), 3 -beKTimes )

	def campKillFeatsReward( self, beKiller, beKTimes ):
		"""
		define method
		阵营击杀功勋奖励
		"""
		if beKTimes >= 3:
			if beKiller.getCamp() == csdefine.CAMP_TAOSIM:
				self.statusMessage(csstatus.CAMP_FEATS_KILL_TAOISM_LIMIT, beKiller.playerName)
			elif beKiller.getCamp() == csdefine.CAMP_DEMON:
				self.statusMessage(csstatus.CAMP_FEATS_KILL_DEMON_LIMIT, beKiller.playerName)
			if self.isInTeam():
				self.teamAddFeats(3 -beKTimes, beKiller)
			return
		self.addFeats(3 -beKTimes, csdefine.FEATS_ADD_REASON_CAMP)
		if self.isInTeam():
			self.teamAddFeats(3 -beKTimes, beKiller)

	def teamAddFeats(self, feats, beKiller):
		"""
		队伍获得功勋规则
		"""	
		for mb in self.getAllTeamMemberMB():
			if mb.id == self.id:
				continue
			if feats <= 0:
				if beKiller.getCamp() == csdefine.CAMP_TAOSIM:
					mb.cell.statusMessage(csstatus.CAMP_FEATS_KILL_TAOISM_LIMIT, beKiller.playerName)
				elif beKiller.getCamp() == csdefine.CAMP_DEMON:
					mb.cell.statusMessage(csstatus.CAMP_FEATS_KILL_DEMON_LIMIT, beKiller.playerName)
			else:
				mb.cell.addFeats(1, csdefine.FEATS_ADD_REASON_CAMP)
				string = self.playerName + "|" + beKiller.playerName
				if beKiller.getCamp() == csdefine.CAMP_TAOSIM:
					mb.cell.statusMessage(csstatus.CAMP_FEATS_TEAM_KILL_TAOISM, string)
				elif beKiller.getCamp() == csdefine.CAMP_DEMON:
					mb.cell.statusMessage(csstatus.CAMP_FEATS_TEAM_KILL_DEMON, string)

	def onCampMoraleChange( self, value, oldValue, otherCampMorale, skillID ):
		"""
		<Define Method>
		阵营气运改变回调
		@param value : 改变后的值，UINT64
		@param value : 原值，UINT64
		@param otherCampMorale : 另外一个阵营的气运值，UINT64
		@param skillID : 当前加成效果的技能ID
		"""
		currentMoraleBuff = self.queryTemp( "currentMoraleBuff", [] )
		buffIDList = g_campMoraleConfig.getAllMoraleSkillID( value - otherCampMorale )

		# 删除skillIDList中没有的技能buff
		removeBuffList = []
		for id in currentMoraleBuff:
			if id not in buffIDList:
				removeBuffList.append( id )

		for id in removeBuffList:
			currentMoraleBuff.remove( id )
			self.removeBuffByID(id)

		if len(buffIDList) != len(currentMoraleBuff):
			self.sendCampMoraleEffectMessage(len(buffIDList))

		# 增加skillIDList中有的技能buff
		for buffID in buffIDList :
			if buffID not in currentMoraleBuff:
				self.addBuff( self, buffID )
				currentMoraleBuff.append( buffID )

		self.setTemp( "currentMoraleBuff", currentMoraleBuff )
		if self.client:
			self.client.CLIENT_onMoraleChange( str(value), str(oldValue), str(otherCampMorale), skillID )

	def onResetCampData(self):
		"""
		<Define Method>
		重置阵营奖励回调
		"""
		self.isGetCampReward = False

	def onQueryCampMorale( self, morale, otherCampMorale ):
		"""
		<Define Method>
		查询气运回调
		@param morale : 自身阵营的气运值，UINT64
		@param otherCampMorale : 另外一个阵营的士气值，UINT64
		"""
		skillID = g_campMoraleConfig.getMoraleSkillID( morale - otherCampMorale )
		self.onCampMoraleChange( morale, morale, otherCampMorale, skillID )

	def onClearCampKillerList(self):
		"""
		<Define Method>
		清除阵营击杀列表回调
		"""
		self.camp_killerList.clear()
		self.dayCampMorale = 0

	def CELL_rquestCampMoraleReward( self, srcEntityID ):
		"""
		exposed method
		申请获得阵营气运奖励
		"""
		if not self.validateClientCall( srcEntityID ):
			return

		if self.getLevel() < 30:
			self.statusMessage( csstatus.CAMP_MORALE_REWARD_LEVEL )
			return
		if self.isGetCampReward:
			return
		KBEngine.globalData["CampMgr"].queryMoraleRewards( self.base, self.getCamp())

	def onQueryMoraleRewards(self, rewardIDList):
		"""
		<Define Method>
		查询气运奖励回调
		@param rewardList : 奖励列表
		"""
		self.isGetCampReward = True
		for rewardID in rewardIDList:
			rewardDatas = RewardMgr.g_rewardMgr.getReward( str( rewardID ), {"player": self} )
			RewardMgr.g_rewardMgr.doRewards( rewardDatas, self.id, csdefine.ADD_REWARD_REASON_COMMON_TYPE_CAMP_MORALE )

	def CELL_rquestQueryCampUIData( self, srcEntityID ):
		"""
		exposed method
		申请查询阵营UI数据
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		KBEngine.globalData["CampMgr"].queryCampUIData( self.base, self.getCamp())
	
	def setClientCampSwitch(self, campSwitch):
		"""
		设置阵营开关
		"""
		if self.client:
			self.client.CLIENT_SetClientCampSwitch(campSwitch)

	def onQueryCampUIData(self, taoismMorale, demonMorale, taoismVenName, demonVenName):
		"""
		查询阵营UI数据回调
		"""
		if self.client:
			self.client.CLIENT_OnQueryCampUIData(str(taoismMorale), str(demonMorale), taoismVenName, demonVenName, self.isGetCampReward)

	def sendCampMoraleEffectMessage(self, count):
		"""
		获得阵营效果发送消息
		"""
		if self.getCamp() == csdefine.CAMP_TAOSIM:
			if count>0:
				self.statusMessage( csstatus.CAMP_TAOISM_MORALE_EFFECT_ONE )
			elif count>1:
				self.statusMessage( csstatus.CAMP_TAOISM_MORALE_EFFECT_TWO )
			elif count>2:
				self.statusMessage( csstatus.CAMP_TAOISM_MORALE_EFFECT_THREE )
			elif count>3:
				self.statusMessage( csstatus.CAMP_TAOISM_MORALE_EFFECT_FOUR )
			elif count>4:
				self.statusMessage( csstatus.CAMP_TAOISM_MORALE_EFFECT_FIVE )
		elif self.getCamp() == csdefine.CAMP_DEMON:
			if count>0:
				self.statusMessage( csstatus.CAMP_DEMON_MORALE_EFFECT_ONE )
			elif count>1:
				self.statusMessage( csstatus.CAMP_DEMON_MORALE_EFFECT_TWO )
			elif count>2:
				self.statusMessage( csstatus.CAMP_DEMON_MORALE_EFFECT_THREE )
			elif count>3:
				self.statusMessage( csstatus.CAMP_DEMON_MORALE_EFFECT_FOUR )
			elif count>4:
				self.statusMessage( csstatus.CAMP_DEMON_MORALE_EFFECT_FIVE )
