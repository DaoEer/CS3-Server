# -*- coding: utf-8 -*-

import time
import Math
from CoreObject.SpaceObject import SpaceObject
import csdefine
import Const
import KBEngine
from KBEDebug import *
import TongLoader
import Define

from ObjectScript.ObjectScriptFactory import g_objFactory


class SpaceTong( SpaceObject ):
	def __init__( self ):
		SpaceObject.__init__( self )
		self.nagual = None
		
	def tongOnDismiss( self ):
		"""
		define method
		帮会解散
		"""
		self.closeSpace()
		
	def onLeave( self,  playerRole, packArgs ):
		"""
		virtual method
		"""
		SpaceObject.onLeave( self,  playerRole, packArgs )
		if self.getSpaceRoleNum() == 0 and self.tongDBID == 0:				# 有可能GM指令手动传入
			self.closeSpace()
		
	def closeSpace( self ):
		"""
		<define method>
		关闭副本唯一入口，所有关闭副本操作（base或cell）都应该走此接口
		"""
		DEBUG_MSG("Close space(%s)! scriptID:%s."%( self.id, self.scriptID ))
		self.clearCellAppDataBeforeClose()
		
		if len( self._spaceRoles ):
			for roleCell in self._spaceRoles:
				roleCell.gotoBindSpace()
			self.addTimerCallBack( 5, "closeSpace", () )	#5秒后再次关闭
			DEBUG_MSG("Delay close space(%s) reason 1! scriptID:%s."%( self.id, self.scriptID ))
		
		elif len( self._readyEnterRoles ):
			for roleBase in self._readyEnterRoles:
				roleBase.cell.gotoBindSpace()
			self._readyEnterRoles = []
			self.addTimerCallBack( 5, "closeSpace", () )	#5秒后再次关闭
			DEBUG_MSG("Delay close space(%s) reason 2! scriptID:%s."%( self.id, self.scriptID ))
		
		else:
			self.destroySelf()

	def changeTongNagual(self, playerBaseEntityCall, nagualType, scriptID):
		"""
		"""
		position = self.getScript().nagualPosition
		direction = self.getScript().nagualDirection
		nagual = g_objFactory.createEntity(scriptID, self, position, direction, {})
		
		if playerBaseEntityCall.client:
			if nagual:
				self.destroyTongNagual()
				self.nagual = nagual
				playerBaseEntityCall.client.OnChangeNagualCB(True)
				playerBaseEntityCall.onChangeNagualSucceed(nagualType)
			else:
				playerBaseEntityCall.client.OnChangeNagualCB(False)

	def createTongNagual(self, scriptID):
		"""
		"""
		position = self.getScript().nagualPosition
		direction = self.getScript().nagualDirection
		self.nagual = g_objFactory.createEntity(scriptID, self, position, direction, {})

	def destroyTongNagual(self):
		"""
		"""
		if self.nagual:
			self.nagual.destroySelf()
		
	#--------------------------创建宝箱 -----------------------------------
	def createBHDropBox(self, tongDBID, allocation, memberDBIDs, rewardKey, level):
		"""
		创建帮会宝箱
		"""
		self.getScript().createTongDropBox(self, tongDBID, allocation, memberDBIDs, rewardKey, level)
		