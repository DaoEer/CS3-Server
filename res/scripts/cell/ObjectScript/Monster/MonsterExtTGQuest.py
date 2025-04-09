# -*- coding: utf-8 -*-
import ObjectScript.Monster.Monster as Monster
import KBEDebug
import time

class MonsterExtTGQuest( Monster.Monster ):
	def __init__( self ):
		Monster.Monster.__init__( self )
		self.buffID = 0					# buffID
		self.sceneID = ""				# 镜头ID

	def initData( self, configData ):
		Monster.Monster.initData( self, configData )
		if configData["Param1"]:
			self.buffID = int(configData["Param1"])
		self.sceneID = configData["Param2"]

