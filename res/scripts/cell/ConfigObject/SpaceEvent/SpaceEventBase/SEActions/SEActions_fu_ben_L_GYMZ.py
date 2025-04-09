# -*- coding: utf-8 -*-

# 副本事件行为
import random
import Math
import KBEMath
import KBEDebug
import KBEngine
import Functions
import csarithmetic
from ConfigObject.SpaceEvent.SpaceEventBase.SEActions.SEActionBase import SEActionBase

class SEAction193( SEActionBase ):
	"""
	鬼域迷阵：副本初始化随机刷出传送门
	"""
	def init ( self, section ):
		SEActionBase.init( self, section )
		
	def do( self, spaceEntity, triggerID, eventParams ):
		if spaceEntity:
			spaceEntity.initCreatePortal()

class SEAction226( SEActionBase ):
	"""
	鬼域迷阵：显示地图界面
	"""
	def init ( self, section ):
		SEActionBase.init( self, section )
		
	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		spaceEntity.displayLocationAndColor()

class SEAction228( SEActionBase ):
	"""
	鬼域迷阵：显示地图界面
	"""
	def init ( self, section ):
		SEActionBase.init( self, section )
		
	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		for playerCell in spaceEntity._spaceRoles:
			playerCell.client.ClIENT_ClearLocationAndColor()


SEActionBase.setActionClass("SEAction193", SEAction193)
SEActionBase.setActionClass( "SEAction226",SEAction226 )
SEActionBase.setActionClass( "SEAction228",SEAction228 )