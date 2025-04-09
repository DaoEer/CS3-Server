# -*- coding: utf-8 -*-
import Monster
class MonsterExtQuest(  Monster.Monster ):
	"""
	任务怪（处理特定任务目标状态下的表现，比如屏蔽主动攻击，语音喊话等）
	"""
	def __init__( self ):
		Monster.Monster.__init__( self )
	def OnStopCurrentAction(self):
		pass
