# -*- coding: utf-8 -*-

import random
import KBEDebug
from ObjectScript.Space.SpaceCopyTong import SpaceCopyTong
import Functions
import KBEMath

class SpaceCopySLZD( SpaceCopyTong ):
	"""
	试炼之地
	"""
	def __init__( self ):
		SpaceCopyTong.__init__( self )
		self.SLZDSrciptIDs = []

	def initData( self, configData ):
		"""
		virtual method
		"""
		SpaceCopyTong.initData( self, configData )
		tempStr = configData["SpaceData"].get("SLZDSrciptIDs","")
		if tempStr:
			self.SLZDSrciptIDs = tempStr.split("|")

	def getSLZDSrciptIDs(self, amount):
		"""
		获得某数量的随机顺序的SrciptID列表
		"""
		random.shuffle(self.SLZDSrciptIDs)
		_amount = amount if amount <= len(self.SLZDSrciptIDs) else len(self.SLZDSrciptIDs)
		return self.SLZDSrciptIDs[:_amount]


	def onConditionChange( self, selfEntity, senderType, senderID, conditionKey, extraValue ):
		"""
		副本某条件改变
		@param senderType: AI发的填"AI"，镜头事件发的填"STORY"
		@param senderID: AI发的填entity scriptID，镜头事件发的填镜头ID
		@param conditionKey: 通知ID，string类型
		"""
		if "Trap" ==  senderType and "SLZDtrap" == conditionKey:
			 selfEntity.onPlayerTreadFlagstone(senderID)
			 return
		SpaceCopyTong.onConditionChange( self, selfEntity, senderType, senderID, conditionKey, extraValue )