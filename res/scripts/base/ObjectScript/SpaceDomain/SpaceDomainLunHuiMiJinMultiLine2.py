# -*- coding: utf-8 -*-
import csdefine
import csstatus
from ObjectScript.SpaceDomain.SpaceDomainMultiLine import SpaceDomainMultiLine
import KBEngine
import KBEDebug

class SpaceDomainLunHuiMiJinMultiLine2( SpaceDomainMultiLine ):
	"""
	轮回秘境第二层地图领域
	"""
	def __init__( self ):
		SpaceDomainMultiLine.__init__( self )
		self.waitCloseSpaceItems = {}
		
	def onSpaceCreateCallBack( self, spaceItem, spaceBase ):
		"""
		virtual method
		space base创建完成
		"""
		SpaceDomainMultiLine.onSpaceCreateCallBack(self, spaceItem, spaceBase)
		if spaceItem.spaceNumber in self.waitCloseSpaceItems:
			spaceItem.spaceMailBox.onControlClose()
			self.waitCloseSpaceItems.remove(spaceItem.spaceNumber)
			
	def findFreeSpaceNumber( self ):
		"""
		找到空闲的spaceNumber
		"""
		if len(self.lineNumberToSpaceNumber) <= 0:
			#key = csdefine.CONTROL_SPACE_KEY + self.scriptID
			#openStatus = KBEngine.globalData.get(key, False)
			#if not openStatus:
			#	return None
			
			self.createNewSpaceItem(self.currInitLine)
			return self.currInitLine	
		
		return SpaceDomainMultiLine.findFreeSpaceNumber(self)
		
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
		if lineNumber > 0 and len(playerDBIDList) <= 0:
			self.lineNumberToPlayerDBID.pop(lineNumber, None)
			self.lineNumberToPlayerDBIDUseTologin.pop(lineNumber, None)
			spaceItem = self.getSpaceItemByLineNumber( lineNumber )
			if spaceItem:
				#KBEDebug.ERROR_MSG("%s pop line %d" %(self.scriptID, lineNumber))
				self.lineNumberToSpaceNumber.pop(lineNumber)
				spaceItem.spaceMailBox.cell.closeSpace()
				#KBEDebug.ERROR_MSG("{} {}".format(self.scriptID, self.lineNumberToSpaceNumber))
			self.onPlayerChange(lineNumber)
		
	#------------------------------外部调用接口-----------------------------------------------------
	def roleLogin( self, roleMB, pickArgs  ):
		"""
		virtual method
		玩家登陆
		"""
		spaceObject = self.getSpaceObject()
		exitScriptID, exitPosition, exitDirection = spaceObject.getReviveToExitInfo( roleMB, pickArgs )
		if exitScriptID == "":
			KBEDebug.CRITICAL_MSG( "Space Config Exit SpaceScriptID is Empty!!!!" )
			return
		
		#key = csdefine.CONTROL_SPACE_KEY + self.scriptID
		#openStatus = KBEngine.globalData.get(key, False)
		#if not openStatus:
		#	roleMB.loginToConfigSpace( exitScriptID, exitPosition, exitDirection )
		#	return
		
		SpaceDomainMultiLine.roleLogin( self, roleMB, pickArgs  )
		
	def onControlCloseSpace( self ):
		"""
		virtual method
		地图关闭
		"""
		for spaceNumber, spaceItem in self.spaceItems.items():
			if spaceItem.baseCreateing:
				self.waitCloseSpaceItems[spaceNumber] = spaceItem
				continue
			
			if spaceItem.spaceMailBox:
				spaceItem.spaceMailBox.onControlClose()
		