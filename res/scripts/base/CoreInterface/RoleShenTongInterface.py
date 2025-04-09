#-*-coding:utf-8-*-
import KBEDebug
import KBEngine
import csdefine
import csstatus

SHENTONG_SKILL_AMOUNT_MAX = 30
SHENTONG_SKILL_TIMES_MAX = 1000

class RoleShenTongInterface:
	"""
	神通技能
	"""
	def __init__(self):
		pass

	def delShenTongQuickBar(self, skillID):
		"""
		define method
		移除快捷栏的幻兽神通技能
		"""
		self.removeShenTongItemBySkillID(skillID)

#----------------------------------------------------------------幻兽神通技能----------------------------------------------------------
	def learnPetShenTongSkill( self, strUid, itemUid, skillID, times, skillIDName ):
		"""
		define method
		学习幻兽神通技能
		"""
		pet = self.petPersistentDatas.get(int(strUid), None)
		if pet == None:
			return
		index = -1
		for i, element in enumerate(pet.petShenTongSKill):
			if list(element.keys())[0] == skillID:
				index = i
				break

		if index == -1 and len(pet.petShenTongSKill) >= SHENTONG_SKILL_AMOUNT_MAX:
			self.statusMessage( csstatus.PET_SHEN_TONG_MAX )
			return

		_times = 0
		if index >= 0:	
			_times = pet.petShenTongSKill[index][skillID]
		if _times >= SHENTONG_SKILL_TIMES_MAX:
			self.statusMessage( csstatus.PET_SHEN_TONG_TIMES_MAX, skillIDName )
			return			
		pet.addShenTongSkill(skillID, times)
		self.cell.onLearnPetShenTongSkill(itemUid)

	def delPetShenTongSkill(self, strUid, skillID):
		"""
		exposed method
		删除幻兽神通技能
		"""
		pet = self.petPersistentDatas.get(int(strUid), None)
		if pet == None:
			return
		pet.removeShenTongSkill(skillID)
		self.removeItemByPetUidAndSkillID(strUid, skillID)

	def onUseShenTongSkill(self, skillID):
		"""
		使用神通技能回调
		"""	
		pet = self.petPersistentDatas.get(self._activePet.uid, None)
		if pet == None:
			return
		index = -1
		for i, element in enumerate(pet.petShenTongSKill):
			if list(element.keys())[0] == skillID:
				index = i
				break
		if index >= 0:
			pet.petShenTongSKill[index][skillID] -= 1
			pet.updatePetEpitomeDatas("petShenTongSKill", pet.petShenTongSKill )
			if pet.petShenTongSKill[index][skillID] <= 0:
				pet.removeShenTongSkill(skillID)
				self.removeItemByPetUidAndSkillID(self._activePet.uid, skillID)



