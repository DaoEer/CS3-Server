# -*- coding: utf-8 -*-

import random
import csstatus
import csdefine
import KBEngine
from KBEDebug import *
from ObjectScript.ObjectScriptBase.ScriptBase import ScriptBase
from ObjectScript.BunchSpaceDomain.BunchSpaceItem import BunchSpaceItem

class BunchSpaceDomainBase( ScriptBase ):
	"""
	一个副本串的管理域
	"""
	def __init__( self ):
		ScriptBase.__init__( self )
		self.bunchItems = []

	def initData( self, configData ):
		ScriptBase.initData( self, configData )
	
	def initDomain( self ):
		pass
	
	def getBunchItem( self, belongType, spaceKey ):
		"""
		"""
		for item in self.bunchItems:
			if item.belongType == belongType and item.spaceKey == spaceKey:
				return item
		return None
	
	def getBunchObject( self ):
		from ObjectScript.ObjectScriptFactory import g_objFactory
		return g_objFactory.getBunchSpaceObject( self.scriptID )
	
	def onSpaceCreateCell( self, belongType, spaceKey,childSpaceScriptID ):
		"""
		子副本创建
		"""
		bunchItem = self.getBunchItem( belongType, spaceKey )
		if not bunchItem:
			bunchItem = BunchSpaceItem( self, belongType, spaceKey )
			self.bunchItems.append( bunchItem )
			KBEngine.globalData["BunchSpaceManager"].onBunchSpaceItemCreate( self.scriptID, bunchItem.belongType, bunchItem.spaceKey )
		bunchItem.onSpaceCreateCell( childSpaceScriptID )
	
	def onSpaceLoseCell( self, belongType, spaceKey, childSpaceScriptID ):
		"""
		子副本销毁
		"""
		bunchItem = self.getBunchItem( belongType, spaceKey )
		bunchItem.onSpaceLoseCell( childSpaceScriptID )
		if bunchItem.canDestroy():
			KBEngine.globalData["BunchSpaceManager"].onBunchSpaceItemDelete( self.scriptID, bunchItem.belongType, bunchItem.spaceKey )
			self.bunchItems.remove( bunchItem )

	def gotoBunchSpace( self, roleMB, pickArgs ):
		"""
		玩家进副本串
		"""
		activityType = pickArgs.get("activityType", csdefine.ACTIVITY_TYPE_UNKNOWN)
		bunchItem = self.getBunchItem( pickArgs["belongType"], pickArgs["spaceKey"] )
		# 进已有副本串
		if bunchItem:
			gotoArgs = { "packBelongType": pickArgs["belongType"], "packSpaceLevel": pickArgs["bunchLevel"], "completeList": bunchItem._completeList, "activityType": activityType }
			roleMB.cell.gotoSpaceEnterPos( bunchItem._createList[-1], gotoArgs )
		
		# 新建副本串
		else:
			destSpace = pickArgs[ "destChildSpace" ]
			if destSpace not in self.getBunchObject().getAllChildScriptID():
				DEBUG_MSG("Dest bunch child space(%s) is invalid." % destSpace )
				return
			
			gotoArgs = { "packBelongType": pickArgs["belongType"], "packSpaceLevel": pickArgs["bunchLevel"], "completeList": [], "activityType": activityType }
			roleMB.cell.gotoSpaceEnterPos( destSpace, gotoArgs )
			for teamMember in pickArgs.get( "teammates", [] ):	# 传送队员
				teamMember.cell.gotoSpaceEnterPos( destSpace, gotoArgs )
	
	def onEnterSpace( self, belongType, spaceKey, activityType, roleMB, roleDBID ):
		"""
		玩家进子副本
		"""
		self.getBunchItem( belongType, spaceKey ).onEnterSpace( activityType, roleMB, roleDBID )
	
	def onSpaceSuccess( self, belongType, spaceKey, childSpaceIndex ):
		"""
		子副本通关
		"""
		self.getBunchItem( belongType, spaceKey ).onSpaceSuccess( childSpaceIndex )