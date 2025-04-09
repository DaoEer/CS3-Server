# -*- coding: utf-8 -*-

import KBEngine
import Const
import csstatus
import csdefine
import cschannel_msgs


class FrozenFightDatas( dict ):
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
		self[id]["player"] = player
		self[id]["name"] = name
		self[id]["camp"] = camp
		self[id]["kill"] = 0
		self[id]["dead"] = 0
		self[id]["assists"] = 0
		self[id]["occupy"] = 0
		self[id]["submits"] = 0
		self[id]["continuityKill"] = 0
		for _id, datas in self.items():
			player.client.CLIENT_AddFrozenFightMember( _id, datas["name"], datas["camp"] )
			if _id != id:
				datas["player"].client.CLIENT_AddFrozenFightMember( id, name, camp )
		
	def remove( self, id ):
		""""""
		if id in self:
			data = self.pop(id)
			data["player"].client.CLIENT_OnLeaveFrozenFight()
			
	def kill( self, diePlayerID, killerID ):
		""""""
		if diePlayerID == killerID:return
		if diePlayerID in self:
			if not killerID in self:			
				p = KBEngine.entities.get( killerID, None )
				if p and p.isEntityFlag( csdefine.ENTITY_FLAG_VEHICLEPET ):	# 幻兽杀死玩家
					killerID = p.baseOwner.id
				else:
					return

			self.checkAssists( killerID )
			killerData = self[killerID]
			diePlayerData = self[diePlayerID]
			oldContinuityKill = diePlayerData["continuityKill"]
			killerData["kill"] += 1
			killerData["continuityKill"] += 1
			diePlayerData["dead"] += 1
			diePlayerData["continuityKill"] = 0
			
			diePlayerData["player"].getCurrentSpace().playerBeKilled( diePlayerData["player"] )
			for data in self.values():
				data["player"].client.CLIENT_OnKillFrozenFight( diePlayerID, killerID )
			campStr = ""
			if killerData["camp"] == csdefine.CAMP_TAOSIM:
				campStr = cschannel_msgs.CAMP_TAOSIM
			else:
				campStr = cschannel_msgs.CAMP_DEMON
			if self.firstKill == 0:				# 首杀
				self.firstKill = killerID
				for data in self.values():
					data["player"].statusMessage( csstatus.SPARHUNTING_KILL_FIRST, campStr, killerData["name"] )
					data["player"].showMessagePlaySound(Const.KILL_VOICE)
					data["player"].client.CLIENT_OnFirstKill(killerData["name"])
			elif killerData["continuityKill"] == 5:		# 无人能挡
				for data in self.values():
					data["player"].statusMessage( csstatus.SPARHUNTING_NOBODY_COMBAT, campStr, killerData["name"] )
			elif killerData["continuityKill"] == 8:		# 疯狂杀戮
				for data in self.values():
					data["player"].statusMessage( csstatus.SPARHUNTING_CRAZY_KILL, campStr, killerData["name"] )
			elif killerData["continuityKill"] >= 12:		# 超神
				for data in self.values():
					data["player"].statusMessage( csstatus.SPARHUNTING_GOD_LIKE, campStr, killerData["name"] )
					data["player"].showMessagePlaySound(Const.KILL_VOICE)
					data["player"].client.CLIENT_OnGodLike(killerData["name"])
			
			if oldContinuityKill >= 12:			# 终结超神
				for data in self.values():
					data["player"].statusMessage( csstatus.SPARHUNTING_KILL_GOD_PLAYER, campStr, killerData["name"], diePlayerData["name"] )
					data["player"].showMessagePlaySound(Const.KILL_VOICE)
					data["player"].client.OnEndLegendary(killerData["name"])
					
	def checkAssists( self, id ):
		"""检查队友助攻"""
		killerData = self[id]
		temp = []
		for data in self.values():
			if data["camp"] == killerData["camp"] and data["id"] != id:
				dist = killerData["player"].position.distTo( data["player"].position )
				if dist <= 20:
					data["assists"] += 1
					temp.append( data["id"] )
		if temp:
			for data in self.values():
				data["player"].client.CLIENT_OnAssistsFrozenFight( temp )
				
	def occupyTower( self, id ):
		"""占领塔基"""
		self[id]["occupy"] += 1
		
	def occupyRevivePos( self, id ):
		"""占领复活点"""
		if id in self:
			self[id]["occupy"] += 1
		
	def submits( self, id, num ):
		"""提交冰晶数量"""
		if id in self:
			self[id]["submits"] += num
	
	#@classmethod
	def isSameType( self, obj ):
		return isinstance( obj, FrozenFightDatas )

g_FrozenFightDatas = FrozenFightDatas()