# -*- coding: utf-8 -*-

import KBEDebug
import KBEngine
import KBEMath
import Functions
import csdefine
import csstatus
import csconst
import cschannel_msgs
from ConfigObject import PatrolRouteLoader
from SpaceCopy import SpaceCopy
from Reward import RewardBasicValueData
import ZyjjRewardData
from ConfigObject.MailContentDataLoader import g_mailContentDataLoader

CAMP_NAMES = {	csdefine.CAMP_TAOSIM : cschannel_msgs.CAMP_TAOSIM,		#仙道
					csdefine.CAMP_DEMON : cschannel_msgs.CAMP_DEMON		#魔道
				}
FINAL_STAGE = 4

SPACE_LEVEL_CF = 40 #超凡
SPACE_LEVEL_CC = 60 #出尘
SPACE_LEVEL_RD = 80 #入道
SPACE_LEVEL_WD = 100 #问鼎

class SpaceCopySGMZ( SpaceCopy ):
	"""
	上古密阵
	"""
	def __init__( self ) :
		self.member = {1:"1",2:"2"}
		SpaceCopy.__init__( self )
		self.timeID = 0
		self.campStageDamage = {}	#记录阵营（之前是队伍）进度，通知客户端界面用的 self.campStageDamage[ camp ] = [stage, monsterPersent]
		self.leadCamp = None
		self.FinalBossScriptID = ""
		self.notArriveBossCamp=[csdefine.CAMP_TAOSIM,csdefine.CAMP_DEMON]	#没有到BOSS区域的阵营。提示用
		self.zyjjRewardDatas = ZyjjRewardData.ZyjjRewardDatas()
		self.playerData = {}
	
	def initSpaceData(self, monsterDict, stageListStr, finalBossScriptID  ):
		if "routeParams" in self.createArgs:
			for camp,route in self.createArgs["routeParams"].items():
				self.member[camp] = str(route)
		for index, camp in enumerate(list(self.member.keys())):
			self.camp_stage[ camp ] = [int(i) for i in stageListStr[ index ].split(" ")]	# {1: [1, 2, 3], 2: [4, 5, 6]}
		for camp,route in self.member.items():
			monsterList = monsterDict[ route ].split("|")
			self.memberDatas.add( camp, monsterList)
		self.FinalBossScriptID = finalBossScriptID
		
	def onEnter( self, playerRole, packArgs ):
		SpaceCopy.onEnter( self, playerRole, packArgs )
		playerRole.onEnterCampSGMZ()
		if self.timeID == 0:
			self.timeID = self.addTimerRepeat( 3.0 ,"sendMonsterHp",())
		if playerRole.playerDBID not in self.playerData:
			self.playerData[playerRole.playerDBID] = [playerRole.getCamp(),playerRole.getName()]

	def onTeleportCompleted( self, playerRole ):
		SpaceCopy.onTeleportCompleted(self,playerRole)
		for camp, stage_HP in self.campStageDamage.items():
			stage, value = stage_HP
			if stage == FINAL_STAGE:
				playerRole.client.SGMZSendMonsterHp( camp, FINAL_STAGE-1, 0)		#如果是最后一个阶段，要把之前BOSS的血量更新给客户端。如果不是，就等自动更新即可
			playerRole.client.CLIENT_SGMZBossKilled( camp, max( stage-1,0 ))			#之前死的BOSS都打上击破的动画
		
	def sendMonsterHp(self):
		"""
		发送怪物血量信息
		"""
		for camp,stage_HP in self.campStageDamage.items():
			stage, value = stage_HP
			for roleCell in self._spaceRoles:
				if stage != FINAL_STAGE:
					roleCell.client.SGMZSendMonsterHp( camp, stage, int(value*100))		#value 是monsterPersent
				else:
					roleCell.client.SGMZSendScore( camp, stage, value)		#value 是score
			
	def addCampScore( self, camp, score ):
		"""
		统计积分
		"""
		if not camp in self.campStageDamage:
			self.campStageDamage[ camp ] = [FINAL_STAGE,score]
		elif self.campStageDamage[ camp ][0] !=FINAL_STAGE:
			self.campStageDamage[ camp ] = [ FINAL_STAGE, score ]
		else:
			self.campStageDamage[ camp ][1] += score
		self.showLeadCamp( camp )

	def onBossHPChanged(self, monsterEntity ):
		#队伍进度的界面表现
		if monsterEntity.HP == monsterEntity.HP_Max:return
		teamCamp = self.memberDatas.fromMonsterGetCamp( str(monsterEntity.scriptID))		#找到怪物对应的队伍
		stage = self.memberDatas.getMonsterStage( teamCamp, str(monsterEntity.scriptID))
		monsterPersent = float( monsterEntity.HP )/monsterEntity.HP_Max
		#boss打到血量50%有提示 
		if monsterPersent <= 0.5:
			if teamCamp not in self.campStageDamage or stage not in self.campStageDamage[teamCamp] or self.campStageDamage[teamCamp][1]>0.5:	#如果不在campStageDamage中,或者在，且记录的血量大于50%，说明还没提示过
				for roleCell in self._spaceRoles:
					if teamCamp != roleCell.getCamp():
						roleCell.statusMessage(csstatus.MI_ZHEN_BOSS_OUTOF_HP, CAMP_NAMES[teamCamp] , stage , monsterEntity.getUname(),monsterEntity.getUname())
		self.campStageDamage[ teamCamp ] = [stage, monsterPersent]
		self.showLeadCamp(teamCamp)
		
	def showLeadCamp(self, teamCamp):
		#界面显示领先队伍的光效
		if self.leadCamp !=  teamCamp:
			if self.leadCamp == None:
				leadCamp = teamCamp
			else:
				if self.campStageDamage[ teamCamp ][0] == self.campStageDamage[ self.leadCamp  ][0]:		#进度相同
					if self.campStageDamage[ teamCamp ][0] == FINAL_STAGE:
						leadCamp = max( self.campStageDamage.items(), key = lambda x:x[1][1])[0]			#如果是FINAL_STAGE，那么积分多的领先
					else:
						leadCamp = min( self.campStageDamage.items(), key = lambda x:x[1][1])[0]			#如果不是FINAL_STAGE，那么剩余血量少的领先
				else:																						#进度不同，进度快的领先
					leadCamp = max( self.campStageDamage.items(), key = lambda x:x[1][0])[0]
			if self.leadCamp != leadCamp:			#领先队伍改变，通知客户端表现
				self.leadCamp = leadCamp
				for role in self._spaceRoles:
					role.client.SGMZLeadTeamChange( self.leadCamp )
	
	def getCampScore( self, camp ):
		"""
		获得积分
		"""
		stage_score = self.campStageDamage.get(camp,[])
		if not stage_score:
			return 0
		elif stage_score[0] != FINAL_STAGE:
			return 0
		else:
			return stage_score[1]
			
	def getCampByStageIndex( self, stageIndex ):
		"""
		通过stageIndex取队伍，分别对应1237和4567
		"""
		for camp,stageList in self.camp_stage.items():
			if stageIndex in stageList:
				return camp

	def onMonsterBeKill(self, monsterID, killer, rate):
		"""
		击杀了普通Boss
		"""
		bossEntity = KBEngine.entities.get(monsterID)
		if not bossEntity:
			KBEDebug.ERROR_MSG("monsterID(%i) is None"%( monsterID ))
			return
		if bossEntity.getEntityFlag() != csdefine.ENTITY_FLAG_MONSTER:
			KBEDebug.ERROR_MSG("monsterID(%i) is not Monster"%( monsterID ))
			return
		if bossEntity.scriptID == self.FinalBossScriptID:
			return
		camp =  killer.getCamp()
		costTime = int (( Functions.getTime()- self.campStageStartTime[ camp ]) / csconst.TIME_ENLARGE_MULTIPLE  )		
		#exp = int(self.recordStageExp[ camp ])
		#level = max( 3-int(costTime / 180 ), 0 )						#上限是3，每超过3分钟降一级，最低为0
		if costTime >= 0 and costTime < 180:
			level = SPACE_LEVEL_WD
		elif costTime >= 180 and costTime < 240:
			level = SPACE_LEVEL_RD
		elif costTime >= 240 and costTime < 360:
			level = SPACE_LEVEL_CC
		else:
			level = SPACE_LEVEL_CF
		exp = int(rate * RewardBasicValueData.datas.get(bossEntity.getLevel(), {}).get("exp", 0) * float(level / 100))
		stage = self.memberDatas.getMonsterStage( camp,str(bossEntity.scriptID) )
		self.memberDatas.onKillBoss( camp, bossEntity.scriptID, bossEntity.getUname(), costTime, exp, level)
		killer.addExp(exp,csdefine.EXP_ADD_REASON_SGMZ_KILL_BOSS)
		for roleCell in self._spaceRoles:
			roleCell.statusMessage(csstatus.MI_ZHEN_KILL_BOSS, CAMP_NAMES[camp], stage ,bossEntity.getUname(), exp, costTime)
			roleCell.client.CLIENT_SGMZBossKilled( camp, stage )

	def onFinalBossBeKill(self, monsterID, extraExp, killer):
		"""
		击杀了最终Boss
		"""
		bossEntity = KBEngine.entities.get(monsterID)
		if not bossEntity:
			KBEDebug.ERROR_MSG("monsterID(%i) is None"%( monsterID ))
			return
		if bossEntity.getEntityFlag() != csdefine.ENTITY_FLAG_MONSTER:
			KBEDebug.ERROR_MSG("monsterID(%i) is not Monster"%( monsterID ))
			return
		killerCamp = killer.getCamp()
		exp = int(self.getScript().getRewardExpRate() * RewardBasicValueData.datas.get(bossEntity.getLevel(), {}).get("exp", 0))
		winCamp = sorted( self.campStageDamage.items(), key = lambda x:x[1][1] ,reverse=True)[0][0]
		self.memberDatas.onKillFinalBoss( winCamp, extraExp, killerCamp, killer.getName() )
		damagePersent = bossEntity.campDamageDict[csdefine.CAMP_TAOSIM]/ bossEntity.HP_Max
		if bossEntity.campDamageDict[csdefine.CAMP_TAOSIM] == bossEntity.HP_Max or bossEntity.campDamageDict[csdefine.CAMP_DEMON] == bossEntity.HP_Max:
			damagePersent = 1.0
		taosimRewardExp = int( exp * damagePersent )
		demonRewardExp = exp - taosimRewardExp
		for camp in [csdefine.CAMP_TAOSIM,csdefine.CAMP_DEMON]:
			score = self.getCampScore(camp)
			if camp == csdefine.CAMP_TAOSIM:
				rewardExp = taosimRewardExp
				tempPersent = damagePersent
			else:
				rewardExp = demonRewardExp
				tempPersent = 1.0 - damagePersent
			if winCamp == camp:
				rewardFeats = self.getScript().getSuccessRewardFeats()
			else:
				rewardFeats = self.getScript().getFailRewardFeats()

			costTime = int (( Functions.getTime()- self.campStageStartTime[ camp ]) / csconst.TIME_ENLARGE_MULTIPLE  )
			if costTime >= 0 and costTime < 180:
				level = SPACE_LEVEL_WD
			elif costTime >= 180 and costTime < 240:
				level = SPACE_LEVEL_RD
			elif costTime >= 240 and costTime < 360:
				level = SPACE_LEVEL_CC
			else:
				level = SPACE_LEVEL_CF
			self.memberDatas.onKillBoss( camp, bossEntity.scriptID, bossEntity.getUname(), costTime, rewardExp, level, tempPersent, rewardFeats, score )
			for roleCell in self._spaceRoles:
				roleCell.setSpaceRelationRule( csdefine.ROLE_RELATION_RULE_PEACE )
				if camp == roleCell.getCamp():
					self.addFinalExpReward(roleCell, int(rewardExp* float(level / 100) ), csdefine.EXP_ADD_REASON_SPACE_SENTLEMENT)
					self.addFeatsReward(roleCell, rewardFeats, csdefine.FEATS_ADD_REASON_CAMP)
					roleCell.statusMessage( csstatus.MI_ZHEN_KILL_LAST_BOSS, killer.getName(), CAMP_NAMES[ killer.getCamp() ] )	
		
	def onRoleBeKill( self, killEntity, dieEntity, param1=0 ):
		"""
		玩家被击杀,积分变化
		"""
		if killEntity.entityFlag != csdefine.ENTITY_FLAG_ROLE:
			return
		campKiller = killEntity.getCamp()
		campDier = dieEntity.getCamp()
		scoreChange = int( self.getCampScore(campDier) *0.05 )
		self.addCampScore( campKiller, scoreChange )
		self.addCampScore( campDier, -scoreChange )
		killEntity.addFeats(self.getScript().getKillRoleRewardFeats(),csdefine.FEATS_ADD_REASON_SGMZ_KILL_ROLE)
		killEntity.addExploit( self.getScript().getKillRoleRewardExploit() )
		rewardExp = int(self.getScript().getKillRoleExpRate() * RewardBasicValueData.datas.get(dieEntity.getLevel(), {}).get("exp", 0))
		killEntity.addExp( rewardExp, csdefine.EXP_ADD_REASON_SGMZ_KILL_ROLE )
		for roleCell in self._spaceRoles:
			roleCell.client.SGMZSendScoreChange( campKiller, scoreChange )		#value 是score


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
					

	def addFinalExploitReward(self):
		"""
		"""
		winCamp = sorted( self.campStageDamage.items(), key = lambda x:x[1][1] ,reverse=True)[0][0]
		for role in self._spaceRoles:
			if role.getCamp() == winCamp:
				role.addExploit( self.getScript().getSuccessRewardExploit() )
				self.zyjjRewardDatas.addExploit( role.playerDBID, self.getScript().getSuccessRewardExploit() )
			else:
				role.addExploit( self.getScript().getFailRewardExploit() )
				self.zyjjRewardDatas.addExploit( role.playerDBID, self.getScript().getFailRewardExploit() )

	def addFinalExpReward(self, playerRole, value, reason):
		"""
		"""
		playerRole.addExp(value, reason)
		self.zyjjRewardDatas.addExp(playerRole.playerDBID, value)

	def addFeatsReward(self, playerRole, value, reason):
		"""
		"""
		playerRole.addFeats(value, reason)
		self.zyjjRewardDatas.addFeats(playerRole.playerDBID, value)

	def addLogoutMemberReward( self ):
		"""
		"""
		dbidList = []
		for role in self._spaceRoles:
			dbidList.append( role.playerDBID )
		winCamp = sorted( self.campStageDamage.items(), key = lambda x:x[1][1] ,reverse=True)[0][0]
		for playerDBID, playerDataList in self.playerData.items():
			if playerDBID not in dbidList:
				if winCamp == playerDataList[0]:
					g_mailContentDataLoader.sendSpaceReward( self.getScript().getSuccRewardMailToLogonOutPlayer(), playerDataList[1] )
				else:
					g_mailContentDataLoader.sendSpaceReward( self.getScript().getFailRewardMailToLogonOutPlayer(), playerDataList[1] )