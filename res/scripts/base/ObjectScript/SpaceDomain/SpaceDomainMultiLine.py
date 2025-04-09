# -*- coding: utf-8 -*-
import csdefine
import csstatus
from ObjectScript.SpaceDomain.DomainBase import DomainBase
import KBEngine
import KBEDebug

class SpaceDomainMultiLine( DomainBase ):
	"""
	多线地图空间领域
	"""
	def __init__( self ):
		DomainBase.__init__( self )
		self.lineNumberToSpaceNumber = {}
		self.lineNumberToPlayerDBID = {}	#lineNumber:[playerDBID,playerDBID...]
		self.lineNumberToPlayerDBIDUseTologin = {} #该数据主要用于玩家登陆时的找lineNumber处理
		self.maxLine = 1
		self.triggerLinePlayerAmount = 0
		self.lineMaxPlayerAmout = 0
		self.currInitLine = 1
	
	def initData( self, configData ):
		DomainBase.initData( self, configData )
		self.maxLine = configData["SpaceData"].get("maxLine",1)
		self.triggerLinePlayerAmount = configData["SpaceData"].get("triggerLinePlayerAmount",0)
		self.lineMaxPlayerAmout = configData["SpaceData"].get("maxPlayerAmount",0)
	
	def initDomain( self ):
		self.createNewSpaceItem( self.currInitLine )

	def createNewSpaceItem( self, lineNumber ):
		"""
		"""
		spaceItem = self.createSpaceItem( { "spaceKey": str(lineNumber), "belongType": csdefine.SPACE_BELONG_NORMAL} )
		self.lineNumberToSpaceNumber[lineNumber] = spaceItem.spaceNumber
		#KBEDebug.ERROR_MSG("{} {}".format(self.scriptID, self.lineNumberToSpaceNumber))
		
	def onSpaceCreateCell( self, spaceNumber, spaceBase ):
		"""
		space cell创建完成
		"""
		DomainBase.onSpaceCreateCell( self, spaceNumber, spaceBase )
		self.broadCastMaxLineNumber()

	def onSpaceLoseCell( self, spaceNumber ):
		"""
		"""
		DomainBase.onSpaceLoseCell( self, spaceNumber )
		self.checkLineNumberData()
		self.broadCastMaxLineNumber()

	def broadCastMaxLineNumber( self ):
		"""
		广播下最大线数
		"""
		lineNumberList = list( self.lineNumberToSpaceNumber.keys() )
		for spaceItem in self.spaceItems.values():
			if spaceItem.spaceMailBox and spaceItem.spaceMailBox.cell:
				spaceItem.spaceMailBox.cell.setMaxLineNumber( max(lineNumberList) )

	def findFreeSpaceNumber( self ):
		"""
		找到空闲的spaceNumber
		"""
		freeTriggerLine = (None, 99999)
		freeMaxPlayerLine = (None, 99999)
		lineNumberList = list(self.lineNumberToSpaceNumber.keys())
		for lineNumber in lineNumberList:
			playerDBIDList = set(self.lineNumberToPlayerDBID.get(lineNumber, []) + self.lineNumberToPlayerDBIDUseTologin.get(lineNumber, []))
			if len(playerDBIDList) < self.triggerLinePlayerAmount:
				if freeTriggerLine[1] > len(playerDBIDList):
					freeTriggerLine = (lineNumber, len(playerDBIDList))
					continue
			
			if freeMaxPlayerLine[1] > len(playerDBIDList):
				freeMaxPlayerLine = (lineNumber, len(playerDBIDList))
		
		if freeTriggerLine[0]:
			return freeTriggerLine[0]
		
		#找出中间某些已经关闭的线重新打开
		maxLineNumber = max(lineNumberList)
		for lineNumber in range(1, maxLineNumber + 1):
			if lineNumber not in lineNumberList:
				self.createNewSpaceItem(lineNumber)
				return lineNumber
		
		if max(lineNumberList) < self.maxLine:
			self.createNewSpaceItem( (max(lineNumberList) + 1) )
			return (max(lineNumberList) + 1)
		
		if freeMaxPlayerLine[0]:
			return freeMaxPlayerLine[0]
		return None

	def getSpaceItemByLineNumber( self, lineNumber ):
		"""
		通过lineNumber找spaceItem
		"""
		spaceNumber = self.lineNumberToSpaceNumber.get( lineNumber,0 )
		return self.getSpaceItem(spaceNumber)

	def incPlayerAmount( self, lineNumber, playerDBID ):
		"""
		增加某线的人数
		"""
		if lineNumber in self.lineNumberToPlayerDBIDUseTologin:
			if playerDBID in self.lineNumberToPlayerDBIDUseTologin[lineNumber]:
				self.lineNumberToPlayerDBIDUseTologin[lineNumber].remove( playerDBID )
		
		if lineNumber in self.lineNumberToPlayerDBID:
			if playerDBID not in self.lineNumberToPlayerDBID[lineNumber]:
				self.lineNumberToPlayerDBID[lineNumber].append( playerDBID )
		else:
			self.lineNumberToPlayerDBID[lineNumber] = [playerDBID]
		
		self.onPlayerChange(lineNumber)

	def decPlayerAmount( self, lineNumber, playerDBID ):
		"""
		减少某线的人数
		"""
		if lineNumber in self.lineNumberToPlayerDBID:
			if playerDBID in self.lineNumberToPlayerDBID[lineNumber]:
				self.lineNumberToPlayerDBID[lineNumber].remove(playerDBID)
		if lineNumber in self.lineNumberToPlayerDBIDUseTologin:
			if playerDBID in self.lineNumberToPlayerDBIDUseTologin[lineNumber]:
				self.lineNumberToPlayerDBIDUseTologin[lineNumber].remove(playerDBID)
		
		#1线不能关闭
		playerDBIDList = set(self.lineNumberToPlayerDBID.get(lineNumber, []) + self.lineNumberToPlayerDBIDUseTologin.get(lineNumber, []))
		if lineNumber > 1 and len(playerDBIDList) <= 0:
			self.lineNumberToPlayerDBID.pop(lineNumber, None)
			self.lineNumberToPlayerDBIDUseTologin.pop(lineNumber, None)
			spaceItem = self.getSpaceItemByLineNumber( lineNumber )
			if spaceItem:
				#KBEDebug.ERROR_MSG("%s pop line %d" %(self.scriptID, lineNumber))
				self.lineNumberToSpaceNumber.pop(lineNumber)
				spaceItem.spaceMailBox.cell.closeSpace()
				#KBEDebug.ERROR_MSG("{} {}".format(self.scriptID, self.lineNumberToSpaceNumber))
			self.onPlayerChange(lineNumber)
		
	def onPlayerChange( self, lineNumber ):
		"""
		"""
		pass
		#这里不广播了，因为已经在这边判断人数了
		#KBEngine.globalData[ self.scriptID + "playerNum" ] = [self.lineNumberToPlayerDBID, self.lineNumberToPlayerDBIDUseTologin]

	def spaceFullCheckOnEnter( self, lineNumber, playerDBID ):
		"""
		检查人数
		"""
		s1 = set(self.lineNumberToPlayerDBID.get(lineNumber,[]))
		if playerDBID in s1:
			return False
		s2 = set(self.lineNumberToPlayerDBIDUseTologin.get(lineNumber, []))
		if playerDBID in s2:
			return False
		
		#两个集合中不重复的元素集合
		return len( s1.symmetric_difference(s2) ) >= self.lineMaxPlayerAmout
	
	#------------------------------外部调用接口-----------------------------------------------------
	def roleLogin( self, roleMB, pickArgs  ):
		"""
		virtual method
		玩家登陆
		"""
		playerDBID = pickArgs["playerDBID"]
		lineNumber = self.findFreeSpaceNumber()
		if lineNumber == None:
			KBEDebug.ERROR_MSG("Has no Space[%s] Can Enter Player" %(self.scriptID))
			return
		
		if lineNumber not in self.lineNumberToPlayerDBIDUseTologin:
			self.lineNumberToPlayerDBIDUseTologin[lineNumber] = [playerDBID]
		else:
			if playerDBID not in self.lineNumberToPlayerDBIDUseTologin[lineNumber]:
				self.lineNumberToPlayerDBIDUseTologin[lineNumber].append(playerDBID)
		
		spaceItem = self.getSpaceItemByLineNumber( lineNumber )
		if spaceItem:
			spaceItem.login( roleMB, pickArgs )
	
	def gotoSpace( self, roleMB, position, direction, pickArgs ):
		"""
		virtual method
		玩家传送
		"""
		lineNumber = int(pickArgs["spaceKey"])
		if lineNumber == -1:
			if self.scriptID == pickArgs["currSpaceScriptID"]:	# 同地图传送又没有选择线的情况下，不转线
				lineNumber = pickArgs["currSpaceLineNumber"]
			else:
				lineNumber = self.findFreeSpaceNumber()

		if lineNumber == None:
			KBEDebug.ERROR_MSG("Has no Space[%s] Can Enter Player" %(self.scriptID))
			return
	
		del pickArgs[ "currSpaceScriptID" ]
		del pickArgs[ "currSpaceLineNumber" ]
		
		if lineNumber not in self.lineNumberToSpaceNumber:
			lineNumberList = list(self.lineNumberToSpaceNumber.keys())
			if lineNumber <= max(lineNumberList):
				self.createNewSpaceItem(lineNumber)
			else:
				KBEDebug.ERROR_MSG("not found spaceItem[%s, %d]" %(self.scriptID, lineNumber))
				return
		
		#这里检查下要进入的分线是否已经满员
		playerDBID = pickArgs["playerDBID"]
		if self.spaceFullCheckOnEnter(lineNumber, playerDBID):
			if hasattr(roleMB, "client") and roleMB.client:
				roleMB.client.statusMessage( csstatus.SPACE_LINENUMBER_IS_FULL, "" )
				roleMB.client.CLIENT_RequestGotoLineNumberSpaceFailure()
			return
			
		if lineNumber not in self.lineNumberToPlayerDBID:
			self.lineNumberToPlayerDBID[lineNumber] = [playerDBID]
		else:
			if playerDBID not in self.lineNumberToPlayerDBID[lineNumber]:
				self.lineNumberToPlayerDBID[lineNumber].append(playerDBID)
		
		pickArgs["spaceKey"] = str(lineNumber)
		spaceItem = self.getSpaceItemByLineNumber(lineNumber)
		if spaceItem:
			spaceItem.enter( roleMB, position, direction, pickArgs )

	def OutputProcessInfos(self):
		"""
		"""
		for lineNumber in self.lineNumberToSpaceNumber.keys():
			playerDBIDList = set(self.lineNumberToPlayerDBID.get(lineNumber, []) + self.lineNumberToPlayerDBIDUseTologin.get(lineNumber, []))
			KBEDebug.OUTPUT_PROCESS_INFOS("space:{}-{}, role:{}".format(self.scriptID, lineNumber, len(playerDBIDList)))
			
	#------------------ 地图频道发言 -------------------------------------
	def onSendChatMessage( self, id, playerDBID, chatData ):
		"""
		"""
		for spaceItem in self.spaceItems.values():
			if spaceItem.spaceMailBox and spaceItem.spaceMailBox.cell:
				if spaceItem.spaceMailBox.id == id: continue
				spaceItem.spaceMailBox.cell.onSendChatMessageFromBase( playerDBID, chatData )
				
	def checkLineNumberData(self):
		"""
		"""
		lineNumberList = []
		for _lineNumber, _spaceNumber in self.lineNumberToSpaceNumber.items():
			if _spaceNumber not in self.spaceItems:	
				lineNumberList.append(_lineNumber)
		
		for lineNumber in lineNumberList:
			self.lineNumberToSpaceNumber.pop(_lineNumber)
			self.lineNumberToPlayerDBID.pop(_lineNumber, None)
			self.lineNumberToPlayerDBIDUseTologin.pop(_lineNumber, None)