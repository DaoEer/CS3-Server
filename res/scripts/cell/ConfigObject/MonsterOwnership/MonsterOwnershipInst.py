# -*- coding: utf-8 -*-

import Singleton
from ConfigObject.MonsterOwnership.MonsterOwnershipFirstDamage import MonsterOwnershipFirstDamage
from ConfigObject.MonsterOwnership.MonsterOwnershipShare import MonsterOwnershipShare
from ConfigObject.MonsterOwnership.MonsterOwnershipNeverChange import MonsterOwnershipNeverChange

import Define


OWNERSHIP_DICT = {
	Define.MONSTER_OWNER_FIRST_DAMAGE:MonsterOwnershipFirstDamage,
	Define.MONSTER_OWNER_SHARE:MonsterOwnershipShare,
	Define.MONSTER_OWNER_NEVER_CHANGE:MonsterOwnershipNeverChange
}

class MonsterOwnershipInst(Singleton.Singleton, dict):
	"""
	"""
	def __init__(self):
		self.registObject()

	def registObject(self):
		"""
		"""
		for ownership, ownershipObj in OWNERSHIP_DICT.items():
			self[ownership] = ownershipObj(ownership)

	def getObject(self, ownership):
		return self.get(ownership, None)


g_MonsterOwnershipInst = MonsterOwnershipInst()