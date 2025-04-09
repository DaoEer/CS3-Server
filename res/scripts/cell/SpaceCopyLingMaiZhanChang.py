# -*- coding: utf-8 -*-

import random
import KBEDebug
from SpaceCopy import SpaceCopy
import Math
import math
import KBEngine
import csdefine
import csstatus
import csconst
import Const
import time
from ConfigObject.MailContentDataLoader import g_mailContentDataLoader
import cschannel_msgs
import ZyjjRewardData
from Reward import RewardBasicValueData

class SpaceCopyLingMaiZhanChang( SpaceCopy ):
	"""
	灵脉战场
	"""
	def __init__( self ) :
		SpaceCopy.__init__( self )
		self._pointTimer = {}
		self._taosimPowerPoint = 0				# 仙道灵能点
		self._demonPowerPoint = 0				# 魔道灵能点
		self._taosimPagadoIndex = 0				# 记录仙魔刷新葫芦的index
		self._demonPagadoIndex = 0
		self._pagoda = {}						
		self._pagoda[csdefine.CAMP_TAOSIM] = {}	# 极阳灵塔 占领数据（{ scriptID : camp }）
		self._pagoda[csdefine.CAMP_DEMON] = {}	# 极阴灵塔 占领数据（{ scriptID : camp }）
		self.zyjjRewardDatas = ZyjjRewardData.ZyjjRewardDatas()

		
	def onEnter( self, playerRole, packArgs ):
		""""""
		SpaceCopy.onEnter( self, playerRole, packArgs )
		playerRole.onEnterLMZC()
		#设置临时阵营
		self.setPlayerTempCamp(playerRole)
		camp = playerRole.getFinalCamp()
		if camp == csdefine.CAMP_TAOSIM:
			campStr = cschannel_msgs.CAMP_BLUE
		else:
			campStr = cschannel_msgs.CAMP_RED
		self.memberDatas.add( playerRole, playerRole.id, playerRole.getName(), camp, campStr, playerRole.getLevel() )
		
	def onLeave( self,  playerRole, packArgs ):
		""""""
		SpaceCopy.onLeave( self, playerRole, packArgs )
		self.memberDatas.leave( playerRole.id )
		self.resetPlayerTempCamp(playerRole)
		if self.getSpaceRoleNum() == 0:
			self.addTimerCallBack(5.0, "closeSpace", ())

	def activityEnd( self ):
		"""
		define method
		活动结束
		"""
		self.onLifeTimeArrive()
		
	def occupyLingMai( self, scriptID, camp, damageObjList ):
		"""占领灵脉"""
		self.memberDatas.occupyLingMai( damageObjList )
		for player in self._spaceRoles:
			player.client.CLIENT_OccupyLingMai( scriptID, camp, self._taosimPowerPoint, self._demonPowerPoint, damageObjList )
		if scriptID in self._pointTimer:
			self.popTimer( self._pointTimer[scriptID] )
		timer = self.addTimerRepeat( 1.0, "addPowerPoint", (camp,))
		self._pointTimer[scriptID] = timer
		
	def addPowerPoint( self, camp ):
		"""增加灵能点，客户端模拟"""
		if camp == csdefine.CAMP_TAOSIM:
			self.addTaosimPowerPoint( 1 )
		elif camp == csdefine.CAMP_DEMON:
			self.addDemonPowerPoint( 1 )
	
	def grabGourdLeave( self, playerID, playerCamp, redPoint ):
		"""抢夺葫芦离开敌方阵营"""
		player = KBEngine.entities.get( playerID )
		if playerCamp == csdefine.CAMP_TAOSIM:					
			self.addTaosimPowerPoint( redPoint )
		else:
			self.addDemonPowerPoint( redPoint )
		if player and player.getFinalCamp() != playerCamp:			# 可能会出现不断来回拉葫芦刷分
			self.memberDatas.grabGourd( playerID, playerCamp )
			for player in self._spaceRoles:
				player.client.CLIENT_OnGrabGourdLeave( playerID, self._taosimPowerPoint, self._demonPowerPoint )
		
	def grabGourdEnter( self, playerID, playerCamp, addPoint ):
		"""抢夺葫芦进入我方阵营"""
		if playerCamp == csdefine.CAMP_TAOSIM:					
			self.addTaosimPowerPoint( addPoint )
		else:
			self.addDemonPowerPoint( addPoint )
		for player in self._spaceRoles:
			player.client.CLIENT_OnPowerPointChange( self._taosimPowerPoint, self._demonPowerPoint )
		
	def onMemberKillPlayer( self, killEntity, dieEntity ):
		"""杀人添加积分"""
		if killEntity.getFinalCamp() == csdefine.CAMP_TAOSIM:
			self.addTaosimPowerPoint( 2 )
		else:
			self.addDemonPowerPoint( 2 )

		if killEntity.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
			#击杀者获得经验奖励
			rate = self.getScript().getKillExpRate()
			exp = int(rate * RewardBasicValueData.datas.get(dieEntity.getLevel(), {}).get("exp", 0))
			killEntity.addExp(exp, csdefine.EXP_ADD_REASON_JMZC_KILL_ROLE)
			#击杀者获得军功奖励
			exploits = self.getScript().getKillExploits()
			killEntity.addExploitRecord(exploits)
		
	def addTaosimPowerPoint( self, point ):
		""""""
		self._taosimPowerPoint += point
		if self._taosimPowerPoint % Const.LMZC_CREATE_ENTITY_BY_POWERPOINT == 0:
			self.createPowerPointCrystal( csdefine.CAMP_TAOSIM )
		if self._taosimPowerPoint >= Const.LMZC_POWER_POINT_WINNER:
			self.winGame( csdefine.CAMP_TAOSIM )
		
	def addDemonPowerPoint( self, point ):
		""""""
		self._demonPowerPoint += point
		if point != 300 and self._demonPowerPoint % Const.LMZC_CREATE_ENTITY_BY_POWERPOINT == 0:
			self.createPowerPointCrystal( csdefine.CAMP_DEMON )
		if self._demonPowerPoint >= Const.LMZC_POWER_POINT_WINNER:
			self.winGame( csdefine.CAMP_DEMON )
		
	def createPowerPointCrystal( self, camp ):
		"""灵能点每300点，刷出一个葫芦"""
		randX = random.uniform( -3, 3 )
		randZ = random.uniform( -3, 3 )
		yaw = random.uniform( -math.pi, math.pi )
		direction = Math.Vector3(0, 0, 0)
		if camp == csdefine.CAMP_TAOSIM:
			position = Math.Vector3( Const.LMZC_CREATE_TAOSIM_CRYSTAL_POS[self._taosimPagadoIndex] )
			self._taosimPagadoIndex += 1
			messageID = csstatus.ACTIVITY_CAMP_XIAN_CREATE_CRYSTAL
		else:
			position = Math.Vector3( Const.LMZC_CREATE_DEMON_CRYSTAL_POS[self._demonPagadoIndex] )
			self._demonPagadoIndex += 1
			messageID = csstatus.ACTIVITY_CAMP_MO_CREATE_CRYSTAL
		for player in self._spaceRoles:
			player.statusMessage( messageID, "" )
		self.createSpellBox( Const.LMZC_POWER_POINT_CRYSTAL_SCRIPTID, position, direction, {} )
		
	def winGame( self, camp ):
		"""获胜"""
		for memberData in self.memberDatas.values():
			if memberData["camp"] == camp:
				g_mailContentDataLoader.sendActivityReward( self.scriptID,1,memberData["name"] )
			else:
				g_mailContentDataLoader.sendActivityReward( self.scriptID,2,memberData["name"] )
		for timer in self._pointTimer.values():
			self.popTimer(timer)
		self._pointTimer.clear()
		leftTime = int( time.time() - self.lifeStartTime )

		#经验奖励
		self.addFinalExpReward(camp)
		#帮贡奖励
		self.addFinalContributionReward()
		#军功奖励
		self.addFinalExploitReward(camp)
		#邮件奖励
		loserMailID = self.getScript().getLoserRewardMailID()
		winnerMailID = self.getScript().getWinnerRewardMailID()
		self.memberDatas.sendRewardMail(camp, loserMailID, winnerMailID)
		#出局者邮件奖励
		self.addOutMailReward(camp)

		for player in self._spaceRoles:
			if player.playerDBID in self.zyjjRewardDatas:
				player.client.ShowZYJJReward(self.zyjjRewardDatas[player.playerDBID])
			player.client.CLIENT_OnWinGameLingMai( camp, leftTime, self._taosimPowerPoint, self._demonPowerPoint )
		self.addTimerCallBack( 30, "closeSpace", () )
	
	def onLifeTimeArrive( self ):
		"""活动时间到达"""
		if self._taosimPowerPoint > self._demonPowerPoint:
			self.winGame( csdefine.CAMP_TAOSIM )
		else:
			self.winGame( csdefine.CAMP_DEMON )
	
	def occupyPagoda( self, type, scriptID, playerID, camp ):
		"""开始占领极阳（极阴）灵塔"""
		if type in self._pagoda:
			if scriptID in self._pagoda[type] and self._pagoda[type][scriptID] == camp:
				return
			self._pagoda[type][scriptID] = camp
			self.memberDatas.occupyPagoda( playerID )
			for player in self._spaceRoles:
				player.client.CLIENT_OccupyPagodaBase( playerID )		# 占领塔基
			if self.isOccupyPagoda( type, camp ):
				self.onOccupyPagoda( type, camp )
		else:
			KBEDebug.ERROR_MSG( "Occupy pagoda err!can not find type(%d)"%type )
			
	def isOccupyPagoda( self, type, camp ):
		"""是否已经占领灵塔"""
		scriptIDs = self.getScript().getPagodaScriptIDs( type )
		if scriptIDs == []:return False
		for scriptID in scriptIDs:
			if not scriptID in self._pagoda[type]:
				return False
			if self._pagoda[type][scriptID] != camp:
				return False
		return True
		
	def onOccupyPagoda( self, type, camp ):
		"""已经占领极阳（极阴）灵塔"""
		scriptIDs = self.getScript().getPagodaScriptIDs( type )
		if scriptIDs:
			for player in self._spaceRoles:
				player.client.CLIENT_OccupyPagoda( scriptIDs[0], camp )
	
	def getEntityDynamicPosBigMapShow( self, player, scriptID ):
		"""获取entity在大地图的位置"""
		entities = []
		temp = SpaceCopy.getEntityDynamicPosBigMapShow( self, player, scriptID )
		huluDist = self.getScript().getHuLuDistance()
		for hulu in list(temp):
			if hulu.position.distTo( Const.LMZC_CREATE_TAOSIM_CENTER_POS ) < huluDist or\
			hulu.position.distTo( Const.LMZC_CREATE_DEMON_CENTER_POS ) < huluDist:
				temp.remove( hulu )
				entities.append( hulu )
		
		occupyTaosim = self.isOccupyPagoda( csdefine.CAMP_TAOSIM, player.getFinalCamp() )
		occupyDemon = self.isOccupyPagoda( csdefine.CAMP_DEMON, player.getFinalCamp() )
		if not occupyTaosim and not occupyDemon:							# 两个灵塔都没有被占领
			return entities
		
		buffID = self.getScript().getCrystalBuff()
		
		for player in self._spaceRoles:
			if player.findBuffsByBuffID(buffID):
				temp.append( player )
				
		distance = self.getScript().getPagodaDistance()
		if occupyTaosim:									# 如果占领了极阳灵塔
			pos = self.getScript().getSunDectPos()
			for entity in temp:
				if entity.position.distTo( pos ) <= distance:
					entities.append( entity )
				
		if occupyDemon:										# 如果占领了极阴灵塔
			pos = self.getScript().getShadeDectPos()
			for entity in temp:
				if entity in entities:
					continue
				if entity.position.distTo( pos ) <= distance:
					entities.append( entity )
			pass
		return entities
		
	def requestSameCampPos( self, player, camp ):
		"""获取地图上同阵营的玩家坐标信息"""
		temp = []
		for role in self._spaceRoles:
			if role.id == player:continue
			if role.getFinalCamp() == camp:
				tempDict = {}
				tempDict["objectID"] = role.id
				tempDict["position"] = Math.Vector3( role.position)
				tempDict["name"] = role.playerName
				temp.append( tempDict )
		player.client.CLIENT_OnRequestSameCampPos( { "infos" : temp } )


	def setPlayerTempCamp(self, playerRole):
		"""
		设置玩家临时阵营
		"""
		playerCampInfo = self.createArgs.get("playerCampInfo", {})
		tempCamp = playerCampInfo.get(playerRole.playerDBID, csdefine.CMAP_NONE)
		buffID = self.getScript().getTempCampBuff(tempCamp)
		if buffID:
			playerRole.addBuff(playerRole, buffID)
		else:
			KBEDebug.ERROR_MSG("tempBuffID=0")

	def resetPlayerTempCamp(self, playerRole):
		buffID = self.getScript().getTempCampBuff(playerRole.tempCamp)
		playerRole.removeBuffByID(buffID)


#-------------------------阵营竞技结算奖励------------------------------------

	def addFinalContributionReward(self):
		#帮贡奖励 CST-13692
		#同一个帮会的成员分类
		tongDict = {}
		for player in self._spaceRoles:
			tongMB = player.tongMB
			if not tongMB:
				continue
			if tongMB.id not in tongDict:
				tongDict[tongMB.id] = []
			tongDict[tongMB.id].append(player)
		#同帮会成员人数达标后才可获得奖励
		for playerList in tongDict.values():
			amount = len(playerList)
			if amount in csconst.ZYJJ_REWARD_CONTRIBUTION:
				ctrbValue = csconst.ZYJJ_REWARD_CONTRIBUTION[amount]
				for player in playerList:
					player.addContribution(ctrbValue)
					self.zyjjRewardDatas.addContribution(player.playerDBID, ctrbValue)

	def addFinalExpReward(self, winnerCamp):
		"""
		副本结算经验奖励
		"""
		for player in self._spaceRoles:
			if player.getFinalCamp() == winnerCamp:
				value = self.getScript().getFinalExpDict(player.getLevel(), 1)
			else:
				value = self.getScript().getFinalExpDict(player.getLevel(), 0)
			if not value:
				continue
			player.addExp(value, csdefine.EXP_ADD_REASON_JMZC_FINAL_EXP)
			self.zyjjRewardDatas.addExp(player.playerDBID, value)

	def addFinalExploitReward(self, winnerCamp):
		"""
		副本结算军功奖励
		"""
		for player in self._spaceRoles:
			if player.getFinalCamp() == winnerCamp:
				value = self.getScript().getFinalWinExploits()
			else:
				value = self.getScript().getFinalLostExploits()
			player.addExploit(value)
			self.zyjjRewardDatas.addExploit(player.playerDBID, value)

	def addOutMailReward(self, winnerCamp):
		"""
		把数值奖励通过邮件发送给不在副本内的玩家
		"""
		for member in self.memberDatas.values():
			if member["isLeave"]:
				if member["camp"] == winnerCamp:
					mailID = self.getScript().getOutRewardMailID(member['level'], 1)
				else:
					mailID = self.getScript().getOutRewardMailID(member['level'], 0)
				g_mailContentDataLoader.sendSpaceReward(mailID, member["name"])
					

