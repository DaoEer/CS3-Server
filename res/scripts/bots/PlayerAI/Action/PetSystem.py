# -*- coding: utf-8 -*-

import KBEngine
import KBEDebug

from PlayerAI.Action.ActionBase import ActionBase

class WithdrawPet(ActionBase):
	"""
	回收幻兽
	"""
	def doAction(self, role, param):
		"""
		"""
		ActionBase.doAction(self, role, param)
		if role.currentPetUID <= 0:
			KBEDebug.ERROR_MSG("role no pet")
			return
	
		role.cell.withdrawPet()
		
class ConjurePet(ActionBase):
	"""
	召唤幻兽
	"""	
	def doAction(self, role, param):
		"""
		"""
		ActionBase.doAction(self, role, param)
		if role.currentPetUID > 0:
			KBEDebug.ERROR_MSG("role has conjure pet")
			return
			
		if len(role.petCages) <= 0:
			KBEDebug.ERROR_MSG("no pet")
			return
			
		role.GMCommand(role, "clearPetSleep")
		for k, v in role.petCages.items():
			#召唤宠物
			role.cell.conjurePet(str(k))
			return 
			
class TransformPet(ActionBase):
	"""
	上/下马
	"""	
	def doAction(self, role, param):
		"""
		"""
		ActionBase.doAction(self, role, param)	
		role.cell.transformPet()
		
ActionBase.setClass("TransformPet", TransformPet)
ActionBase.setClass("ConjurePet", ConjurePet)
ActionBase.setClass("WithdrawPet", WithdrawPet)

		