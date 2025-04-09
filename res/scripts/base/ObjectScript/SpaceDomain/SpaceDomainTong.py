# -*- coding: utf-8 -*-

import KBEngine
import csdefine
from ObjectScript.SpaceDomain.DomainBase import DomainBase
import KBEDebug

class SpaceDomainTong( DomainBase ):
	"""
	帮会空间领域
	"""
	def __init__( self ):
		DomainBase.__init__( self )

	def findSpaceItem( self,  roleMB, pickArgs ):
		"""
		virtual method
		查找一个空间
		"""
		spaceKey = pickArgs["spaceKey"]
		belongType = pickArgs["belongType"]
		for spaceItem in self.spaceItems.values():
			if spaceItem.spaceKey == spaceKey and spaceItem.belongType == belongType:
				return spaceItem
		return None
		
	def onSpaceCreateCell( self, spaceNumber, spaceBase ):
		"""
		space cell创建完成
		"""
		DomainBase.onSpaceCreateCell( self, spaceNumber, spaceBase )
		KBEngine.globalData["TongMgr"].onTongSpaceCreateFinish( spaceBase.tongDBID, spaceBase )				# 因为spaceTong在同一个Base创建，所以这里是实体
	#------------------------------外部调用接口-----------------------------------------------------
	def roleLogin( self, roleMB, pickArgs  ):
		"""
		virtual method
		玩家登陆
		"""
		spaceItem = self.findSpaceItem( roleMB, pickArgs )
		if not spaceItem:
			if int(pickArgs["spaceKey"]) == 0: # 表示没有帮会了 直接在绑定点复活
				roleMB.loginToBindReviveSpace()
				return
			else:
				spaceItem = self.createSpaceItem( pickArgs )
		
		spaceItem.login( roleMB, pickArgs )
		
	def gotoSpace( self, roleMB, position, direction, pickArgs ):
		"""
		virtual method
		玩家传送
		"""
		spaceItem = self.findSpaceItem( roleMB, pickArgs )
		if not spaceItem:
			if int(pickArgs["spaceKey"]) == 0:
				if hasattr(roleMB, "cell") and roleMB.cell:
					roleMB.cell.gotoBindSpace()
				else:
					roleMB.loginToReviveSpace()
				return
			else:
				spaceItem = self.createSpaceItem( pickArgs )
		
		spaceItem.enter( roleMB, position, direction, pickArgs )