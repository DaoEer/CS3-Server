# -*- coding: utf-8 -*-

import KST
import csstatus
import csdefine
import csconst
import KBEngine
import KBEDebug
import Functions
import PetCage
import ItemFactory
import random, weakref
from PetEpitome import PetBaseEpitome
from PetEpitome import OriginPetEpitome
from ObjectScript.Pet.PetFactory import g_petFactory
from VehiclePetFormulas import formulas
from MsgLogger import g_logger

class RolePetInterface:
	def __init__( self ):
		petCage = PetCage.PetCage()
		for uid, pet in self.petPersistentDatas.items():
			pet.ownerID = self.id
			petCage.add( uid, pet )
		self.cellData["petCages"] = petCage
		
	def initClientData( self ):
		"""
		初始化客户端数据
		"""
		if hasattr(self, "client") and self.client:
			for petDataObj  in self.petPersistentDatas.values(): #更新数据给客户端
				#直接将自定义类型发给客户端 不用toJsonString
				self.client.PetAddData( petDataObj )
		self.cell.initClientPetDataFinish()

	def petReqTeleport( self, petBase ):
		"""
		幻兽请求传送到主人身边
		"""
		self.cell.petReqTeleport( petBase )
		
	# -----------------------------------驯养原兽--------------------------------------------------
	def activePetEnterFence( self, uid ):
		"""
		<define method>
		出战幻兽进入兽栏
		"""
		if self._activePet:
			KBEDebug.ERROR_MSG("must be err!!as pet(%d) is active!"%self._activePet.uid)
			return
		if uid in self.petPersistentDatas:
			petBase = self.petPersistentDatas.pop(uid)
			
			self.cell.onPetEnterFence(uid)
			self.client.CLIENT_OnActivePetEnterFence( str(uid) )
			KBEngine.globalData["SpaceLunHuiMiJinMgr"].activePetEnterFence( self.databaseID, petBase )
			
	def exChangePetFromFence( self, enterUID, leaveUID ):
		"""
		<define method>
		出战幻兽 和 兽栏里的幻兽交换位置
		"""
		if enterUID in self.petPersistentDatas:
			petBase = self.petPersistentDatas.pop(enterUID)
			
			self.cell.onPetEnterFence(enterUID)
			self.client.CLIENT_OnExChangePetFromFence( str(enterUID), str(leaveUID) )
			KBEngine.globalData["SpaceLunHuiMiJinMgr"].exChangePetFromFence( self, self.databaseID, petBase, leaveUID )
		
	def petOutsideFromFence( self, pet ):
		"""
		<define method>
		幻兽出栏，并召唤到玩家身边
		"""
		if pet:
			self.petPersistentDatas[pet.uid] = pet
			self.cell.onPetOutsideFromFence(pet)
		else:
			KBEDebug.ERROR_MSG("player(%d) OriginPetEpitome is None,can not join petPersistentDatas"%self.id)

	def onGenerateOriginPet( self, itemID ):
		"""原兽入栏"""
		item = ItemFactory.ItemFactoryInst.createDynamicItem( itemID )
		scriptID, eggQuality, abilityRoll = item.getOriginPetData()
		KBEngine.globalData["SpaceLunHuiMiJinMgr"].generateOriginPet( self, self.databaseID, scriptID, abilityRoll, eggQuality, self.camp )
	# -----------------------------------孵化幻兽--------------------------------------------------
	def generatePet( self, scriptID, quality, solution ):
		"""
		<define method>
		孵化幻兽蛋
		"""
		pet = PetBaseEpitome()
		pet.ownerID = self.id
		pet.generatePetAttr( scriptID, quality, solution, self.camp )
		self.petPersistentDatas[ pet.uid ] =  pet
		self.cell.onGeneratePetResult( pet )
		self.statusMessage( csstatus.PET_HATCH_SUCCESS, pet.getName() )
		#直接将自定义类型发给客户端 不用toJsonString
		self.client.OnGeneratePet( pet )
		g_logger.petAddLog( self.databaseID, self.getName(), pet.name, pet.uname, pet.uid, pet.quality, pet.level, csdefine.PET_ADD_REASON_COMPLETE_QUEST, pet )

	def generateSealPet( self, pet ):
		"""
		<define method>
		孵化封印幻兽蛋
		"""
		pet.ownerID = self.id
		self.petPersistentDatas[ pet.uid ] =  pet
		self.cell.onGenerateSealPetResult( pet )
		self.statusMessage( csstatus.PET_HATCH_SUCCESS, pet.getName() )
		self.client.OnGeneratePet( pet )
	
	# -----------------------------------召唤幻兽--------------------------------------------------

	def conjurePet( self, uid, position, direction ):
		"""
		<define method>
		召唤幻兽
		"""
		if self._activePet:
			KBEDebug.ERROR_MSG( "role[%d]:why has active pet[%d:%d]?must be err!" %(self.id, uid, self._activePet.id))
			return
			
		petDataObject = self.petPersistentDatas.get( uid )
		petDict = petDataObject.getDictForPetCreate()
		petDict.update( {"position":position, "direction":direction, "camp":self.camp} )
		
		petObjectScript = g_petFactory.getObject( petDataObject.scriptID )
		if petObjectScript is None:
			KBEDebug.ERROR_MSG("can not find pet ObjectScript(%s)"%petDataObject.scriptID)
			return
			
		petEntity = petObjectScript.createLocalEntity( petDict )
		if petEntity:
			self._activePet = weakref.proxy(petEntity)
			petEntity.initialization( self )
			self.cell.onConjurePetResult( uid, petEntity )
			
			if hasattr(self, "client") and self.client:
				self.client.onConjurePetResult( str(uid), petEntity.id )
	

	def getActivePet( self ):
		"""
		获取当前幻兽
		"""
		return self._activePet
	# -----------------------------------骑乘幻兽--------------------------------------------------
	def mountPet( self ):
		"""
		<define method>
		上马
		"""
		if self._activePet:
			self.withdrawPet( csdefine.PET_WITHDRAW_MOUNT_PET )
		else:
			KBEDebug.ERROR_MSG("active pet is None??something err!")
			
	def onMountPet( self, uid, writeToDBDatas ):
		""""""
		pet = self.petPersistentDatas.get(uid, None)
		if pet:
			pet.updateDBDatas( writeToDBDatas )
		self.cell.onMountPetResult()
		
	def dismountPet( self, position, direction ):
		"""
		<define method>
		下马
		"""
		if self._activePet:
			self._activePet.cellData["position"] = position
			self._activePet.cellData["direction"] = direction
			self._activePet.initialization( self )
			self.cell.onDismountPetResult()
		else:
			KBEDebug.ERROR_MSG("active pet is None??something err!")
	# -----------------------------------回收幻兽--------------------------------------------------
	def withdrawPet( self, reason ):
		"""
		<define method>
		回收幻兽
		"""
		if self._activePet and self._activePet.isDestroyed == False:
			self._activePet.withdraw( reason )
			
			if reason == csdefine.PET_WITHDRAW_DEATH:
				uid = self._activePet.uid
				pet = self.petPersistentDatas.get(uid, None)
				if pet:
					pet.withdrawPetByDead()
			
	def onWithdrawPet( self, uid, reason, writeToDBDatas ):
		"""
		回收幻兽回调
		"""
		pet = self.petPersistentDatas.get(uid, None)				# 因为幻兽不保存数据库，只能下线的时候保存到玩家身上
		if pet:
			pet.updateDBDatas( writeToDBDatas )
			
		self._activePet = None
		self.cell.onWithdrawPetResult( reason )
		if self.client:									# 玩家下线回收幻兽，客户端已失去
			self.client.onWithdrawPetResult()
			
	def savePetVolatileAttr(self, HP, MP, exp):
		"""
		define method
		玩家销毁之前，优先保存幻兽数据
		"""
		uid = self._activePet.uid
		pet = self.petPersistentDatas.get(uid, None)
		if pet:
			datas = {}
			datas["HP"] = HP
			datas["MP"] = MP
			datas["exp"] = exp
			pet.updateDBDatas( datas )
	# -----------------------------------放生幻兽--------------------------------------------------
	def freePet( self, uid ):
		"""
		<define method>
		"""
		pet = self.petPersistentDatas.pop( uid )
		self.cell.onFreePetResult( uid )
		self.client.PetRemoveData( str(uid) )
		self.statusMessage( csstatus.PET_FREE_IS_SUCCESS, pet.getName() )
		g_logger.petDelLog( self.databaseID, self.getName(), pet.name, pet.uname, pet.uid, pet.quality, pet.level, csdefine.PET_REMOVE_REASON_FREE, pet )
		
	# -----------------------------------封印幻兽--------------------------------------------------
	def sealPet( self, uid, amount ):
		"""
		define method
		封印幻兽
		"""
		pet = self.petPersistentDatas.pop( uid )
		self.cell.onSealPetResult( pet )
		self.client.PetRemoveData( str(uid) )
		self.client.OnSealSuccess()
		g_logger.petSealLog( self.databaseID, self.getName(), pet.name, pet.uname, pet.uid, pet.quality, pet.level, amount, pet )

	# -----------------------------------合成幻兽----------------------------------------------------
	def composePet(self, main_uid, second_uid, isUseMatertial ):
		"""
		define method
		合成幻兽
		"""
		main_pet = self.petPersistentDatas.get(main_uid, None)
		second_pet = self.petPersistentDatas.get(second_uid, None)
		beforeAbility = main_pet.ability
		#成长度
		ability_Max = main_pet.ability_Max if main_pet.ability_Max > second_pet.ability_Max else second_pet.ability_Max
		main_pet.setAbilityMax( ability_Max )
		srcAbility = main_pet.ability
		upper_ability = main_pet.ability if main_pet.ability >= second_pet.ability else second_pet.ability
		ability_low = int((upper_ability*95)/100)
		ability_high = int((upper_ability*110)/100) if int((upper_ability*110)/100) <= main_pet.ability_Max else main_pet.ability_Max
		ability = random.randint( ability_low, ability_high)
		main_pet.setAbility( ability )
		#被动技能
		templist = []
		templist.extend( main_pet.passiveSkillBox )
		templist.extend( second_pet.passiveSkillBox )
		passiveSkills = sorted(set(templist),key = templist.index)
		old_amount = len(main_pet.passiveSkillBox)
		rNumber = random.randint(1, 100)
		if rNumber <= 75:
			passiveSkill_amount = old_amount
		else:
			passiveSkill_amount = random.randint( old_amount, len(passiveSkills) )
			
		passiveSkillBox = random.sample( passiveSkills, passiveSkill_amount )
		
		main_pet.passiveSkillBox = passiveSkillBox
		main_pet.calProperties()
		for i in main_pet._propertiesDict:
			main_pet.updatePetEpitomeDatas(i,main_pet._propertiesDict[i])
		main_pet.updatePetEpitomeDatas("passiveSkillBox", passiveSkillBox )

		self.cell.onComposePetResult( main_uid, second_uid, isUseMatertial )
		self.petPersistentDatas.pop( second_uid )
		self.client.PetRemoveData( str(second_uid) )
		self.client.OnComposePet( str(main_uid), srcAbility )
		g_logger.petComposeLog( self.databaseID, self.getName(), main_pet.name, main_pet.uname, main_pet.uid, main_pet.quality, main_pet.level,\
			second_pet.name, second_pet.uname, second_pet.uid, second_pet.quality, second_pet.level, main_pet.ability, beforeAbility, \
			formulas.getComposeMoney( main_pet.quality ), 0, formulas.getComposeMaterials( main_pet.quality ), main_pet )

	def onComposeCostGold( self, gold ):
		"""
		define method
		合成幻兽 消耗元宝
		"""
		self.payShiTou( gold, csdefine.CHANGE_XIANSHI_PETCOMPOSE )

	# -----------------------------------幻兽打书------------------------------------------------------
	def replacePetSkill( self, uid, SkillID, SkillBookID, replaceSKillID ):
		"""
		替换主动技能
		"""
		pet = self.petPersistentDatas.get(uid, None)
		if SkillID == 0 and len(pet.attrSkillBox) >= csconst.PET_SKILL_CAGES[pet.quality]:
			return
		pet.setAttrSkillBox( SkillID, "sub" )
		pet.setAttrSkillBox( replaceSKillID, "add" )
		self.cell.onReplacePetSkillResult( SkillBookID, replaceSKillID )
		self.client.OnReplacePetSkill()
		g_logger.petReplaceActiveSkillLog( self.databaseID, self.getName(), pet.name, pet.uname, pet.uid, pet.quality, pet.level, replaceSKillID, SkillID, len(pet.attrSkillBox), pet, SkillBookID, 0, 0 )

	def upgradePetSkill( self, uid, skillID, nextSkillID, Potential ):
		"""
		升级主动技能
		"""
		pet = self.petPersistentDatas.get(uid, None)
		pet.setAttrSkillBox( skillID, "sub" )
		pet.setAttrSkillBox( nextSkillID, "add" )
		self.cell.onUpgradePetSkillResult( nextSkillID )
		self.client.OnUpgradePetSkill( 0, 1 )			# 0表示不发消息，1表示成功
		g_logger.petUpgradeActiveSkillLog( self.databaseID, self.getName(), pet.name, pet.uname, pet.uid, pet.quality, pet.level, nextSkillID, skillID, Potential, 0, pet )

	def replacePetPassiveSkill( self, uid, skillID, SkillBookID, replaceSkillID ):
		"""
		替换被动技能
		"""
		pet = self.petPersistentDatas.get(uid, None)
		if skillID == 0 and len(pet.passiveSkillBox) >= csconst.PET_SKILL_CAGES[pet.quality]:
			return
		pet.setPassiveSkill( skillID,"sub" )
		pet.setPassiveSkill( replaceSkillID,"add" )
		self.cell.onReplacePetPassiveSkillResult( SkillBookID, replaceSkillID )
		self.client.OnReplacePetPassiveSkill()
		g_logger.petReplacePassiveSkillLog( self.databaseID, self.getName(), pet.name, pet.uname, pet.uid, pet.quality, pet.level, replaceSkillID, skillID, len(pet.passiveSkillBox), pet, SkillBookID, 0, 0 )

	def upgradePetPassiveSkill( self, uid, skillID, money, nextSkillID ):
		"""
		升级被动技能
		"""
		pet = self.petPersistentDatas.get(uid, None)
		pet.setPassiveSkill( skillID,"sub" )
		pet.setPassiveSkill( nextSkillID,"add" )
		self.cell.onUpgradePetPassiveSkillResult( nextSkillID )
		self.client.OnUpgradePetPassiveSkill( 0, 1 )		# 0表示不发消息，1表示成功
		g_logger.petUpgradePassiveSkillLog( self.databaseID, self.getName(), pet.name, pet.uname, pet.uid, pet.quality, pet.level, nextSkillID, skillID, 0, money, 1, 1, pet )

	# -----------------------------------幻兽 其他功能--------------------------------------------------
	def setPetStep( self, uid, step ):
		"""
		define method
		幻兽升介
		"""
		pet = self.petPersistentDatas[uid]
		pet.setStep( step )
		needExp = formulas.getNeedExpNextStep( step, pet.quality )
		g_logger.petUpStepLog( self.databaseID, self.getName(), pet.name, pet.uname, pet.uid, pet.quality, pet.level, pet.step-1, pet.step, needExp, pet )
		
	def onActivateCageCostGold( self, gold ):
		"""
		define method
		激活幻兽栏 消耗元宝
		"""
		result = self.payShiTou( gold, csdefine.CHANGE_XIANSHI_PETCAGES )
		self.cell.activateCageResult( result )
		
	def reName( self, UIDStr, name ):
		"""
		exposed method
		幻兽改名
		"""
		if self._activePet and self._activePet.uid == int(UIDStr):
			self.client.OnPetReNameFail( UIDStr, csstatus.PET_BATTLE_UNABLE_RENAME )
			return
		nameLength = 0                   # 名字长度
		for a in name:
			if len(a.encode("utf8")) == 1:
				nameLength += 1
			else:
				nameLength += 2          # 汉字有2个字节
		uid = int(UIDStr)

		if nameLength < 4 or nameLength > 14:
			self.client.OnPetReNameFail( UIDStr , csstatus.PET_NAME_LONG_NO_SUITABLE )
			return
		if name == self.getName():
			self.client.OnPetReNameFail( UIDStr , csstatus.PET_NAME_THE_SAME_TO_ROLE_NAME )
			return

		pet = self.petPersistentDatas.get(uid,None)
		if pet:
			pet.reName( name )
			self.statusMessage( csstatus.PET_MODIFY_NAME_SUCCESS )
		else:
			KBEDebug.ERROR_MSG("can not get PetEpitome(uid = %d)"%uid)
		
	# ----------------------------------------------------------------
	# callbacks of engine
	# ----------------------------------------------------------------
	def onLoseCell( self ) :
		"""
		when my cell entity has lost, it will be called by engine
		"""
		self.withdrawPet( csdefine.PET_WITHDRAW_OFFLINE )

	def addRolePetProtect( self ):
		"""
		添加幻兽保护
		"""
		activePetMB =  self.getActivePet()
		if activePetMB and activePetMB.cell:
			activePetMB.cell.addVehicePetProtect()

	def removeRolePetProtect( self ):
		"""
		移除幻兽保护
		"""
		activePetMB =  self.getActivePet()
		if activePetMB and activePetMB.cell:
			activePetMB.cell.removeVehicePetProtect()

	def removePetSleeptime( self ):
		"""
		移除幻兽休眠时间
		"""
		for petDataObj  in self.petPersistentDatas.values():
			petDataObj.updatePetEpitomeDatas( "sleepTime", 0 )

	def delPetShenTongQuickBar(self, petUid):
		"""
		define method
		移除快捷栏的幻兽神通技能
		"""
		self.removeItemByPetUid(petUid)
		