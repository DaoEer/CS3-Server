# -*- coding: utf-8 -*-

import random
import KBEDebug
from SpaceCopy import SpaceCopy
import time
from ConfigObject.SpaceCopyLLBZNoticeLoader import g_SpaceCopyLLBZNotice

class SpaceCopyLLBZ( SpaceCopy ):
	"""
	玲珑宝珠副本
	"""
	def __init__( self ):
		SpaceCopy.__init__( self )
		self.getScript().setDiffcultyDatas(self)

	def onTeleportCompleted( self, playerRole ):
		"""
		传送结束，场景已加载完毕
		"""
		SpaceCopy.onTeleportCompleted( self, playerRole )
		string = ""
		for scriptID, diffcult in self.diffcultyDatas.items():
			string += scriptID
			string += ":"
			string += str(diffcult)
			string += "|"
		playerRole.client.CLIENT_LLBZShowAllDiffcult(string)

	def StartLLBZGame(self, playerRole, NPCID):
		"""
		开始玲珑宝珠游戏
		"""
		number = random.randint(0, 100)
		if number < 50:
			diffculty = self.diffcultyDatas[NPCID]
			amount = g_SpaceCopyLLBZNotice.getLingQiAmount(diffculty)
			speed = g_SpaceCopyLLBZNotice.getLingQiSpeed(diffculty)
			playerRole.client.CLIENT_startLingQiLock(NPCID, diffculty, amount, speed)
		else:
			diffculty = self.diffcultyDatas[NPCID]
			amount = g_SpaceCopyLLBZNotice.getLingHuanAmount(diffculty)
			playerRole.client.CLIENT_startLingHuanJue(NPCID, diffculty, amount)
		