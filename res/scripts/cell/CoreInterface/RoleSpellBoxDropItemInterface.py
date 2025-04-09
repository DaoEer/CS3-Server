
# -*- coding: utf-8 -*-
import KBEngine
import KBEDebug
import csdefine

class RoleSpellBoxDropItemInterface:
	"""
	玩家SpellBox拾取物品接口
	"""
	def __init__( self ):
		"""
		初始化
		"""
		pass
		
	def notifySpellBoxInteractiveOver( self, srcEntityID, spellBoxEntityID ):
		"""
		通知箱子交互完毕
		"""
		if not self.validateClientCall( srcEntityID ):
			return
	
		self.clearInteractiveSpellBox()

	def pickUpSpellBoxItem( self, srcEntityID, spellBoxEntityID, itemUIDs ):
		"""
		拾取箱子中的物品
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		
		spellBoxEntity = KBEngine.entities.get( spellBoxEntityID,None )
		if not spellBoxEntity:
			return

		spellBoxEntity.pickUpItem( self, itemUIDs )

	def CELL_pickUpSpellBoxToMember(self, srcEntityID, spellBoxEntityID, uid, dstEntityID):
		"""
		Exposed method
		分配箱子中的物品给成员
		"""
		if not self.validateClientCall(srcEntityID):
			return
		
		spellBoxEntity = KBEngine.entities.get(spellBoxEntityID,None)
		if not spellBoxEntity:
			return

		spellBoxEntity.pickUpSpellBoxToMember(self, uid, dstEntityID)
		
	def setInteractiveSpellBox( self, spellBoxEntity ):
		"""
		设置正在SpellBoxPickItem交互的ID
		"""
		self.interactSpellBoxID = spellBoxEntity.id
		self.otherClients.RefreshAroundBoxStatus(csdefine.SPELL_BOX_LISTEN_EVENT_ROLE_IS_INTERACT)
		#spellBoxEntity.allClients.CLIENT_RefreshBoxStatus()

	def clearInteractiveSpellBox( self ):
		"""
		清除交互SpellBoxPickItem ID
		"""
		spellBoxEntity = KBEngine.entities.get( self.interactSpellBoxID,None )
		if spellBoxEntity:
			spellBoxEntity.notifySpellBoxInteractiveOver(self.id)
			spellBoxEntity.allClients.CLIENT_RefreshBoxStatus()
		self.interactSpellBoxID = 0

	def getInteractiveSpellBox( self ):
		"""
		是否有正在交互的箱子
		"""
		return self.interactSpellBoxID

	def beforeDestroy( self ):
		"""
		virtual method
		销毁前做一些事
		"""
		self.clearInteractiveSpellBox()
