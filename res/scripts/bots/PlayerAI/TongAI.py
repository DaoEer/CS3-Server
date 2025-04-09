# -*- coding: utf-8 -*-

import KBEngine
from KBEDebug import *

import csdefine
import KST_Config

from PlayerAI.Base.AIBase import AIBase
from PlayerAI.State.CStateInterface import eAIState
from PlayerAI.State.AI_System import CCleanAISys
from PlayerAI.State.AI_Tong import CTongAI


class TongAI( AIBase ):
	"""
	"""
	def __init__(self):
		AIBase.__init__(self)
		self.actionStatus[eAIState.CleanSys] = CCleanAISys(self)
		self.actionStatus[eAIState.Tong] = CTongAI(self)
		
		self.callbackID = 0
		
	def attache(self, owner):
		"""
		"""
		AIBase.attache(self, owner)
		
		#清理已经存在的帮会
		#之所以放在这里，是因为这里是最先执行的。
		if KST_Config.tong_clear:
			self.owner.GMCommand(self.owner, "disbandAllTong", "")
			KST_Config.tong_clear = False
		
	def onSetSpaceData(self):
		"""
		"""
		AIBase.onSetSpaceData(self)
		if not self.enterDefaultMap:
			#设置玩家等级、修为、金钱
			self.owner.GMCommand(self.owner, "setLevel", "30")
			self.owner.GMCommand(self.owner, "setXiuwei", "100000000")
			self.owner.GMCommand(self.owner, "setMoney", "300000000")
			
			self.enterDefaultSpace()
			return
		
		self.think()
		
	def think(self):
		"""
		"""
		if self.callbackID > 0:
			KBEngine.cancelCallback(self.callbackID)
			self.callbackID = 0
			
		#帮会数据还未初始化完毕
		if not self.owner.isTongInit:
			if self.callbackID == 0:
				self.callbackID = KBEngine.callback(3, self.think)
				return
		
		if self.owner.tongDBID == 0:
			self.changeAIState(eAIState.Tong)
		else:
			if self.callbackID == 0:
				delay = 5
				if self.owner.tongLeader == self.owner.playerDBID:
					delay = 60 * 2	#如果是帮主的话，延时2分钟在退出帮会

				self.callbackID = KBEngine.callback(delay, self.onCallBack)
	
	def onCallBack(self):
		self.callbackID = 0
		self.changeAIState(eAIState.CleanSys)
		
AIBase.setClass("TongAI", TongAI)