# -*- coding: utf-8 -*-

import KBEngine
import Const
import csstatus
import csdefine
import KBEngine
import cschannel_msgs


class FHLTMemberDatas( dict ):
	#FIXED_DICT dict
	def __init__( self ):
		dict.__init__( self )
		self.firstKill = 0
	
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
	
	def add( self, player, id, name, camp ):
		""""""
		self[id] = {}
		self[id]["id"] = id
		self[id]["name"] = name
		self[id]["camp"] = camp
		self[id]["kill"] = 0
		self[id]["dead"] = 0
		self[id]["assists"] = 0
		self[id]["continuityKill"] = 0
		for _id, datas in self.items():
			player.client.OnAddFHLTMember( _id, datas["name"], datas["camp"] )
			if _id != id:
				otherPlayer = KBEngine.entities.get( _id )
				if otherPlayer:
					otherPlayer.client.OnAddFHLTMember( id, name, camp )
		
	def remove( self, id ):
		""""""
		if id in self:
			data = self.pop(id)
			player = KBEngine.entities.get( id )
			if player and player.client:
				player.client.OnLeaveFHLT()
			
	def kill( self, diePlayerID, killerID ):
		""""""
		if diePlayerID == killerID:return
		if diePlayerID in self:
			if not killerID in self:			
				p = KBEngine.entities.get( killerID, None )
				if p and p.isEntityFlag( csdefine.ENTITY_FLAG_VEHICLEPET ):	# 幻兽杀死玩家
					killerID = p.baseOwner.id
				else:			
					self[diePlayerID]["dead"] += 1			# 被boss杀死
					self[diePlayerID]["continuityKill"] = 0
					for data in self.values():
						player = KBEngine.entities.get( data["id"] )
						if player and player.client:
							player.client.OnKillFHLT( diePlayerID, killerID )
					return

			self.checkAssists( killerID )
			killerData = self[killerID]
			diePlayerData = self[diePlayerID]
			oldContinuityKill = diePlayerData["continuityKill"]
			killerData["kill"] += 1
			killerData["continuityKill"] += 1
			diePlayerData["dead"] += 1
			diePlayerData["continuityKill"] = 0
			
			killer = KBEngine.entities.get( killerID )
			if killer:
				killer.getCurrentSpace().onMemberKillPlayer( killer )
			for data in self.values():
				player = KBEngine.entities.get( data["id"] )
				if player and player.client:
					player.client.OnKillFHLT( diePlayerID, killerID )
			campStr = ""
			if killerData["camp"] == csdefine.CAMP_TAOSIM:
				campStr = cschannel_msgs.CAMP_TAOSIM
			else:
				campStr = cschannel_msgs.CAMP_DEMON
			if self.firstKill == 0:				# 首杀
				self.firstKill = killerID
				for data in self.values():
					player = KBEngine.entities.get( data["id"] )
					if player and player.client:
						player.statusMessage( csstatus.SPARHUNTING_KILL_FIRST, campStr, killerData["name"] )
						player.showMessagePlaySound(Const.KILL_VOICE)
						player.client.CLIENT_OnFirstKill(killerData["name"])
			elif killerData["continuityKill"] == 5:		# 无人能挡
				for data in self.values():
					player = KBEngine.entities.get( data["id"] )
					if player and player.client:
						player.statusMessage( csstatus.SPARHUNTING_NOBODY_COMBAT, campStr, killerData["name"] )
			elif killerData["continuityKill"] == 8:		# 疯狂杀戮
				for data in self.values():
					player = KBEngine.entities.get( data["id"] )
					if player and player.client:
						player.statusMessage( csstatus.SPARHUNTING_CRAZY_KILL, campStr, killerData["name"] )
			elif killerData["continuityKill"] >= 12:		# 超神
				for data in self.values():
					player = KBEngine.entities.get( data["id"] )
					if player and player.client:
						player.statusMessage( csstatus.SPARHUNTING_GOD_LIKE, campStr, killerData["name"] )
						player.showMessagePlaySound(Const.KILL_VOICE)
						player.client.CLIENT_OnGodLike(killerData["name"])
			
			if oldContinuityKill >= 12:			# 终结超神
				for data in self.values():
					player = KBEngine.entities.get( data["id"] )
					if player and player.client:
						player.statusMessage( csstatus.SPARHUNTING_KILL_GOD_PLAYER, campStr, killerData["name"], diePlayerData["name"] )
						player.showMessagePlaySound(Const.KILL_VOICE)
						player.client.CLIENT_OnEndLegendary(killerData["name"])
					
	def checkAssists( self, id ):
		"""检查队友助攻"""
		killerData = self[id]
		temp = []
		for data in self.values():
			if data["camp"] == killerData["camp"] and data["id"] != id:
				srcPlayer = KBEngine.entities.get( id )
				dstPlayer = KBEngine.entities.get( data["id"])
				if srcPlayer and dstPlayer:
					dist = srcPlayer.position.distTo( dstPlayer.position )
					if dist <= 20:
						data["assists"] += 1
						temp.append( data["id"] )
		if temp:
			for data in self.values():
				player = KBEngine.entities.get( data["id"] )
				if player and player.client:
					player.client.OnAssistsFHLT( temp )
	
	#@classmethod
	def isSameType( self, obj ):
		return isinstance( obj, FHLTMemberDatas )

g_FHLTMemberDatas = FHLTMemberDatas()