# -*- coding: utf-8 -*-
import csdefine
import csstatus
from ObjectScript.SpaceDomain.DomainBase import DomainBase
import KBEngine
import KBEDebug

class SpaceDomainHomeBarracks( DomainBase ):
	"""
	大本营空间领域
	"""
	def __init__( self ):
		DomainBase.__init__( self )
		self.lineMaxPlayerAmount = 0 #分线的人数上线
		self.maxLineNum = 0 #最大分线数
		self.lineNumberToSpaceNumber = {}
		self.lineNumberToPlayerDBID = {} #lineNumber:[playerDBID,playerDBID...]
	
	def initData( self, configData ):
		DomainBase.initData( self, configData )
		self.maxLineNum = configData["SpaceData"].get( "maxLineNum",0 )
		self.lineMaxPlayerAmount = configData["SpaceData"].get( "lineMaxPlayerAmount",0 )

	def createNewSpaceItem( self, lineNumber ):
		"""
		"""
		spaceItem = self.createSpaceItem( { "spaceKey": str(lineNumber), "belongType": csdefine.SPACE_BELONG_NORMAL} )
		self.lineNumberToSpaceNumber[lineNumber] = spaceItem.spaceNumber
		
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
		self.broadCastMaxLineNumber()

	def broadCastMaxLineNumber( self ):
		"""
		广播下最大线数
		"""
		lineNumberList = list( self.lineNumberToSpaceNumber.keys() )
		for spaceItem in self.spaceItems.values():
			if spaceItem.spaceMailBox and spaceItem.spaceMailBox.cell:
				spaceItem.spaceMailBox.cell.setMaxLineNumber( max(lineNumberList) )

	def decPlayerAmount( self, lineNumber, playerDBID ):
		"""
		减少某线的人数
		"""
		if lineNumber in self.lineNumberToPlayerDBID:
			if playerDBID in self.lineNumberToPlayerDBID[lineNumber]:
				self.lineNumberToPlayerDBID[lineNumber].remove(playerDBID)

		playerDBIDList = self.lineNumberToPlayerDBID.get( lineNumber, [] )
		if len(playerDBIDList) <= 0:
			self.lineNumberToPlayerDBID.pop(lineNumber, None)
			spaceItem = self.getSpaceItemByLineNumber( lineNumber )
			if spaceItem:
				self.lineNumberToSpaceNumber.pop(lineNumber)
				spaceItem.spaceMailBox.cell.closeSpace()

	def getSpaceItemByLineNumber( self, lineNumber ):
		"""
		通过lineNumber找spaceItem
		"""
		spaceNumber = self.lineNumberToSpaceNumber.get( lineNumber,0 )
		return self.getSpaceItem(spaceNumber)

	def findFreeSpaceNumber( self ):
		"""
		找到空闲的线
		"""
		lineNumberList = list( self.lineNumberToPlayerDBID.keys() )
		if not len( lineNumberList ):
			self.createNewSpaceItem(1)
			return 1

		playerAmountList = []
		for lineNumber in lineNumberList:
			playerAmountList.append(len(self.lineNumberToPlayerDBID.get( lineNumber,[] )))

		minPlayerAmount = min( playerAmountList )
		if minPlayerAmount < self.lineMaxPlayerAmount:	#如果自小分线人数都小于分线最大人数
			index = playerAmountList.index( minPlayerAmount )
			return lineNumberList[index]

		#找出中间某些已经关闭的线重新打开
		maxLineNumber = max(lineNumberList)
		for lineNumber in range(1, maxLineNumber + 1):
			if lineNumber not in lineNumberList:
				self.createNewSpaceItem(lineNumber)
				return lineNumber

		if max(lineNumberList) < self.maxLineNum:
			self.createNewSpaceItem( (max(lineNumberList) + 1) )
			return (max(lineNumberList) + 1)

		return None

	def spaceFullCheckOnEnter( self, lineNumber, playerDBID ):
		"""
		检查人数
		"""
		s1 = set(self.lineNumberToPlayerDBID.get(lineNumber,[]))
		if playerDBID in s1:
			return False

		return len( s1 ) >= self.lineMaxPlayerAmount
	
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

		if lineNumber not in self.lineNumberToPlayerDBID:
			self.lineNumberToPlayerDBID[lineNumber] = [playerDBID]
		else:
			if playerDBID not in self.lineNumberToPlayerDBID[lineNumber]:
				self.lineNumberToPlayerDBID[lineNumber].append(playerDBID)

		spaceItem = self.getSpaceItemByLineNumber( lineNumber )
		if spaceItem:
			spaceItem.login( roleMB, pickArgs )
	
	def gotoSpace( self, roleMB, position, direction, pickArgs ):
		"""
		virtual method
		玩家传送
		"""
		lineNumber = int( pickArgs["spaceKey"] )
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

		#这里检查下要进入的分线是否已经满员
		playerDBID = pickArgs["playerDBID"]
		if self.spaceFullCheckOnEnter(lineNumber, playerDBID):
			if hasattr(roleMB, "client") and roleMB.client:
				roleMB.client.statusMessage( csstatus.SPACE_LINENUMBER_IS_FULL,"" )
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
