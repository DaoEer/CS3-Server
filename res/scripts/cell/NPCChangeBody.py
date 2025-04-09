# -*- coding: utf-8 -*-
#
import random
import KBEngine
import Const
import QuestEventDefine
from KBEDebug import *
import CoreObject.NPCObject as NPCObject
import CoreInterface.NPCTalkInterface as NPCTalkInterface
import CoreInterface.NPCQuestInterface as NPCQuestInterface


class NPCChangeBody(NPCObject.NPCObject, NPCTalkInterface.NPCTalkInterface, NPCQuestInterface.NPCQuestInterface ):
	"""
	变身NPC
	"""
	def __init__(self):
		NPCObject.NPCObject.__init__(self)
		NPCTalkInterface.NPCTalkInterface.__init__(self)
		NPCQuestInterface.NPCQuestInterface.__init__(self)
		self.addTimerCallBack( Const.BEGIN_CHANGE_BODY_TIME, "beginChangeBody", () )
	
	def beginChangeBody( self ):
		"""
		开始变身
		"""
		if random.random() <= Const.CHANGE_BODY_ROLL:
			datas = random.sample( Const.CHANGE_BODY_DATAS.keys(), 1 )
			modelNumber = datas[0]
			voice = Const.CHANGE_BODY_DATAS[datas[0]]["voice"]
		else:
			datas = random.sample( Const.CHANGE_BODY_DATAS.keys(), 2 )
			modelNumber = datas[0]
			voice = Const.CHANGE_BODY_DATAS[datas[1]]["voice"]
		self.allClients.CLIENT_BubbleDialogue(voice)
		self.addTimerCallBack( Const.CHANGE_BODY_TIME, "changeBody", (modelNumber,) )
		
	def changeBody( self, modelNumber ):
		"""
		变身
		"""
		self.setExtraModelNumber( modelNumber )
		self.addTimerCallBack( Const.CHECK_CHANGE_BODY_TIME, "checkChangeBody", () )
	
	def checkChangeBody( self ):
		"""
		变身检测
		"""
		Roles = self.entitiesInRangeExt( Const.CHANGE_BODY_CHECK_ROLE_RANGE, "Role" )
		buffID = Const.CHANGE_BODY_DATAS[self.getExtraModelNumber()]["buffID"]
		for role in Roles:
			if role.findBuffsByBuffID( buffID ):
				self.changeBodyCorrect( role )
				num = self.queryTemp( "changeBobyNum", 0 )
				self.setTemp( "changeBobyNum", num + 1 )
			else:
				self.changeBodyError( role )
		self.setExtraModelNumber( "" )
		
		if self.queryTemp("changeBobyNum", 0 ) < Const.CHANGE_BODY_NUM:
			self.beginChangeBody()
		
		
	def changeBodyCorrect( self, player ):
		"""
		变身正确
		"""
		spaceEntity = self.getCurrentSpace()
		spaceEntity.getScript().onConditionChange( spaceEntity, "CHANGE_BODY", self.scriptID, "CORRECT", player.getName() )
		player.triggerQuestEvent( QuestEventDefine.EVENT_HUAN_COMMON_TASK, self.scriptID )
		
	def changeBodyError( self, player ):
		"""
		变身错误
		"""
		spaceEntity = self.getCurrentSpace()
		spaceEntity.getScript().onConditionChange( spaceEntity, "CHANGE_BODY", self.scriptID, "ERROR", player.getName() )
