#-*-coding:utf-8-*-
import KBEDebug
import KBEngine
import csdefine
import csstatus
from ObjectScript.Pet.PetFactory import g_petFactory
from ConfigObject.ShenTongSkillLoader import g_ShenTongSkillLoader


class RoleShenTongInterface:
	"""
	神通技能
	"""
	def __init__(self):
		pass

	#------------------------------精研---------------------------------------
	def CELL_rquestComminution(self, srcEntityID, Suid, ItemUidList ):
		"""	
		<Exposed method>
		神通技能精研
		"""
		item = self.getItemInstByUid(int(Suid))
		if not item.isComminution:  #不可精研
			return
		List = []
		if ItemUidList:
			List = ItemUidList.split("|")
		if len(List) == 0 and  len(List) > 6:
			self.statusMessage(csstatus.SHEN_TONG_NOT_ENOUGH_ITEM)
			return
		for itemUID in List:
			i = self.getItemInstByUid(int(itemUID))
			if i.isHighQuality():
				self.inquireMessage( csstatus.SHEN_TONG_IS_COMMINUTION, [], "onComminution", Suid, ItemUidList )
				return
		self.continueComminution(Suid, ItemUidList)


	def onComminution(self, isComminution, Suid, ItemUidList ):
		"""
		精研
		"""
		if not isComminution:
			return
		self.continueComminution(Suid, ItemUidList)

	def continueComminution(self,  Suid, ItemUidList ):
		"""
		继续精研
		"""
		List = []
		if ItemUidList:
			List = ItemUidList.split("|")
		item = self.getItemInstByUid(int(Suid))
		skill = item.dynamicData["shenTongSkillID"]
		nextSkill = g_ShenTongSkillLoader.getNextShenTongSkill(skill)
		if not nextSkill:
			self.statusMessage(csstatus.SHEN_TONG_HAS_SUCCEED)
			return
		needPotential = g_ShenTongSkillLoader.getShenTongNeedPotential(skill)
		if self.potential < needPotential:
			self.statusMessage(csstatus.SHEN_TONG_NOT_ENOUGH_POTENTIAL)
			return
		needMoney = g_ShenTongSkillLoader.getShenTongNeedMoney(skill)
		if self.money < needMoney:
			self.statusMessage(csstatus.SHEN_TONG_NOT_ENOUGH_MONEY)
			return
		#计算精研经验
		nextLevelExp = g_ShenTongSkillLoader.getShenTongNeedExp(skill)
		allExp = item.dynamicData["preExp"]
		for itemUID in List:
			i = self.getItemInstByUid(int(itemUID))
			allExp += i.comminutionExp
			self.removeItemByAmount( i, 1, csdefine.ITEM_REMOVE_BY_USE )  #消耗精研材料
		if allExp >= nextLevelExp:
			level = item.dynamicData["shenTongLevel"]
			level += 1
			item.updateDynamicData(self, {"shenTongSkillID": nextSkill, "shenTongLevel":level, "preExp": 0})
		else:
			item.updateDynamicData(self, {"preExp": allExp})

		#处理消耗
		self.subPotential( needPotential )
		self.subMoney( needMoney, csdefine.MONEY_SUB_REASON_COMMONUTION_SKILL )
		
#-----------------------------------------------------------------神通技能（新版）----------------------------------------------------------
	def initShenTongSKill(self):
		"""
		玩家初始化神通技能
		"""
		for element in self.shentongSkills:
			self.client.UpdateShenTongSKill(element["skillID"], element["times"], False)

	def learnShenTongSkill( self, skillID, times ):
		"""
		学习神通技能
		"""
		index = -1
		_times = times
		for i, element in enumerate(self.shentongSkills):
			if element["skillID"] ==  skillID:
				index = i
				break
		if index != -1:
			self.shentongSkills[index]["times"] += times
			_times = self.shentongSkills[index]["times"]
		else:
			self.shentongSkills.append( { "skillID":skillID, "times":times } )
		skillIDName = self.getSkill( skillID )._name
		self.statusMessage(csstatus.SHEN_TONG_SKILL_LEARN, skillIDName, times)
		self.client.UpdateShenTongSKill(skillID, _times, True)


	def onUseShenTongSkill(self, skillID):
		"""
		使用神通技能回调
		"""
		index = -1
		for i, element in enumerate(self.shentongSkills):
			if element["skillID"] ==  skillID:
				index = i
				break		

		if index != -1:
			self.shentongSkills[index]["times"] -= 1
			_times = max(0, self.shentongSkills[index]["times"])
			if self.shentongSkills[index]["times"] <= 0:
				del self.shentongSkills[index]
				self.base.delShenTongQuickBar(skillID)
			self.client.UpdateShenTongSKill(skillID, _times, False)		

	def useItemLearnShenTong(self, shenTongSkillID, addTimes, maxTimes, itemUID):
		"""
		使用神通技能道具
		"""		
		for element in self.shentongSkills:
			if element["skillID"] == shenTongSkillID:
				if element["times"] + addTimes > maxTimes:
					remainTimes = maxTimes - element["times"]
					self.inquireMessage( csstatus.SHEN_TONG_TIMES_WILL_FULL, [], "comminutionUseItemLearnShenTong",  shenTongSkillID, remainTimes, itemUID )
					return			
				break
		self.learnShenTongSkill(shenTongSkillID, addTimes)
		item = self.getItemInstByUid(itemUID)
		self.removeItemByAmount( item, 1, csdefine.ITEM_REMOVE_BY_USE )

	def comminutionUseItemLearnShenTong(self, reply, shenTongSkillID, addTimes, itemUID):
		if reply:
			self.learnShenTongSkill(shenTongSkillID, addTimes)
			item = self.getItemInstByUid(itemUID)
			self.removeItemByAmount( item, 1, csdefine.ITEM_REMOVE_BY_USE )

#----------------------------------------------------------------幻兽神通技能----------------------------------------------------------
	def learnPetShenTongSkill( self, srcEntityID, petUid, itemUid ):
		"""
		exposed method
		学习幻兽神通技能
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		item = self.getItemInstByUid(int(itemUid))
		if item.getItemDir("Script") == "ItemLearnShenTong":
			self.statusMessage(csstatus.PET_SHEN_TONG_CANT_LEARN)
			return
		if item.getItemDir("Script") != "ItemPetShenTong":
			self.statusMessage(csstatus.SKILL_UNKNOWN)
			return
		# 幻兽种族判断
		pet = self.petCages.get( int(petUid), None )
		if pet is None:return
		petObject = g_petFactory.getObject( pet.scriptID )
		profession = petObject.getEntityProperty( "profession", 1 )
		if item._profession and profession != item._profession:
			self.statusMessage(csstatus.PET_SHEN_TONG_PROFESSION)
			return			

		skillID = item._shenTongSkillID
		skillIDName = self.getSkill( skillID )._name
		times = item.dynamicData["shentongUseTimes"]
		self.base.learnPetShenTongSkill(petUid, itemUid, skillID, times, skillIDName)

	def onLearnPetShenTongSkill(self, itemUid):
		"""
		学习幻兽神通技能回调
		"""
		item = self.getItemInstByUid(int(itemUid))
		self.removeItemByAmount( item, 1, csdefine.ITEM_REMOVE_BY_USE )


	def delPetShenTongSkill(self, srcEntityID, strUid, skillID):
		"""
		exposed method
		删除幻兽神通技能
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		
		self.base.delPetShenTongSkill(strUid, skillID)

	def onUsePetShenTongSkill(self, skillID):
		"""
		使用神通技能回调
		"""
		self.base.onUseShenTongSkill(skillID)