# -*- coding: utf-8 -*-

import KST
import KBEngine
from CoreObject import MgrPersistentObject
from KBEDebug import *

class BunchSpaceManager( MgrPersistentObject.MgrPersistentObject ):
	"""
	副本串管理器
	"""
	def __init__( self ):
		MgrPersistentObject.MgrPersistentObject.__init__( self )
		self.bunchDomains = KST.g_objFactory.getAllBunchSpaceDomian()
		self.bunchGlobalRecord = {}		# 副本串记录，用于cell进副本时预先查找某spaceKey的副本串是否存在
		KBEngine.globalData["BunchSpaceGlobalRecord"] = {}
		self.onCompleteInit()
	
	def onSpaceCreateCell( self, bunchScriptID, belongType, spaceKey,childSpaceScriptID ):
		"""
		<define method>
		子副本创建
		"""
		self.bunchDomains[ bunchScriptID ].onSpaceCreateCell( belongType, spaceKey,childSpaceScriptID )
	
	def onSpaceLoseCell( self, bunchScriptID, belongType, spaceKey, childSpaceScriptID ):
		"""
		<define method>
		子副本销毁
		"""
		self.bunchDomains[ bunchScriptID ].onSpaceLoseCell( belongType, spaceKey, childSpaceScriptID )
	
	def gotoBunchSpace( self, bunchScriptID, roleMB, pickArgs ):
		"""
		<define method>
		进副本串
		"""
		self.bunchDomains[ bunchScriptID ].gotoBunchSpace( roleMB, pickArgs )
	
	def onEnterSpace( self, bunchScriptID, belongType, spaceKey, activityType, roleMB, roleDBID ):
		"""
		<define method>
		进子副本
		"""
		self.bunchDomains[ bunchScriptID ].onEnterSpace( belongType, spaceKey, activityType, roleMB, roleDBID )
	
	def onSpaceSuccess( self, bunchScriptID, belongType, spaceKey, childSpaceIndex ):
		"""
		<define method>
		子副本通关
		"""
		self.bunchDomains[ bunchScriptID ].onSpaceSuccess( belongType, spaceKey, childSpaceIndex )
	
	def onBunchSpaceItemCreate( self, bunchScriptID, belongType, spaceKey ):
		"""
		<define method>
		bunchItem创建
		"""
		if bunchScriptID not in self.bunchGlobalRecord:
			self.bunchGlobalRecord[ bunchScriptID ] = {}
		if belongType not in self.bunchGlobalRecord[ bunchScriptID ]:
			self.bunchGlobalRecord[ bunchScriptID ][ belongType ] = []
		self.bunchGlobalRecord[ bunchScriptID ][ belongType ].append( spaceKey )
		KBEngine.globalData["BunchSpaceGlobalRecord"] = self.bunchGlobalRecord
	
	def onBunchSpaceItemDelete( self, bunchScriptID, belongType, spaceKey ):
		"""
		<define method>
		bunchItem删除
		"""
		self.bunchGlobalRecord[ bunchScriptID ][ belongType ].remove( spaceKey )
		if len( self.bunchGlobalRecord[ bunchScriptID ][ belongType ] ) == 0:
			self.bunchGlobalRecord[ bunchScriptID ].pop( belongType )
		if len( self.bunchGlobalRecord[ bunchScriptID ] ) == 0:
			self.bunchGlobalRecord.pop( bunchScriptID )
		KBEngine.globalData["BunchSpaceGlobalRecord"] = self.bunchGlobalRecord