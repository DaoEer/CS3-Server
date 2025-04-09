# -*- coding: utf-8 -*-
import csdefine
import ConfigObject.Item.ItemUse as ItemUse
from ConfigObject.Quest.QuestBase.QuestLoader import g_QuestLoader
import Const

class ItemActMQRSG( ItemUse.ItemUse ):
	"""
	冥气人参果
	"""
	def __init__(self, srcData):
		ItemUse.ItemUse.__init__(self, srcData)

	def use(self, owner, target):
		ItemUse.ItemUse.use(self, owner, target)
		if not target:
			target = owner
		owner.useSkillToEntity( self.skillID, owner.id  )
		if owner.getClient():
			owner.client.OnEnterAimingMode()
