# -*- coding: utf-8 -*-

import random
import KBEDebug
from SpaceCopyTong import SpaceCopyTong
import Math
import KBEngine
import csdefine
import csstatus
from ConfigObject.Skill.Buff.BuffChangeBody import BuffChangeBody
import math

class SpaceCopyLingHunZhiShi( SpaceCopyTong ):
	"""
	灵魂之誓副本
	"""
	def __init__( self ) :
		SpaceCopyTong.__init__( self )

		#玩家当前所附身的怪物ScriptID
		self.playerCurScriptID = ""
		self.soulNum = 0
		self.isOpen = 1


	def getWeakBuffID(self):
		"""
		获取虚弱状态buffID
		"""
		return self.getScript().weakBuffID


	def getMonsterData(self):
		"""
		获取自定义monster数据
		"""
		return self.getScript().monsterData


	def getGradeByScriptID(self, scriptID):
		"""
		获取“等级”
		"""
		if not scriptID in self.getMonsterData():
			return 0

		return self.getMonsterData()[scriptID]["grade"]


	def isWeak(self, targetEntity):
		"""
		判断目标是否为虚弱状态
		"""
		return len(targetEntity.findBuffsByBuffID(self.getWeakBuffID()))


	def canUsurp(self, targetEntity):
		"""
		能否附身
		"""
		#非虚弱状态的怪物不可被附身
		if not self.isWeak(targetEntity):
			return False

		grade = self.getGradeByScriptID(self.playerCurScriptID) + 1
		#等级不等于玩家等级+1的怪物不可被附身;  等级5的怪物不可被附身
		if grade != self.getGradeByScriptID(targetEntity.scriptID) or grade >= 5:
			return False

		return True


	def usurpStart(self, player, targetScriptID, isValid):
		"""
		附身
		"""
		if not isValid:
			return
		#获取怪物身上的特性(buff)
		self.playerCurScriptID = targetScriptID
		for buffID in self.getMonsterData()[targetScriptID]["buffIDs"]:
			player.addBuff(player, buffID)
		self.getScript().onConditionChange( self, "LHZS", "", str(self.getGradeByScriptID(self.playerCurScriptID)), "" )
		self.soulNum = 0
		self.updateSoulPercent(player, 1)


	def usurpEnd(self, player):
		"""
		附身结束
		"""
		#移除怪物身上的特性(buff)
		if self.playerCurScriptID in self.getMonsterData():
			buffIDs = self.getMonsterData()[self.playerCurScriptID]["buffIDs"]
			for buffData in list( player.getAttrBuffs().values() ) :
				if buffData.buffID not in buffIDs:
					continue
				buff = player.getBuff(buffData.buffID)
				if isinstance( buff, BuffChangeBody ):
					continue
				player.removeBuffByID(buffData.buffID)
		self.playerCurScriptID = ""
		self.soulNum = 0
		self.updateSoulPercent(player, 1)
	
		
	def updateSoulPercent(self, player, isOpen):
		"""
		"""
		if not self.isOpen:
			player.client.ShowCircleHPPercentBar( 0, 0 )
			return
			
		if not isOpen:
			player.client.ShowCircleHPPercentBar( 0, 0 )
			return
		index = self.getGradeByScriptID(self.playerCurScriptID)

		percent = int(math.floor(self.soulNum / self.getScript().soulNumList[index] * 100 ))
		player.client.ShowCircleHPPercentBar( isOpen, percent )
		player.client.OnAbsorbSoulLayerLevelChanged(index)


	def addSoulNum(self, player):
		"""
		"""
		num = self.soulNum + 1
		#当能量球再次满了之后就不再处理
		index = self.getGradeByScriptID(self.playerCurScriptID)
		maxNum = self.getScript().soulNumList[index]
		if num > maxNum:
			return

		self.soulNum = num
		self.updateSoulPercent(player, 1)
		
		#当能量球满的时候 清除附身技能CD
		if self.soulNum == maxNum:
			buffID = self.getScript().clearCDBuffID
			if player:
				player.addBuff(player, buffID)
			self.getScript().onConditionChange( self, "", "", "send"+str(self.getGradeByScriptID(self.playerCurScriptID)+1), "" )