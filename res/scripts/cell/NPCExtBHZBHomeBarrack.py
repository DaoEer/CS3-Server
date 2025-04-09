# -*- coding: utf-8 -*-
#
import KBEngine
import NPC
import csdefine

class NPCExtBHZBHomeBarrack(NPC.NPC):
	"""
	帮会争霸大本营
	"""
	def __init__(self):
		NPC.NPC.__init__( self )
		spaceEntity = self.getCurrentSpace()
		if spaceEntity and spaceEntity.getScript().getSpaceChildType() == csdefine.SPACE_TYPE_CHILD_BHZB_STAND_MAP:
			spaceEntity.addNpcHomeBarracksEntitys( self )
	
	def setBelongTongDBID( self, belongTongDBID ):
		"""
		设置归属帮会
		"""
		self.belongTongDBID = belongTongDBID

	def getBelongTongDBID( self ):
		"""
		"""
		return self.belongTongDBID

	def beforeDestroy( self ):
		"""
		virtual method
		销毁前做一些事
		"""
		NPC.NPC.beforeDestroy( self )
		spaceEntity = self.getCurrentSpace()
		if spaceEntity and spaceEntity.getScript().getSpaceChildType() == csdefine.SPACE_TYPE_CHILD_BHZB_STAND_MAP:
			spaceEntity.removeNpcHomeBarracksEntitys( self )