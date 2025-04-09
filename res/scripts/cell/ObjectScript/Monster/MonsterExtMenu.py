# -*- coding: utf-8 -*-

import KBEngine
import Math
import csdefine
import csstatus
import ObjectScript.Monster.Monster as Monster

# 参数1 菜单条目
class MonsterExtMenu( Monster.Monster ):
	def __init__( self ):
		Monster.Monster.__init__( self )
		self._menuList = []
		
	def initData( self, configData ):
		"""
		初始化数据
		@param configData: dict
		"""
		Monster.Monster.initData( self, configData )
		if configData["Param1"]:
			for i in range( len(configData["Param1"].split("|"))):
				self._menuList.append( i )
			self.setEntityProperty("menuList",self._menuList)

	def onEnterFree( self, selfEntity ):
		"""
		virtual method
		进入自由状态
		"""
		selfEntity.setBootyOwner( None )
		selfEntity.changeDefaultMove()

	def onPlayerSelectMenu(self, selfEntity, player, index):
		""""""
		selfEntity.monsterAITriggerEvent(csdefine.ENTITY_EVENT_COMMAND, (selfEntity.id, selfEntity.scriptID, "Menu_" + str(index)), player)
