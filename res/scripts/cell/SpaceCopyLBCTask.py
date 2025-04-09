#-*-coding:utf-8 -*-

import KBEngine
from SpaceCopy import SpaceCopy
import Functions
import KBEMath
import KBEDebug
import copy
import random
from Barracks.TrainingGroundCombatDatas import Datas as TGCombatDatas
import Const
import csdefine
import math
import Math


class SpaceCopyLBCTask(SpaceCopy):
	"""
	"""
	def __init__(self):
		SpaceCopy.__init__(self)
		self.pointDatas = []
		self.monsterDatas= []
		self.moveSpeed = 6.0
		self.actionTimes = 1
		self.index = 0
		self.isReversed = False
		self.vectoryTimes = 0 #胜利次数
		self.initData()
		

	def initData(self):
		"""
		"""
		self.pointDatas = copy.deepcopy(self.getScript().pointDatas)
		self.monsterDatas = copy.deepcopy(self.getScript().monsterDatas)
		self.taskExp = copy.deepcopy(self.getScript().taskExp)
		self.sceneDatas = copy.deepcopy(self.getScript().sceneDatas)
		self.routes = copy.deepcopy(self.getScript().routes)
		self.voiceIDs = copy.deepcopy(self.getScript().voiceIDs)
		self.actionTimes = self.getScript().actionTimes
		#每次随机一个方向
		self.isReversed = random.choice([0,1])
		if self.isReversed:
			self.pointDatas.reverse()
			self.monsterDatas.reverse()
			self.taskExp.reverse()
			self.sceneDatas.reverse()
			self.routes.reverse()
			self.voiceIDs.reverse()
			for posList in self.routes:
				posList.reverse()

	def startPlay(self):
		"""
		游戏开始
		"""
		self.actionBegin()


	def actionBegin(self):
		"""
		行动
		1.玩家移动到指定点
		2.刷出当前index对应的怪物
		"""
		self.moveRole()
		if self.isReversed:
			delayTime = self.getScript().createMonsterDelayReverse[self.index]
		else:
			delayTime = self.getScript().createMonsterDelay[self.index]
		self.addTimerCallBack(delayTime, "createLbcMonster",())
		

	def beginFight(self):
		"""
		接敌，做战斗表现
		"""
		#隐藏模型
		role = self.getRole()
		monster = self.getMonster()
		monster.destroySelf()
		#设置玩家头顶光效
		role.addBuff(role, self.getScript().battleBuffID)

		if not role:
			KBEDebug.ERROR_MSG("role is not exist!")
			return
		else:
			role.setTemp("extraModelNumber", role.extraModelNumber)
			role.setTemp("armyModelList", role.armyModelList)
			role.setExtraModelNumber("")
			role.resetArmyModelList()
			#播放战斗镜头
			data = self.sceneDatas[self.index]
			role.client.StartPlayStory(data["sceneID"], 1)
			result,args = self.calc()
			self.addTimerCallBack(data["sceneTime"], "endFight",(result,args))

	def endFight(self, result, args):
		"""
		战斗结束
		"""
		role = self.getRole()
		#经验奖励
		exp = args[1]
		role.addBarracksExp( exp )
		#恢复模型
		role.setExtraModelNumber(role.queryTemp("extraModelNumber"))
		role.setArmyModelList(role.queryTemp("armyModelList"))
		if role.findBuffsByBuffID(self.getScript().battleBuffID):
			role.removeBuffByID(self.getScript().battleBuffID)

		role.client.ShowLbcTaskResult(result, *args)

		self.actionEnd(result)


	def actionEnd(self, result):
		"""
		行动结束
		如果剩余行动次数不为0，进行下一个回合的行动
		"""
		if result:
			self.vectory()
		else:
			#失败，怪物部队返回
			self.defeat()

		self.actionTimes-=1

		if self.actionTimes>0:
			self.addTimerCallBack(4.0, "doNextAction", ())
		else:
			self.overPlay()


	def doNextAction(self):
		"""
		下一步行动
		"""
		self.index+=1
		self.actionBegin()


	def overPlay(self):
		"""
		游戏结束
		"""
		voiceID = self.getLeaveVoiceID(self.vectoryTimes)
		self.getRole().showMessagePlaySound(voiceID)
		self.addTimerCallBack(5.0, "closeSpace", ())
		

	def getLeaveVoiceID(self, vectoryTimes):
		"""
		获取获胜语音ID
		"""
		key = str(vectoryTimes)
		return  self.getScript().leaveVoiceIDs[key] if key in self.getScript().leaveVoiceIDs else ""


	def moveMonster(self):
		"""
		"""
		#怪物移动到指定点
		monster = self.getMonster()
		targetPos = KBEMath.Unreal2KBEnginePosition(self.routes[self.index][-1])
		monster.gotoPosition(targetPos)
		#播放一条语音
		role = self.getRole()
		voiceID = self.voiceIDs[self.index]
		role.showMessagePlaySound(voiceID)


	def moveRole(self):
		"""
		"""
		role = self.getRole()
		if not role:
			KBEDebug.ERROR_MSG("role is None")
			return
		posList = self.routes[self.index]
		moveSpeed = self.getScript().moveSpeed
		nearDist = self.getScript().nearDist
		role.client.RoleMoveToLocation(posList, moveSpeed, nearDist)


	def createLbcMonster(self):
		"""
		"""
		scriptID = self.getScript().cmderID
		spawnPos = self.pointDatas[self.index]["spawnPos"]
		spawnDir = self.pointDatas[self.index]["spawnDir"]
		
		params = {
			"extraModelNumber":self.monsterDatas[self.index]["cmderModel"],
			"armyModelList":[self.monsterDatas[self.index]["soldierModel"]],
			"spawnPos":spawnPos,
			}
		self.createMonster(scriptID, spawnPos, spawnDir, params)


	def vectory(self):
		"""
		玩家获胜
		"""
		self.vectoryTimes+=1
		#胜利，播放胜利光效
		role = self.getRole()
		role.client.CLIENT_OnPlayParticles(role.id, self.getScript().vectoryEffectID, "", -1.0, Math.Vector3(0,0,0))
		#创建怪物尸体
		soldierModel = self.monsterDatas[self.index]["soldierModel"]
		centerPos = self.routes[self.index][-1]
		amount = self.getScript().bodyAmount
		radius = self.getScript().bodyRadius
		role.client.LbcTaskCreateBody(soldierModel, amount, radius, centerPos)


	def defeat(self):
		"""
		玩家失败
		"""
		pass



	def getMonster(self):
		"""
		"""
		scriptID = self.getScript().cmderID
		monsterID = self.getEntityRecord(scriptID)[-1]
		return KBEngine.entities.get(monsterID, None)


	def getRole(self):
		"""
		"""
		return self.getSpaceRoles()[0] if self.getSpaceRoles() else None


	def calc(self):
		"""
		判断胜负
		"""
		role = self.getRole()
		army = role.getRoleArmyDataByID(self.index)
		playerCombat = self.calcRoleCombat(army)
		enemyCombat = self.calcEnemyCombat()
		combatRate = playerCombat / enemyCombat if enemyCombat!=0 else playerCombat*100
		if combatRate < Const.TRAIN_GROUND_QUEST_MIN_RATE_NUM:
			result = 0
		elif combatRate >= Const.TRAIN_GROUND_QUEST_MAX_RATE_NUM:
			result = 1
		else:
			result = int( math.pow( (math.sin( combatRate - 1) + 1), 1.8 ) * 0.5 >= random.random() )
		
		if combatRate == 0:
			rate = 0.01
		rate = combatRate if not combatRate==0 else 0.01
		if result:
			averLossNum = round( 1 / rate * 1.125)
			exp = self.taskExp[self.index][0]
		else:
			averLossNum = round(1 / rate * 3.375)
			exp = self.taskExp[self.index][1]
		addExp = 0
		if role.findLastBuffByBuffID( Const.TRAIN_GROUND_QUEST_DOU_BUFF ) >= 0:
			addExp = exp
			exp += addExp
		elif role.findLastBuffByBuffID( Const.TRAIN_GROUND_QUEST_POiNT_FIVE_BUFF ) >= 0:
			addExp = int( exp / 2 )
			exp += addExp
		
		
		lossNum = min( max(averLossNum + random.randint(-3, 3), 0), len(army.soldierIDs)) if army else 0
		lossSoldiers = random.sample(army.soldierIDs, lossNum) if lossNum>0 else []
		for id in lossSoldiers:
			role.onSoliderDead( self.index, csdefine.BARRACKS_SOLDIER_COMMON_TYPE, army.soldierScriptID, id )
		cmderScriptID = self.monsterDatas[self.index]["cmderScriptID"]
		firstGuardScriptID = army.firstGuardScriptID if army else ""
		args = (firstGuardScriptID, exp, addExp, lossNum, cmderScriptID)

		return result, args

	def calcEnemyCombat(self):
		"""
		"""
		data = self.monsterDatas[self.index]
		totalCombat = 0
		cmderScriptID = data["cmderScriptID"]
		cmderLevel = data["cmderLevel"]
		soldierScriptID = data["soldierScriptID"]
		soldierLevel = data["soldierLevel"]
		soldierNum = data["soldierNum"]
		
		cmderCombat = self.getMonsterCombat(cmderScriptID, cmderLevel)
		soldierCombat = self.getMonsterCombat(soldierScriptID, soldierLevel)*soldierNum

		return cmderCombat+soldierCombat

	def calcRoleCombat(self, army):
		"""
		策划的需求是取玩家身上对应的部队 如果index是0 则去部队index为0的队伍进行战斗力计算
		"""
		if not army:
			return 0
		role = self.getRole()
		totalCombat = 0
		tempDict = {}
		tempList = []
		tempList.extend( role.roleBarracksMgr.getBarracksSoldiersByScriptID( csdefine.BARRACKS_SOLDIER_GUARD_TYPE, army.firstGuardScriptID ) )
		tempList.extend( role.roleBarracksMgr.getBarracksSoldiersByScriptID( csdefine.BARRACKS_SOLDIER_GUARD_TYPE, army.secondGuardScriptID ) )
		soldiers = role.roleBarracksMgr.getBarracksSoldiersByScriptID( csdefine.BARRACKS_SOLDIER_COMMON_TYPE, army.soldierScriptID )
		for soldier in soldiers:
			if soldier.id in army.soldierIDs:
				tempList.append( soldier )
		for soldier in tempList:
			if not soldier.scriptID in tempDict:
				tempDict[soldier.scriptID] = []
			tempDict[soldier.scriptID].append( soldier.level )
		for scriptID, levels in tempDict.items():
			for level in levels:
				totalCombat += role.getSoldireCombat(scriptID, level)
		return totalCombat



	def getMonsterCombat(self, scriptID, level):
		"""
		"""
		if not scriptID in TGCombatDatas:
			KBEDebug.ERROR_MSG("cannot find soldier(%s) combat in the config(TrainingGroundCombatDatas)"%scriptID)
			return 0
		if not level in TGCombatDatas[scriptID]:
			KBEDebug.ERROR_MSG("cannot find soldier(%d) level(%d) combat in the config(TrainingGroundCombatDatas)"%(scriptID,level))
			return 0
		return TGCombatDatas[scriptID][level]



	def closeSpace( self ):
		"""
		<define method>
		关闭副本唯一入口，所有关闭副本操作（base或cell）都应该走此接口
		"""
		KBEDebug.DEBUG_MSG("Close space(%s)! scriptID:%s."%( self.id, self.scriptID ))
		self.clearCellAppDataBeforeClose()
		
		if len( self._spaceRoles ):
			for roleCell in self._spaceRoles:
				roleCell.leaveLbcTaskSpace(self)
			self.addTimerCallBack( 5, "closeSpace", () )	#5秒后再次关闭
			KBEDebug.DEBUG_MSG("Delay close space(%s) reason 1! scriptID:%s."%( self.id, self.scriptID ))
		
		elif len( self._readyEnterRoles ):
			for roleBase in self._readyEnterRoles:
				roleBase.cell.leaveLbcTaskSpace(self)
			self._readyEnterRoles = []
			self.addTimerCallBack( 5, "closeSpace", () )	#5秒后再次关闭
			KBEDebug.DEBUG_MSG("Delay close space(%s) reason 2! scriptID:%s."%( self.id, self.scriptID ))
		
		else:
			self.destroySelf()