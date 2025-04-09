# -*- coding: utf-8 -*-

import random
import KBEDebug
from ObjectScript.Space.SpaceCopy import SpaceCopy
import Functions
import KBEMath

class SpaceCopyJDCY( SpaceCopy ):
	"""
	禁地采药
	"""
	def __init__( self ):
		SpaceCopy.__init__( self )
		self.LXCPositionList = []
		self.LXCSrciptID = ""

	def initData( self, configData ):
		"""
		virtual method
		"""
		SpaceCopy.initData( self, configData )
		self.LXCSrciptID = configData["SpaceData"].get("LXCSrciptID","")
		LXCPositionStr = configData["SpaceData"].get("LXCPosition","")
		if LXCPositionStr:
			for i in LXCPositionStr.split("|"):
				self.LXCPositionList.append(KBEMath.Unreal2KBEnginePosition(Functions.vector3TypeConvert(i)))

	def onConditionChange( self, selfEntity, senderType, senderID, conditionKey, extraValue ):
		"""
		副本某条件改变
		@param senderType: AI发的填"AI"，镜头事件发的填"STORY"
		@param senderID: AI发的填entity scriptID，镜头事件发的填镜头ID
		@param conditionKey: 通知ID，string类型
		"""
		if "AI" ==  senderType and "XIANCAO" == conditionKey:
			 selfEntity.onCollectedXLC()
			 return
		SpaceCopy.onConditionChange( self, selfEntity, senderType, senderID, conditionKey, extraValue )

	def getLXCPositionList(self):
		return self.LXCPositionList

	def getLXCSrciptID(self):
		return self.LXCSrciptID


