# -*- coding: utf-8 -*-
import KBEDebug
import KBEngine
class RolePetInterface:
	"""
	"""
	def __init__(self):
		self.isInitPets = False
		self.petCages = {}
		self.currentPetUID = 0
		
	def isMountOnPet(self):
		"""
		是否处于骑乘状态
		"""
		return self.carrierId
		
	def resetPet(self):
		for uid in self.petCages.keys():
			self.cell.freePet(uid)
			self.outputMsg("freePet {}".format(uid))
			
	def initClientPetDataFinish(self):
		self.isInitPets = True
		
	def PetAddData(self, petData):
		uid = int(petData["uid"])
		self.petCages[ uid ] = petData
		
	def getPetbySID(self, scriptID):
		for p in self.petCages.values():
			if p.scriptID == scriptID:
				return p.uid
		return ""
		
	def PetRemoveData(self,uid):
		self.petCages.pop(int(uid))
		
	def OnGeneratePet(self, petData):
		uid = int(petData["uid"])
		self.petCages[ uid ] = petData
		
	def onConjurePetResult( self, uid, petEntityid ):
		"""
		召唤成功
		"""
		self.currentPetUID = int(uid)
		self.eventObj.fireEvent("Event_CPetAISys_onConjurePet")
		
	def onWithdrawPetResult(self):
		"""
		回收宠物
		"""
		self.currentPetUID = 0
		self.eventObj.fireEvent("Event_CPetAISys_onWithdrawPet")
	
	def updatePetEpitomeDatas( self, uid, attrName, value ):
		pass
		
	def OnPetReNameFail( uid , result):
		pass
	
	def petOnSetAttackState( self , AICurrentState):
		pass
		
	def OnSealSuccess(self):
		pass
		
	def OnComposePet( self, uid, int1 ):
		pass
		
	def OnPetComposeFailed( self, msgID, flag ):
		pass
		
	def OnReplacePetSkill(self):
		pass
			
	def OnIsmountSuccess(self, b1):
		"""
		"""
		self.eventObj.fireEvent("Event_CPetAISys_onIsmountSuccess")
		
	def OnUpgradePetSkill( self, msgID, flag ):
		pass
		
	def OnReplacePetPassiveSkill(self):
		pass
			
	def OnUpgradePetPassiveSkill( self, msgID, flag ):
		pass
		
	def OnGetSealPetEggAttr(self, params):
		pass
		
	def OnAIStopCommand(self):
		pass
		
		
	def CLIENT_OnPetExtraHPChanged( self, p1, p2 ):
		pass
	def CLIENT_OnPetExtraMPChanged( self, p1, p2 ):
		pass
	def CLIENT_OnFeedPetExp( self, p1, p2 ):
		pass
	def CLIENT_OnFreePetFromFence( self, p1 ):
		pass
	def CLIENT_addOriginPet( self, p1 ):
		pass
	def CLIENT_OnFeedPetWildness( self, p1, p2 ):
		pass
	def CLIENT_onEvolutionPet( self, p1 ):
		pass
	def CLIENT_OnSetActivePetExp( self, p1 ):
		pass
	def CLIENT_OnPetOutsideFromFence( self, p1 ):
		pass
	def CLIENT_openOriginPetUI( self, p1, p2 ):
		pass
	def CLIENT_clearPetCDTime( self ):
		pass
	def CLIENT_showOriginPetModel( self, p1 ):
		pass
	def CLIENT_OnRemoveOriginPetModel( self, p1, p2 ):
		pass
	def CLIENT_OnActivePetEnterFence( self, p1 ):
		pass
	def CLIENT_OnExChangePetFromFence( self, p1, p2 ):
		pass
	def CLIENT_OnExChangeOriginPetModel( self, p1, p2 ):
		pass
	def CLIENT_OnAddOriginPetModel( self, p1 ):
		pass
	def updateOriginPetEpitomeDatas( self, p1, p2, p3 ):
		pass
	def OnChangePetAI(self, p1):
		pass
	def OnFinishChangePetAI(self):
		pass
		
