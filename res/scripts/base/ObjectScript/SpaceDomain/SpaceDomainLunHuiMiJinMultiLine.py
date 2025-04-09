# -*- coding: utf-8 -*-
import csdefine
from ObjectScript.SpaceDomain.DomainBase import DomainBase
import KBEngine
import KBEDebug

class SpaceDomainLunHuiMiJinMultiLine( DomainBase ):
	"""
	轮回秘境多线地图空间领域
	"""
	def __init__( self ):
		DomainBase.__init__( self )
		self.lineNumberToSpaceNumber = {}
	
	def initData( self, configData ):
		DomainBase.initData( self, configData )
	
	def initDomain( self ):
		""""""
		KBEngine.globalData["SpaceLunHuiMiJinMgr"].initDFSpace()
		
	def initDFSpace( self, lineNumberList ):
		"""
		创建洞府Space
		"""
		for lineNumber in lineNumberList:
			self.createNewSpaceItem( lineNumber )

	def activityStart( self ):
		"""
		活动开始(开始刷怪)
		"""
		for spaceItem in self.spaceItems.values():
			if spaceItem.spaceMailBox:
				spaceItem.spaceMailBox.activityStart()

	def activityEnd( self ):
		"""
		活动结束(停止刷怪)
		"""
		for spaceItem in self.spaceItems.values():
			if spaceItem.spaceMailBox:
				spaceItem.spaceMailBox.activityEnd()

	def createNewSpaceItem( self, lineNumber ):
		"""
		"""
		spaceItem = self.createSpaceItem( { "spaceKey": str(lineNumber), "belongType": csdefine.SPACE_BELONG_NORMAL} )
		self.lineNumberToSpaceNumber[lineNumber] = spaceItem.spaceNumber
		return spaceItem

	def getSpaceItemByLineNumber( self, lineNumber ):
		"""
		通过lineNumber找spaceItem
		"""
		spaceNumber = self.lineNumberToSpaceNumber.get( lineNumber, 0 )
		return self.getSpaceItem(spaceNumber)

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
			if spaceItem.spaceMailBox:
				spaceItem.spaceMailBox.cell.setMaxLineNumber( max(lineNumberList) )
	
	#------------------------------外部调用接口-----------------------------------------------------
	def roleLogin( self, roleMB, pickArgs  ):
		"""
		virtual method
		玩家登陆
		"""
		playerDBID = pickArgs["playerDBID"]
		KBEngine.globalData["SpaceLunHuiMiJinMgr"].requestLineNumberDataOnLogin( roleMB, playerDBID, pickArgs )

	def createAppointSpaceItem( self, roleMB, lineNumber, pickArgs ):
		"""
		玩家是否指定线存在
		"""
		spaceItem = self.getSpaceItemByLineNumber(lineNumber)
		if not spaceItem:
			spaceItem = self.createNewSpaceItem( lineNumber )
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
				self.onRealEnter( roleMB, lineNumber, position, direction, pickArgs )
			else:
				playerDBID = pickArgs["playerDBID"]
				KBEngine.globalData["SpaceLunHuiMiJinMgr"].requestLineNumberData( roleMB, playerDBID, position, direction, pickArgs )
		else:
			self.gotoAppointSpaceItem( roleMB, lineNumber, position, direction, pickArgs )

	def gotoAppointSpaceItem( self, roleMB, lineNumber, position, direction, pickArgs ):
		"""
		玩家传送
		"""
		spaceItem = self.getSpaceItemByLineNumber(lineNumber)
		if not spaceItem:
			self.createNewSpaceItem( lineNumber )
		self.onRealEnter( roleMB, lineNumber, position, direction, pickArgs )

	def onRealEnter( self, roleMB, lineNumber, position, direction, pickArgs ):
		"""
		真正的要传送走了
		"""
		if lineNumber == None:
			KBEDebug.ERROR_MSG("Has no Space[%s] Can Enter Player" %(self.scriptID))
			return

		del pickArgs[ "currSpaceScriptID" ]
		del pickArgs[ "currSpaceLineNumber" ]

		pickArgs["spaceKey"] = str(lineNumber)
		spaceItem = self.getSpaceItemByLineNumber(lineNumber)
		if spaceItem:
			spaceItem.enter( roleMB, position, direction, pickArgs )

	def createCellEntityByScriptID(self, id, playerDBID, lineNumber, scriptID, npcID, group):
		"""创建cellEntity"""
		spaceItem = self.getSpaceItemByLineNumber(lineNumber)
		if spaceItem:
			spaceItem.spaceMailBox.cell.createCellEntityByScriptID(id, playerDBID, scriptID, npcID, group)
		
	def noticeMECPEnter( self, lineNumber, group, playerID ):
		""""""
		spaceItem = self.getSpaceItemByLineNumber(lineNumber)
		if spaceItem:
			spaceItem.spaceMailBox.cell.noticeMECPEnter( group, playerID )
		
	def destroyCellEntityByScriptID(self, lineNumber, group):
		"""销毁 cellEntity"""
		spaceItem = self.getSpaceItemByLineNumber(lineNumber)
		if spaceItem:
			spaceItem.spaceMailBox.cell.destroyCellEntityByScriptID(group)