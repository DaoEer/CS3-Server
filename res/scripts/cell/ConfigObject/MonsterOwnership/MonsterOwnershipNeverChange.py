# -*-coding:utf-8 -*-


#怪物归属权固定不变类型

import ConfigObject.MonsterOwnership.MonsterOwnershipBase as MonsterOwnershipBase

class MonsterOwnershipNeverChange(MonsterOwnershipBase.MonsterOwnershipBase):
	"""
	"""
	def __init__(self, ownership):
		MonsterOwnershipBase.MonsterOwnershipBase.__init__(self, ownership)


	def canAddOwnerCheck(self, monsterEntity, ownerEntity):
		"""
		"""
		return False

	#移除归属者
	def onRemoveEnemy(self, monsterEntity, ownerEntityID):
		"""
		"""
		return