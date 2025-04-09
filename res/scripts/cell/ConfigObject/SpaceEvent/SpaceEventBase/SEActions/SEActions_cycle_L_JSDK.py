# -*- coding: utf-8 -*-

# 副本事件行为
import random
import time
import KBEMath
import KBEDebug
import KBEngine
import Const
import Functions
import csdefine
from ObjectScript.SpawnPoint.SpawnPointFactory import g_spawnPointFactory
from ConfigObject.SpaceEvent.SpaceEventBase.SEActions.SEActionBase import SEActionBase
from ConfigObject.Quest.QuestBase.QuestLoader import g_QuestLoader
import ConfigObject.Reward.RewardBase.RewardMgr as RewardMgr
import Reward.RewardBasicValueData as RewardBase
import LogDefine
from MsgLogger import g_logger

class SEAction229( SEActionBase ):
	"""
	环任务【晶石洞窟】 晶石从怪物身上弹出
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self._minDistance = float(section["param1"])	# 最短距离
		self._maxDistance = float(section["param2"])	# 最大距离
		self._angle = float(section["param3"])			# 角度
		self._scriptID = section["param4"]				# 怪物的scriptID
		
	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return

		distance = random.uniform( self._minDistance, self._maxDistance )
		angle = random.uniform( -self._angle/2, self._angle/2 )
		entitylist = spaceEntity.getEntityRecord( self._scriptID )
		if len(entitylist) == 0: return
		entity = KBEngine.entities.get( entitylist[0], None )
		if not entity:
			return
		if entity.redCount == 0 and entity.yellowCount == 0 and entity.blueCount == 0:
			return
		if entity.redCount != 0:
			colorNum = 1
			entity.redCount -= 1
		elif entity.yellowCount != 0:
			colorNum = 2
			entity.yellowCount -= 1
		else:
			colorNum = 3
			entity.blueCount -= 1

		for player in spaceEntity._spaceRoles:
			if player.getClient():
				player.client.CLIENT_NotifyMonsterPopCrystal( entity.id, colorNum, float(angle), float(distance) )
				player.client.CLIENT_NotifyMonsterAddCount( colorNum, 1, False )

class SEAction230( SEActionBase ):
	"""
	环任务【晶石洞窟】 晶石从玩家身上弹出
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return

		for player in spaceEntity._spaceRoles:
			if spaceEntity.redCounts == 0 and spaceEntity.yellowCounts == 0 and spaceEntity.blueCounts == 0:
				return
			if spaceEntity.redCounts != 0:
				colorNum = 1
				spaceEntity.redCounts -= 1
			elif spaceEntity.yellowCounts != 0:
				colorNum = 2
				spaceEntity.yellowCounts -= 1
			else:
				colorNum = 3
				spaceEntity.blueCounts -= 1
			player.client.CLIENT_NotifyPlayerPopCrystal( colorNum )
			player.client.CLIENT_NotifyPlayerAddCount( colorNum, 1, False)

class SEAction243( SEActionBase ):
	"""
	环任务【晶石洞窟】 通知开始反弹
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		for player in spaceEntity._spaceRoles:
			if player.getClient():
				player.client.CLIENT_NotifyStartRebound( spaceEntity.colorNum )

class SEAction244( SEActionBase ):
	"""
	环任务【晶石洞窟】 通知开始刷新灵晶
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		spaceEntity.onRefreshSpiritCrystal()
		for player in spaceEntity._spaceRoles:
			if player.getClient():
				player.client.CLIENT_InitializeCrystalCount( spaceEntity.crystalCount1, spaceEntity.crystalCount2, spaceEntity.crystalCount3 )

class SEAction245( SEActionBase ):
	"""
	环任务【晶石洞窟】 通知开始掉灵晶
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self._scriptID = section["param1"]

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
			
		entitylist = spaceEntity.getEntityRecord( self._scriptID )
		if len(entitylist) == 0: return
		for player in spaceEntity._spaceRoles:
			if player.getClient():
				player.client.CLIENT_dropSpiritCrystal( entitylist[0], spaceEntity.spiritCrystalNum )

class SEAction246( SEActionBase ):
	"""
	环任务【晶石洞窟】 通知停止播放闪电
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self._scriptID = section["param1"]
		
	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return

		entitylist = spaceEntity.getEntityRecord( self._scriptID )
		if len(entitylist) == 0: return
		entity = KBEngine.entities.get( entitylist[0], None )
		if not entity:
			return
		for player in spaceEntity._spaceRoles:
			if player.getClient() and entity.touchCount >= 5:
				player.client.CLIENT_NotifyCrystalStopPlayLight()

class SEAction247(SEActionBase):
	"""
	环任务【晶石洞窟】奖励
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.questID = section["param1"].strip()
		self.msgInfo = section["param2"].strip()

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		num = spaceEntity.redCounts + spaceEntity.yellowCounts + spaceEntity.blueCounts
		for roleCell in spaceEntity._spaceRoles:
			roleCell.setLoopQuestTaskCompleteNum( num )
			if self.questID and self.msgInfo:
				quest = g_QuestLoader.getScript( int(self.questID) )
				gradeExpRatio, gradeMoneyRatio = quest.getGradeReward( roleCell )
				expRatio, moneyRatio = quest.getLoopRewardRadio( roleCell )
				
				expBase = RewardBase.datas[roleCell.level]["exp"]
				exp = int( expRatio * gradeExpRatio * expBase )
				money = 0
				if roleCell.loopQuest["isRewardMoney"]:
					moneyBase = RewardBase.datas[roleCell.level]["money"]
					money = int( moneyRatio * gradeMoneyRatio * moneyBase )
				roleCell.client.ShowLoopRewardTip( self.msgInfo + str(num), exp, money, 0, 0 )
				
				#添加日志
				startTime = int(spaceEntity.lifeStartTime)
				costTime = int(time.time() - spaceEntity.lifeStartTime)
				if int(exp) > 0:
					g_logger.roleActiveRecord(LogDefine.ACTIVE_SPACE_TYPE_JSTK, roleCell.accountDBID, roleCell.playerDBID, roleCell.getLevel(), 
						LogDefine.ACTIVE_REWARD_TYPE_EXP, exp, startTime, costTime, LogDefine.ACTIVE_STATE_TYPE_SUCCESS)
				if int(money) > 0:
					g_logger.roleActiveRecord(LogDefine.ACTIVE_SPACE_TYPE_JSTK, roleCell.accountDBID, roleCell.playerDBID, roleCell.getLevel(), 
						LogDefine.ACTIVE_REWARD_TYPE_MONEY, money, startTime, costTime, LogDefine.ACTIVE_STATE_TYPE_SUCCESS)
				
class SEAction248(SEActionBase):
	"""
	移除记录不能重复执行的某事件
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.eventType = int(section["param1"])

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		for roleCell in spaceEntity._spaceRoles:
			roleCell.getCurrentSpaceObject().removeSpaceEventRecord(spaceEntity, self.eventType)

class SEAction256( SEActionBase ):
	"""
	副本内所有玩家播放界面提示并播放声音（多个语音中随机播放其中一条）
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.soundIDList = section["param1"].split( "|" )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return

		soundID = random.choice( self.soundIDList )
		for e in spaceEntity._spaceRoles:
			e.showMessagePlaySound( soundID )

SEActionBase.setActionClass("SEAction229", SEAction229)
SEActionBase.setActionClass("SEAction230", SEAction230)
SEActionBase.setActionClass("SEAction243", SEAction243)
SEActionBase.setActionClass("SEAction244", SEAction244)
SEActionBase.setActionClass("SEAction245", SEAction245)
SEActionBase.setActionClass("SEAction246", SEAction246)
SEActionBase.setActionClass("SEAction247", SEAction247)
SEActionBase.setActionClass("SEAction248", SEAction248)
SEActionBase.setActionClass("SEAction256", SEAction256)