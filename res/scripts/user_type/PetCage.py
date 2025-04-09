# -*- coding: utf-8 -*-


class PetCage( dict, ):
	def __init__(self):
		dict.__init__( self )

	def add(self, key, pet):
		assert key not in self,\
			"Pet %i has been aleady in pet cage." % key
		self[key] = pet

	def pets(self):
		return self.values()
	
	@classmethod
	def getDictFromObj(self, cage):
		""""""
		data = {}
		pets = []
		for pet in cage.pets():
			pets.append(pet)
			
		data["pets"] = pets
		return data
	
	@classmethod
	def createObjFromDict(self, dict):
		cage = PetCage()
		for pet in dict["pets"]:
			cage[ pet.uid ] = pet
		return cage
	
	@classmethod
	def isSameType(self, obj):
		return isinstance(obj, PetCage)

class PetFence( dict, ):
	def __init__(self):
		dict.__init__( self )

	def add(self, key, pet):
		assert key not in self,\
			"Pet %i has been aleady in pet cage." % key
		self[key] = pet

	def pets(self):
		return self.values()
	
	@classmethod
	def getDictFromObj(self, cage):
		""""""
		data = {}
		pets = []
		for pet in cage.pets():
			pets.append(pet)
			
		data["pets"] = pets
		return data
	
	@classmethod
	def createObjFromDict(self, dict):
		cage = PetFence()
		for pet in dict["pets"]:
			cage[ pet.uid ] = pet
		return cage
	
	@classmethod
	def isSameType(self, obj):
		return isinstance(obj, PetFence)

class PlayerPetFence( dict, ):
	def __init__(self):
		dict.__init__( self )
	
	def addPet( self, playerDBID, pet ):
		""""""
		if not playerDBID in self:
			self[playerDBID] = {}
		self[playerDBID].update( {pet.uid : pet } )
		
	def popPet( self, playerDBID, uid ):
		""""""
		if playerDBID in self and uid in self[playerDBID]:
			pet = self[playerDBID].pop( uid )
			if not self[playerDBID]:
				self.pop( playerDBID )
			return pet
		KBEDebug.ERROR_MSG("Can not find playerDBID in PetFence?(%s) or uid not in cage?(%s)"%(playerDBID in self, uid in self[playerDBID] if playerDBID in self else False))
		return None
	
	def getPet( self, playerDBID, uid ):
		""""""
		if playerDBID in self:
			if uid in self[playerDBID]:
				return self[playerDBID][uid]
			else:
				KBEDebug.ERROR_MSG("Can not find playerDBID(%d) in petFence!"%playerDBID)
		else:
			KBEDebug.ERROR_MSG("Can not find uid(%d) in PetFence!"%uid)
		return None
	
	def getPetSimpleData( self, playerDBID ):
		""""""
		datas = []
		if playerDBID in self:
			for uid, pet in self[playerDBID].items():
				temp = {}
				temp["uid"] = uid
				temp["scriptID"] = pet.scriptID
				temp["quality"] = pet.quality
				temp["bEvolution"] = pet.isEvolution()
				datas.append( temp )
		return datas
	
	def getPetNum( self, playerDBID ):
		"""获取多少只幻兽"""
		if playerDBID in self:
			return len( self[playerDBID] )
		return 0
	
	@classmethod
	def getDictFromObj(self, cage):
		""""""
		data = {}
		data["pPets"] = []
		for dbid, pets in cage.items():
			temp = {}
			temp["playerDBID"] = dbid
			temp["pets"] = list(pets.values())
			data["pPets"].append( temp )
			
		return data
	
	@classmethod
	def createObjFromDict(self, dict_):
		cage = PlayerPetFence()
		for playerPets in dict_["pPets"]:
			cage[ playerPets["playerDBID"] ] = {}
			for pet in playerPets["pets"]:
				cage[ playerPets["playerDBID"] ].update( { pet.uid : pet } )
		return cage
	
	@classmethod
	def isSameType(self, obj):
		return isinstance(obj, PlayerPetFence)

instance = PetCage()
petFenceInst = PetFence()
playerPetFenceInst = PlayerPetFence()