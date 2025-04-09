# -*-coding:utf-8 -*-


#怪物归属权见者有份类型
import csdefine
import KBEngine
import ConfigObject.MonsterOwnership.MonsterOwnershipBase as MonsterOwnershipBase

class MonsterOwnershipShare(MonsterOwnershipBase.MonsterOwnershipBase):
	"""
	"""
	def __init__(self, ownership):
		MonsterOwnershipBase.MonsterOwnershipBase.__init__(self, ownership)


	def canAddOwnerCheck(self, monsterEntity, ownerEntity):
		"""
		"""
		if monsterEntity.bootyOwnerTypeObj is None:
			return True
		
		#判断当前玩家或者玩家队伍是否已经拥有归属权 如果已经有了返回False
		if ownerEntity.isInTeam():
			if monsterEntity.bootyOwnerTypeObj.ownnerID == ownerEntity.teamMailbox.id:
				return False
		else:
			if monsterEntity.bootyOwnerTypeObj.ownnerID == ownerEntity.id:
				return False
		return True

	#移除归属者
	def onRemoveEnemy(self, monsterEntity, ownerEntityID):
		"""
		"""
		#如果怪物敌人列表为空，清空所有的归属者
		if not monsterEntity.enemyList:
			monsterEntity.bootyOwnerTypeObj = None
			return
			
		if monsterEntity.bootyOwnerTypeObj is None:
			return

		entity = KBEngine.entities.get(ownerEntityID, None)
		#如果entity不存在了,需要monster去检查一下 归属权的有效性
		if not entity:
			isClear = True
			obj = monsterEntity.bootyOwnerTypeObj
			ownerIDs = obj.getOwnerIDs(monsterEntity).keys()

			for oid in ownerIDs:
				if oid in monsterEntity.enemyList.keys():
					isClear = False
					break
			
			#移除归属权
			if isClear:
				monsterEntity.bootyOwnerTypeObj = None

		else:
			if entity.getEntityFlag()!=csdefine.ENTITY_FLAG_ROLE:
				return

			if entity.isInTeam():
				if monsterEntity.bootyOwnerTypeObj.ownnerID != entity.teamMailbox.id:
					return
			else:
				if monsterEntity.bootyOwnerTypeObj.ownnerID != entity.id:
					return
			
			ownerIDs = monsterEntity.bootyOwnerTypeObj.getOwnerIDs(monsterEntity).keys()
			isClear = True
			for oid in ownerIDs:
				if oid in monsterEntity.enemyList:
					isClear = False
					break
			
			if isClear:
				monsterEntity.bootyOwnerTypeObj = None