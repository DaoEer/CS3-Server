# -*- coding: utf-8 -*-
import csdefine
import csstatus
from ObjectScript.SpaceDomain.DomainBase import DomainBase
import KBEngine
import KBEDebug

class SpaceDomainHomeBarracksBHZB( DomainBase ):
	"""
	帮会争霸大本营空间领域
	"""
	def __init__( self ):
		DomainBase.__init__( self )
		self.lineNumberToTongDBIDs = {} 	# 分线对应的帮会数据
		self.lineNumberToSpaceNumber = {}
		self.lineNumberToPlayerDBIDs ={} #玩家对应分线编号 主要是用于重登
		
	def initData( self, configData ):
		DomainBase.initData( self, configData )
		
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

	def getSpaceItemByLineNumber( self, lineNumber ):
		"""
		通过lineNumber找spaceItem
		"""
		spaceNumber = self.lineNumberToSpaceNumber.get( lineNumber,0 )
		return self.getSpaceItem(spaceNumber)

	def getSpaceLineNumberByTongDBID( self, tongDBID ):
		"""
		通过TongDBID获得spaceLineNumber
		"""
		findLineNumber = 0
		for lineNumber, tongDBIDs in self.lineNumberToTongDBIDs.items():
			if tongDBID in tongDBIDs:
				findLineNumber = lineNumber
				break
		return findLineNumber

	def getOnLoginSpaceLineNumberByPlayerDBID( self, playerDBID ):
		"""
		通过玩家的DBID 获得 lineNumber
		"""
		findLineNumber = 0
		for lineNumber, playerDBIDs in self.lineNumberToTongDBIDs.items():
			if playerDBID in playerDBIDs:
				findLineNumber = lineNumber
				break
		return findLineNumber

	def requestNewSpace( self, params ):
		"""
		define method.
		请求预创建一个指定的space
		"""
		tongDBIDs = params.pop("tongDBIDs")
		spaceItem = self.createSpaceItem( params )
		self.lineNumberToTongDBIDs[int(spaceItem.spaceKey)] = tongDBIDs
		self.lineNumberToSpaceNumber[int(spaceItem.spaceKey)] = spaceItem.spaceNumber

	#------------------------------外部调用接口-----------------------------------------------------
	def roleLogin( self, roleMB, pickArgs  ):
		"""
		virtual method
		玩家登陆
		"""
		playerDBID = pickArgs["playerDBID"]
		lineNumber = self.getOnLoginSpaceLineNumberByPlayerDBID( playerDBID )
		spaceItem = self.getSpaceItemByLineNumber( lineNumber )
		if spaceItem:
			pickArgs["spaceKey"] = lineNumber
			spaceItem.login( roleMB, pickArgs )
		else:
			spaceObject = self.getSpaceObject()
			exitScriptID, exitPosition, exitDirection = spaceObject.getReviveToExitInfo( roleMB, pickArgs )
			if exitScriptID == "":
				KBEDebug.CRITICAL_MSG( "Space Config Exit SpaceScriptID is Empty!!!!" )
				return
			roleMB.loginToConfigSpace( exitScriptID, exitPosition, exitDirection )
	
	def gotoSpace( self, roleMB, position, direction, pickArgs ):
		"""
		virtual method
		玩家传送
		"""
		tongDBID = pickArgs["spaceKey"]
		playerDBID = pickArgs["playerDBID"]
		lineNumber = self.getSpaceLineNumberByTongDBID( tongDBID )
		spaceItem = self.getSpaceItemByLineNumber( lineNumber )
		if spaceItem:
			pickArgs["spaceKey"] = lineNumber
			spaceItem.enter( roleMB, position, direction, pickArgs )
			if lineNumber not in self.lineNumberToPlayerDBIDs:
				self.lineNumberToPlayerDBIDs[lineNumber] = []
			if playerDBID not in self.lineNumberToPlayerDBIDs[lineNumber]:
				self.lineNumberToPlayerDBIDs[lineNumber].append(playerDBID)
		else:
			spaceObject = self.getSpaceObject()
			exitScriptID, exitPosition, exitDirection = spaceObject.getReviveToExitInfo( roleMB, pickArgs )
			if exitScriptID == "":
				KBEDebug.CRITICAL_MSG( "Space Config Exit SpaceScriptID is Empty!!!!" )
				return
			roleMB.loginToConfigSpace( exitScriptID, exitPosition, exitDirection )