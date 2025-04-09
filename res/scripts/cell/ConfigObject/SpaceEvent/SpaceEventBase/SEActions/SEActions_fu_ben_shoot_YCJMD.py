# -*- coding: utf-8 -*-

# 副本事件行为:勇闯绝命岛
import random
import math
import Math
import KBEMath
import KBEDebug
import KBEngine
import Functions
import csarithmetic
import csdefine
from ConfigObject.SpaceEvent.SpaceEventBase.SEActions.SEActionBase import SEActionBase


class SEAction403( SEActionBase ):
	"""
	CCST-9020 副本里所有玩家恢复能量
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self._itemID = int(section["param1"])
		self._amount = 1
		if section["param2"]:
			self._amount = int(section["param2"])
		self._amount_max = 10
		if section["param3"]:
			self._amount_max = int(section["param3"])

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		for p in spaceEntity._spaceRoles:
			amount = p.calcItemListAmount(p.getItemInstsByID(self._itemID))
			if amount < self._amount_max and p.unLockSpaceCopyGridNum > 0:
				p.addItemByID( self._itemID, self._amount )

class SEAction404( SEActionBase ):
	"""
	CCST-9020 玩家显示/关闭灵能
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self._isshow = bool(int(section["param1"]))

	def do( self, spaceEntity, triggerID, eventParams ):
		trigger = KBEngine.entities.get( triggerID )
		if not trigger or trigger.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
			return
		trigger.client.ShowShootYCJMDLNUI(self._isshow)

class SEAction461( SEActionBase ):
	"""
	CST-12221 修改玩家子弹槽的最大数量
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self._bulletID = 302010080
		if section["param1"]:
			self._bulletID = int(section["param1"])

	def do( self, spaceEntity, triggerID, eventParams ):
		trigger = KBEngine.entities.get( triggerID )
		if not trigger or trigger.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
			return
		trigger.client.SetYCJMDBulletSlotMax(self._bulletID)



SEActionBase.setActionClass( "SEAction403",SEAction403 )
SEActionBase.setActionClass( "SEAction404",SEAction404 )
SEActionBase.setActionClass( "SEAction461",SEAction461 )