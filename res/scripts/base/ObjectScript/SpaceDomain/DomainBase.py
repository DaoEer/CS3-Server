# -*- coding: utf-8 -*-

import KBEngine
import KBEMath
import Math
import math
import Functions
from ObjectScript.SpaceDomain.SpaceItem import SpaceItem
from ObjectScript.ObjectScriptBase.ScriptBase import ScriptBase

from ObjectScript import Space

class DomainBase( ScriptBase ):
	"""
	空间领域
	"""
	def __init__( self ):
		ScriptBase.__init__( self )
		self.spaceItems = {}

	def initData( self, configData ):
		ScriptBase.initData( self, configData )
		
	def initDomain( self ):
		"""
		virtual method
		"""
		pass
	
	def getSpaceObject( self ):
		"""
		获取副本object对象
		"""
		return Space.getObect( self.scriptID )
	
	def createSpaceItem(self, params):
		"""
		创建一个新的空间
		"""
		SpaceMgrBaseCall = KBEngine.globalData["SpaceManager"] #SpaceManger和Domain肯定在一个base上
		SpaceMgr = KBEngine.entities[ SpaceMgrBaseCall.id ]
		number = SpaceMgr.getNewSpaceNumber()
		cid = SpaceMgr.getFreeCellAppCid(self.scriptID)
		spaceItem = SpaceItem( self, number, cid, params )
		spaceItem.createBase( self.onSpaceCreateCallBack )
		SpaceMgr.incCellAppSpace(self.scriptID, cid)
		self.spaceItems[ number ] = spaceItem
		return spaceItem
		
	def findSpaceItem( self,  roleMB, pickArgs ):
		"""
		virtual method
		查找一个空间
		"""
		return None
	
	def getSpaceItem( self, spaceNumber ):
		return self.spaceItems.get( spaceNumber, None )
	
	def onSpaceCreateCallBack( self, spaceItem, spaceBase ):
		"""
		virtual method
		space base创建完成
		"""
		pass
	
	def onSpaceCreateCell( self, spaceNumber, spaceBase ):
		"""
		space cell创建完成
		"""
		self.spaceItems[ spaceNumber ].onGetCell()
	
	def onSpaceLoseCell( self, spaceNumber ):
		"""
		"""
		self.spaceItems[ spaceNumber ].onLoseCell()
		spaceItem = self.spaceItems.pop( spaceNumber )
		spaceMgr = KBEngine.globalData["SpaceManager"]
		spaceMgr.decCellAppSpace(self.scriptID, spaceItem.cid)
		
#------------------------------外部调用接口-----------------------------------------------------
	def roleLogin( self, roleMB, pickArgs  ):
		"""
		virtual method
		玩家登陆
		"""
		pass
	
	def gotoSpace( self, roleMB, position, direction, pickArgs ):
		"""
		virtual method
		玩家传送
		"""
		pass
		
	def onControlCloseSpace( self ):
		"""
		virtual method
		地图关闭接口
		"""
		pass