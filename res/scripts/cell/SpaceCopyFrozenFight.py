# -*- coding: utf-8 -*-

import random
import KBEDebug
from SpaceCopy import SpaceCopy
import Math
import math
import KBEngine
import csdefine
import csstatus
import Const
import time


TOWER_STATUS_NORMAL = 0   #己方占领
TOWER_STATUS_LOST = 1     #被敌方占领

class SpaceCopyFrozenFight( SpaceCopy ):
	"""
	冰雪之战
	"""
	def __init__( self ) :
		SpaceCopy.__init__( self )
		self._pointTimer = 0
		self._towerTimer = {}
		self._tower = {}		# 哨塔信息
		self.begainTime = 0.0
		

	def initSpaceData(self, initCampPoint, revivePosInfo, towerInfo, pointInfo):
		""""""
		self._campPointInfo = {csdefine.CAMP_DEMON:{"point":initCampPoint, "time":0.0}, csdefine.CAMP_TAOSIM:{"point":initCampPoint, "time":0.0}} 			#阵营分数
		self._revivePosInfo = revivePosInfo 																	#复活点信息
		self._towerInfo = towerInfo
		self._pointInfo = pointInfo 																			#计分项信息
		

	def onEnter( self, playerRole, packArgs ):
		""""""
		SpaceCopy.onEnter( self, playerRole, packArgs )
		self.memberDatas.add( playerRole, playerRole.id, playerRole.getName(), playerRole.camp )
		playerRole.client.CLIENT_OnFrozenFightPointChanged(self._campPointInfo[csdefine.CAMP_TAOSIM]["point"], self._campPointInfo[csdefine.CAMP_DEMON]["point"])
		

	def onLeave( self, playerRole, packArgs ):
		""""""
		SpaceCopy.onLeave( self, playerRole, packArgs )
		self.memberDatas.remove( playerRole.id )

	def onLogin( self, selfEntity, playerRole ):
		"""
		"""
		SpaceCopy.onLogin( self, selfEntity, playerRole )
		self.memberDatas.add( playerRole, playerRole.id, playerRole.getName(), playerRole.camp )
		playerRole.client.CLIENT_OnFrozenFightPointChanged(self._campPointInfo[csdefine.CAMP_TAOSIM]["point"], self._campPointInfo[csdefine.CAMP_DEMON]["point"])


	def occupyRivivePos( self, scriptID, player ):
		"""占领复活点"""
		#更新面板复活点占领数据
		for _player in self._spaceRoles:
			_player.client.CLIENT_OnFrozenFightOccupyRivivePos( scriptID, player.getCamp(), _player.id,)	
		if self._revivePosInfo.get(scriptID, None):
			self._revivePosInfo[scriptID]["camp"] = player.getCamp()
			self.memberDatas.occupyRevivePos(player.id)
			

	def killBoss(self, killerEntity):
		"""击杀Boss,移除地方阵营所有分数"""
		#广播击杀boss的消息
		
		camp = self._getOpposedCamp(killerEntity.getCamp())
		if camp == csdefine.CAMP_TAOSIM:
			msg = csstatus.ACTIVITY_CAMP_FROZEN_FIGHT_MO_KILL_BOSS
		else:
			msg = csstatus.ACTIVITY_CAMP_FROZEN_FIGHT_XIAN_KILL_BOSS

		for player in self._spaceRoles:
			player.statusMessage( msg ,"")
		
		point = self._campPointInfo[camp]["point"]
		self._addPoint(camp, -point)


	def playerBeKilled(self, dieEntity):
		"""击杀玩家获得分数"""
		camp = dieEntity.getCamp()
		self._addPoint(camp, self._pointInfo["player"])
		self.onPlayerDeadDrop(dieEntity)


	def onPlayerDeadDrop(self, dieEntity):
		"""玩家死亡掉落"""
		itemInst = dieEntity.getItemInstsByID(self.getScript().iceCrystalsItemID)
		if not itemInst:
			return
		amount = itemInst.amount

		for i in range(0, amount):
			Obj = dieEntity.createEntityByScriptID(self.getScript().iceCrystalsSpBoxID, tuple(Math.Vector3(dieEntity.position)), dieEntity.direction,  {})


	def towerDestroy(self, scriptID):
		"""哨塔被摧毁，扣除己方阵营分数"""
		info = self._towerInfo.get(scriptID, None)
		if not info:
			return	
		#广播哨塔被摧毁的消息
		camp = info["camp"]
		if camp == csdefine.CAMP_TAOSIM:
			msg = csstatus.ACTIVITY_CAMP_FROZEN_FIGHT_MO_DESTROY_TOWER
		else:
			msg = csstatus.ACTIVITY_CAMP_FROZEN_FIGHT_XIAN_DESTROY_TOWER

		for player in self._spaceRoles:
			player.statusMessage( msg ,"")

		self._addPoint(camp, self._pointInfo["tower"])
		self._towerInfo.pop(scriptID)
		#一个scriptID 一座哨塔
		towerIDList = self.getEntityRecord(scriptID)
		if len(towerIDList):
			tid = towerIDList[0]
			tower = KBEngine.entities.get(tid, None)
			if tower:
				tower.destroySelf()


	def takeTower(self, scriptID):
		"""夺取敌方阵营哨塔"""
		info = self._towerInfo.get(scriptID, None)
		if not info:
			return
		info["status"] = TOWER_STATUS_LOST
		timerID = self.addTimerCallBack(60, "towerDestroy", (scriptID,))
		self._towerTimer.update({scriptID:timerID})


	def takeBackTower(self, scriptID):
		"""夺回己方阵营哨塔"""
		info = self._towerInfo.get(scriptID, None)
		if not info:
			return
		info["status"] = TOWER_STATUS_NORMAL
		timerID = self._towerTimer[scriptID]
		self.popTimer(timerID)
		self._towerTimer.pop(scriptID)


	def winGame( self, camp ):
		"""获胜"""
		#清理定时器
		self.popTimer(self._pointTimer)
		for value in self._towerTimer.values():
			self.popTimer(value)

		#广播阵营获胜的消息
		winnerPoint = self._campPointInfo[camp]["point"]
		loserPoint = self._campPointInfo[self._getOpposedCamp(camp)]["point"]
		duration = int(time.time()-self.begainTime)
		for player in self._spaceRoles:
			player.client.CLIENT_OnWinGameFrozenFight( camp, winnerPoint, loserPoint, duration )
		self.addTimerCallBack( 30, "closeSpace", () )
	

	def onLifeTimeArrive( self ):
		"""活动时间到达"""
		#得分多的赢
		if self._campPointInfo[csdefine.CAMP_TAOSIM]["point"] > self._campPointInfo[csdefine.CAMP_DEMON]["point"]:
			self.winGame( csdefine.CAMP_TAOSIM )
		elif self._campPointInfo[csdefine.CAMP_TAOSIM]["point"] < self._campPointInfo[csdefine.CAMP_DEMON]["point"]:
			self.winGame( csdefine.CAMP_DEMON )
		#等分一样，取时间大的一方赢
		else:
			if self._campPointInfo[csdefine.CAMP_TAOSIM]["time"] > self._campPointInfo[csdefine.CAMP_DEMON]["time"]:
				self.winGame( csdefine.CAMP_TAOSIM )
			else:
				self.winGame( csdefine.CAMP_DEMON )
	

	def _decreasePowerPoint(self):
		"""双方阵营资源点随时间持续减少"""
		info = self._pointInfo["time"]
		self._pointTimer = self.addTimerRepeat(info[0], "_addPoint", (csdefine.CMAP_NONE, info[1]))
		self.begainTime = time.time()


	def _addPoint( self, camp, point ):
		"""增加分数"""
		if camp == csdefine.CMAP_NONE:
			self._onAddPoint(csdefine.CAMP_TAOSIM, point, time.time())
			self._onAddPoint(csdefine.CAMP_DEMON, point, time.time())
		else:
			self._onAddPoint(camp, point, time.time())
			

	def _onAddPoint(self, camp, point, time):
		""""""
		self._campPointInfo[camp]["point"] += point
		#更新面板阵营分数
		for player in self._spaceRoles:
			player.client.CLIENT_OnFrozenFightPointChanged(self._campPointInfo[csdefine.CAMP_TAOSIM]["point"], self._campPointInfo[csdefine.CAMP_DEMON]["point"])
		self._campPointInfo[camp]["time"]=time
		#得分为0的一方输掉比赛，对方获胜
		if self._campPointInfo[camp]["point"]==0:
			self.winGame(self._getOpposedCamp(camp))


	def _getOpposedCamp( self, camp ):
		"""获取对立阵营"""
		if camp == csdefine.CAMP_TAOSIM:
			return csdefine.CAMP_DEMON
		else:
			return csdefine.CAMP_TAOSIM


	def isTowerCanGossip(self, scriptID, camp):
		"""哨塔能否交互"""
		info = self._towerInfo[scriptID]
		if not info:
			return False
		#哨塔未被对方夺取时，只能被对方交互
		if info["status"] == TOWER_STATUS_NORMAL:
			if info["camp"] == camp:
				return False
			else:
				return True
		#哨塔被对方夺取时，只能被已方交互
		elif info["status"] == TOWER_STATUS_LOST:
			if info["camp"] == camp:
				return True
			else:
				return False


	def isRevivePosCanGossip(self, scriptID, camp):
		"""复活点水晶能否被交互"""
		info = self._revivePosInfo.get(scriptID,None)
		if not info:
			return False
		#当水晶归属阵营与交互者阵营不同时才可交互
		if info["camp"] == camp:
			return False
		else:
			return True


	def gossipResultWithTower(self, scriptID, player):
		"""与哨塔交互"""
		info = self._towerInfo[scriptID]
		#夺取哨塔
		if info["camp"] != player.getCamp():
			self.takeTower(scriptID)
		#夺回哨塔
		else:
			self.takeBackTower(scriptID)

		self.memberDatas.occupyTower(player.id)
		#更新面板塔的占领情况
		for _player in self._spaceRoles:
			_player.client.CLIENT_OnFrozenFightOccupyTower( scriptID, player.getCamp(), _player.id)


	def onTowerBeAttack(self, towerID, attackID):
		"""
		哨塔被争夺 闪烁提示
		"""
		for _player in self._spaceRoles:
			_player.client.OnFrozenFightTowerBeAttack()


	def submitIceCrystals(self, player):
		"""
		提交冰晶核心
		"""
		itemInstList = player.getItemInstsByID(self.getScript().iceCrystalsItemID)
		if not len(itemInstList):
			return
		amount = 0
		for inst in itemInstList:
			amount += inst.amount
			player.removeItemByAmount( inst, amount, csdefine.ITEM_REMOVE_BY_USE )

		point = self._pointInfo["iceCrystals"] * amount
		camp = player.getCamp()
		self._addPoint(camp, point)
		self.memberDatas.submits(player.id, amount)
		#更新面板玩家冰晶提交数据
		for _player in self._spaceRoles:
			_player.client.CLIENT_OnFrozenFightSubmit(player.id, self.memberDatas[player.id]["submits"])


	def getReviveInfo(self, player):
		"""
		获取复活点信息
		"""
		camp = player.getCamp()
		minDist = 1000000
		pos = (0.0, 0.0, 0.0)
		dir = (0.0, 0.0, 0.0)
		for value in self._revivePosInfo.values():
			if value["camp"] == camp:
				_pos = Math.Vector3(value["pos"])
				dist = _pos.flatDistTo(player.position)
				if dist<=minDist:
					minDist = dist
					pos = value["pos"]
					dir = value["dir"]
		return (pos, dir)
