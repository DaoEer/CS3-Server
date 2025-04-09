# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
from ObjectScript.NPC import NPC
import csstatus


class NPCExtCompose( NPC.NPC ):
	def __init__( self ):
		NPC.NPC.__init__( self )
		self.dongFuType = csdefine.SPACE_TYPE_PRIVATE
		self.composeType = csdefine.COMPOSE_TOOL_NORMAL
		self.actionID = ""
		self.monsterScriptID = 0
		self.particleID = ""

	def initData( self, configData ):
		NPC.NPC.initData( self, configData )
		if configData["Param1"]:
			self.dongFuType = int( configData["Param1"])
		if configData["Param2"]:
			self.composeType = int(configData["Param2"])
		if configData["Param3"]:
			self.actionID = configData["Param3"]
		if configData["Param4"]:
			strList = configData["Param4"].split("|")
			if len( strList ) >= 2:
				self.monsterScriptID = int( strList[0] )
				self.particleID = strList[1]

