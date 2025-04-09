# -*- coding: utf-8 -*-

import csdefine
import csconst
import KBEDebug
#engine
import KBEngine
#cell
from ConfigObject.Skill.Buff.BuffReplace import BuffReplace


class BuffAircraft( BuffReplace ):
	"""
	飞行器（CST-5288）
	"""
	def __init__( self ):
		BuffReplace.__init__( self )
		self._flyMeshID = ""					# 飞行器meshID
		self.radius = 0.0
		self.height = csconst.AI_ENTITIES_IN_RANGE_HEIGHT
		self.scriptIDs = []
		self.entityType = ""
		self.removeStates = [csdefine.ENTITY_STATE_PEAD, csdefine.ENTITY_STATE_DEAD]
	def init( self, dictDat ):
		"""
		virtual method;
		读取buff配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		BuffReplace.init( self, dictDat )
		if self._loopTime == 0.0:		# CST-9200提供缺省支持
			self._loopTime = 1.0
		param5 = dictDat["Param5"].split("|")
		if param5[0] != "":
			self.radius = float(param5[0])
		if len(param5)>1:
			self.entityType = param5[1]
		if len(param5)>2:
			self.height = float(param5[2])
		self._flyMeshID = dictDat["Param3"]
		if dictDat["Param4"].strip()!="":
			self.scriptIDs = dictDat["Param4"].strip().split("|")
	def doBegin( self, receiver, buffData ):
		"""
		效果开始
		"""
		BuffReplace.doBegin( self, receiver, buffData )
		receiver.allClients.CLIENT_CreateAircraft(self._flyMeshID, receiver.id)
	
	def doLoop( self, receiver, buffData ):
		"""
		周期打击
		"""
		BuffReplace.doLoop( self, receiver, buffData )
		if receiver.enemyList:
			enemyID = receiver.findFirstEnemyByTime()
			receiver.allClients.CLIENT_AircraftUseSkill( receiver.id, enemyID)
		else:
			eid = self.detectionTarget( receiver )
			if eid:
				receiver.allClients.CLIENT_AircraftUseSkill( receiver.id, eid)
	def onClientActorCreate( self, receiver, buffData, srcEntityID ):
		"""
		virtual method
		receiver在某客户端被创建出来
		"""
		playerEntity = KBEngine.entities.get( srcEntityID )
		if not playerEntity: return
		try:
			clientEntity = playerEntity.clientEntity( receiver.id )
		except:
			clientEntity = None
		if clientEntity:
			clientEntity.CLIENT_CreateAircraft(self._flyMeshID, receiver.id)
	
	def doEnd( self, receiver, buffData,reason ):
		"""
		效果结束
		"""
		BuffReplace.doEnd( self, receiver, buffData,reason )
		receiver.allClients.CLIENT_RemoveAircraft( receiver.id)

	def detectionTarget( self , receiver ):
		eid = 0
		distance = 10000.0
		entities = receiver.entitiesInRangeExtForAI(self.radius, self.height, self.entityType, self.scriptIDs,self.removeStates  )
		for e in entities:
			if e.hasEffectState( csdefine.EFFECT_STATE_HIDE ):continue
			dis = receiver.position.flatDistTo(e.position)
			if distance > dis:
				eid = e.id
				distance = dis
		return eid



