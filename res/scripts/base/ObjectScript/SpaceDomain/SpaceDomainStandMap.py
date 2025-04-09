# -*- coding: utf-8 -*-
import csdefine
import csstatus
from ObjectScript.SpaceDomain.DomainBase import DomainBase
import KBEngine
import KBEDebug

class SpaceDomainStandMap( DomainBase ):
	"""
	沙盘大地图空间领域
	"""
	def __init__( self ):
		DomainBase.__init__( self )
		self.maxLineNum = 0 	# 最大分线数
		self.triggerLinePlayerAmount = 0 #触发分线人数
		self.lineMaxPlayerAmount = 0	#分线容纳的最大人数
		self.lineNumberToSpaceNumber = {}
		self.lineNumberToPlayerDBID = {} #lineNumber:[playerDBID,playerDBID...]
	
	def initData( self, configData ):
		DomainBase.initData( self, configData )
		self.maxLineNum = configData["SpaceData"].get("maxLineNum",0)
		self.triggerLinePlayerAmount = configData["SpaceData"].get("triggerLinePlayerAmount",0)
		self.lineMaxPlayerAmount = configData["SpaceData"].get("lineMaxPlayerAmount",0)

	def createNewSpaceItem( self, lineNumber ):
		"""
		"""
		spaceItem = self.createSpaceItem( { "spaceKey": str(lineNumber), "belongType": csdefine.SPACE_BELONG_NORMAL} )
		self.lineNumberToSpaceNumber[lineNumber] = spaceItem.spaceNumber
		self.lineNumberToPlayerDBID[lineNumber] = []
		
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

		# playerDBIDList = self.lineNumberToPlayerDBID.get( lineNumber, [] )
		# if len(playerDBIDList) <= 0:
		# 	self.lineNumberToPlayerDBID.pop(lineNumber, None)
		# 	spaceItem = self.getSpaceItemByLineNumber( lineNumber )
		# 	if spaceItem:
		# 		self.lineNumberToSpaceNumber.pop(lineNumber)
		# 		spaceItem.spaceMailBox.cell.closeSpace()
								

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
		lineNumberList = list( self.lineNumberToPlayerDBID.keys() )
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

	def requestNewSpace( self, params ):
		"""
		define method.
		请求预创建一个指定的space
		"""
		enterAmount = params.get("enterAmount",0)
		lineNumberList = list(self.lineNumberToSpaceNumber.keys())
		if len(lineNumberList):
			maxLineNumber = max(lineNumberList)
			if maxLineNumber * self.triggerLinePlayerAmount > enterAmount:
				lineNumber = max( lineNumberList ) + 1
				self.createSpaceItem( lineNumber )
		else:
			self.createSpaceItem( 1 )

	def preCreateSpace( self, needCreateStandMapNum ):
		"""
		预创建沙盘space 
		"""
		lineNumberList = list(self.lineNumberToSpaceNumber.keys())
		maxLineAmount = 0
		if len( lineNumberList ):
			maxLineAmount = max( lineNumberList )
		if maxLineAmount < needCreateStandMapNum:
			num = needCreateStandMapNum - maxLineAmount
			for i in range(0, num ):
				self.createNewSpaceItem( maxLineAmount + i + 1 )

	def notifySpaceTrainSoldierGroundOccupy( self, lineNumber, index, playerDBID, playerName, playerProfession ):
		"""
		通知space更新数据
		"""
		spaceItem = self.getSpaceItemByLineNumber( lineNumber )
		if not spaceItem:
			return
		if spaceItem.spaceMailBox and spaceItem.spaceMailBox.cell:
			spaceItem.spaceMailBox.cell.notifyTrainSoldierGroundOccupyed( index, playerDBID, playerName, playerProfession )

	def clearOtherIsOccupyPlayerDBIDGroundData( self, lineNumber, index ):
		"""
		通知space更新数据
		"""
		spaceItem = self.getSpaceItemByLineNumber( lineNumber )
		if not spaceItem:
			return
		if spaceItem.spaceMailBox and spaceItem.spaceMailBox.cell:
			spaceItem.spaceMailBox.cell.clearOtherIsOccupyPlayerDBIDGroundData( lineNumber, index )

	def notifySpaceNPCTrainSoldierGroundState( self, lineNumber, index ):
		"""
		通知space更新数据
		"""
		spaceItem = self.getSpaceItemByLineNumber( lineNumber )
		if not spaceItem:
			return
		if spaceItem.spaceMailBox and spaceItem.spaceMailBox.cell:
			spaceItem.spaceMailBox.cell.notifySpaceNPCTrainSoldierGroundState( index )

	def openAllGroundDetail( self, roleOccupylineNumber, roleOccupytrainSoldierGroundIndex, roleMB, lineNumber, npcID ):
		"""
		打开练兵场所有面板详情
		"""
		spaceItem = self.getSpaceItemByLineNumber( lineNumber )
		if not spaceItem:
			return
		maxLineNumber = max(list(self.lineNumberToSpaceNumber.keys()))
		if spaceItem.spaceMailBox and spaceItem.spaceMailBox.cell:
			spaceItem.spaceMailBox.cell.openAllGroundDetail( roleOccupylineNumber, roleOccupytrainSoldierGroundIndex, roleMB, lineNumber, maxLineNumber,npcID )

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
		needCreateStandMapNum = pickArgs.get( "needCreateStandMapNum", -1)
		if needCreateStandMapNum > 0:
			lineNumberList = list(self.lineNumberToSpaceNumber.keys())
			maxLineAmount = 0
			if len( lineNumberList ):
				maxLineAmount = max( lineNumberList )
			if maxLineAmount < needCreateStandMapNum:
				num = needCreateStandMapNum - maxLineAmount
				for i in range(0, num ):
					self.createNewSpaceItem( maxLineAmount + i + 1 )
			del pickArgs["needCreateStandMapNum"]

		lineNumber = int( pickArgs["spaceKey"] )
		if lineNumber == -1:
			if self.scriptID == pickArgs["currSpaceScriptID"]:	# 同地图传送又没有选择线的情况下，不转线
				lineNumber = pickArgs["currSpaceLineNumber"]
			else:
				lineNumber = self.findFreeSpaceNumber()

		if lineNumber == None:
			KBEDebug.ERROR_MSG("Has no Space[%s] Can Enter Player" %(self.scriptID))
			return

		if "currSpaceScriptID" in pickArgs:
			del pickArgs[ "currSpaceScriptID" ]
		if "currSpaceLineNumber" in pickArgs:
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
