# -*- coding: utf-8 -*-

import KBEngine
import csdefine
from ObjectScript.SpaceDomain.DomainBase import DomainBase
import KBEDebug
import csstatus

class SpaceDomainCopyTongPlunder(DomainBase):
	"""
	帮会掠夺战
	"""
	def __init__(self):
		DomainBase.__init__(self)
		self.spaceKeyToSpaceNumber = {}
		self.closeSpaceTongDBIDList = []
	
	def initData(self, configData):
		DomainBase.initData(self, configData)

	def activityStart(self, signUpTongInfos):
		"""
		活动开始
		"""
		self.spaceKeyToSpaceNumber.clear()
		self.closeSpaceTongDBIDList.clear()

		for info in signUpTongInfos:
			spaceKey = str(info["attackTongInfo"]["dbid"])
			pickArgs = {}
			pickArgs["spaceKey"] = spaceKey
			pickArgs["belongType"] = csdefine.SPACE_BELONG_TONG
			pickArgs["attackTongInfo"] = info["attackTongInfo"]
			pickArgs["protectTongInfo"] = info["protectTongInfo"]
			spaceItem = self.getSpaceItemByKey(spaceKey)
			if not spaceItem:
				spaceItem = self.createSpaceItem(pickArgs)

	def activityEnd(self):
		"""
		活动结束
		"""
		for spaceNumber, spaceItem in self.spaceItems.items():
			if spaceItem and spaceItem.spaceMailBox and spaceItem.spaceMailBox.cell:
				spaceItem.spaceMailBox.cell.closeSpace()

		self.spaceKeyToSpaceNumber.clear()
		self.closeSpaceTongDBIDList.clear()

	def gotoSpace(self, roleMB, position, direction, pickArgs):
		"""
		virtual method
		玩家传送
		"""
		spaceObject = self.getSpaceObject()
		exitScriptID, exitPosition, exitDirection = spaceObject.getReviveToExitInfo(roleMB, pickArgs)
		spaceKey = pickArgs.get("spaceKey")
		spaceItem = self.getSpaceItemByKey(spaceKey)
		if not spaceItem:
			if str(spaceKey) in self.closeSpaceTongDBIDList:
				roleMB.client.statusMessage(csstatus.TONG_PLUNDER_ACTIVITY_END, "")
				return
			spaceItem = self.createSpaceItem(pickArgs)

		posInfo = []
		if spaceKey == str(pickArgs["attackTongInfo"]["dbid"]):
			posInfo = spaceObject.getEnterPos(csdefine.BELONG_SIDE_ATTACK)
		elif spaceKey == str(pickArgs["protectTongInfo"]["dbid"]):
			posInfo = spaceObject.getEnterPos(csdefine.BELONG_SIDE_PROTECT)

		spaceItem.enter(roleMB, posInfo[0], posInfo[1], pickArgs)

	def roleLogin(self, roleMB, pickArgs):
		"""
		virtual method
		玩家登陆
		"""
		spaceObject = self.getSpaceObject()
		exitScriptID, exitPosition, exitDirection = spaceObject.getReviveToExitInfo(roleMB, pickArgs)

		if exitScriptID == "":
			KBEDebug.CRITICAL_MSG("Space Config Exit SpaceScriptID is Empty!!!!")
			return

		spaceKey = pickArgs.get("spaceKey")
		spaceItem = self.getSpaceItemByKey(spaceKey)
		if not spaceItem:
			if int(spaceKey) == 0: #已经退出帮会
				exitScriptID, exitPosition, exitDirection = spaceObject.getLeaveTongSpaceInfo()
				if exitScriptID == "":
					KBEDebug.CRITICAL_MSG("Space Config Leave Tong SpaceScriptID is Empty!!!!")
					return
			roleMB.loginToConfigSpace(exitScriptID, exitPosition, exitDirection)
		else:	
			spaceItem.login( roleMB, pickArgs )

	def onSpaceCreateCell( self, spaceNumber, spaceBase ):
		"""
		space cell创建完成
		"""
		DomainBase.onSpaceCreateCell(self, spaceNumber, spaceBase)	#基类方法必须放前面

		spaceItem = self.spaceItems[spaceNumber]
		if spaceItem.belongType == csdefine.SPACE_BELONG_TONG:
			attackTongDBID = spaceItem.createArgs.get("attackTongInfo").get("dbid")
			protectTongDBID = spaceItem.createArgs.get("protectTongInfo").get("dbid")
			self.spaceKeyToSpaceNumber[str(attackTongDBID)] = spaceNumber
			self.spaceKeyToSpaceNumber[str(protectTongDBID)] = spaceNumber
			tempData = {"attackTongInfo": spaceItem.createArgs.get("attackTongInfo"), "protectTongInfo": spaceItem.createArgs.get("protectTongInfo")}
			if spaceItem.spaceMailBox and spaceItem.spaceMailBox.cell:
				spaceItem.spaceMailBox.cell.setBothSidesInfo(tempData)

	def onSpaceLoseCell( self, spaceNumber ):
		"""
		"""
		spaceItem = self.spaceItems[ spaceNumber ]
		if spaceItem.belongType == csdefine.SPACE_BELONG_TONG:
			attackTongDBID = spaceItem.createArgs.get("attackTongInfo").get("dbid")
			protectTongDBID = spaceItem.createArgs.get("protectTongInfo").get("dbid")
			if str(attackTongDBID) in self.spaceKeyToSpaceNumber:
				self.spaceKeyToSpaceNumber.pop(str(attackTongDBID))
			if str(protectTongDBID) in self.spaceKeyToSpaceNumber:
				self.spaceKeyToSpaceNumber.pop(str(protectTongDBID))

			self.closeSpaceTongDBIDList.append(str(attackTongDBID))
			self.closeSpaceTongDBIDList.append(str(protectTongDBID))

		DomainBase.onSpaceLoseCell(self, spaceNumber)
 
	def getSpaceItemByKey(self, spaceKey):
		"""
		根据spaceKey查找相应的space 
		"""
		if spaceKey in self.spaceKeyToSpaceNumber:
			number = self.spaceKeyToSpaceNumber[spaceKey]
			return self.getSpaceItem(number)
		else:
			return None