# -*- coding: utf-8 -*-

import random
import KBEDebug
from SpaceCopyRingTask import SpaceCopyRingTask
import Math
import KBEngine
import csdefine
import Functions
import KBEMath

KEY_S = "123"
KEY_F = "321"
KEY_C = "666"
class SpaceCopyShenYueDiaoXiang( SpaceCopyRingTask ):
	"""
	神乐雕像副本
	"""
	def __init__( self ) :
		self.lingqiuIndex = 0 			#当前灵球的位置
		self.createTimerID = 0
		self.patrolListsIndex = 0 		#巡逻路线列表index
		self.lastYueQiScriptID = "" 	#上次刷的乐器ID
		self.yueqiScriptIDs =[]
		self.submitInfoDict = {}
		self.readyStatueInfoDict = {}
		SpaceCopyRingTask.__init__( self )


	def initSpaceData(self, shentanPos, lingqiuNum, lingqiuScriptID, submitInfoDict, statueNum):
		self.shentanPos = shentanPos
		self.lingqiuNum = lingqiuNum
		self.lingqiuScriptID = lingqiuScriptID
		self.statueNum = statueNum
		
		#从配置中随机选择几个雕像数据
		keys = random.sample(submitInfoDict.keys(), self.statueNum)
		for key in keys:
			self.submitInfoDict[key] = submitInfoDict[key]
			self.yueqiScriptIDs.append(self.submitInfoDict[key]["yueqiID"])
			submitInfoDict.pop(key)
		self.readyStatueInfoDict = dict(submitInfoDict)

	def initStatue(self):
		"""
		初始化雕像
		根据配置刷出雕像交互对象 并且给不需要交互的大雕像上挂件
		"""
		for key, value in self.submitInfoDict.items():
			scriptID = key
			position = (0.0, 0.0, 0.0)
			direction = (0.0, 0.0, 0.0)
			pos = Functions.vector3TypeConvert(value["pos"])
			if pos:
				position = KBEMath.Unreal2KBEnginePosition( pos )
			dire =  Functions.vector3TypeConvert(value["dire"])
			if dire:
				direction = KBEMath.Unreal2KBEngineDirection(dire)
			self.createEntityByScriptID(scriptID, position, direction, {})	

		for key, value in self.readyStatueInfoDict.items():
			statueBuffID = [int(buffID) for buffID in value["statueBuffID"].split("|")]
			#给雕像上乐器
			esIDs = self.getEntityRecord(value["statueID"])
			if len(esIDs)>0:
				statue = KBEngine.entities.get(esIDs[0],None)
				if statue:
					for buffID in statueBuffID:
						statue.addBuff(statue, buffID)

	def removeYueqi(self, scriptID):
		"""
		从列表中移除指定scriptID
		"""
		if scriptID in self.yueqiScriptIDs:
			self.yueqiScriptIDs.remove(scriptID)

	def createLingQiu(self, delayTime):
		"""
		刷灵球
		一次连续发射出15个灵球。15个灵球中会有一个灵球装有随机一把乐器，乐器有笛、萧、锣、钹、鼓、琴、二胡和琵琶8种
		"""
		#随机刷灵球的位置
		if not len(self.yueqiScriptIDs):
			return
		info = random.choice(self.shentanPos)

		#随机带有乐器的灵球ScriptID
		yueqiScriptIDs = list(self.yueqiScriptIDs)
		if self.lastYueQiScriptID in yueqiScriptIDs and len(yueqiScriptIDs)>1:
			yueqiScriptIDs.remove(self.lastYueQiScriptID)
		yueqiScriptID = random.choice(yueqiScriptIDs)
		self.lastYueQiScriptID = yueqiScriptID

		#随机出带有乐器的灵球位置
		yueqiIndex = random.randint(1, self.lingqiuNum)

		self.createTimerID = self.addTimerRepeat(delayTime, "_createLQ", (yueqiScriptID, self.lingqiuScriptID, yueqiIndex, info))
		

	def _createLQ(self, yueqiScriptID, lingqiuScriptID, yueqiIndex, info):
		"""
		"""
		pos = info["pos"]
		patrolLists = info["patrolLists"]
		if self.lingqiuIndex > self.lingqiuNum:
			self.popTimer(self.createTimerID)
			self.createTimerID = 0
			self.lingqiuIndex = 1
			self.patrolListsIndex = 0
			return

		if yueqiIndex == self.lingqiuIndex:
			scriptID = yueqiScriptID
		else:
			scriptID = lingqiuScriptID
		self.lingqiuIndex+=1
		self.createEntityByScriptID(str(scriptID), pos, (0.0,0.0,0.0),{"spawnPos":pos, "patrolList":patrolLists[self.patrolListsIndex]})
		self.patrolListsIndex = (self.patrolListsIndex+1) % len(patrolLists)


	def submitYueQi(self, boxEntity, player):
		"""
		提交乐器
		"""
		scriptID = boxEntity.scriptID
		info = self.submitInfoDict[scriptID]
		sceneID = info["sceneID"] 		#镜头ID
		statueID = info["statueID"]		 #雕像scriptID
		playerBuffID = info["playerBuffID"] #根据玩家身上是否有次buff 判断提交结果	
		statueBuffID = [int(buffID) for buffID in info["statueBuffID"].split("|")] 	#提交正确 给目标上挂件buffID
		monsterID = info["monsterID"] 	#提交错误 刷怪ID
		yueqiID = info["yueqiID"] 		#乐器ID

		#提交正确乐器
		if len(player.findBuffsByBuffID(playerBuffID)):
			player.client.StartPlayStory( sceneID, 1 )
			self.removeYueqi(yueqiID)
			#给雕像上乐器
			esIDs = self.getEntityRecord(statueID)
			if len(esIDs)>0:
				statue = KBEngine.entities.get(esIDs[0],None)
				if statue:
					for buffID in statueBuffID:
						statue.addBuff(statue, buffID)
					#通知副本提交成功
					self.getScript().onConditionChange( self, "", "", KEY_S, "" )
					self.getScript().spaceEvent_addCount(self, KEY_C, 1)
		#提交错误乐器
		else:
			#在交互目标当前位置刷出一只怪，销毁交互目标
			self.createEntityByScriptID(monsterID, boxEntity.position, boxEntity.direction, {"spawnPos":boxEntity.position})
			#通知副本提交错误
			self.getScript().onConditionChange( self, "", "", KEY_F, "" )
		boxEntity.destroySelf()
		#移除玩家持有乐器的buff
		player.removeBuffByEffect("HoldEffectAddOnsMesh")