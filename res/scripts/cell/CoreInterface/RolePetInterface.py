# -*- coding: utf-8 -*-
import random
import ItemTypeEnum
import csdefine
import csstatus
import csconst
import Const
import copy
import time
import math
import Math
import random
import KBEngine
import KBEDebug
import Functions
from ItemFactory import ItemFactoryInst as g_itemFactory
from ObjectScript.Pet.PetFactory import g_petFactory
from ObjectScript.ObjectScriptFactory import g_objFactory
from VehiclePetFormulas import formulas
from PetSkillLearnLoader import g_PetSkillLearn
from MsgLogger import g_logger
import PetExtraHPMPSlotCfg

class RolePetInterface:
	"""
	角色幻兽接口
	"""
	def __init__(self):
		pass
		
	def initClientPetDataFinish( self ):
		"""
		define method
		初始化完客户端数据
		"""
		# 读取配置初始化幻兽额外血槽和蓝槽的最大值
		self.onSetPetSlotValue()

		if self._activePetUID:
			self.base.conjurePet( self._activePetUID, self.position + ( random.randint( -2, 2 ), 0,  random.randint( -2, 2  ) ), self.direction )

		if self.getClient():
			#通知客户端，数据初始化完毕
			self.client.initClientPetDataFinish()
			
	def beforeDestroy( self ):
		""""""
		# 走正常流程，保存不了幻兽的数据。要预先保存
		cellPet = self.getActivePetCell()
		if cellPet:
			self.base.savePetVolatileAttr(cellPet.HP, cellPet.MP, cellPet.exp)
	
	def onEnterDead( self ):
		"""玩家死亡回调"""
		self.base.withdrawPet( csdefine.PET_WITHDRAW_OWNER_DEATH )
	
	def onAddEnemy( self, enemyID ):
		"""
		加敌人列表
		"""
		petEntity = self.getActivePetCell()
		if petEntity:
			petEntity.onOwnerAddEnemy( enemyID  ) #通知宠物
			
	def onEnterSpaceNotify( self, packArgs ):
		if self._activePetBase:
			self.petReqTeleport( self._activePetBase )
	
	def petReqTeleport( self, petBase ):
		"""
		define method
		宠物请求传送到主人身边
		"""
		petBase.cell.onTeleportToOwner( self.getCurrentSpace(), self.position )
			
	def onTeleportCompleted( self ):
		""""""
		self.conjurePetByWithdraw()
	
	def updatePetAttrInCage( self, uid ):
		"""
		<define method>
		更新幻兽笼子数据
		"""
		pass
		
	def updatePetEpitomeDatas( self, UID, attrName, value ):
		"""
		define method
		幻兽属性自动更新
		"""
		pet = self.petCages.get(UID, None)
		if pet:
			pet.updateAttr( attrName, value )
	
	def petCageIsFull( self ):
		"""幻兽栏是否已满"""
		return self.petCageMax <= len( self.petCages )
	
	def getActivePetCell( self ):
		"""
		获取当前出战的宠物对象
		"""
		if self._activePetBase:
			return KBEngine.entities.get( self._activePetBase.id )
		return None
		
	def getRightPos( self ):
		yaw = self.direction.z + math.pi / 2
		pos = Math.Vector3( math.sin(yaw), 0, math.cos(yaw) ) * Const.PET_DIST_ROLE
		return self.position + pos
# -----------------------------------锁定幻兽--------------------------------------------------
# 需要远程操作的都必须锁定操作，在回调的结果解锁
# ---------------------------------------------------------------------------------------------
	def lockPetOperation(self):
		"""
		锁定操作，该锁定操作是为了防止某个操作还没从 base 或别的 cell 返回时，
		另一个操作又出现这样将会造成某些物品或金钱的数量本来只允许操作一次的，
		但两次操作都通过了
		"""
		if time.time() - self._operateTime < 2.0:
			self.statusMessage(csstatus.GB_OPERATE_FREQUENTLY)
			return False

		self._operateTime = time.time()
		return True

	def unlockPetOperation(self):
		"""解锁宠物操作"""
		self._operateTime = 0.0
# -----------------------------------孵化幻兽--------------------------------------------------
	def generatePet( self, scriptID, quality, solution ):
		"""生成幻兽"""
		petObject = g_petFactory.getObject( scriptID )
		if petObject is None:
			KBEDebug.ERROR_MSG("pet object cannot find by scriptID(%s)"%scriptID)
			return
		if self.lockPetOperation():
			self.base.generatePet( scriptID, quality, solution )
	
	def onGeneratePetResult( self, pet  ):
		"""
		<define method>
		生成结果
		"""
		self.petCages.add( pet.uid, pet )
		self.unlockPetOperation()
		
		#添加日志
		#g_logger.petAddLog( roleDBID, roleName, petName, petUname, petUid, petQuality, petLevel, reason ,pet)

	def generateSealPet(self):
		"""封印蛋生成幻兽"""
		usingItemUid = self.getUsingItem()
		item = self.getItemInstByUid(usingItemUid)
		if self.lockPetOperation():
			self.base.generateSealPet( item.dynamicData["pet"] )
		
	def onGenerateSealPetResult( self, pet  ):
		"""
		<define method>
		生成结果
		"""
		self.petCages.add( pet.uid, pet )
		self.unlockPetOperation()

	def GetSealPetEggAttr(self, srcEntityID, itemUidstr):
		"""
		<Exposed method>
		客户端请求获得封印幻兽属性信息
		"""
		if not self.validateClientCall( srcEntityID ):
			return

		itemUid = int(itemUidstr)
		item = self.getItemInstByUid(itemUid)
		pet = item.dynamicData["pet"]
		self.client.OnGetSealPetEggAttr( pet )

# -----------------------------------召唤幻兽--------------------------------------------------
	def conjurePet( self, srcEntityID, UIDstr ):
		"""
		<Exposed method>
		召唤幻兽
		"""
		if self.id != srcEntityID:return
		self.triggerSkillEvent(csdefine.SKILL_EVENT_REQUEST_ACTION, self.id, {"requestType" : csdefine.SKILL_EVENT_ACTION_TYPE_PET})
		if not UIDstr.isdigit():return
		
		UID = int( UIDstr )
		if UID not in self.petCages:return
		if UID == self._activePetUID:return
		
		result = self.canConjurePet( UID )
		if result == csstatus.SKILL_GO_ON:
			if self._activePetUID and self._activePetUID != UID:				# 如果已经召唤了幻兽，并且不是当前召唤的幻兽。先回收当前幻兽
				self._conjurePetUID = UID
				self.base.withdrawPet( csdefine.PET_WITHDRAW_CONJURE )
				return
			if self.lockPetOperation():
				self.base.conjurePet( UID, self.position, self.direction )
		else:
			self.statusMessage(result)
			
	def conjurePetByWithdraw( self ):
		"""召唤回收的幻兽"""
		uid = self.queryTemp( "withdrawPetUID" )
		if uid:
			self.actCounterDec( csdefine.ACTION_FORBID_CONJURE_PET )
			self.conjurePet( self.id, str(uid) )
			self.removeTemp( "withdrawPetUID" )
			
	def isActivePet( self, UID ):
		"""是否是出战幻兽"""
		return UID and self._activePetUID == UID
	
	def canConjurePet( self, UID ):
		"""能否召唤幻兽"""
		if self.actionForbidSign( csdefine.ACTION_FORBID_CONJURE_PET ):
			return csstatus.PET_CANNOT_HATCH_AS_STATE
		
		pet = self.petCages[UID]
		if pet.isSleepTime():
			return csstatus.PET_IS_IN_DORMANT_CANOT_CONJURE
			
		petObject = g_petFactory.getObject( pet.scriptID )
		takeLevel = petObject.getEntityProperty( "takeLevel", 0 )
		if self.level < takeLevel:
			return csstatus.PET_TAKE_LEVEL_NO_ENOUGH
		
		return csstatus.SKILL_GO_ON
	
	def onConjurePetResult( self, UID, baseRef ):
		"""
		<define method>
		召唤幻兽结果
		"""
		if UID:
			self._activePetUID = UID
			self._activePetBase = baseRef
			if self._preActivePetUID and self._activePetUID != self._preActivePetUID:
				KBEDebug.print_stack()
				self.base.delPetShenTongQuickBar(self._preActivePetUID)
		
		self.unlockPetOperation()
		
		pet = self.petCages.get( UID )
		self.activePetID = self._activePetBase.id
		petObject = g_petFactory.getObject( pet.scriptID )
		petObject.onConjurePet( self )
		self.triggerSkillEvent( csdefine.SKILL_EVENT_PET_ACTIVE, self.id, {"isActive":True} )

# -----------------------------------骑乘幻兽--------------------------------------------------
	def transformPet( self, srcEntityID ):
		"""
		<Exposed method>
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		self.triggerSkillEvent(csdefine.SKILL_EVENT_REQUEST_ACTION, self.id, {"requestType" : csdefine.SKILL_EVENT_ACTION_TYPE_PET})
		if not self.lockPetOperation():return
		
		if self._activePetUID:								# 如果有出战的，才可以上、下马
			if self.isMountOnPet():
				self._dismountPet( self._activePetUID )
			else:
				self._mountPet( self._activePetUID )
		else:
			self.client.OnIsmountSuccess( False )
		
	def isMountOnPet( self ):
		"""
		是否在骑乘状态
		"""
		return self.carrierId
		
	def mountCheck( self, UID ):
		""""""
		if self.isState( csdefine.ENTITY_STATE_FIGHT ):
			self.statusMessage( csstatus.PET_CAN_NOT_MOUNT_PET_BY_FIGHT_STATE )
			return False
			
		if self.actionForbidSign( csdefine.ACTION_FORBID_MOUNT_PET ):
			self.statusMessage( csstatus.PET_CAN_NOT_MOUNT_PET_BY_ACTFORBID )
			return False
			
		if self._activePetBase:
			cellPet = KBEngine.entities.get( self._activePetBase.id, None )
			if cellPet and cellPet.isState( csdefine.ENTITY_STATE_DEAD ):
				self.statusMessage( csstatus.PET_CAN_NOT_MOUNT_AS_STATE_NOT_ALLOW )
				return False
				
		return True
		
	def _mountPet( self, UID ):
		"""上马"""
		if self.mountCheck( UID ):
			if self.getExtraModelNumber():
				self.setExtraModelNumber("")
			self.triggerSkillEvent(csdefine.SKILL_EVENT_INTERRUPT_BUFF_CHANGEMODEL, self.id, {})
			self.triggerSkillEvent(csdefine.SKILL_EVENT_PET_ACTIVE, self.id, {"isActive": False})

			self.base.mountPet()			#不再使用技能上马，改为直接上马
			#self.useSkillToEntityFC( self.id, Const.MOUNT_ON_PET_SKILLID, self.id )
			self.client.OnIsmountSuccess( True )
		else:
			self.client.OnIsmountSuccess( False )
			
	def onSkillBeginMountPet( self ):
		"""技能 开始时"""
		self.mountPetTimerID = 0
		self.actCounterInc( Const.MOUNT_PET_ACT_FORBID )
		
	def onSkillEndMountPet( self ):
		"""技能 结束时"""
		if self.mountPetTimerID:
			self.popTimer( self.mountPetTimerID )
			self.mountPetTimerID = 0
			return
		self.actCounterDec( Const.MOUNT_PET_ACT_FORBID )
			
	def onMountPet( self ):
		""""""
		if self._activePetBase:
			self.base.mountPet()
			
	def onMountPetResult( self ):
		"""
		<define method>
		上马回调
		"""
		self.unlockPetOperation()
		pet = self.petCages[self._activePetUID]
		petObject = g_petFactory.getObject(pet.scriptID)
		self.setCarrierId("eCarrierId", petObject.carrierId)
		speedPercent = formulas.getSpeedPlusByStep( pet.step, pet.quality )
		speedBase = formulas.getSpeedBaseByStep( pet.step, pet.quality )
		self.setBuffProperties( { "_percent" : { ItemTypeEnum.SPEED : speedPercent } } )
		self.setBuffProperties( { "_extra" : { ItemTypeEnum.SPEED : speedBase } } )
		self.calcAttachProperties()
		
		petObject.onMountPet( self )
		
	def _dismountPet( self, UID ):
		"""下马"""
		self.base.dismountPet( self.position, self.direction )
		self.carrierId = ""											# CST-2422

	def disMountPet( self ):
		"""
		下马 (只处理下马)
		"""
		if not self.lockPetOperation():return
		if not self._activePetUID:return						
		if not self.isMountOnPet():return
			
		self._dismountPet( self._activePetUID )
		
	def onDismountPetResult( self ):
		"""
		<define method>
		下马回调
		"""
		self.unlockPetOperation()
		#self.petID = ""
		pet = self.petCages[self._activePetUID]
		speedPercent = formulas.getSpeedPlusByStep( pet.step, pet.quality )
		speedBase = formulas.getSpeedBaseByStep( pet.step, pet.quality )
		self.setBuffProperties( { "_percent" : { ItemTypeEnum.SPEED : -speedPercent } } )
		self.setBuffProperties( { "_extra" : { ItemTypeEnum.SPEED : -speedBase } } )
		self.calcAttachProperties()
		self.triggerSkillEvent( csdefine.SKILL_EVENT_PET_ACTIVE, self.id, {"isActive":True} )

# -----------------------------------回收幻兽-------------------------------------------------		
	def withdrawPetByReason( self, reason ):
		"""
		回收幻兽外部接口
		例如：摆摊、飞行等
		"""
		if self._activePetBase:
			self.triggerSkillEvent( csdefine.SKILL_EVENT_PET_ACTIVE, self.id, {"isActive":False} )
			self.base.withdrawPet( reason )
			
			if reason in [csdefine.PET_WITHDRAW_FLYTELEPORT, csdefine.PET_WITHDRAW_STALL]:
				self.setTemp("withdrawPetUID", self._activePetUID )
			if self.carrierId:							# 如果回调的时候，再下马。客户端会出现无法飞行的情况
				self.carrierId = ""
				self.onDismountPetResult()

	def withdrawPet( self, srcEntityID ):
		"""
		<Exposed method>
		回收幻兽
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		self.triggerSkillEvent(csdefine.SKILL_EVENT_REQUEST_ACTION, self.id, {"requestType" : csdefine.SKILL_EVENT_ACTION_TYPE_PET})
		if not self.lockPetOperation():return
		
		if self._activePetBase:
			self.triggerSkillEvent( csdefine.SKILL_EVENT_PET_ACTIVE, self.id, {"isActive":False} )
			self.base.withdrawPet( csdefine.PET_WITHDRAW_COMMON )
			
	def onWithdrawPetResult( self, reason ):
		"""
		<define method>
		回收幻兽回调
		"""
		if self.carrierId:
			self.carrierId = ""
			self.onDismountPetResult()
		self._preActivePetUID = self._activePetUID
		self._activePetUID = 0
		self.activePetID = 0
		self._activePetBase = None
			
		if reason == csdefine.PET_WITHDRAW_CONJURE and self._conjurePetUID:					# 如果是因为召唤其他幻兽，回收的幻兽。需要继续召唤幻兽流程
			self.base.conjurePet( self._conjurePetUID, self.position, self.direction )
		elif reason == csdefine.PET_WITHDRAW_ENTER_FENCE:		# 出战幻兽入栏
			petUID = self.removeTemp("EnterFencePet")
			self.base.activePetEnterFence( petUID )
		elif reason == csdefine.PET_WITHDRAW_EXCHANGE_FROM_FENCE:
			enterUID = self.removeTemp("EnterFencePet")
			leaveUID = self.removeTemp("LeaveFencePet")
			self.base.exChangePetFromFence(enterUID, leaveUID)
		else:
			self.unlockPetOperation()
# -----------------------------------放生幻兽--------------------------------------------------
	def freePet( self, srcEntityID, UIDstr ):
		"""
		Exposed method
		放生幻兽
		"""
		if not self.validateClientCall( srcEntityID ):
			return

		UID = int( UIDstr )
		if not UID in self.petCages:return
		
		result = self.canFreePet( UID )
		if result != csstatus.SKILL_GO_ON:
			self.statusMessage( result )
		else:
			if self.lockPetOperation():
				self.base.freePet( UID )
				self.base.delPetShenTongQuickBar(UID)
			
	def canFreePet( self, UID ):
		"""能否放生"""
		if self.level < Const.CAN_FREE_PET_LEVEL:
			KBEDebug.ERROR_MSG("Can not freePet!player level(%d)"%self.level)		# CST-13884
			return 0
		if self._activePetUID == UID:
			return csstatus.PET_FREE_FAIL_AS_BATTLE
		pet = self.petCages[UID]
		if pet.isSleepTime():
			return csstatus.PET_IS_IN_DORMANT_CANOT_OPERATE
		
		return csstatus.SKILL_GO_ON
	
	def onFreePetResult( self, UID ):
		"""
		define method
		放生幻兽
		"""
		self.unlockPetOperation()
		pet = self.petCages.pop( UID )
		
		#添加日志
		#g_logger.petDelLog( roleDBID, roleName, petName, petUname, petUid, petQuality, petLevel, reason )
	
# -----------------------------------封印幻兽--------------------------------------------------
	def sealPet( self, srcEntityID, UIDstr ):
		"""
		Exposed method
		封印幻兽
		"""
		if not self.validateClientCall( srcEntityID ):
			return

		uid = int( UIDstr )
		pet = self.petCages.get( uid, None )
		petObject = g_petFactory.getObject( pet.scriptID )
		if pet is None:return
		
		if self._activePetUID == uid:
			self.statusMessage( csstatus.PET_IS_ACTIVE )
			return
		if pet.isSleepTime():
			self.statusMessage( csstatus.PET_IS_IN_DORMANT_CANOT_OPERATE )
			return
			
		# 消耗判断 封印符
		takeLevel = petObject.getEntityProperty( "takeLevel", 0 )
		amount = formulas.getSealCharmAmount( int(pet.scriptID), takeLevel, pet.quality )
		self.inquireMessage( csstatus.PET_SEAL_CHARM_CAN_NOT_CONSUME, [amount], "onSealPet", uid )

	def onSealPet( self, isSeal, uid ):
		"""
		"""
		if isSeal:
			pet = self.petCages.get( uid, None )
			petObject = g_petFactory.getObject( pet.scriptID )
			takeLevel = petObject.getEntityProperty( "takeLevel", 0 )
			if pet is None:return
			sealItemID = formulas.getSealCharmItemID( int(pet.scriptID), takeLevel, pet.quality )
			if sealItemID:
				item = g_itemFactory.createDynamicItem( sealItemID, 1 )
				state = self.addItemCheck( item )
				if not state == csstatus.ITEM_GO_ON:
					self.statusMessage( state )
					return
			# 消耗	
			itemInstList = self.getItemInstsByID( csdefine.PET_SEAL_CHARM_ITEMID )
			amount = formulas.getSealCharmAmount( int(pet.scriptID), takeLevel, pet.quality )
			hasSealAmount = 0
			for itemInst in itemInstList:
				hasSealAmount += itemInst.amount
			if hasSealAmount < amount:
				self.statusMessage( csstatus.PET_SEAL_CHARM_NOT_ENOUGN )
				return
			if self.lockPetOperation():
				self.base.sealPet( uid, amount )

	def onSealPetResult( self, params ):
		"""
		define method
		封印幻兽回调
		"""
		#扣除消耗 封印符
		itemInstList = self.getItemInstsByID( csdefine.PET_SEAL_CHARM_ITEMID )
		if itemInstList:
			uid = params.uid
			scriptID = params.scriptID
			quality = params.quality
			isBinded = self.isBindedSeal(itemInstList)
			pet = self.petCages.pop( uid )
			petObject = g_petFactory.getObject( scriptID )
			takeLevel = petObject.getEntityProperty( "takeLevel", 0 )
			
			amount = formulas.getSealCharmAmount( int(scriptID), takeLevel, quality )
			self.removeItemListByAmount( itemInstList, amount, csdefine.ITEM_REMOVE_BY_USE )

			sealItemID = formulas.getSealCharmItemID( int(scriptID), takeLevel, quality )
			param = {"dynamicData":{"pet":params}}
			if sealItemID:
				item = g_itemFactory.createDynamicItem( sealItemID, 1, param )
				item.setBindType(None,isBinded) 
				self.addItem( item, csdefine.ITEM_ADD_BY_PICKUP )
		
		self.unlockPetOperation()

	def isBindedSeal(self, itemlist):
		"""是否绑定"""
		for mItem in itemlist:
			if mItem.isBinded():
				return 1
		return 0
# -----------------------------------合成幻兽--------------------------------------------------
	def composePet( self, srcEntityID, firstUIDstr, secondUIDstr ):
		"""
		Exposed method
		合成幻兽
		"""
		if not self.validateClientCall( srcEntityID ):
			return

		first_uid = int( firstUIDstr )
		second_uid = int( secondUIDstr )
		first_pet = self.petCages.get( first_uid, None )	
		second_pet = self.petCages.get( second_uid, None )
		itemInstList = self.getItemInstsByID( csdefine.PET_COMPOSE_XIANLINGGUO )
		amount = formulas.getComposeMaterials( first_pet.quality )
		money = formulas.getComposeMoney( first_pet.quality )

		if not first_pet or not second_pet:
			self.client.OnPetComposeFailed( csstatus.PET_COMPOSE_INPUT_VPET, 0 )
			return
		if self._activePetUID == first_uid or self._activePetUID == second_uid:
			self.client.OnPetComposeFailed( csstatus.PET_IS_ACTIVE, 0 )
			return
		if first_pet.isSleepTime() or second_pet.isSleepTime():
			self.client.OnPetComposeFailed( csstatus.PET_IS_IN_DORMANT_CANOT_OPERATE, 0 )
			return
		if first_pet.quality != second_pet.quality:
			self.client.OnPetComposeFailed( csstatus.PET_COMPOSE_QUALITY_IS_NOT_SAME, 0 )
			return
		if first_pet.step < 3 or second_pet.step < 3:
			self.client.OnPetComposeFailed( csstatus.PET_COMPOSE_FAIL_VPET_STEP_NOT_ENOUGH, 0 )
			return
		#消耗判断 仙灵果,金钱
		if self.money < money:
			self.client.OnPetComposeFailed( csstatus.PET_COMPOSE_NO_ENOUGH_MONEY, 0 )
			return
		hasAmount = 0
		for item in itemInstList:
			hasAmount += item.amount
		if hasAmount < amount:
			self.client.OnPetComposeFailed( csstatus.PET_COMPOSE_NO_ENOUGH_MATERIALS, 0 )
			return
		isUseMatertial = True
		if self.lockPetOperation():
			self.base.composePet( first_uid, second_uid, isUseMatertial )

	def onComposePetBygold( self, srcEntityID, isCompose,  firstUIDstr, secondUIDstr ):
		"""
		当仙灵果不够时使用仙石合成
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		self.statusMessage( csstatus.PET_COMPOSE_NO_ENOUGH_MATERIALS )	
		#self.client.OnPetComposeFailed( csstatus.PET_COMPOSE_NO_ENOUGH_MATERIALS, 0 )

	def onComposePetResult( self,first_uid, second_uid, isUseMatertial ):
		"""
		define method
		合成幻兽回调
		"""
		#扣除消耗 仙灵果，金钱
		first_pet = self.petCages.get( first_uid, None )	
		second_pet = self.petCages.get( second_uid, None )
		if isUseMatertial:
			itemInstList = self.getItemInstsByID( csdefine.PET_COMPOSE_XIANLINGGUO )
			amount = formulas.getComposeMaterials( first_pet.quality )
			self.removeItemListByAmount( itemInstList, amount, csdefine.ITEM_REMOVE_BY_USE )
			needMoney = formulas.getComposeMoney( first_pet.quality )
			self.subMoney( needMoney, csdefine.MONEY_SUB_REASON_COMPOSE_PET )

		second_pet = self.petCages.pop( second_uid )
		self.unlockPetOperation()

# -----------------------------------幻兽打书--------------------------------------------------
	def replacePetSkill( self, srcEntityID, UIDstr, SKillID, SkillBookID ):
		"""
		Exposed method
		替换主动技能
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		uid = int( UIDstr )
		pet = self.petCages.get( uid, None )
		if pet is None:return
		if self._activePetUID == uid:
			self.statusMessage( csstatus.PET_IS_ACTIVE )
			return
		if pet.isSleepTime():
			self.statusMessage( csstatus.PET_IS_IN_DORMANT_CANOT_OPERATE )
			return

		if 0 == SkillBookID:
			self.statusMessage( csstatus.PET_SKILL_NO_SKILL_BOOK )
			return

		SkillItem = g_itemFactory.getItemData( SkillBookID )
		replaceSkillID = int(SkillItem.get("Param1"))			#技能ID
		bookProfession = int(SkillItem.get("Param2"))			#技能书种族
		isActiveType = int(SkillItem.get("Param3"))				#是否为主动技能
		if isActiveType != 1:
			self.statusMessage( csstatus.PET_IS_ACTIVE_SKILL_TYPE )
			return

		skillQuality = 0
		skillLevel = 0
		if SKillID != 0:
			skill = self.getSkill( SKillID )
			skillQuality =skill.getQuality()						#被替换技能品质
			skillLevel = g_PetSkillLearn.getLevel( SKillID )		#被替换技能等级
		petObject = g_petFactory.getObject( pet.scriptID )
		profession = petObject.getEntityProperty( "profession", 1 )
		if 0 == replaceSkillID:
			return

		replaceSkillLevel = g_PetSkillLearn.getLevel( replaceSkillID )
		if (replaceSkillLevel - skillLevel > 1) or replaceSkillLevel > 1:
			self.statusMessage( csstatus.PET_SKILL_LEARN_LEVEL )
			return
		#种族
		if bookProfession != 0 and profession != bookProfession:
			self.statusMessage( csstatus.PET_SKILL_NOT_SAME_RACES )
			return			
		if skillQuality >= 2:
			self.inquireMessage( csstatus.PET_SKILL_NOT_SAME_QUALITY, [], "onReplacePetSkillByQuality", uid, SKillID, SkillBookID, replaceSkillID )
			return
		if skillLevel > 7:
			self.inquireMessage( csstatus.PET_SKILL_NOT_SAME_LEVEL, [], "onReplacePetSkillByLevel", uid, SKillID, SkillBookID, replaceSkillID)
			return
		self.onReplacePetSkill(uid, SKillID, SkillBookID, replaceSkillID)
	
	def onReplacePetSkillByQuality( self, isreplace, uid, SKillID, SkillBookID, replaceSKillID ):
		"""
		当被替换技能品质大于2时
		"""
		if isreplace:
			#技能等级判断
			skillLevel = g_PetSkillLearn.getLevel( SKillID )
			if skillLevel > 7:
				self.inquireMessage( csstatus.PET_SKILL_NOT_SAME_LEVEL, [], "onReplacePetSkillByLevel", uid, SKillID, SkillBookID, replaceSKillID)
				return
			self.onReplacePetSkill(uid, SKillID, SkillBookID, replaceSKillID)

	def onReplacePetSkillByLevel( self, isreplace, uid, SKillID, SkillBookID, replaceSKillID ):
		"""
		当被替换技能技能大于7时
		"""
		if isreplace:
			self.onReplacePetSkill( uid, SKillID, SkillBookID, replaceSKillID )


	def onReplacePetSkill( self, uid, SKillID, SkillBookID, replaceSKillID ):
		"""
		替换主动技能回调
		"""
		#消耗判断
		needPotential = g_PetSkillLearn.getReqPotential( replaceSKillID )
		money = g_PetSkillLearn.getMoney( replaceSKillID )

		# 金钱不足
		if self.money < money:
			self.statusMessage( csstatus.PET_SKILL_NO_ENOUGH_MONEY )
			return

		# 潜能不足
		if self.potential < needPotential:
			self.statusMessage( csstatus.CAN_NOT_LEARN_SKILL_AS_POTENTIAL_NOT_ENOUGH, "" )
			return

		# 技能书不足
		hasAmount = 0
		itemList = self.getItemInstsByID(SkillBookID)
		for item in itemList:
			hasAmount += item.getAmount()
		if hasAmount < 1:
			self.statusMessage( csstatus.CAN_NOT_MATERIAL_UPGRADE_SKILL, "" )
			return

		if self.lockPetOperation():
			self.base.replacePetSkill( uid, SKillID, SkillBookID, replaceSKillID )

	def onReplacePetSkillResult( self, SkillBookID, replaceSKillID ):
		"""
		替换主动技能结果回调
		"""
		#扣除消耗
		needPotential = g_PetSkillLearn.getReqPotential( replaceSKillID )
		money = g_PetSkillLearn.getMoney( replaceSKillID )
		
		self.subMoney( money, csdefine.MONEY_SUB_REASON_REPLACE_PET_SKILL )
		self.subPotential( needPotential, csdefine.POTENTIAL_REMOVE_REASON_STUDY_SKILL )
		self.removeItemsByItemID( SkillBookID, 1, csdefine.ITEM_REMOVE_BY_USE)

		self.unlockPetOperation()

	def upgradePetSkill( self, srcEntityID, UIDstr, SKillID ):
		"""
		Exposed method
		升级主动技能
		"""
		if srcEntityID != self.id:return
		uid = int( UIDstr )
		pet = self.petCages.get( uid, None )
		if pet is None:return

		skilldata = g_PetSkillLearn.getskilldata(SKillID)
		if not skilldata:
			KBEDebug.ERROR_MSG("pet skilldata cannot find by skillID(%s)"%SKillID)
			return
		nextskillLevel = g_PetSkillLearn.getLevel(SKillID)+1
		nextLevelId = g_PetSkillLearn.getNextSkill(SKillID)
		skill = self.getSkill( nextLevelId )
		nextskillQuality = skill.getQuality()
		Potential = g_PetSkillLearn.getReqPotential(nextLevelId)
		money = g_PetSkillLearn.getMoney( nextLevelId )
		SkillBookID = g_PetSkillLearn.getSkillBook( nextLevelId )
		if nextLevelId == 0:
			return

		if self._activePetUID == uid:
			self.client.OnUpgradePetSkill( csstatus.PET_IS_ACTIVE, 0 )
			return
		if pet.isSleepTime():
			self.client.OnUpgradePetSkill( csstatus.PET_IS_IN_DORMANT_CANOT_OPERATE, 0 )
			return
		#技能等级和幻兽介位
		if nextskillLevel > pet.step:
			self.client.OnUpgradePetSkill( csstatus.PET_SKILL_NO_ENOUGH_STEP, 0 )
			return
		#消耗判断   潜能
		if self.potential < Potential:
			self.client.OnUpgradePetSkill( csstatus.PET_SKILL_NO_ENOUGH_POTENTIAL, 0 )
			return
		
		# 金钱不足
		if self.money < money:
			self.client.OnUpgradePetSkill( csstatus.PET_SKILL_NO_ENOUGH_MONEY, 0 )
			return

		# 技能书不足
		hasAmount = 0
		itemList = self.getItemInstsByID(SkillBookID)
		for item in itemList:
			hasAmount += item.getAmount()
		if hasAmount < 1:
			self.client.OnUpgradePetSkill( csstatus.CAN_NOT_MATERIAL_UPGRADE_SKILL, 0 )
			return			

		if self.lockPetOperation():
			self.base.upgradePetSkill( uid, SKillID, nextLevelId, Potential )

	def onUpgradePetSkillResult( self, SKillID):
		"""
		define method
		升级主动技能结果回调		
		"""
		#消耗扣除  潜能
		needPotential = g_PetSkillLearn.getReqPotential( SKillID )
		money = g_PetSkillLearn.getMoney( SKillID )
		SkillBookID = g_PetSkillLearn.getSkillBook( SKillID )
		self.subMoney( money, csdefine.MONEY_SUB_REASON_REPLACE_PET_SKILL )
		self.subPotential( needPotential, csdefine.POTENTIAL_REMOVE_REASON_STUDY_SKILL )
		self.removeItemsByItemID( SkillBookID, 1, csdefine.ITEM_REMOVE_BY_USE)
		self.unlockPetOperation()

	def replacePetPassiveSkill( self, srcEntityID, UIDstr, SKillID, SkillBookID ):
		"""
		Exposed method
		替换被动技能
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		uid = int( UIDstr )
		pet = self.petCages.get( uid, None )
		if pet is None:return
		if self._activePetUID == uid:
			self.statusMessage( csstatus.PET_IS_ACTIVE )
			return
		if pet.isSleepTime():
			self.statusMessage( csstatus.PET_IS_IN_DORMANT_CANOT_OPERATE )
			return

		if 0 == SkillBookID:
			self.statusMessage( csstatus.PET_PASSIVE_SKILL_NO_SKILL_BOOK )
			return

		SkillItem = g_itemFactory.getItemData( SkillBookID )
		replaceSkillID = int(SkillItem.get("Param1"))		#要替换的被动技能ID
		bookProfession = int(SkillItem.get("Param2"))			#技能书种族
		isActiveType = int(SkillItem.get("Param3"))			#是否为主动技能
		# quality = SkillItem.get("Quality", 1)				#技能书品质
		if isActiveType != 0:
			self.statusMessage( csstatus.PET_IS_ACTIVE_SKILL_TYPE )
			return

		skillQuality = 0
		skillLevel = 0
		if SKillID != 0:
			skill = self.getSkill( SKillID )
			skillQuality =skill.getQuality()						#被替换技能品质
			skillLevel = g_PetSkillLearn.getLevel( SKillID )		#被替换技能等级
		petObject = g_petFactory.getObject( pet.scriptID )
		profession = petObject.getEntityProperty( "profession", 1 )

		replaceSkillLevel = g_PetSkillLearn.getLevel( replaceSkillID )
		if (replaceSkillLevel - skillLevel > 1) or replaceSkillLevel > 1:
			self.statusMessage( csstatus.PET_SKILL_LEARN_LEVEL )
			return
		# if quality > pet.quality:
		# 	self.statusMessage( csstatus.PET_PASSIVE_SKILL_NOT_ENOUGH_QUALITY )
		# 	return
		#种族
		if bookProfession != 0 and profession != bookProfession:
			self.statusMessage( csstatus.PET_SKILL_NOT_SAME_RACES )
			return
		if SKillID == replaceSkillID:
			self.statusMessage( csstatus.PET_PASSIVE_SKILL_IS_SAME )
			return

		if skillQuality >= 2:
			self.inquireMessage( csstatus.PET_SKILL_NOT_SAME_QUALITY, [], "onReplacePetPassiveSkillByQuality", uid, SKillID, SkillBookID, replaceSkillID )
			return
		if skillLevel > 7:
			self.inquireMessage( csstatus.PET_SKILL_NOT_SAME_LEVEL, [], "onReplacePetPassiveSkillByLevel", uid, SKillID, SkillBookID, replaceSkillID)
			return
		self.onReplacePetPassiveSkill(uid, SKillID, SkillBookID, replaceSkillID)

	def onReplacePetPassiveSkillByQuality( self, isreplace, uid, SKillID, SkillBookID, replaceSkillID ):
		"""
		当被替换技能品质大于2时
		"""
		if isreplace:
			#技能等级判断
			skillLevel = g_PetSkillLearn.getLevel( SKillID )
			if skillLevel > 7:
				self.inquireMessage( csstatus.PET_SKILL_NOT_SAME_LEVEL, [], "onReplacePetPassiveSkillByLevel", uid, SKillID, SkillBookID, replaceSkillID)
				return
			self.onReplacePetPassiveSkill(uid, SKillID, SkillBookID, replaceSkillID)
	
	def onReplacePetPassiveSkillByLevel( self, isreplace, uid, SKillID, SkillBookID, replaceSkillID ):
		"""
		当被替换技能技能大于7时
		"""
		if isreplace:
			self.onReplacePetPassiveSkill( uid, SKillID, SkillBookID, replaceSkillID )


	def onReplacePetPassiveSkill( self, uid, SKillID, SkillBookID, replaceSkillID ):	
		"""
		替换被动技能回调
		"""	
		#消耗判断
		needPotential = g_PetSkillLearn.getReqPotential( replaceSkillID )
		money = g_PetSkillLearn.getMoney( replaceSkillID )

		# 金钱不足
		if self.money < money:
			self.statusMessage( csstatus.PET_SKILL_NO_ENOUGH_MONEY )
			return

		# 潜能不足
		if self.potential < needPotential:
			self.statusMessage( csstatus.CAN_NOT_LEARN_SKILL_AS_POTENTIAL_NOT_ENOUGH, "" )
			return

		# 技能书不足
		hasAmount = 0
		itemList = self.getItemInstsByID(SkillBookID)
		for item in itemList:
			hasAmount += item.getAmount()
		if hasAmount < 1:
			self.statusMessage( csstatus.CAN_NOT_MATERIAL_UPGRADE_SKILL, "" )
			return

		if self.lockPetOperation():
			self.base.replacePetPassiveSkill( uid, SKillID, SkillBookID, replaceSkillID )
		

	def onReplacePetPassiveSkillResult( self, SkillBookID, replaceSkillID ):
		"""
		define method
		替换被动技能结果回调
		"""
		#消耗扣除
		needPotential = g_PetSkillLearn.getReqPotential( replaceSkillID )
		money = g_PetSkillLearn.getMoney( replaceSkillID )
		
		self.subMoney( money, csdefine.MONEY_SUB_REASON_REPLACE_PET_P_SKILL )
		self.subPotential( needPotential, csdefine.POTENTIAL_REMOVE_REASON_STUDY_SKILL )
		self.removeItemsByItemID( SkillBookID, 1, csdefine.ITEM_REMOVE_BY_USE)

		self.unlockPetOperation()

	def upgradePetPassiveSkill( self, srcEntityID, UIDstr, SKillID ):
		"""
		Exposed method
		升级被动技能
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		uid = int( UIDstr )
		pet = self.petCages.get( uid, None )
		if pet is None:return
		if self._activePetUID == uid:
			self.client.OnUpgradePetPassiveSkill( csstatus.PET_IS_ACTIVE, 0 )
			return
		if pet.isSleepTime():
			self.client.OnUpgradePetPassiveSkill( csstatus.PET_IS_IN_DORMANT_CANOT_OPERATE, 0 )
			return

		nextLevelId = g_PetSkillLearn.getNextSkill( SKillID )
		needPotential = g_PetSkillLearn.getReqPotential( nextLevelId )
		money = g_PetSkillLearn.getMoney( nextLevelId )
		SkillBookID = g_PetSkillLearn.getSkillBook( nextLevelId )

		if nextLevelId == 0:
			return

		# 金钱不足
		if self.money < money:
			self.client.OnUpgradePetPassiveSkill( csstatus.PET_PASSIVE_SKILL_NO_ENOUGH_MONEY, 0 )
			return

		# 潜能不足
		if self.potential < needPotential:
			self.client.OnUpgradePetPassiveSkill( csstatus.CAN_NOT_LEARN_SKILL_AS_POTENTIAL_NOT_ENOUGH, 0 )
			return

		# 技能书不足
		hasAmount = 0
		itemList = self.getItemInstsByID(SkillBookID)
		for item in itemList:
			hasAmount += item.getAmount()
		if hasAmount < 1:
			self.client.OnUpgradePetPassiveSkill( csstatus.CAN_NOT_MATERIAL_UPGRADE_SKILL, 0 )
			return

		if self.lockPetOperation():
			self.base.upgradePetPassiveSkill( uid, SKillID, money, nextLevelId )

	def onUpgradePetPassiveSkillResult( self, nextSkillID ):
		"""
		define method
		升级被动技能回调		
		"""
		#扣除消耗 残卷,魂珠,金钱
		needPotential = g_PetSkillLearn.getReqPotential( nextSkillID )
		money = g_PetSkillLearn.getMoney( nextSkillID )
		SkillBookID = g_PetSkillLearn.getSkillBook( nextSkillID )
		self.subMoney( money, csdefine.MONEY_SUB_REASON_UPGRADE_PET_P_SKILL )
		self.subPotential( needPotential, csdefine.POTENTIAL_REMOVE_REASON_STUDY_SKILL )
		self.removeItemsByItemID( SkillBookID, 1, csdefine.ITEM_REMOVE_BY_USE)

		self.unlockPetOperation()

# -----------------------------------幻兽 其他功能--------------------------------------------------
	def addPetExp( self, exp, reason ):
		"""添加出战幻兽经验"""
		if reason in [csdefine.EXP_ADD_REASON_KILL_MONSTER, csdefine.EXP_ADD_REASON_GM_SET]:			#幻兽杀怪，获得经验
			petEntity = self.getActivePetCell()
			if petEntity:
				petData = self.petCages[self._activePetUID]
				needLevel = formulas.getLevelByStep( petData.step + 1 )
				if needLevel > self.level:
					return
				maxStep = formulas.getPetMaxStep()
				if petData.step == maxStep:				# 幻兽达到最大介次
					maxExp = formulas.getNeedExpNextStep( maxStep, petData.quality )
					if petData.exp == maxExp:
						return
					petData.exp = min( maxExp, petData.exp + exp )
				else:
					allExp = exp + petData.exp
					needExp = formulas.getNeedExpNextStep( petData.step + 1, petData.quality )
					addStep = 0
					addExp = allExp
					while(allExp >= needExp):
						allExp -= needExp
						addStep += 1
						addExp = allExp
						nextStepNeedLevel = formulas.getLevelByStep( petData.step + addStep )
						if nextStepNeedLevel > self.level:
							addExp = min( allExp, needExp )
							addStep -= 1
							break
						elif petData.step + addStep >= maxStep:
							addExp = min( allExp, needExp )
							allExp = 0
						else:
							needExp = formulas.getNeedExpNextStep( petData.step  + addStep + 1, petData.quality )
					
					petData.exp = addExp
					petEntity.setExp( petData.exp )			# 经验在幻兽销毁的时候，才同步到 玩家
					if addStep:
						petData.step += addStep
						petEntity.setStep( petData.step )
						self.base.setPetStep( self._activePetUID, petData.step )
				
				self.statusMessage(csstatus.PET_GET_EXT, exp)
				self.client.CLIENT_OnSetActivePetExp( petData.exp )
		
	def setPetStep( self, step ):
		"""GM指令 设置幻兽介次"""
		petEntity = self.getActivePetCell()
		if petEntity:
			petData = self.petCages[self._activePetUID]
			maxStep = formulas.getPetMaxStep()
			step = min(maxStep, step)
			petData.step = step
			petEntity.setStep( step )
			self.base.setPetStep( self._activePetUID, step )
		
	def activateCage( self, srcEntityID ):
		"""
		Exposed method
		激活幻兽笼子
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		if self.petCageMax >= Const.VPET_CAGE_MAX:return
		
		if self.petCageMax < Const.VPET_CAGE_MAX - 1:
			money = csconst.ACTIVATE_PET_CAGES[self.petCageMax+1]["needMoney"]
			moneyToStr = Functions.moneyToStr( money )
			self.inquireMessage( csstatus.PET_ACTIVATE_CAGE_CONST_MONEY , [moneyToStr], "onActivateCage" )
		elif self.petCageMax == Const.VPET_CAGE_MAX - 1:
			gold = csconst.ACTIVATE_PET_CAGES[self.petCageMax+1]["needGold"]
			self.inquireMessage( csstatus.PET_ACTIVATE_CAGE_CONST_GOLD, [gold], "onActivateCage" )
			
	def onActivateCage( self, isActive ):
		""""""
		if isActive:
			needLevel = csconst.ACTIVATE_PET_CAGES[self.petCageMax+1]["needLevel"]
			if needLevel > self.level:
				self.statusMessage( csstatus.PET_ACTIVATE_CAGE_NO_ENOUGH_LEVEL, needLevel )
				return
				
			if self.petCageMax < Const.VPET_CAGE_MAX - 1:
				needMoney = csconst.ACTIVATE_PET_CAGES[self.petCageMax+1]["needMoney"]
				if not self.subMoney( needMoney, csdefine.MONEY_SUB_REASON_ACTIVATE_CAGE ):
					self.statusMessage( csstatus.PET_ACTIVATE_CAGE_NO_ENOUGH_MONEY )
					return
				self.petCageMax = self.petCageMax + 1
				
			elif self.petCageMax == Const.VPET_CAGE_MAX - 1:
				needGold = csconst.ACTIVATE_PET_CAGES[self.petCageMax+1]["needGold"]
				self.base.onActivateCageCostGold( needGold )
		
	def activateCageResult( self, result ):
		"""
		define method
		激活幻兽结果
		"""
		if result:
			self.petCageMax = self.petCageMax + 1
		else:
			self.statusMessage( csstatus.PET_ACTIVATE_CAGE_NO_ENOUGH_GOLD )

# -----------------------------------幻兽战斗--------------------------------------------------
	def CELL_petAIChangeState( self, exposed, newState ):
		"""
		exposed method
		切换AI模式
		"""
		if not self.validateClientCall( exposed ):
			return
		if self.getActivePetCell():
			self.getActivePetCell().AIOwnerChangeState( newState )

	def CELL_petAIChangeCommand ( self, exposed, newCmd ):
		"""
		exposed method
		切换AI命令
		"""
		if not self.validateClientCall( exposed ):
			return
		if self.getActivePetCell():
			self.getActivePetCell().AIOwnerUseCommand( newCmd )
	
	def CELL_petAIAttackTarget( self, exposed, skillID, targetID ):
		"""
		exposed method
		攻击指定目标
		"""
		if not self.validateClientCall( exposed ):
			return
		if self.getActivePetCell():
			self.getActivePetCell().AIOwnerAttack( skillID, targetID )

	def AICommandEndNotice( self ):
		"""
		跟随和停留命令结束通知客户端
		"""
		if self.getActivePetCell():
			self.client.OnAIStopCommand()

	def CELL_requestAttackTarget( self, exposed, skillID, targetID ):
		"""
		幻兽攻击模式
		"""
		if not self.validateClientCall( exposed ):
			return
		if self.getActivePetCell():
			self.getActivePetCell().RequestAttackTarget( skillID, targetID )

	def CELL_requestTeleporToOwner( self, exposed ):
		"""
		请求幻兽传送到玩家身边
		"""
		#if not self.validateClientCall( exposed ):
		#	return
		#if self._activePetBase:
		#	self.petReqTeleport( self._activePetBase )
		return

#--------------------------------------------------------------------------------------
	def onActionForbid( self, actForbid ):
		"""
		行为禁止时
		"""
		if actForbid == csdefine.ACTION_FORBID_MOUNT_PET:
			if self.isMountOnPet():
				self.transformPet( self.id )

#-----------------血槽--------------------------------------------------------------------------
	def onSetPetSlotValue( self ):
		"""
		读取配置初始化幻兽额外血槽和蓝槽的最大值
		"""
		slotData = PetExtraHPMPSlotCfg.datas
		if self.level in slotData:
			self.petExtraHP_Max = slotData[self.level][0]
			self.petExtraMP_Max = slotData[self.level][1]

	def CELL_onActiveHPSlot( self, exposed, isActiveHP, percentHP ):
		"""
		是否激活幻兽的血槽
		"""
		if not self.validateClientCall( exposed ):
			return
		self.isActiveHP = isActiveHP
		self.percentHP = percentHP

	def CELL_onActiveMPSlot( self, exposed, isActiveMP, percentMP):
		"""
		是否激活幻兽的蓝槽
		"""
		if not self.validateClientCall( exposed ):
			return
		self.isActiveMP = isActiveMP
		self.percentMP = percentMP

	def setExtraHP( self, value ):
		"""
		设置ExtraHP
		"""
		if value < 1.0:
			value = 0
		elif value > self.petExtraHP_Max:
			value = self.petExtraHP_Max

		oldValue = self.petExtraHP
		self.petExtraHP = value
		if oldValue != value:
			self.allClients.CLIENT_OnPetExtraHPChanged( self.petExtraHP, oldValue )

	def setExtraMP( self, value ):
		"""
		设置ExtraMP
		"""
		if value < 1.0:
			value = 0
		elif value > self.petExtraMP_Max:
			value = self.petExtraMP_Max

		oldValue = self.petExtraMP
		self.petExtraMP = value
		if oldValue != value:
			self.allClients.CLIENT_OnPetExtraMPChanged( self.petExtraMP, oldValue )
			
	
	# --------------------------------------------------原兽功能 ----------------------------------------------------
	def delayRequestOriginPet( self ):
		"""延迟请求原兽数据，因为有可能登录的时候去请求"""
		self.addTimerCallBack(1.0, "requestOriginPet", ())
		
	def requestOriginPet( self ):
		""""""
		KBEngine.globalData["SpaceLunHuiMiJinMgr"].requestOriginPet( self, self.playerDBID )
	
	def CELL_activePetEnterFence( self, srcEntityID ):
		"""
		<Exposed method>
		出战幻兽入栏
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		if self._activePetUID and self.canEnterPetFence():
			pet = self.petCages.get( self._activePetUID )
			if pet and pet.quality in [csdefine.VEHICLE_PET_QUALITY_HOLY, csdefine.VEHICLE_PET_QUALITY_DEITY]:
				if self.occupySpaceDF != csdefine.SPACE_TYPE_HIGH_DF:
					self.statusMessage( csstatus.ONLY_HIGH_DF_CAN_ENTER )
					return
			
			self.setTemp("EnterFencePet", self._activePetUID)
			self.withdrawPetByReason(csdefine.PET_WITHDRAW_ENTER_FENCE)
			
	def getPetFenceMax( self ):
		"""获取 兽栏最大容量"""
		return self.getLHMJBuildLevel(csdefine.LHMJ_BUIILD_SHOU_LAN) + 1
			
	def canEnterPetFence( self ):
		"""能否入兽栏"""
		max = self.getPetFenceMax()
		if max <= self.petFenceVolume:
			self.statusMessage( csstatus.CANOT_ENTER_PET_FENCE )
			return False
		return True
			
	def onPetEnterFence( self, petUid ):
		"""
		<define method>
		幻兽入栏回调
		"""
		self.unlockPetOperation()
		pet = self.petCages.pop( petUid )
		self.petFenceVolume += 1
	
	def CELL_freePetFromFence( self, srcEntityID, uidStr ):
		"""
		<exposed method>
		原兽从兽栏放生
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		KBEngine.globalData["SpaceLunHuiMiJinMgr"].freePetFromFence( self, self.playerDBID, int(uidStr))
	
	def CELL_feedOriginPet( self, srcEntityID, UIDstr, quality, itemID, num ):
		"""
		<Exposed method>
		喂养原兽（在兽栏中）
		"""
		if not self.validateClientCall( srcEntityID ):
			return
			
		pyItems = copy.deepcopy( formulas.getFeedPetCost(num, quality) )
		pyItems[csdefine.TRADE_PAY_ITEM_GOODS_BY_ID] = {itemID:num}
		pyItems[csdefine.TRADE_PAY_ITEM_FEED_PET] = {"uid":int(UIDstr), "itemID":itemID, "num" : num, "spaceType":self.occupySpaceDF}
		self.requestPay( csdefine.TRADE_TYPE_FEED_PET , 0, pyItems, () )
		
	def CELL_evolutionOriginPet( self, srcEntityID, UIDstr ):
		"""
		<Exposed method>
		原兽进化
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		
		pyItems = {}
		pyItems[csdefine.TRADE_PAY_ITEM_GOODS_BY_ID] = {csdefine.PET_ENVOLUTION_ITEMID:1}
		pyItems[csdefine.TRADE_PAY_ITEM_EVOLUTION_PET] = {"uid" : int(UIDstr)}
		self.requestPay( csdefine.TRADE_TYPE_EVOLUTION_PET , 0, pyItems, () )
			
	def CELL_PetOutsideFromFence( self, srcEntityID, uidStr, scriptID ):
		"""
		<exposed method>
		幻兽出栏，并召唤到玩家身边
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		if not self._activePetUID:
			KBEDebug.ERROR_MSG("Can not find activePet!!")
			return
		pet = self.petCages.get( self._activePetUID )
		if pet and pet.quality in [csdefine.VEHICLE_PET_QUALITY_HOLY, csdefine.VEHICLE_PET_QUALITY_DEITY]:
			if self.occupySpaceDF != csdefine.SPACE_TYPE_HIGH_DF:
				self.statusMessage( csstatus.ONLY_HIGH_DF_CAN_ENTER )
				return
		if self.petCageIsFull():
			self.statusMessage( csstatus.PET_CANNOT_GET_MORE )
			return
		if self.actionForbidSign( csdefine.ACTION_FORBID_CONJURE_PET ):
			self.statusMessage( csstatus.PET_CANNOT_HATCH_AS_STATE )
			return
		petObject = g_petFactory.getObject( scriptID )
		takeLevel = petObject.getEntityProperty( "takeLevel", 0 )
		if self.level < takeLevel:
			self.statusMessage( csstatus.PET_TAKE_LEVEL_NO_ENOUGH )
			return
		
		self.inquireMessage( csstatus.PET_EXCHAGE_EACH_OTHER, [], "exChangePet", int(uidStr) )
		return
			
		if self.lockPetOperation():
			KBEngine.globalData["SpaceLunHuiMiJinMgr"].petOutsideFromFence( self.base, self.playerDBID, int(uidStr) )
			
	def onPetOutsideFromFence( self, pet ):
		"""
		<define method>
		幻兽出栏
		"""
		self.petCages[pet.uid] = pet
		self.unlockPetOperation()
		self.petFenceVolume -= 1
		self.conjurePet(self.id, str(pet.uid) )
		
	def exChangePet( self, bSure, petUID ):
		"""
		出战幻兽进入兽栏
		兽栏里的幻兽，出栏
		"""
		if bSure:
			self.setTemp("EnterFencePet", self._activePetUID)
			self.setTemp("LeaveFencePet", petUID)
			self.withdrawPetByReason(csdefine.PET_WITHDRAW_EXCHANGE_FROM_FENCE)
	
	def generateOriginPet( self, srcEntityID, itemID ):
		"""
		<Exposed method>
		原兽入栏
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		if self.canEnterPetFence():
			item = g_itemFactory.createDynamicItem( itemID )
			scriptID, eggQuality, abilityRoll = item.getOriginPetData()
			if eggQuality in [csdefine.VEHICLE_PET_QUALITY_HOLY, csdefine.VEHICLE_PET_QUALITY_DEITY]:
				if self.occupySpaceDF != csdefine.SPACE_TYPE_HIGH_DF:
					self.statusMessage( csstatus.ONLY_HIGH_DF_CAN_ENTER )
					return
			
			pyItems = {}
			pyItems[csdefine.TRADE_PAY_ITEM_GOODS_BY_ID] = {itemID:1}
			pyItems[csdefine.TRADE_PAY_ITEM_GENERATE_ORIGIN_PET] = {"itemID":itemID}
			self.requestPay( csdefine.TRADE_TYPE_GENERATE_ORIGIN_PET , 0, pyItems, () )
	
	def onGenerateOriginPet( self ):
		""""""
		self.petFenceVolume += 1
		
	def onUpdateOriginPetVolume( self, volume):
		"""
		<define method>
		更新兽栏容量
		"""
		self.petFenceVolume = volume
		
	def onGetPetByKillPetCorral( self, originPet ):
		"""
		<define method>
		击杀兽栏，掉落原兽
		"""
		# 如果原兽进化了，走幻兽封印流程！否则，给原兽蛋
		if originPet.isEvolution():
			petObject = g_petFactory.getObject( originPet.scriptID )
			takeLevel = petObject.getEntityProperty( "takeLevel", 0 )
			sealItemID = formulas.getSealCharmItemID( int(originPet.scriptID), takeLevel, originPet.quality )
			param = {"dynamicData":{"pet":originPet}}
			if sealItemID:
				item = g_itemFactory.createDynamicItem( sealItemID, 1, param )
		else:
			spaceObj = g_objFactory.getSpaceObject( csconst.DONGFU_MAP_SPACESCRIPTID[csdefine.SPACE_TYPE_PRIVATE] )
			item = None
			for itemID in spaceObj.originPetEggItems:
				itemData = g_itemFactory.getItemData( itemID )
				if itemData["Param1"] == originPet.scriptID and itemData["Param2"] == str( originPet.quality ):
					item = g_itemFactory.createDynamicItem( itemID, 1, {} )
					break
			if item is None:
				KBEDebug.ERROR_MSG("config err!!space(%s) must be deploy param originPetEggItems"%csconst.DONGFU_MAP_SPACESCRIPTID[csdefine.SPACE_TYPE_PRIVATE])
				return
		pos = self.position + (random.random(), 0, random.random())
		dir = self.direction
		self.createEntityNear( "DropBox", pos, dir, {"modelNumber":"SM_DropBox", "modelScale":0.2, "ownershipIDs":[self.playerDBID], "allocationItems": {self.playerDBID: [item]}, "notAllocationItems": [], "allocation": 1} )