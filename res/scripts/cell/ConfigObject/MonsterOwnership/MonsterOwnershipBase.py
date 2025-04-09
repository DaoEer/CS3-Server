# -*-coding:utf-8 -*-


#怪物归属权类型基类

class MonsterOwnershipBase:
	"""
	"""
	def __init__(self, ownership):
		"""
		"""
		self.ownership = ownership

	def canAddOwnerCheck(self, monsterEntity, ownerEntity):
		"""
		"""
		return True
