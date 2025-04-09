# -*- coding: utf-8 -*-

import KBEngine
import Const
import csstatus
import csdefine
import KBEngine
import cschannel_msgs

GENERAL_MONSTER_ID = 0				# 将领的entityID

class TrainingGroundImp( dict ):
	#FIXED_DICT dict
	def __init__( self ):
		dict.__init__( self )
	
	@classmethod
	def getDictFromObj( self, obj ):
		datalist = []
		for id, _dict in obj.items():
			datalist.append( _dict )
			
		return { "dictData" : datalist }
		
	#@classmethod
	def createObjFromDict( self, dict ):
		obj = self.__class__()
		for r in dict[ "dictData" ]:
			id = r["id"]
			obj[id] = r
			
		return obj
	
	def add( self, player, id, name, belongSide ):
		""""""
		if id in self:
			for _id, datas in self.items():
				player.client.CLIENT_AddTrainingGroundMember( datas["id"], datas["name"], datas["belongSide"] )
			return
			
		self[id] = {}
		self[id]["id"] = id
		self[id]["name"] = name
		self[id]["belongSide"] = belongSide		# 攻方/防方
		self[id]["kill"] = 0
		self[id]["killMt"] = 0
		self[id]["dead"] = 0
		self[id]["loseSD"] = 0
		if player is None:return			# 因为防守boss，也加进来了
		for _id, datas in self.items():
			player.client.CLIENT_AddTrainingGroundMember( datas["id"], datas["name"], datas["belongSide"] )
			if id != _id:
				otherPlayer = KBEngine.entities.get( _id )
				if otherPlayer and otherPlayer.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ):
					otherPlayer.client.CLIENT_AddTrainingGroundMember( id, name, belongSide )
		
	def remove( self, id ):
		""""""
		if id in self:
			data = self.pop(id)
			
	def kill( self, diePlayerID, killerID ):
		""""""
		if diePlayerID == killerID:return
		
		if diePlayerID in self:
			self[diePlayerID]["dead"] += 1
			self.updateClientDeadData( diePlayerID )
		p = KBEngine.entities.get( killerID, None )
		if p and p.isEntityFlag( csdefine.ENTITY_FLAG_VEHICLEPET ):	# 幻兽杀死
			killerID = p.baseOwner.id
		if p and p.isEntityFlagExt(csdefine.ENTITY_FLAG_MONSTER_CTRL_BY_CLIENT):	# 玩家带领士兵
			killerID = p.controlEntityID
			
		if not killerID in self and GENERAL_MONSTER_ID in self:
			killerID = GENERAL_MONSTER_ID
			
		if killerID in self:
			if diePlayerID in self:
				self[killerID]["kill"] += 1
				self.updateClientKillData( killerID )
			else:
				self[killerID]["killMt"] += 1
				self.updateClientKillMTData( killerID )
			
				
	def killSD( self, diePlayerID, killerID ):
		"""杀死士兵"""
		sdEntity = KBEngine.entities.get(diePlayerID)
		if sdEntity.isEntityFlagExt(csdefine.ENTITY_FLAG_MONSTER_CTRL_BY_CLIENT):
			if sdEntity.controlEntityID in self:
				self[sdEntity.controlEntityID]["loseSD"] += 1
				controlEntity = sdEntity.getControlEntity()
				if controlEntity:
					controlEntity.client.CLIENT_updateLBCLoseSDData(sdEntity.controlEntityID, self[sdEntity.controlEntityID]["loseSD"])
			p = KBEngine.entities.get( killerID, None )
			if p and p.isEntityFlag( csdefine.ENTITY_FLAG_VEHICLEPET ):	# 幻兽杀死
				killerID = p.baseOwner.id
			if p and p.isEntityFlag(csdefine.ENTITY_FLAG_MONSTER_CTRL_BY_CLIENT):	# 玩家带领士兵
				killerID = p.controlEntityID
			if killerID in self:
				self[killerID]["killMt"] += 1
				self.updateClientKillMTData( killerID )
			elif GENERAL_MONSTER_ID in self:									# 因为pve中，怪物将领加进来了
				self[GENERAL_MONSTER_ID]["killMt"] += 1
				self.updateClientKillMTData( GENERAL_MONSTER_ID )
		
	def killGeneral( self, diePlayerID, killerID ):
		"""将领被杀死 kill的计算不在这里"""
		if GENERAL_MONSTER_ID in self:
			self[GENERAL_MONSTER_ID]["dead"] += 1
			self.updateClientDeadData( GENERAL_MONSTER_ID )
			
		p = KBEngine.entities.get( killerID, None )
		if p and p.isEntityFlag( csdefine.ENTITY_FLAG_VEHICLEPET ):	# 幻兽杀死
			killerID = p.baseOwner.id
		if p and p.isEntityFlagExt(csdefine.ENTITY_FLAG_MONSTER_CTRL_BY_CLIENT):	# 玩家带领士兵
			killerID = p.controlEntityID
		if killerID in self:
			self[killerID]["kill"] += 1
			self.updateClientKillData( killerID )
		
	def updateClientDeadData( self, id ):
		""""""
		num = self[id]["dead"]
		for _id, datas in self.items():
			player = KBEngine.entities.get( _id )
			if player and player.client:
				player.client.CLIENT_updateLBCDeadData( id, num )
		
	def updateClientKillData( self, id ):
		""""""
		num = self[id]["kill"]
		for _id, datas in self.items():
			player = KBEngine.entities.get( _id )
			if player and player.client:
				player.client.CLIENT_updateLBCKillData( id, num )
				
	def updateClientKillMTData( self, id ):
		""""""
		num = self[id]["killMt"]
		for _id, datas in self.items():
			player = KBEngine.entities.get( _id )
			if player and player.client:
				player.client.CLIENT_updateLBCKillMTData( id, num )
				
	#@classmethod
	def isSameType( self, obj ):
		return isinstance( obj, TrainingGroundImp )

instance = TrainingGroundImp()