# -*- coding: utf-8 -*-

import KBEngine
import csdefine
from ObjectScript.SpaceDomain.SpaceDomainCopy import SpaceDomainCopy
import KBEDebug

class SpaceDomainCopyDongFu( SpaceDomainCopy ):
	"""
	洞府 空间领域
	"""
	def __init__( self ):
		SpaceDomainCopy.__init__( self )
		self.spaceNumberToPlayerDBID = {}
	
	def createSpaceItem(self, params):
		"""
		创建一个新的空间
		"""
		spaceItem = SpaceDomainCopy.createSpaceItem(self, params)
		self.spaceNumberToPlayerDBID[spaceItem.spaceNumber] = params["belongDBID"]
		return spaceItem
	
	def onSpaceCreateCell( self, spaceNumber, spaceBase ):
		"""
		space cell创建完成
		"""
		SpaceDomainCopy.onSpaceCreateCell( self, spaceNumber, spaceBase )	#基类方法必须放前面
		belongDBID = self.spaceNumberToPlayerDBID.pop(spaceNumber)
		KBEngine.globalData["SpaceLunHuiMiJinMgr"].onSpaceDongFuCreateFinish( belongDBID, spaceNumber )
		
	def createBattleformation(self, spaceNumber, scriprID, insPos, insDir):
		""""""
		spaceItem = self.spaceItems[spaceNumber]
		if spaceItem:
			spaceItem.spaceMailBox.cell.createBattleformation( scriprID, insPos, insDir )
			
	def destroyBattleformation( spaceNumber ):
		""""""
		spaceItem = self.spaceItems[spaceNumber]
		if spaceItem:
			spaceItem.spaceMailBox.cell.destroyBattleformation()
			
	def onChallengeActiveStart( self, pickArgs ):
		"""争夺战/掠夺战 活动开启"""
		spaceItem = self.findSpaceItem( None, pickArgs )			# 活动开启，就创建空间
		if not spaceItem:
			spaceItem = self.createSpaceItem( pickArgs )
		else:
			spaceItem.spaceMailBox.cell.onChallengeActiveStart()
		
	def onChallengeActiveEnd( self, isChallenge, pickArgs ):
		"""争夺战/掠夺战 活动结束"""
		spaceItem = self.findSpaceItem( None, pickArgs )
		if spaceItem:
			spaceItem.spaceMailBox.cell.onChallengeActiveEnd( isChallenge )
			
	def onAddOriginPet( self, pickArgs, petData ):
		"""添加原兽"""
		spaceItem = self.findSpaceItem( None, pickArgs )
		if spaceItem:
			spaceItem.spaceMailBox.cell.onAddOriginPet( petData )
			
	def onRemoveOriginPet( self, pickArgs, uid, directDel ):
		"""移除原兽"""
		spaceItem = self.findSpaceItem( None, pickArgs )
		if spaceItem:
			spaceItem.spaceMailBox.cell.onRemoveOriginPet( uid, directDel )
			
	def onExChangeOriginPet( self, pickArgs, petData, uid ):
		"""交换 原兽"""
		spaceItem = self.findSpaceItem( None, pickArgs )
		if spaceItem:
			spaceItem.spaceMailBox.cell.onExChangeOriginPet( petData, uid )
	
	def onBuildRepair( self, pickArgs, buildType ):
		"""建筑修复完成"""
		spaceItem = self.findSpaceItem( None, pickArgs )
		if spaceItem:
			spaceItem.spaceMailBox.cell.onBuildRepair( buildType )