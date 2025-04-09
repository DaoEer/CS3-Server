
# -*- coding: utf-8 -*-
import KBEngine
import KBEDebug
import GMCommand
import KBEMath

import KST
import Math
import random
import Const
import csdefine
import csstatus
import math
import time
import LogDefine
from MsgLogger import g_logger

from ConfigObject.JiYuanCfgLoader import g_jiYuanCfgLoader
from Reward import RewardBasicValueData

class RoleSpaceContentInterface:
	"""
	玩家空间内容类
	"""
	def __init__( self ):
		"""
		初始化
		"""
		pass
	def beforeDestroy( self ):
		"""
		销毁前做一些事
		"""
		self.processVehicle()
		
	def onEnterDead(self):
		"""
		死亡
		"""
		#玩家死亡下载具
		self.processVehicle()
		# 跳伞恢复
		if self.parachutingState != csdefine.PARACHUTE_STATE_NORMAL:
			self.parachutingState = csdefine.PARACHUTE_STATE_NORMAL
		
#-------------------------环任务:欢乐鼎  JIRA:CST-2138------------------------------------
		
	def StartHLDRound( self, srcEntityID ):
		"""
		exposed method
		开始一波欢乐鼎大搬运
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			spaceEntity.getScript().onConditionChange( spaceEntity, "HLD", spaceEntity.id, "START", "" )

#-------------------------环任务:钓鱼  JIRA：CST-2140---------------------------------------

	def throwFishRod( self, srcEntityID, speed, fishFoodType ):
		"""
		exposed method
		甩鱼竿
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			spaceEntity.setTemp("fishFoodType",fishFoodType)
			spaceEntity.getScript().onConditionChange( spaceEntity, "FISH", spaceEntity.id, "START", str(speed) )

	def startCheckFish( self, entityID ):
		"""
		开始检测周围鱼
		entityID：鱼饵ID
		"""
		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			spaceEntity.setTemp("fishFoodEntity",entityID)
			spaceEntity.getScript().onConditionChange( spaceEntity, "FISH", spaceEntity.id, "CHECK", "")

	def ChangeWrestlingWidget( self ):
		"""
		改变界面为角力界面
		"""
		self.client.ChangeWrestlingWidget()

	def catchFishCheck( self, srcEntityID, power ):
		"""
		exposed method
		拉钩
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			spaceEntity.getScript().onConditionChange( spaceEntity, "FISH", spaceEntity.id, "CatchCheck", str(power) )

#----------------------------晶石狩猎场------------------------------------------------------

	def addPlayerIntegral( self, integral, isCanOverFlow = False ):
		"""
		增加 晶石狩猎场积分
		"""
		hasBuff = False
		#找到是否拥有某buffID 来增加积分
		for buffID in Const.INTEGRAL_DOUBLE_BUFF_LIST:
			buffList = self.findBuffsByBuffID(buffID)
			if len(buffList) > 0:
				hasBuff = True
		if hasBuff:
			integral = integral * 2
		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			spaceEntity.onAddPlayerIntegral( self,integral, isCanOverFlow )
		
#------------------------CST-11339 晶石狩猎场机缘玩法------------------
	def setSparHunTingTotalIntegral(self, value):
		"""
		设置晶石狩猎场总积分
		#玩家晶石狩猎场积分分为两部分：处于晶石狩猎场副本时的总积分和处于机缘副本时在机缘副本中获得的积分，
		#在机缘副本中获得的积分，会在玩家离开机缘副本并回到晶石狩猎场副本时累加到晶石狩猎场总积分上
		"""
		self.sparHunTingTotalIntegral = value
		
	def addSparHunTingTotalIntegral(self, value):
		"""
		添加晶石狩猎场总积分
		"""
		self.sparHunTingTotalIntegral += value
		
	def reduceSparHunTingTotalIntegral(self, value):
		"""
		减少晶石狩猎场总积分
		"""
		self.sparHunTingTotalIntegral -= value
		if self.sparHunTingTotalIntegral < 0:
			self.sparHunTingTotalIntegral = 0
		
	def setSparHunTingIntegral(self, value):
		"""
		设置晶石狩猎场机缘玩法积分
		"""
		self.sparHunTingIntegral = value
		
	def addSparHunTingIntegral(self, value):
		"""
		添加晶石狩猎场机缘玩法积分
		"""
		self.sparHunTingIntegral += value
	
	def playerExchangeToMoney(self, exchMoneyScale, integral):
		"""
		玩家的晶石狩猎场积分兑换成金钱
		"""
		if integral > 0:
			basicValue = RewardBasicValueData.datas.get(self.getLevel(), {}).get("money", 1)
			money = int(integral * exchMoneyScale * basicValue)
			self.addMoney( money, csdefine.MONEY_ADD_REASON_SPAR_HUN_TING )
			
			spaceEntity = self.getCurrentSpace()
			if spaceEntity:
				spaceEntity.onPlayerExchangeToMoney(self, integral, money)
		
		

#-----------------------------荷花法阵--------------------------------------------------------
				
	def dismountHeHua( self, srcEntityID ):
		"""
		exposed method
		下荷花
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		tempPos = self.queryTemp("CurrentPos",None)
		if not tempPos: #加入判断 防止有客户端连续调用下荷花导致报错
			return
		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			self.client.DismountHeHua()
			spaceEntity.createPieceByPieceType(tempPos)
			self.removeTemp("CurrentPos")
			self.dismountHeHuaRemoveBuff()

	def forceDismountHeHua( self ):
		"""
		强制玩家下荷花
		"""
		tempPos = self.queryTemp("CurrentPos",None)
		if tempPos:
			self.removeTemp("CurrentPos")
		if self.getClient():
			self.client.DismountHeHua()
		self.dismountHeHuaRemoveBuff()


	def dismountHeHuaRemoveBuff(self):
		"""
		下荷花移除buff
		"""
		profession = self.getProfession()
		gender = self.getGender()
		if profession == csdefine.CLASS_FIGHTER:
			if gender == csdefine.MALE:
				self.removeBuffByID(Const.BUFF_HHFZ_MALE_FIGHTER)
			else:
				self.removeBuffByID(Const.BUFF_HHFZ_FEMALE_FIGHTER)
		elif profession == csdefine.CLASS_SWORDMAN:
			if gender == csdefine.MALE:
				self.removeBuffByID(Const.BUFF_HHFZ_MALE_SWORDMAN)
			else:
				self.removeBuffByID(Const.BUFF_HHFZ_FEMALE_SWORDMAN)
		elif profession == csdefine.CLASS_ARCHER:
			if gender == csdefine.MALE:
				self.removeBuffByID(Const.BUFF_HHFZ_MALE_ARCHER)
			else:
				self.removeBuffByID(Const.BUFF_HHFZ_FEMALE_ARCHER)
		elif profession == csdefine.CLASS_MAGE:
			if gender == csdefine.MALE:
				self.removeBuffByID(Const.BUFF_HHFZ_MALE_MAGE)
			else:
				self.removeBuffByID(Const.BUFF_HHFZ_FEMALE_MAGE)


	def mountHeHuaAddBuff(self):
		"""
		上荷花添加buff
		"""
		profession = self.getProfession()
		gender = self.getGender()
		if profession == csdefine.CLASS_FIGHTER:
			if gender == csdefine.MALE:
				self.addBuff(self,Const.BUFF_HHFZ_MALE_FIGHTER)
			else:
				self.addBuff( self, Const.BUFF_HHFZ_FEMALE_FIGHTER )
		elif profession == csdefine.CLASS_SWORDMAN:
			if gender == csdefine.MALE:
				self.addBuff(self,Const.BUFF_HHFZ_MALE_SWORDMAN)
			else:
				self.addBuff( self, Const.BUFF_HHFZ_FEMALE_SWORDMAN )
		elif profession == csdefine.CLASS_ARCHER:
			if gender == csdefine.MALE:
				self.addBuff(self,Const.BUFF_HHFZ_MALE_ARCHER)
			else:
				self.addBuff( self, Const.BUFF_HHFZ_FEMALE_ARCHER )
		elif profession == csdefine.CLASS_MAGE:
			if gender == csdefine.MALE:
				self.addBuff(self,Const.BUFF_HHFZ_MALE_MAGE)
			else:
				self.addBuff( self, Const.BUFF_HHFZ_FEMALE_MAGE )
			

	def move( self, srcEntityID, moveType ):
		"""
		exposed method
		移动
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		spaceEntity = self.getCurrentSpace()
		if not spaceEntity:
			return
		targetPos = Math.Vector3(0,0,0)
		currentPos = self.queryTemp("CurrentPos")
		if currentPos == None:
			return
		if moveType == "w":   #上
			if spaceEntity.checkMoveforward(currentPos[0]):
				targetPos = Math.Vector3(spaceEntity.getBoardPosition( currentPos[0][0],currentPos[0][1]  + 1 ))
				self.setTemp("CurrentPos",[(currentPos[0][0] ,currentPos[0][1] + 1),currentPos[1]])

		elif moveType == "s": #下
			if spaceEntity.checkMoveDown(currentPos[0]):
				targetPos = Math.Vector3(spaceEntity.getBoardPosition( currentPos[0][0] ,currentPos[0][1] - 1))
				self.setTemp("CurrentPos",[(currentPos[0][0],currentPos[0][1] - 1),currentPos[1]])
			
		elif moveType == "a": #左
			if spaceEntity.checkMoveLeft(currentPos[0]):
				targetPos = Math.Vector3(spaceEntity.getBoardPosition( currentPos[0][0] - 1,currentPos[0][1] ))
				self.setTemp("CurrentPos",[(currentPos[0][0] - 1,currentPos[0][1]),currentPos[1]])

		elif moveType == "d": #右
			if spaceEntity.checkMoveRight(currentPos[0]):
				targetPos = Math.Vector3(spaceEntity.getBoardPosition( currentPos[0][0] + 1,currentPos[0][1] ))
				self.setTemp("CurrentPos",[(currentPos[0][0] + 1,currentPos[0][1]),currentPos[1]])

		if targetPos.length != 0:
			spaceEntity.removePiece(currentPos[0])
			srcPos = Math.Vector3(spaceEntity.getBoardPosition( currentPos[0][0], currentPos[0][1] ))
			distance = srcPos.distTo(targetPos)
			self.addTimerCallBack( distance/self.getSpeed(),"checkCoord",() )
			targetPos.y += 0.9 #抬高0.9的原因是为了磨合地图
		else:
			self.statusMessage(csstatus.HEHUAFAZHEN_NOT_CAN_MOVE,"")

		targetPos = KBEMath.KBEngine2UnrealPosition( tuple(targetPos) )
		self.client.MoveToTargetPosition( Math.Vector3(targetPos) )

	def checkCoord( self ):
		"""
		检查荷花阵
		"""
		spaceEntity = self.getCurrentSpace()
		if not spaceEntity:
			return
		tempPos = self.queryTemp("CurrentPos")
		if tempPos == None:
			return
		spaceEntity.setPointPiece(tempPos[0],tempPos[1])

		links = spaceEntity.checkCoordsLink([tempPos[0]])
		if not links:
			return
		self.dismountHeHua(self.id)


#----------------------------------------幻阵迷宫 相关---------------------------------------

	def CELL_requestRandomDice(self, srcEntityID):
		"""
		Exposed method
		幻阵迷宫请求点击按钮
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		
		spaceEntity = self.getCurrentSpace()
		if not spaceEntity:
			return
		
		spaceEntity.nextIsland(self)
		
	def CELL_onMagicMazeEndFly(self, srcEntityID):
		"""
		Exposed method
		幻阵迷宫结束飞行回调
		"""
		if not self.validateClientCall( srcEntityID ):
			return
			
		spaceEntity = self.getCurrentSpace()
		if not spaceEntity:
			return
		
		spaceEntity.onMagicMazeEndFly(self)

	def CELL_onMagicMazeNodeFly(self, srcEntityID):
		"""
		Exposed method
		幻阵迷宫飞行到第一个点后回调
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		spaceScriptID = self.getCurrentSpaceScriptID()
		if spaceScriptID == Const.MAZE_SPACE_SCRIPTID_ONE:
			dirPos = Const.MAZE_SPACE_DIRECTION_ONE
		elif spaceScriptID == Const.MAZE_SPACE_SCRIPTID_TWO:
			dirPos = Const.MAZE_SPACE_DIRECTION_TWO
		elif spaceScriptID == Const.MAZE_SPACE_SCRIPTID_THREE:
			dirPos = Const.MAZE_SPACE_DIRECTION_THREE
		else:
			dirPos = Const.MAZE_SPACE_DIRECTION_FOUR
		direction = KBEMath.Unreal2KBEngineDirection( dirPos )
		self.changeDirection(direction, csdefine.REASON_CHANGE_DIR_FORCE)
		if self.isInTeam():
			self.client.ShowMazeDice( self.isTeamCaptain() )
		else:
			self.client.ShowMazeDice(True)

	def onMagicMazeFallDown( self ):
		"""
		玩家掉落死亡回调
		"""
		spaceEntity = self.getCurrentSpace()
		if not spaceEntity:
			return
		spaceEntity.onMagicMazeFallDown( self )
			
	def CELL_playerAnswer(self, srcEntityID, questionID, answer):
		"""
		Exposed method
		幻阵迷宫回答问题
		"""
		if not self.validateClientCall( srcEntityID ):
			return
			
		spaceEntity = self.getCurrentSpace()
		if not spaceEntity:
			return
			
		spaceEntity.getScript().playerAnswer(spaceEntity, self, self.playerDBID, questionID, answer)
		
	def CELL_selectNextQuestion(self, srcEntityID):
		"""
		Exposed method
		幻阵迷宫选择下一个问题
		"""
		if not self.validateClientCall( srcEntityID ):
			return
			
		spaceEntity = self.getCurrentSpace()
		if not spaceEntity:
			return
			
		spaceEntity.getScript().selectNextQuestion(spaceEntity, self, self.playerDBID)

	def CELL_randomMagicMazeZhuanPan(self, srcEntityID):
		"""
		"""
		if not self.validateClientCall( srcEntityID ):
			return
			
		spaceEntity = self.getCurrentSpace()
		if not spaceEntity:
			return
			
		spaceEntity.getScript().randomZhuanPan(spaceEntity)

#------------------------------环任务 ：收集法宝碎片--------------------------------------
	def updateEnergyBar( self, curEnergy, maxEnergy ):
		"""
		CST-3740 更新能量条
		"""
		if curEnergy >= maxEnergy:
			curEnergy = maxEnergy
			self.closeReStoreEnergy()
		else:
			if curEnergy < 0:
				curEnergy = 0
			self.openRestoreEnergy()
			
		#当前是否能加速
		canAddSpeed = False
		_expendEnergy = self.queryTemp("expendEnergy")
		if _expendEnergy:
			if curEnergy >= _expendEnergy:
				canAddSpeed = True
			
		if self.queryTemp("isExpendEnergyAddSpeed", False):
			canAddSpeed = True
		
		self.setTemp("MaxEnergyValue",maxEnergy)
		self.setTemp("CurEnergyValue",curEnergy)
		self.client.UpdateEnergyBar( curEnergy, maxEnergy, canAddSpeed )
		
	
	def showFaBaoCollectSuccMsg( self, scriptID):
		"""
		法宝收集成功消息
		"""
		self.client.ShowFaBaoCollectSuccMsg(scriptID)
		
	#----------服务器玩家能量恢复 CST-4225------------------------------------
	def openRestoreEnergy( self ):
		"""
		"""
		if not self.restoreEnergyTimerID:
			self.restoreEnergyTimerID = self.addTimerRepeat( 1.0, "onRestoreEnergyTimer", () )
			
	def onRestoreEnergyTimer( self ):
		"""
		"""
		if self.isDestroyed:
			return
			
		_addSpeedBuffID = self.queryTemp("addSpeedBuffID")
		if not _addSpeedBuffID:
			KBEDebug.ERROR_MSG("RolePerformanceInterface:onRestoreEnergyTimer, not found buff")
			return
		
		#如果处于加速过程中，则不恢复能量
		if len(self.findBuffsByBuffID(_addSpeedBuffID)):
			return
			
		maxEnergyValue = self.queryTemp("MaxEnergyValue")
		curEnergyValue = self.queryTemp("CurEnergyValue")
		if maxEnergyValue is None or curEnergyValue is None:
			KBEDebug.ERROR_MSG("RolePerformanceInterface: onRestoreEnergyTimer, error")
			return
			
		curEnergyValue += 2
		if curEnergyValue > maxEnergyValue:
			curEnergyValue = maxEnergyValue
		
		self.updateEnergyBar( curEnergyValue, maxEnergyValue )
			
	def closeReStoreEnergy( self ):
		"""
		"""
		#移除定时器
		if self.restoreEnergyTimerID != 0:
			self.popTimer( self.restoreEnergyTimerID )
			self.restoreEnergyTimerID = 0
			
	def openAddSpeedExpendEnergy( self, srcEntityID ):
		"""
		Exposed method
		通过消耗能量开启加速
		"""
		if not self.validateClientCall( srcEntityID ):
			return
			
		maxEnergyValue = self.queryTemp("MaxEnergyValue")
		curEnergyValue = self.queryTemp("CurEnergyValue")
		if maxEnergyValue is None or curEnergyValue is None:
			KBEDebug.ERROR_MSG("RolePerformanceInterface: openAddSpeedExpendEnergy, error")
			return
		
		_expendEnergy = self.queryTemp("expendEnergy")
		if not _expendEnergy:
			KBEDebug.ERROR_MSG("RolePerformanceInterface:openAddSpeedExpendEnergy, get energy error")
			return
			
		_addSpeedBuffID = self.queryTemp("addSpeedBuffID")
		if not _addSpeedBuffID:
			KBEDebug.ERROR_MSG("RolePerformanceInterface:openAddSpeedExpendEnergy, not found buff")
			return
		
		#能量不够
		if curEnergyValue < _expendEnergy:
			return
			
		#看当前是否已经在加速状态
		_isExpendEnergyAddSpeed = self.queryTemp("isExpendEnergyAddSpeed", False)
		if _isExpendEnergyAddSpeed: return
		self.setTemp("isExpendEnergyAddSpeed", True)
		
		#不知道是什么原因，竟然已经加了一个定时器，那就打印一条警告
		if self.expendEnergyTimerID > 0:
			KBEDebug.WARNING_MSG("RolePerformanceInterface:openAddSpeedExpendEnergy, addTimer")
		else:
			self.expendEnergyTimerID = self.addTimerRepeat( 1.0, "onAddSpeedTimer", () )
		
		#看是否已经有相应的buff加在身上了
		if len(self.findBuffsByBuffID(_addSpeedBuffID)) <= 0:
			self.addBuff(self, _addSpeedBuffID)
		self.client.OnOpenAddSpeedExpendEnergy()
		
	def onAddSpeedTimer( self ):
		"""
		"""
		if self.isDestroyed:
			return
		
		maxEnergyValue = self.queryTemp("MaxEnergyValue")
		curEnergyValue = self.queryTemp("CurEnergyValue")
		if maxEnergyValue is None or curEnergyValue is None:
			KBEDebug.ERROR_MSG("RolePerformanceInterface: onAddSpeedTimer, error")
			return
		
		_expendEnergy = self.queryTemp("expendEnergy")
		if _expendEnergy is None:
			KBEDebug.ERROR_MSG("RolePerformanceInterface:onAddSpeedTimer, get energy error")
			return
		
		#能量不够，关闭消耗能量，移动加速的功能
		curEnergyValue -= _expendEnergy
		if curEnergyValue <= 0:
			curEnergyValue = 0
			self.closeAddSpeedExpendEnergy(self.id)
		
		#更新能量条
		self.updateEnergyBar(curEnergyValue, maxEnergyValue)
		
	def closeAddSpeedExpendEnergy( self, srcEntityID ):
		"""
		Exposed method
		关闭消耗能量来加速移动的功能
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		
		#移除状态标识
		_isExpendEnergyAddSpeed = self.queryTemp("isExpendEnergyAddSpeed")
		if _isExpendEnergyAddSpeed:
			self.removeTemp("isExpendEnergyAddSpeed")
		
		if self.expendEnergyTimerID != 0:
			self.popTimer( self.expendEnergyTimerID )
			self.expendEnergyTimerID = 0
		
		_addSpeedBuffID = self.queryTemp("addSpeedBuffID")
		if _addSpeedBuffID is None:
			KBEDebug.ERROR_MSG("RolePerformanceInterface:closeAddSpeedExpendEnergy, not found buff")
			return
		
		#移除buff
		if len(self.findBuffsByBuffID(_addSpeedBuffID)):
			self.removeBuffByID(_addSpeedBuffID)
		self.client.OnCloseAddSpeedExpendEnergy()
		
	def setExpendEnergyData(self, expendEnergy, addSpeedBuffID):
		"""
		设置几个临时数据
		"""
		self.setTemp("expendEnergy", expendEnergy)
		self.setTemp("addSpeedBuffID", addSpeedBuffID)
		
	def clearWithExpendEnergyData( self ):
		"""
		define method
		清理数据
		"""
		#移除定时器
		if self.restoreEnergyTimerID != 0:
			self.popTimer( self.restoreEnergyTimerID )
			self.restoreEnergyTimerID = 0
			
		if self.expendEnergyTimerID != 0:
			self.popTimer( self.expendEnergyTimerID )
			self.expendEnergyTimerID = 0
		
		#移除标识
		_isExpendEnergyAddSpeed = self.queryTemp("isExpendEnergyAddSpeed")
		if _isExpendEnergyAddSpeed:
			self.removeTemp("isExpendEnergyAddSpeed")
		
		_addSpeedBuffID = self.queryTemp("addSpeedBuffID")
		if _addSpeedBuffID is None:
			KBEDebug.ERROR_MSG("RolePerformanceInterface:clearWithExpendEnergyData, not found buff")
		else:
			#移除buff
			if len(self.findBuffsByBuffID(_addSpeedBuffID)):
				self.removeBuffByID(_addSpeedBuffID)
		
		#移除临时属性
		self.removeTemp("CurEnergyValue")
		self.removeTemp("MaxEnergyValue")
		self.removeTemp("expendEnergy")
		self.removeTemp("addSpeedBuffID")


#----------------------------------环任务：灵箭化元---------------------------------
	def transformShield( self, srcEntityID ):
		"""
		exposed method
		举起/放下 盾牌
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		profession = self.getProfession()
		if profession == csdefine.CLASS_FIGHTER:
			if len(self.findBuffsByBuffID(Const.BUFF_SHIELD_FIGHTER)) > 0:
				self.removeBuffByID(Const.BUFF_SHIELD_FIGHTER)
				return
			self.addBuff(self,Const.BUFF_SHIELD_FIGHTER)
		elif profession == csdefine.CLASS_SWORDMAN:
			if len(self.findBuffsByBuffID(Const.BUFF_SHIELD_SWORDMAN)) > 0:
				self.removeBuffByID(Const.BUFF_SHIELD_SWORDMAN)
				return
			self.addBuff(self,Const.BUFF_SHIELD_SWORDMAN)
		elif profession == csdefine.CLASS_ARCHER:
			if len(self.findBuffsByBuffID(Const.BUFF_SHIELD_ARCHER)) > 0:
				self.removeBuffByID(Const.BUFF_SHIELD_ARCHER)
				return
			self.addBuff(self,Const.BUFF_SHIELD_ARCHER)
		elif profession == csdefine.CLASS_MAGE:
			if len(self.findBuffsByBuffID(Const.BUFF_SHIELD_MAGE)) > 0:
				self.removeBuffByID(Const.BUFF_SHIELD_MAGE)
				return
			self.addBuff(self,Const.BUFF_SHIELD_MAGE)

#--------------------------幻阵迷宫 奇遇副本 逃出丹炉 JIRA:CST-4019--------------------------------

	def CELL_receiveFireDamage(self, srcEntityID):
		"""
		Exposed method
		玩家被火灼烧     CST-4019
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		self.addBuff( self, 12077901 )

	def CELL_receiveFireDamageEnd(self, srcEntityID):
		"""
		Exposed method
		玩家离开火灼烧     CST-4019
		"""
		if not self.validateClientCall( srcEntityID ):
			return
			
		self.removeBuffByID( 12077901 )	

	def CELL_destroyLinkTrap(self, srcEntityID, dstEntityID):
		"""
		Exposed method
		销毁光圈陷阱     CST-4019
		"""
		if not self.validateClientCall( srcEntityID ):
			return

		dstEntity = KBEngine.entities.get( int(dstEntityID), None )
		if dstEntity:
			dstEntity.destroySelf()

#---------------------------幻阵迷宫 奇遇副本 雷池阵 JIRA:CST-4358---------------------------------
	def CELL_enterThunderArea(self, srcEntityID):
		"""

		"""
		if not self.validateClientCall( srcEntityID ):
			return
		self.useSkillToEntity(120808001, self.id)


#---------------------------炼狱之塔副本 JIRA:CST-3135---------------------------------------------
	def onMovingPlatformTriggerBegin( self, playerID, dstEntityID ):
		"""
		Exposed method
		炼狱之塔机石柱撞到玩家  CST-3135
		"""
		if not self.validateClientCall( playerID ) or not dstEntityID:
			return
			
		player = KBEngine.entities.get( playerID, None )
		dstEntity = KBEngine.entities.get( int(dstEntityID), None )
		if dstEntity:
			dstEntity.onMovingPlatformTrigger(player)

	def CELL_onMovingPlatformTriggerStart( self, playerID, dstEntityID ):
		"""
		Exposed method
		炼狱之塔机石柱撞到玩家  CST-3135
		"""
		if not self.validateClientCall( playerID ):
			return

		player = KBEngine.entities.get( playerID, None )
		dstEntity = KBEngine.entities.get( int(dstEntityID), None )
		if dstEntity:
			dstEntity.onMovingPlatformTriggerStart(player)
		
			

#---------------------------幻莲天池 JIRA:CST-3803---------------------------------------------		
	def onPlayeTrampleLotus(self, srcEntityID, dstEntityID ):
		"""
		<Expose method>
		玩家踩在莲叶上
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		dstEntity = KBEngine.entities.get(int(dstEntityID), None)
		if dstEntity:
			dstEntity.onsTandLotus()

	def onFishHitPlayer(self, srcEntityID):
		"""
		<Expose method>
		金鱼溅出起的水珠撞到玩家	
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		self.client.CLIENT_OnPlayAction( "HitFly_01", -1.0 )

#---------------------------拷问剧情需求---------------------------------------------
	def CELL_onTortureNotice( self, srcEntityID, isHit ):
		"""
		<Expose method>
		是否打中指定区域
		@param	isHit 0:未打中，1:打中
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			if self.isInSpaceCopy() or self.isInSpacePlane():
				spaceEntity.getScript().onConditionChange( spaceEntity, "", srcEntityID, "ISHIT", isHit )

	def CELL_onMoveStartTorureNotice( self, srcEntityID ):
		"""
		<Expose method>
		玩家禁止移动
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		
		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			if self.isInSpaceCopy() or self.isInSpacePlane():
				spaceEntity.getScript().onConditionChange( spaceEntity, "", spaceEntity.id, "USEITEM", str(self.id))
				
	def CELL_onMoveEndTorureNotice( self, srcEntityID ):
		"""
		<Expose method>
		玩家取消禁止移动
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		
		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			if self.isInSpaceCopy() or self.isInSpacePlane():
				spaceEntity.getScript().onConditionChange( spaceEntity, "", spaceEntity.id, "CANCELUSEITEM", str(self.id))

	def CELL_onCameraEndMove( self, srcEntityID):
		"""
		<Expose method>
		视角改变完成
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		self.allClients.CLIENT_onStartTorureNotice()
		self.useSkillToEntity(Const.SKILL_KWWF_ROLE, self.id)
		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			if self.isInSpaceCopy() or self.isInSpacePlane():
				spaceEntity.getScript().onConditionChange( spaceEntity, "", spaceEntity.id, "ADDBUFF", str(self.id))

	def notifyContinueTorture( self ):
		"""
		通知客户端继续拷问
		"""
		self.client.CLIENT_onContinueTorture()


#---------------------------环任务【雷电晶石】---------------------------------------------
	def CELL_onEncounteredInDead( self, srcEntityID ):
		"""
		<Expose method>
		被电网碰到的玩家死亡
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		self.setHP( 0 )

#-----------------------------金沙古城------------------------------------------------------
	def onPlayerTouchLaser( self, srcEntityID ):
		"""
		<Expose method>
		玩家碰到激光死亡
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		self.useSkillToEntity(121016001, self.id)

#-----------------------------镇煞宫---------------------------------------------------------
	def onPlayerBeHammer( self, srcEntityID, dstEntityID ):
		"""
		<Expose method>
		玩家被石锤锤到
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		dstEntity = KBEngine.entities.get(int(dstEntityID), None)
		if dstEntity:
			dstEntity.onPlayerBeImpact(self.id)

	def onArmorLockBroke(self, srcEntityID, dstEntityID):
		"""
		<Expose method>
		怪物金钟罩消失
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		dstEntity = KBEngine.entities.get(int(dstEntityID), None)
		if dstEntity:
			buffs = dstEntity.findBuffsByBuffScript( "BuffShield" )
			for index in buffs:
				dstEntity.removeBuff(index)

#-----------------------------迷幻丛书---------------------------------------------------------
	def CELL_onPlayerMetSandman( self, srcEntityID ):
		"""
		玩家碰到瞌睡虫
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			spaceEntity.sandmanCollisionPunishment( self )

#-----------------------------密道历险---------------------------------------------------------
	def CELL_FireWallCallBack( self, srcEntityID ):
		"""
		<Expose method>
		玩家碰到火造成伤害
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		self.useSkillToEntity(121288001, self.id)


#-----------------------------神风秘径---------------------------------------------------------
	def CELL_onRoleDismountCopyGlede(self, srcEntityID, isThrow ):
		"""
		<Expose method>
		玩家落下老鹰
		"""
		if not self.validateClientCall( srcEntityID ):
			return

		self.triggerSkillEvent( csdefine.SKILL_EVENT_ROLE_DROP_GLEDE, self.id, {"isThrow" : int(isThrow)} )
		spaceEntity = self.getCurrentSpace()
		if int(isThrow):
			spaceEntity.getScript().onConditionChange( spaceEntity, "", spaceEntity.id, "SUCESS", "")
		else:
			spaceEntity.getScript().onConditionChange( spaceEntity, "", spaceEntity.id, "FAILS", "")

#---------------------------幻阵迷宫 奇遇 帝宫石印阵 JIRA:CST-4617---------------------------------
	def CELL_onInterruptBlowDGSZ(self, srcEntityID ):
		if not self.validateClientCall( srcEntityID ):
			return
		self.removeBuffByID(Const.BUFF_HHFZ_SWORDMAN)

#-----------------------------环任务【晶石洞窟】-------------------------------------------------------
	def CELL_onSpiritCrystalHitPlayer( self, srcEntityID ):
		"""
		<Expose method>
		灵晶击中玩家
		"""
		if not self.validateClientCall( srcEntityID ):
			return

		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			spaceEntity.onSpiritCrystalHitPlayer( self.id )

	def CELL_onCrystalHitMonster( self, srcEntityID ):
		"""
		<Expose method>
		水晶球击中怪物
		"""
		if not self.validateClientCall( srcEntityID ):
			return

		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			spaceEntity.onCrystalHitMonster()

	def CELL_onPlayerTouchCrystal( self, srcEntityID, colorNum ):
		"""
		<Expose method>
		玩家碰撞到灵晶
		"""
		if not self.validateClientCall( srcEntityID ):
			return

		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			spaceEntity.onPlayerTouchCrystal(colorNum)

	def CELL_onMonsterTouchCrystal( self, srcEntityID, colorNum ):
		"""
		<Expose method>
		怪物碰撞到灵晶
		"""
		if not self.validateClientCall( srcEntityID ):
			return

		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			spaceEntity.onMonsterTouchCrystal( colorNum )

	def CELL_onSpiritCrystalPos( self, srcEntityID, position ):
		"""
		<Expose method>
		掉落灵晶的位置
		"""
		if not self.validateClientCall( srcEntityID ):
			return

		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			spaceEntity.SpiritCrystalPos.append(tuple(position))
			#spaceEntity.moveToSpiritCrystalPos(position)

	def CELL_onRemoveSpiritCrystalNum( self, srcEntityID, spiritCrystalNum ):
		"""
		移除掉落的灵晶
		"""
		if not self.validateClientCall( srcEntityID ):
			return

		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			spaceEntity.onRemoveSpiritCrystalNum( spiritCrystalNum )

	def CELL_onRemoveSpiritCrystalPos( self, srcEntityID, position ):
		"""
		<Expose method>
		移除掉落灵晶的位置
		"""
		if not self.validateClientCall( srcEntityID ):
			return

		spaceEntity = self.getCurrentSpace()
		pos = tuple(position)
		if spaceEntity:
			if pos in spaceEntity.SpiritCrystalPos:
				spaceEntity.SpiritCrystalPos.remove( pos )
			#spaceEntity.moveToSpiritCrystalSkyPos()

	def CELL_onLocationBrushStrange( self, srcEntityID, colorNum, position ):
		"""
		<Expose method>
		在指定位置刷怪
		"""
		if not self.validateClientCall( srcEntityID ):
			return

		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			spaceEntity.getScript().onConditionChange( spaceEntity, "", srcEntityID, "ERROR", "" )
			spaceEntity.onLocationBrushStrange( colorNum, position )

#-----------------------------环任务消灭妖影-------------------------------------------------------
	def CELL_openMonsterMirror( self, srcEntityID ):
		"""
		exposed method
		打开照妖镜
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			spaceEntity.getScript().onConditionChange( spaceEntity, "",self.id,"OPEN","")
		if self.reduceLingEnergyTimerID > 0:
			KBEDebug.WARNING_MSG("RolePerformanceInterface:CELL_openMonsterMirror, addTimer")
		else:
			self.reduceLingEnergyTimerID = self.addTimerRepeat(1.0,"reduceLingEnergyValue",())

	def CELL_closeMonsterMirror( self, srcEntityID ):
		"""
		exposed method
		关闭照妖镜
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		if self.reduceLingEnergyTimerID:
			self.popTimer( self.reduceLingEnergyTimerID )
			self.reduceLingEnergyTimerID = 0
		if self.getClient():
			self.client.CLIENT_CloseMonsterMirror()

	def reduceLingEnergyValue( self ):
		"""
		减少灵能
		"""
		if self.isDestroyed:
			return

		curLingEnergyValue = self.queryTemp("curLingEnergyValue")
		maxLingEnergyValue = self.queryTemp("maxLingEnergyValue")
		reduceLingEnergyValue = self.queryTemp("reduceLingEnergyValue")
		isPlaySound = self.queryTemp("isPlaySound")
		mirrorSoundID = self.queryTemp("mirrorSoundID")
		if curLingEnergyValue is None or maxLingEnergyValue is None or reduceLingEnergyValue is None or isPlaySound is None:
			KBEDebug.ERROR_MSG("RolePerformanceInterface: reduceLingEnergyValue, error")
			return
		if curLingEnergyValue >= reduceLingEnergyValue:
			curLingEnergyValue -= reduceLingEnergyValue
			self.setTemp("curLingEnergyValue",curLingEnergyValue )
			if float(curLingEnergyValue) / maxLingEnergyValue <= 0.3 and not isPlaySound: # 少于百分之30 播放语音
				self.showMessagePlaySound(mirrorSoundID)
				self.setTemp("isPlaySound",1)
		else:
			self.CELL_closeMonsterMirror( self.id )
		if self.getClient():
			self.client.CLIENT_UpdateLingEnergyBar( maxLingEnergyValue, curLingEnergyValue, reduceLingEnergyValue )

	def CELL_MonsterListInMonsterMirror( self, srcEntityID, entityIDs ):
		"""
		exposed method
		某些怪物在照妖镜内
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		for entityID in entityIDs:
			entity = KBEngine.entities.get(entityID,None)
			if not entity or entity.getEntityFlag() != csdefine.ENTITY_FLAG_MONSTER:
				return
			entity.monsterAISendCommand( entity.id, "InMirror" )

	def CELL_MonsterOutMonsterMirror( self, srcEntityID, entityID ):
		"""
		exposed method
		怪物出了照妖镜
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		entity = KBEngine.entities.get(entityID,None)
		if not entity or entity.getEntityFlag() != csdefine.ENTITY_FLAG_MONSTER:
			return
		entity.monsterAISendCommand( entity.id, "OutMirror" )

#------------------------------环任务【仙岛归墟】------------------------------
	def FirstFloorPosition( self, srcEntityID, firstFloorPos, gridLenth, gridWidth ):
		"""
		第一个格子的宽度和长度和坐标
		exposed method
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		firstFloorPos = Math.Vector3(KBEMath.Unreal2KBEnginePosition( tuple(firstFloorPos) ))
		gridLenth = gridLenth / 100
		gridWidth = gridWidth / 100
		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			spaceEntity.firstFloorPosition( firstFloorPos, gridLenth, gridWidth )

	def CELL_floorStartFalling( self, srcEntityID ):
		"""
		玩家掉落
		exposed method
		"""
		if not self.validateClientCall( srcEntityID ):
			return

		self.changeState( csdefine.ENTITY_STATE_DEAD )

#-----------------------------环任务【玄天宝录】-------------------------------------------------------
	def CELL_onStoneInSunShone( self, srcEntityID, entityID ):
		"""
		exposed method
		怪物石像在日光中
		"""
		if not self.validateClientCall( srcEntityID ):
			return

		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			spaceEntity.onStoneInSunShone( entityID )

	def CELL_onStoneOutSunShone( self, srcEntityID, entityID ):
		"""
		exposed method
		怪物石像不在日光中
		"""
		if not self.validateClientCall( srcEntityID ):
			return

		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			spaceEntity.onStoneOutSunShone( entityID )

#-----------------------------CST-6262 蟠龙秘境-------------------------------------------------------
	def CELL_roleMountCarrier(self, srcEntityID, isMount):
		"""
		<Expose method>
		玩家上下载具
		"""
		if not self.validateClientCall( srcEntityID ):
			return

		self.triggerSkillEvent( csdefine.SKILL_EVENT_ROLE_PLMJ_CARRIER, self.id, {"isMount" : isMount} )

#-----------------------------CST-6262 冥域缉凶------------------------------------------------------
	def CELL_MYJXPressJumBtn( self, srcEntityID ):
		"""
		<Exposed method>
		玩家弹射出去
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		spaceEntity = self.getCurrentSpace()
		if not spaceEntity:
			return
		traps = spaceEntity.getEntityMailBoxRecord( Const.MYJX_MACHINE_TRAP_SCRIPTID )
		if not len( traps ):
			return
		pos = Math.Vector3( self.position )
		forword = self.direction.z
		jumpLong,jumpHigh = traps[0].calculateJumpLong()
		dstPos = (pos.x + math.sin( forword ) * jumpLong, pos.y, pos.z + jumpLong * math.cos( forword ))
		dstPos = Math.Vector3(KBEMath.KBEngine2UnrealPosition( dstPos ))
		traps[0].clearEnergy()
		self.setTemp("MoveSpeed",self.getSpeed())
		self.setSpeed(20.0)
		self.addTimerCallBack( 2.0, "setSpeed", (self.queryTemp("MoveSpeed"),) )
		self.addTimerCallBack( 3.0,"removeTemp",("MoveSpeed",) )
		self.client.CLIENT_JumpToDstPos( dstPos,jumpHigh )

#-----------------------------CST-7419 金树种子--------------------------------------------
	def CELL_ReplyAcceptJSZZQuest( self, srcEntityID,itemUID ):
		"""
		<Exposed method>
		接受金树种子任务
		"""
		if not self.validateClientCall( srcEntityID ):
			return

		item = self.getItemInstByUid( int(itemUID) )
		if not item:
			return
		itemID = item.addItemID
		spaceScriptID,position,direction = item.getJSZZEnterData()
		self.removeItemByAmount( item, 1, csdefine.ITEM_REMOVE_BY_USE )
		self.addItemByID( itemID )
		self.gotoSpace( spaceScriptID, position,direction )
		#self.acceptQuest( Const.JSZZ_QUEST_ID )

	def CELL_ClickJSZZSearch( self, srcEntityID ):
		"""
		<Exposed method>
		点击第二阶段搜索按钮
		"""
		if not self.validateClientCall( srcEntityID ):
			return

		if not self.hasQuest( Const.JSZZ_QUEST_ID ):
			return
		searchSkillID = self.questTable[Const.JSZZ_QUEST_ID].getSecondTaskSearchSkillID()
		self.useSkillToEntity( searchSkillID, self.id )

	def CELL_ClickJSZZPlant( self, srcEntityID ):
		"""
		<Exposed method>
		点击第二阶段种植按钮
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		if not self.hasQuest( Const.JSZZ_QUEST_ID ):
			return
		plantSkillID = self.questTable[Const.JSZZ_QUEST_ID].getSecondTaskPlantSkillID()
		self.useSkillToEntity( plantSkillID, self.id )

	def clickJSZZSearchBtn( self, srcEntityID ):
		"""
		<Exposed method>
		点击搜索按钮
		"""
		if not self.validateClientCall( srcEntityID ):
			return

		spaceEntity = self.getCurrentSpace()
		if spaceEntity and spaceEntity.getScript().getSpaceChildType() == csdefine.SPACE_CHILD_TYPE_JSZZ:
			searchSkillID =	spaceEntity.getScript().getSearchSkillID()
			self.useSkillToEntity( searchSkillID, self.id )

	def clickJSZZPlantBtn( self, srcEntityID ):
		"""
		<Exposed method>
		点击种植按钮
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		spaceEntity = self.getCurrentSpace()
		if spaceEntity and spaceEntity.getScript().getSpaceChildType() == csdefine.SPACE_CHILD_TYPE_JSZZ:
			plantSkillID =	spaceEntity.getScript().getPlantSkillID()
			self.useSkillToEntity( plantSkillID, self.id )

#-----------------------------CST-6327 冥气人参果--------------------------------------------
	def CELL_NotifyDropDownCiku( self, srcEntityID ):
		"""
		<Exposed method>
		通知掉落的人参果
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			spaceEntity.getScript().onConditionChange( spaceEntity, "", spaceEntity.id, "AddCiKuCount", "")

	def CELL_HitRightCiku( self, srcEntityID, ciKuPos ):
		"""
		<Exposed method>
		击中正确的人参果
		"""
		if not self.validateClientCall( srcEntityID ):
			return

		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			spaceEntity.creatHitRightCikuMonster( ciKuPos )

	def CELL_HitErrorCiku( self, srcEntityID, ciKuPos ):
		"""
		<Exposed method>
		击中错误的人参果
		"""
		if not self.validateClientCall( srcEntityID ):
			return

		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			spaceEntity.creatHitErrorCikuMonster( ciKuPos )

#-----------------------------幻阵迷宫第三版--------------------------------------------
	def notifyNextLevel( self, nextLevel, isLoad, isLoadDoor ):
		"""
		幻阵迷宫获取下一个子关卡
		"""
		self.client.OnVideoLoading( nextLevel, isLoad, isLoadDoor )

	def CELL_OnPlaySpaceIntroduceVoice( self, srcEntityID ):
		"""
		幻阵迷宫获取下一个子关卡
		"""
		if not self.validateClientCall( srcEntityID ):
			return

		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			spaceEntity.getScript().onPlaySpaceIntroduceVoice( spaceEntity, self )

#-----------------------------副本浩灵谷--------------------------------------------
	def onCompleteQTENotyfy( self, srcEntityID, isSucceed ):
		"""
		QTE结束通知
		"""
		if not self.validateClientCall( srcEntityID ):
			return

		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			spaceEntity.onCompleteQTENotyfy( self.id, isSucceed )

#-----------------------------------环任务副本相关-----------------------------------
	def onNotyfyCloseSpace( self, srcEntityID, result ):
		"""
		<Exposed method>
		环任务副本结束通知
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		
		#主动退出环任务副本，添加日志
		self.addLoopQuestCopyRecordLog(result)
		
		self.gotoExitSpacePos()
		
	def addLoopQuestCopyRecordLog(self, result):
		"""
		添加环任务副本记录日志
		@param result: 0 未完成任务主动退出, 1 已完成任务主动退出，2 未完成任务被动退出副本
		"""
		if result == 2: #在副本失败的方法（onLoopQuestSpaceFailure）写日志
			return
		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			startTime = int(spaceEntity.lifeStartTime)
			if startTime == 0: #可能会有没开始就退出的情况
				startTime = int(time.time())
			costTime = int(time.time() - startTime)
			scriptID = spaceEntity.getScript().scriptID
			copyResult = LogDefine.ACTIVE_STATE_TYPE_SUCCESS
			if result == 0:
				copyResult = LogDefine.ACTIVE_STATE_TYPE_ABANDON
			currSpaceName = LogDefine.ACTIVE_SPACE_NAME_DICT.get(LogDefine.ACTIVE_SPACE_SCRIPT_ID_DICT.get(scriptID, ""), "")
			if currSpaceName == "" or result == 0:
				#这里无法确认是哪个副本，通过spaceScriptID判断
				g_logger.roleActiveRecord(LogDefine.ACTIVE_SPACE_TYPE_DEFAULT, self.accountDBID, self.playerDBID, self.getLevel(), "", "", startTime, costTime, copyResult, scriptID)
				return
			else:
				flag = False
				for questID, questInst in self.questTable.items():
					if questInst.type != csdefine.QUEST_TYPE_LOOP:
						continue
					if questInst.getScript().getTitle() == currSpaceName:
						flag = True
						rewards = questInst.getScript().getRewardByAward( self )
						for reward in rewards:
							rewardType = ""
							rewardValue = ""
							if reward.getRewardType() in LogDefine.LOOP_QUEST_REWARD_DICT:
								rewardType = LogDefine.LOOP_QUEST_REWARD_DICT.get(reward.getRewardType())
								rewardDatas = reward.sendClientData(self)
								for rewardData in rewardDatas.values():
									rewardValue = rewardData
							elif reward.getRewardType() == csdefine.QUEST_REWARD_TYPE_ITEM:
								rewardType = LogDefine.ACTIVE_REWARD_TYPE_ITEM
								rewardValue = reward._itemID
							elif reward.getRewardType() == csdefine.QUEST_REWARD_TYPE_ITEM_CHOOSE:
								rewardType = LogDefine.ACTIVE_REWARD_TYPE_SKILL
								rewardValue = reward._chooseItemID
							g_logger.roleActiveRecord(LogDefine.ACTIVE_SPACE_TYPE_DEFAULT, self.accountDBID, self.playerDBID, self.getLevel(), rewardType, rewardValue, startTime, costTime, copyResult, scriptID)
				if not flag:
					g_logger.roleActiveRecord(LogDefine.ACTIVE_SPACE_TYPE_DEFAULT, self.accountDBID, self.playerDBID, self.getLevel(), "", "", startTime, costTime, copyResult, scriptID)
		
	def onClickSignOutSpace( self, srcEntityID ):
		"""
		<Exposed method>
		环任务点击退出副本
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		
		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			spaceEntity.getScript().onConditionChange( spaceEntity, "", spaceEntity.id, "SignOut", "")

	def onNotifyPreloadSpace( self, preloadLevel, isPreload ):
		"""
		通知预加载关卡
		"""
		self.client.OnNotifyPreloadSpace( preloadLevel, isPreload )

	def onNotifyLoadingSpace( self, loadingLevel ):
		"""
		正常切换地图
		"""
		self.client.AgainNotifySpaceData( loadingLevel )

#-----------------------------------玲珑宝珠-----------------------------------
	def CELL_onUseItemLLBZ(self, exposed, uid, spaceStr):
		"""
		选择使用金枝玉庭物品后
		"""
		if not self.validateClientCall( exposed ):
			return
		item = self.getItemInstByUid(int(uid))
		self.removeItemByAmount( item, 1, csdefine.ITEM_REMOVE_BY_USE )
		argList = spaceStr.split()
		position  = KBEMath.Unreal2KBEnginePosition((float(argList[1]) , float(argList[2]) , float(argList[3])))
		direction = KBEMath.Unreal2KBEngineDirection((float(argList[4]), float(argList[5]), float(argList[6])))
		self.gotoSpace( argList[0], position, direction )
		
	def CELL_onLingQiLock(self, exposed, scriptID, diffculty, time):
		"""
		完成灵气锁游戏
		"""
		if not self.validateClientCall( exposed ):
			return
		self.getCurrentSpaceObject().onPlayLingQiLock(self, scriptID, diffculty, time)

	def CELL_onLingHuanJue(self, exposed, scriptID, diffculty, time):
		"""
		完成灵灵幻诀游戏
		"""
		if not self.validateClientCall( exposed ):
			return
		self.getCurrentSpaceObject().onPlayLingHuanJue(self, scriptID, diffculty, time)

	def CELL_onLLBZGameComplete(self, exposed):
		"""
		玲珑宝珠完成所有游戏
		"""
		if not self.validateClientCall( exposed ):
			return

		self.getCurrentSpaceObject().onLLBZGameComplete()

#------------------------------CST-9020 勇闯绝命岛----------------------------
	def addYCJMDSkillBarData( self, srcEntityID,index, type, id ):
		"""
		增加勇闯绝命岛快捷栏数据
		"""
		if not self.validateClientCall( srcEntityID ):
			return

		spaceEntity = self.getCurrentSpace()
		if spaceEntity and spaceEntity.getScript().getSpaceChildType() == csdefine.SPACE_CHILD_TYPE_YCJMD:
			spaceEntity.addYCJMDSkillBarData( self,index, type, id )

	def removeYCJMDSkillBarData( self, srcEntityID, index ):
		"""
		移除勇闯绝命岛快捷栏数据
		"""
		if not self.validateClientCall( srcEntityID ):
			return

		spaceEntity = self.getCurrentSpace()
		if spaceEntity and spaceEntity.getScript().getSpaceChildType() == csdefine.SPACE_CHILD_TYPE_YCJMD:
			spaceEntity.removeYCJMDSkillBarData( self, index )

	def exchangeYCJMDSkillBarData( self, srcEntityID, srcIndex, dstIndex ):
		"""
		交换勇闯绝命岛快捷栏的数据
		"""
		if not self.validateClientCall( srcEntityID ):
			return

		spaceEntity = self.getCurrentSpace()
		if spaceEntity and spaceEntity.getScript().getSpaceChildType() == csdefine.SPACE_CHILD_TYPE_YCJMD:
			spaceEntity.exchangeYCJMDSkillBarData( self, srcIndex, dstIndex )

	def changeParachutingState( self, srcEntityID, state ):
		"""
		exposed method
		离开飞行器，自由下落
		"""
		self.parachutingState = state
		if state == csdefine.PARACHUTE_STATE_NORMAL:
			self.onParachutingOver()

	def onParachutingOver(self):
		"""
		跳伞结束
		"""
		self.spaceEvent_onPlayerParachutingOver(self.id)

#-------------------------CST-5301 天之幻境------------------------------------
		
	def inPosRefreshFabao( self, srcEntityID, scriptID , position, parentID):
		"""
		exposed method
		法宝掉落到地面后
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		if not scriptID:
			return
		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			entity = spaceEntity.createEntityByScriptID( scriptID, KBEMath.Unreal2KBEnginePosition( position ), Math.Vector3(0,0,0),{})
			parentEntity = KBEngine.entities.get( parentID, None )
			if parentEntity:
				entity.parent = parentEntity
#-------------------------CST-5301 灵兽圈------------------------------------
	def lXQIsHit( self, srcEntityID, isHit ):
		"""
		exposed method
		灵兽圈是否命中
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		if isHit:
			hitNum = self.queryTemp("LXQHitNum")
			self.setTemp("LXQHitNum", ( 1 if not hitNum else  hitNum + 1) )
		else:
			missNum = self.queryTemp("LXQMissNum")
			self.setTemp("LXQMissNum", ( 1 if not missNum else  missNum + 1) )
	
		if self.hitNum >= 3:
			self.onLingShouQuan( True )
			return
		if self.missNum >= 3:
			self.onLingShouQuan( False )
			return

	def onLingShouQuan( self,  isVictory ):
		"""
		完成灵兽圈玩法
		"""
		self.removeTemp( "LXQHitNum" )
		self.removeTemp( "LXQMissNum" )
		if isVictory:
			self.setLoopQuestTaskCompleteNum( 1 )
		else:
			self.setLoopQuestTaskCompleteNum( 0 )

		self.forceQuestTaskIncreaseState( self.loopQuest["loopQuestList"][0] , 2)

	def LXQEnterAimingMode( self , srcEntityID):
		"""
		exposed method
		进入灵兽圈瞄准模式
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		self.client.OnLXQEnterAimingMode( Const.LXQ_AIM_SKILLID )

	def LXQLeaveAimingMode( self ,srcEntityID):
		"""
		exposed method
		退出灵兽圈瞄准模式
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		self.client.OnLXQLeaveAimingMode()

#-------------------------CST-5301 接火把------------------------------------

	def JHBIsCatch(self, srcEntityID, isCatch):
		"""
		exposed method
		是否接住火把
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		if isCatch:
			catchNum = self.queryTemp("JHBCatchNum")
			self.setTemp("JHBCatchNum", ( 1 if not catchNum else catchNum + 1) )
		else:
			missNum = self.queryTemp("JHBMissNum")
			self.setTemp("JHBMissNum", ( 1 if not missNum else missNum + 1) )
			
		if self.catchNum >= 6:
			self.onJieHuoBa( True )
			return
		if self.missNum >= 5:
			self.onJieHuoBa( False )
			

	def onJieHuoBa( self , isVictory ):
		"""
		完成接火把玩法
		"""
		self.removeTemp( "JHBCatchNum" )
		self.removeTemp( "JHBMissNum" )
		if isVictory:
			self.setLoopQuestTaskCompleteNum( 1 )
		else:
			self.setLoopQuestTaskCompleteNum( 0 )

		self.forceQuestTaskIncreaseState( self.loopQuest["loopQuestList"][0] , 2)
	
#-------------------------CST-9960 阵营战场“勇闯绝命岛”------------------------------------
	def onCampYCJMDPlayerPressKeyF(self, srcEntityID):
		"""
		exposed method
		玩家按F键
		"""
		if not self.validateClientCall( srcEntityID ):
			return

		self.getCurrentSpaceObject().onCampYCJMDPlayerParachuteLand(self)

	def onCampYCJMDLeaveSkyDiving(self, srcEntityID):
		"""
		exposed method
		玩家离开跳伞模式		
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		self.triggerSkillEvent( csdefine.SKILL_EVENT_ROLE_PARACHUTE, self.id, {} )
		
#--------------------CST-4246 帮会副本【九字真言】 ------------------------------------------
	def onAddShangHaiBuff(self, buffID):
		"""
		"""
		clearBuffTimerID = self.queryTemp("CLEARJZZYBUFFTIMERID", 0)	
		if clearBuffTimerID:
			self.popTimer(clearBuffTimerID)
			self.removeTemp("CLEARJZZYBUFFTIMERID")
			clearBuffTimerID = 0
		
		self.setTemp("JZZYBUFFID", buffID)
		addBuffTimerID = self.queryTemp("ADDJZZYBUFFTIMERID", 0)
		if not addBuffTimerID:
			addBuffTimerID = self.addTimerRepeat( 10.0, "onAddJZZYBuffTimer", () )
			self.setTemp("ADDJZZYBUFFTIMERID", addBuffTimerID)
			if self.getClient(): self.getClient().onNotifyJZZYBuffTime(10)
		
	def onReduceShangHaiBuff(self):
		"""
		"""
		addBuffTimerID = self.queryTemp("ADDJZZYBUFFTIMERID", 0)
		if addBuffTimerID:
			self.popTimer(addBuffTimerID)
			self.removeTemp("ADDJZZYBUFFTIMERID")
			addBuffTimerID = 0
			if self.getClient(): self.getClient().onNotifyJZZYBuffTime(0)
			
		clearBuffTimerID = self.queryTemp("CLEARJZZYBUFFTIMERID", 0)
		if not clearBuffTimerID:
			clearBuffTimerID = self.addTimerRepeat( 3.0, "onClearJZZYBuffTimer", () )
			self.setTemp("CLEARJZZYBUFFTIMERID", clearBuffTimerID)
			return
		
	def onAddJZZYBuffTimer(self):
		"""
		"""
		#看是否已经有相应的buff加在身上了
		buffID = self.queryTemp("JZZYBUFFID", 0)
		if len(self.findBuffsByBuffID(buffID)) <= 5:
			self.addBuff(self, buffID)
			if self.getClient(): self.getClient().onNotifyJZZYBuffTime(10)
		
	def onClearJZZYBuffTimer(self):
		"""
		"""
		#移除buff
		buffID = self.queryTemp("JZZYBUFFID", 0)
		if len(self.findBuffsByBuffID(buffID)) > 0:
			self.removeBuffByID(buffID)
		
	def clearJZZYData(self):
		"""
		清理副本数据
		"""
		addBuffTimerID = self.queryTemp("ADDJZZYBUFFTIMERID", 0)
		if addBuffTimerID:
			self.popTimer(addBuffTimerID)
			self.removeTemp("ADDJZZYBUFFTIMERID")
		
		clearBuffTimerID = self.queryTemp("CLEARJZZYBUFFTIMERID", 0)	
		if clearBuffTimerID:
			self.popTimer(clearBuffTimerID)
			self.removeTemp("CLEARJZZYBUFFTIMERID")
		
		#移除所有的相关的buff
		buffID = self.queryTemp("JZZYBUFFID", 0)
		if buffID and len(self.findBuffsByBuffID(buffID)) > 0:
			self.removeBuffByID(buffID)
		
#------------------------CST-8954 攻城战------------------
	def callArmyToWar( self, srcEntityID, id ):
		"""
		Exposed method
		出战某支部队
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		if self.callArmyIndex == id:
			return
		
		self.callIDArmyToWar( id )

	def callArmyOnRevive( self ):
		"""
		复活时重新召出部队
		如果玩家现有部队还没死光，则召现有部队，否则召第一顺位部队
		"""
		armyData = self.getRoleArmyDatas()
		if len(armyData) == 0:
			return
		
		if self.callArmyIndex in armyData and self.isArmyHasLiveMember( self.callArmyIndex ):
			self.callIDArmyToWar( self.callArmyIndex )
		else:
			armyID = self.getDefaultArmyIndex()
			if armyID != -1:
				self.callIDArmyToWar( armyID )

	def callIDArmyToWar( self, id ):
		"""
		"""
		self.destroyArms()
		isCall = False
		if len(self.getRoleArmyDatas()) > 0:
			self.callRoleArmySoldier( id )
			isCall = True
		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			if spaceEntity.getScript().getSpaceChildType() == csdefine.SPACE_CHILD_TYPE_GCZ and not isCall:
				armyData = spaceEntity.getGCZRoleDefultArmyData( self.playerDBID, id )
				self.callGCZDefultArmy( armyData,id )
			
			spaceEntity.getScript().onPlayerCallArmy( spaceEntity, self.id, self.playerDBID, self.callArmyIndex )

#----------------------- 潜能副本(目前主要是幻阵迷宫) -----------------------------
	def getPotentialSpaceLoopAndIndex(self):
		"""
		"""
		loop = self.qianNengData.get("Loop", 0)
		index = self.qianNengData.get("Index", 0)
		return loop, index
		
	def onFixedTimeUpdate(self, fixedTimeType, token):
		"""
		"""
		if fixedTimeType == csdefine.FIXED_UPDATE_TOKEN_FIVE:
			#如果当前正在潜能副本中,数据不进行重置
			spaceEntity = self.getCurrentSpace()
			if spaceEntity and spaceEntity.getScript().getSpaceChildType() == csdefine.SPACE_TYPE_POTENTIAL:
				self.qianNengData["Token"] = token
				return
			
			#重置潜能副本相应数据
			self.qianNengData["Loop"] = 0
			self.qianNengData["LoopFlag"] = True
			
#-----------------------CST-12032  帮会掠夺战) -----------------------------
	def createApparatus( self, srcEntityID, scriptID , position, direction, itemUID):
		"""
		exposed method
		
		创建器械
		"""
		if not self.validateClientCall( srcEntityID ):
			return
			
		if not scriptID:
			return
			
		item = self.getItemInstByUid( int(itemUID) )
		if not item:
			return
			
		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			entity = spaceEntity.createEntityByScriptID(scriptID, KBEMath.Unreal2KBEnginePosition(position), KBEMath.Unreal2KBEngineDirection(direction),{})
			
			self.removeItemByAmount(item, 1, csdefine.ITEM_REMOVE_BY_USE)
	
#-----------------------------CST-12218 大荒战场-------------------------------------------------------
	def processVehicle( self ):
		if self.vehicleId:
			vehicleEntity = KBEngine.entities.get( self.vehicleId, None )
			if vehicleEntity:
				vehicleEntity.dismountVehicle( self.id )
		
	def CELL_mountVehicle( self, exposed, vehicleID ):
		"""
		<Exposed method>
		上载具
		"""
		if not self.validateClientCall( exposed ):
			return
		vehicleEntity = KBEngine.entities.get( vehicleID, None )
		if not vehicleEntity:
			return
		vehicleEntity.mountVehicle( self.id )
		
	def CELL_dismountVehicle( self, exposed, vehicleID ):
		"""
		<Exposed method>
		下载具
		"""
		if not self.validateClientCall( exposed ):
			return
		vehicleEntity = KBEngine.entities.get( vehicleID, None )
		if not vehicleEntity:
			return
		vehicleEntity.dismountVehicle( self.id )
		
	def CELL_reqVehicleData( self, exposed, targetID, vehicleID ):
		"""
		<Exposed method>
		请求目标entity的载具数据
		"""
		if not self.validateClientCall( exposed ):
			return
		vehicleEntity = KBEngine.entities.get( vehicleID, None )
		if not vehicleEntity:
			return
		vehicleEntity.reqVehicleData( exposed, targetID )
	
	def CELL_inviteMountVehicle( self, exposed, beInviteID ):
		"""
		exposed method
		邀请上载具
		"""
		if not self.validateClientCall( exposed ):
			return
		beInviteEntity = KBEngine.entities.get( beInviteID, None )
		if not beInviteEntity:
			return
		if abs( self.position.x - beInviteEntity.position.x ) > 5 or abs( self.position.z - beInviteEntity.position.z ) > 5:#KBE的y是高度值
			self.statusMessage( csstatus.VEHICLE_BEYOND_INTERACTIVE_DISTANCE)#距离过远
			return
		if beInviteEntity.carrierId or beInviteEntity.vehicleId:
			self.statusMessage( csstatus.VEHICLE_TO_MOUNT_CANNOT_INVITE)#对方在骑乘状态玩家不能邀请他上载具
			return
		if self.vehicleId:
			beInviteEntity.inquireMessage(csstatus.VEHICLE_INVITE_TO_MOUNT, [self.playerName], 'replyMountVehicleInvite', self.id, self.vehicleId)#邀请你共同骑乘，是否接受？
		
	def replyMountVehicleInvite(self, reply, inviteID, vehicleID):
		"""
		目标玩家答复上载具邀请
		"""
		if reply:
			vehicleEntity = KBEngine.entities.get( vehicleID, None )
			if not vehicleEntity:
				return
			vehicleEntity.mountVehicle( self.id )
		else:
			inviteEntity = KBEngine.entities.get( inviteID, None )
			if not inviteEntity:
				return
			inviteEntity.statusMessage( csstatus.VEHICLE_TO_REFUSE_INVITE, self.playerName)#拒绝邀请
			
	def CELL_applyMountVehicle( self, exposed, targetID ):
		"""
		exposed method
		申请上载具
		"""
		if not self.validateClientCall( exposed ):
			return
		if self.vehicleId:
			return
		targetEntity = KBEngine.entities.get( targetID, None )
		if not targetEntity:
			return
		if abs( self.position.x - targetEntity.position.x ) > 5 or abs( self.position.z - targetEntity.position.z ) > 5:#KBE的y是高度值
			self.statusMessage( csstatus.VEHICLE_BEYOND_INTERACTIVE_DISTANCE)#距离过远
			return
		if not targetEntity.vehicleId:
			self.statusMessage( csstatus.NO_VEHICLE_CANNOT_APPLY )#对方没有多人坐骑，申请失败
			return
		targetEntity.inquireMessage(csstatus.VEHICLE_APPLY_TO_MOUNT, [self.playerName], 'replyMountVehicleApply', self.id)#申请共同骑乘，是否接受？
		
	def replyMountVehicleApply(self, reply, applicantID):
		"""
		目标玩家答复上载具申请
		"""
		if reply:
			if not self.vehicleId:
				return
			vehicleEntity = KBEngine.entities.get( self.vehicleId, None )
			if not vehicleEntity:
				return
			vehicleEntity.mountVehicle( applicantID )
		else:
			applicantEntity = KBEngine.entities.get( applicantID, None )
			if not applicantEntity:
				return
			applicantEntity.statusMessage( csstatus.VEHICLE_TO_REFUSE_APPLY, self.playerName )#拒绝申请
		
	def onBeforeMountVehicle( self, vehicleID ):
		"""
		玩家上载具通知
		"""
		self.triggerSkillEvent( csdefine.SKILL_EVENT_ROLE_YCJMD_CARRIER, self.id, {"isMount" : 1} )
		# buffs = self.findBuffsByBuffScript( "BuffYCJMDTPS" )
		# # 一般只存在一个
		# if len(buffs):
		# 	buffData = self.getBuffData(buffs[0])
		# 	self.setTemp("BuffYCJMDTPS", buffData.buffID)
		# 	self.removeBuff(buffs[0])
		
	def onAfterDismountVehicle( self, vehicleID ):
		"""
		玩家下载具通知
		"""
		self.triggerSkillEvent( csdefine.SKILL_EVENT_ROLE_YCJMD_CARRIER, self.id, {"isMount" : 0} )
		# buffID = self.queryTemp("BuffYCJMDTPS", 0)
		# if buffID:
		# 	self.addBuff(self, buffID)
		# 	self.removeTemp("BuffYCJMDTPS")

#---------------------------------------------------------------------------------------------------------------
	def CELL_notifyMediaStartPlay( self, srcEntityID, arg ):
		"""
		<Exposed method>
		客户端通知服务器
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		
		if arg == "JIYUAN":
			id = self.queryTemp("JiYuanXinXi", None)
			if id is None:
				KBEDebug.ERROR_MSG("JiYuanXinXi is None %s" %(self.id))
				return
			
			data = g_jiYuanCfgLoader.getCfgByID(id)
			if data is None:
				KBEDebug.ERROR_MSG("not found config %s" %(id))
				return
			
			params = self.queryTemp("JIYUANDATA", {})
			params.update({"JiYuanXinXi" : id})
			self.removeTemp("JIYUANDATA")
			self.setTemp("JiyuanSpaceData", (self.getCurrentSpace().spaceID, self.getCurrentSpace().scriptID, Math.Vector3(self.position), Math.Vector3(self.direction)))
			self.gotoSpaceUseArg(data["scriptID"], data["position"], data["direction"], params)