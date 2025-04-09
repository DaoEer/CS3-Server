# -*- coding: utf-8 -*-
import time, random
import KST
import KBEngine
from KBEDebug import *
import uuid
import KST_Config
class Account(
	KBEngine.Entity,
	):
	def __init__(self):
		"""
		"""
		KBEngine.Entity.__init__(self)
		
		DEBUG_MSG( "account entity %s created" % self.id )
		#self.base.requestSystemTime()
		self.base.requestInitRoles()
		
	def onStatusMessage(self, state, params):
		"""
		"""
		if state != 10001:
			ERROR_MSG( "%s: state = '%s', params = '%s'" % (self.id, state, params) )
		
		# re-create player
		if state == 10005:
			name = self.makePlayerName()
			DEBUG_MSG( "%s: creating player '%s'" % (self.id, name) )
			self.base.createRole(name, self.makeProfession(), self.makeCamp(), self.makeGender())
			
	def RequestInitRolesCB(self, playerDatas):
		"""
		@param playerDatas:	<Arg>	ARRAY <of>	PLAYER_DATA	</of>	</Arg>
		"""
		#DEBUG_MSG( "found player %s" % len( playerDatas["infos"]  ) )
		self.playerDatas = playerDatas["infos"] 
		if len( playerDatas["infos"] ):
			address = hex(uuid.getnode())[2:]
			self.base.login( playerDatas["infos"][0]["dbid"], address )
		else:
			name = self.makePlayerName()
			DEBUG_MSG( "%s: creating player '%s'" % (self.id, name) )
			self.base.createRole(name, self.makeProfession(), self.makeCamp(), self.makeGender())
	
	def AccountCreateCB(self):
		DEBUG_MSG( "accountCreateCB" )
		
	def TimeSynchronization(self, str):
		"""
		"""
		pass
		
	def AddRoleCB(self, playerData):
		"""
		@param playerData: PLAYER_DATA
		"""
		address = hex(uuid.getnode())[2:]
		DEBUG_MSG( "'%s(%s)' login now" % (playerData["dbid"], playerData["playerName"]) )
		self.base.login( playerData["dbid"], address)
		
	def DeleteRoleCB(self, playerDBID):
		"""
		"""
		pass
		
	def OnStatusMessageCB(self, state, params):
		"""
		"""
		if state != 10001:
			ERROR_MSG( "%s: state = '%s', params = '%s'" % (self.id, state, params) )
		
		# re-create player
		if state == 10005:
			n = self.makePlayerName()
			DEBUG_MSG( "%s: creating player '%s'" % (self.id, n) )
			self.base.createPlayer(n, self.makeProfession())
			
	def makeProfession(self):
		"""
		随机职业
		"""
		keys = [1,2,3,4]
		if KST_Config.profession in keys:
			return KST_Config.profession
		else:
			return random.choice(keys)
	
	def makePlayerName(self):
		"""		"""
		t = int( time.time() )
		return "p_%s_%s" % ( self.id, random.randint(1, 999))
		
	def makeCamp(self):
		"""
		随机阵营
		"""
		#如果是测试阵营副本，在这里平均分配阵营
		if KST_Config.aiPer.get("SpaceCampAI", 0) > 0:
			if "camp_1" not in KST.tempData:
				KST.tempData["camp_1"] = 0
			if "camp_2" not in KST.tempData:
				KST.tempData["camp_2" ] = 0
			
			if KST.tempData["camp_1"] > KST.tempData["camp_2" ]:
				KST.tempData["camp_2" ] += 1
				return 2
			
			KST.tempData["camp_1"] += 1
			return 1
		
		if KST_Config.camp in [1, 2]:
			return KST_Config.camp
		else:
			return random.randint(1,2)
		
	def makeGender(self):
		"""
		性别
		"""
		if KST_Config.gender in [1, 2]:
			return KST_Config.gender
		else:
			return random.randint(1,2)
		
	def CreateRoleCallback(self):
		pass
		
	def ReceiveWattingInfo( self, p1, p2, p3 ):
		ERROR_MSG("Account[%d] Login rank[%d], time[%s], count[%d]" %(self.id, p1, p2, p3))
		pass
	
	def OnCancelLoginQueue(self, p1):
		pass
	def GameTimeHasUsedUp( self ):
		pass
	def SetAccountInfo( self, p1 ):
		pass
		
	def RoleFrozenNotification(self, time):
		pass

	def onActivationKeyResult( self, p1 ):
		pass