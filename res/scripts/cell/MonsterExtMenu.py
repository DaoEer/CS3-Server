# -*- coding: utf-8 -*-

import KBEngine
import Monster
import csdefine
import csstatus
import ItemFactory
import weakref

class MonsterExtMenu( Monster.Monster ):
	"""
	可提供菜单的怪物（可用ItemSpellPosAndDirAssist生成）
	"""
	def __init__( self ):
		Monster.Monster.__init__( self )
		self.owner = None
		self.setMonsterType( csdefine.MONSTER_TYPE_MONSTER_EXT_CALL )
	
	def setSelfEntityFlagExt(self):
		"""
		virtual method
		"""
		self.setEntityFlagExt(csdefine.ENTITY_FLAG_EXT_MONSTER_EXT_MENU)
	
	def setMenu( self, menuList ):
		"""设置 菜单类目"""
		self.menuList = menuList
		if self.ownerID:
			owner = KBEngine.entities.get( self.ownerID )
			if owner and self.spaceID == owner.spaceID:
				owner.clientEntity(self.id).AddMenuList( menuList )
	
	def CELL_onClientReady( self, srcEntityID ):
		"""
		<Expose method>
		玩家客户端Character Actor已经准备好
		"""
		Monster.Monster.CELL_onClientReady( self, srcEntityID )
		player = KBEngine.entities.get( srcEntityID )
		if player and player.playerDBID == self.belongDBID:
			self.ownerID = player.id
			self.owner = player.base
			if self.menuList:
				player.clientEntity(self.id).AddMenuList( self.menuList )
	
	def onPlayerSelectMenu( self, player, index ):
		"""
		玩家选择了
		"""
		if self.ownerID == player.id and index in self.menuList:					# 只有一个玩家才可以选择菜单
			self.getScript().onPlayerSelectMenu(self, player, index)
	
	def getOwnerEntity( self ):
		"""
		"""
		if self.ownerID:
			return KBEngine.entities.get( self.ownerID,None )
		return None