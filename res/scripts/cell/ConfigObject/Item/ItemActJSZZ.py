# -*- coding: utf-8 -*-
import csdefine
import ConfigObject.Item.ItemUse as ItemUse
from ConfigObject.Quest.QuestBase.QuestLoader import g_QuestLoader
import Const
import Math
import Functions
import KBEMath

class ItemActJSZZ( ItemUse.ItemUse ):
	"""
	金树种子
	"""
	def __init__(self, srcData):
		ItemUse.ItemUse.__init__(self, srcData)
		self._rewardList = []
		self.addItemID = 0
		self.spaceScriptID = ""
		self.position = Math.Vector3(0,0,0)
		if srcData["Param1"]:
			self._rewardList = [int(i) for i in srcData["Param1"].split("|")]
		if srcData["Param2"]:
			self.addItemID = int(srcData["Param2"])
		if srcData["Param3"]:
			self.spaceScriptID = srcData["Param3"].split("|")[0]
			positionStr = srcData["Param3"].split("|")[1]
			directionStr = srcData["Param3"].split("|")[2]
			self.position = Math.Vector3( KBEMath.Unreal2KBEnginePosition(tuple(Functions.vector3TypeConvert(positionStr))) )
			self.direction = Math.Vector3( KBEMath.KBEngine2UnrealDirection(tuple(Functions.vector3TypeConvert(directionStr))) )

	def use(self, owner, target):
		ItemUse.ItemUse.use(self, owner, target)
		if owner.getClient():
			owner.client.CLIENT_ShowJSZZAcceptWin(self._rewardList, (25 * 60), str( self.uid ))

	def getJSZZEnterData( self ):
		return self.spaceScriptID,self.position,self.direction
