# -*- coding: utf-8 -*-
import random, Math, time

import KBEngine
from KBEDebug import *

from PlayerAI.State.CStateInterface import CStateBase

#幻兽蛋ID
PET_ITEM_ID = 204010020
class CPetAI(CStateBase):
	"""
	"""
	def __init__(self, ai):
		CStateBase.__init__(self, ai)
		self.callbackID = 0
		self.hasAddPetItem = False
		
	def reset(self):
		"""
		"""
		self.resetCallBack()
		
	def resetCallBack(self):
		"""
		"""
		if self.callbackID:
			KBEngine.cancelCallback(self.callbackID)
			self.callbackID = 0
			
	def addCallBack(self, t, func):
		"""
		"""
		self.resetCallBack()
		self.callbackID = KBEngine.callback(t, func)
	
	def enter(self):
		"""
		"""
		#注册事件
		self.ai.owner.eventObj.registerEvent("Event_CPetAISys_onConjurePet", self)
		self.ai.owner.eventObj.registerEvent("Event_CPetAISys_onWithdrawPet", self)
		self.ai.owner.eventObj.registerEvent("Event_CPetAISys_onIsmountSuccess", self)
		
		self.conjugatePet()
		
	def leave(self):
		"""
		"""
		self.withdrawPet()
		self.reset()
		
		#反注册
		self.ai.owner.eventObj.unregisterEvent("Event_CPetAISys_onConjurePet", self)
		self.ai.owner.eventObj.unregisterEvent("Event_CPetAISys_onWithdrawPet", self)
		self.ai.owner.eventObj.unregisterEvent("Event_CPetAISys_onIsmountSuccess", self)
		
	def onEvent(self, name, *argv):
		"""
		"""
		if name == "Event_CPetAISys_onConjurePet":
			self.onConjurePet()
		elif name == "Event_CPetAISys_onWithdrawPet":
			self.onWithdrawPet()
		elif name == "Event_CPetAISys_onIsmountSuccess":
			self.onTransformPet()
			
	def conjugatePet(self):
		"""
		召唤
		"""
		if self.ai.owner.currentPetUID > 0:
			self.withdrawPet()
			return
			
		if len(self.ai.owner.petCages) <= 0:
			if not self.hasAddPetItem:
				self.ai.owner.GMCommand(self.ai.owner, "addItem", str(PET_ITEM_ID))
				self.hasAddPetItem = True
				self.addCallBack(3, self.conjugatePet)
				return
			else:
				items = self.ai.owner.items
				for itemOrder, item in items.items():
					if item.id == PET_ITEM_ID:
						self.ai.owner.cell.CELL_useItem( str(item.uid), str(self.ai.owner.id) )
						self.ai.owner.outputMsg("CELL_useItem")
						break
				
				self.addCallBack(3, self.conjugatePet)
				return
		else:
			self.ai.owner.GMCommand(self.ai.owner, "clearPetSleep")
			for k, v in self.ai.owner.petCages.items():
				#召唤宠物
				self.ai.owner.cell.conjurePet(str(k))
				self.ai.owner.outputMsg("conjurePet")
				return
		
	def onConjurePet(self):
		"""
		"""
		if self.ai.owner.currentPetUID <= 0:
			self.conjugatePet()
			return
		
		self.addCallBack(3, self.transformPet)
		
	def withdrawPet(self):
		"""
		回收
		"""
		if self.ai.owner.currentPetUID <= 0:
			self.conjugatePet()
			self.ai.owner.outputMsg("conjugatePet")
			return
		
		#回收幻兽
		self.ai.owner.cell.withdrawPet()
		self.ai.owner.outputMsg("withdrawPet")
		
	def onWithdrawPet(self):
		"""
		"""
		if self.ai.owner.currentPetUID > 0:
			self.withdrawPet()
			return
		
		self.addCallBack(3, self.conjugatePet)
		
	def transformPet(self):
		"""
		骑乘
		"""
		if self.ai.owner.currentPetUID <= 0:
			self.conjugatePet()
			return
		
		self.ai.owner.cell.transformPet()	
		self.ai.owner.outputMsg("transformPet")
		
	def onTransformPet(self):
		"""
		"""
		self.withdrawPet()
