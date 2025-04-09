# -*- coding: utf-8 -*-
#python
import math
import Math
#engine
import KBEngine
import KBEMath
#common
import csdefine
#cell
from MovingPlatform import MovingPlatform

class MovingPlatformVehicle( MovingPlatform ):
	"""
	可移动载具(多人载具)
	"""
	def __init__( self ):
		MovingPlatform.__init__( self )
		self.removeFlag(csdefine.FLAG_MESH_COLLISION)
		self.removeFlag(csdefine.FLAG_OPEN_GROUND_TRACE_COLLISION_CHANNEL)
		self.driverID = 0		#司机EntityID
		self.passengerIDList = []	#乘客EntityID列表
		self.moveSpeed = self.getSpeed()
		self.gossipScriptID = ""	#交互对象的脚本ID

	def onWitnessed( self, isWitnessed ):
		"""
		玩家视野范围内才开始执行
		"""
		if isWitnessed:
			pass
		
	def CELL_onClientReady( self, srcEntityID ):
		"""
		<Expose method>
		客户端Character Actor已经准备好
		"""
		pass
		
	def beforeDestroy( self ):
		"""
		virtual method
		销毁前做一些事
		"""
		if self.driverID != 0:
			self._removeVehicleDiver()
		
	def _setVehicleDiver( self, diverID ):
		"""
		设置司机ID
		"""
		self.driverID = diverID
		if self.driverID != 0:
			player = KBEngine.entities.get(self.driverID,None)
			if player and player.getClient():
				self.controlledBy = player.base
				player.parent = self
				#player.direction = self.direction
				player.vehicleId = self.id
				#player.position = self.position
				player.onBeforeMountVehicle( self.id )
				self._onAddBuff(player)
				player.allClients.CLIENT_OnMountVehicle( self.id, self.driverID, self.getScript().socketList[0], self.getScript().riderModelId, self.getScript().childrenCanMove )	#广播到AOI的所有玩家上载具
		
	def _removeVehicleDiver( self ):
		"""
		删除司机
		"""
		player = KBEngine.entities.get(self.driverID,None)
		if player and player.getClient():
			player.parent = None
			player.vehicleId = 0
			player.allClients.CLIENT_OnDismountVehicle( self.id )	#广播到AOI的所有玩家下载具
			player.position = self.position + Math.Vector3(0.0, 0.0, 3.0)
			self._onRemoveBuff(player)
			self.driverID = 0
			player.onAfterDismountVehicle( self.id )
		for passengerID in self.passengerIDList:
			passenger = KBEngine.entities.get(passengerID,None)
			if passenger and passenger.getClient():
				passenger.parent= None
				passenger.vehicleId = 0
				passenger.allClients.CLIENT_OnDismountVehicle( self.id ) ##广播到AOI的所有玩家下载具
				passenger.position = self.position + Math.Vector3(0.0, 0.0, 3.0)
				self._onRemoveBuff(passenger)
				passenger.onAfterDismountVehicle( self.id )
		self.passengerIDList.clear()
		self._createGossipEntity()
		self.destroySelf()
		
	def _addPassenger( self, passengerID ):
		"""
		增加乘客
		"""
		if passengerID != 0:
			if passengerID not in self.passengerIDList:
				passenger = KBEngine.entities.get(passengerID,None)
				if passenger and passenger.getClient():
					self.passengerIDList.append( passengerID )
					passenger.parent = self
					#passenger.direction = self.direction
					passenger.vehicleId = self.id
					#passenger.position = self.position
					passenger.onBeforeMountVehicle( self.id )
					self._onAddBuff(passenger)
					passenger.allClients.CLIENT_OnMountVehicle( self.id, self.driverID, self.getScript().socketList[(len(self.passengerIDList))], self.getScript().riderModelId, self.getScript().childrenCanMove )	#通知乘客
	
	def _removePassenger( self, passengerID ):
		"""
		删除乘客
		"""
		if passengerID != 0:
			if passengerID in self.passengerIDList:
				self.passengerIDList.remove( passengerID )
				passenger = KBEngine.entities.get(passengerID,None)
				if passenger and passenger.getClient():
					passenger.parent = None
					passenger.vehicleId = 0
					passenger.allClients.CLIENT_OnDismountVehicle( self.id )	#通知乘客
					passenger.position = self.position + Math.Vector3(0.0, 0.0, 3.0)
					self._onRemoveBuff(passenger)
					passenger.onAfterDismountVehicle( self.id )
	
	def _createGossipEntity( self ):
		if self.gossipScriptID != "":
			spellBoxEntity = self.createEntityByScriptID( self.gossipScriptID, self.position,self.direction,{ "spawnPos":tuple(self.position)} )

	def _onAddBuff(self, player):
		if not self.getScript().triggerBuffs:
			return
		for buffID in self.getScript().triggerBuffs:
			indexList = player.findBuffsByBuffID(buffID)
			if indexList:
				continue
			else:
				player.addBuff(player, buffID)

	def _onRemoveBuff(self, player):
		if not self.getScript().triggerBuffs:
			return
		for buffID in self.getScript().triggerBuffs:
			player.removeBuffByID(buffID)

#-------------------------------remote call-------------------------------
	def gossipMountVehicle( self, requestID, spellboxScriptID):
		"""
		<define method>
		与spellBox交互上载具
		"""
		self.gossipScriptID = spellboxScriptID
		self.mountVehicle(requestID)
		
	def mountVehicle( self, requestID ):
		"""
		<define method>
		上载具
		"""
		if requestID == 0:
			return
		request = KBEngine.entities.get( requestID, None )
		if not request:
			return
		if request.carrierId or request.vehicleId:
			request.statusMessage( csstatus.VEHICLE_TO_MOUNT_CANNOT_GOSSIP )#骑乘状态不能上载具
			return
		if self.driverID == 0:
			self._setVehicleDiver( requestID )	#第一个上载具的是司机
		else:
			if len(self.passengerIDList) +1 >= self.getScript().maxNum:
				request.statusMessage( csstatus.VEHICLE_NUM_TO_REACH_FULL )#共同骑乘人数已满，申请失败
			else:
				self._addPassenger( requestID )
		
	def dismountVehicle( self, requestID ):
		"""
		<define method>
		下载具
		"""
		if requestID == 0:
			return
		if requestID == self.driverID:
			self._removeVehicleDiver()
		else:
			self._removePassenger( requestID )
	
	def reqVehicleData( self, requestID, targetPlayerID):
		"""
		<define method>
		请求目标entity的载具数据
		"""
		request = KBEngine.entities.get( requestID, None )
		if not request:
			return
		targetPlayer = KBEngine.entities.get( targetPlayerID, None )
		if not targetPlayer:
			return
		if not request.isEntityInView(targetPlayer):
			return
		
		if targetPlayerID == self.driverID:
			request.clientEntity( targetPlayerID ).CLIENT_OnMountVehicle( self.id, self.driverID, self.getScript().socketList[0], self.getScript().riderModelId, self.getScript().childrenCanMove )	#通知请求者的客户端上的目标玩家上载具
		elif targetPlayerID in self.passengerIDList:
			request.clientEntity( targetPlayerID ).CLIENT_OnMountVehicle( self.id, self.driverID, self.getScript().socketList[(self.passengerIDList.index(targetID)+1)], self.getScript().riderModelId, self.getScript().childrenCanMove )	#通知请求者的客户端的目标玩家上载具
		else:
			return