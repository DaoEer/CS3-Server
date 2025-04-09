# -*- coding: utf-8 -*-
"""
用于空间的基类
"""
import KBEDebug
import KBEngine
import KST
from CoreObject.HasCellOjbect import HasCellOjbect
from CoreInterface.SpawnInterface import SpawnInterface
import csdefine
import Settings

import KBEDebug

class SpaceObject( KBEngine.Entity, HasCellOjbect, SpawnInterface ):
	def __init__( self ):
		KBEngine.Entity.__init__( self )
		HasCellOjbect.__init__( self )
		SpawnInterface.__init__( self )
		self.scriptID = self.cellData[ "scriptID" ]
		self.spaceNumber = self.cellData[ "spaceNumber" ]
		self._enters = []
		self._logons = []
		self._createTimes = 0	#计数器
		self.createSpaceCell()
	
		
	def initEntityFlag( self ):
		self.entityFlag = csdefine.ENTITY_FLAG_SPACE
	
	def createSpaceCell( self ):
		"""
		"""	
		if self.cid < 0: KBEDebug.ERROR_MSG("space(%s) create cell error, cid(%d) error" %(self.scriptID, self.cid))
		cellIndex = (KST.temp_cellApps.get(self.cid, {})).get("groupID", 0)
		self.createCellEntityInNewSpace( cellIndex )
		
	def getScript( self ):
		return KST.g_objFactory.getSpaceObject( self.scriptID )
	
	def createLoginRoleCell( self, roleBase ):
		roleBase.createCellFromSpace( self.cell )

#-----------------传送------------------------------------------

	def pushPlayerToEnterList( self, playerbase, position, direction, packArgs ):
		"""
		压入等待进入的玩家
		"""
		self._enters.append( ( playerbase, position, direction, packArgs ) )
		self.onProcessEnterTimer()
		
	def registerLogonPlayer( self, playerbase ):
		"""
		<Define method>
		注册在这个space登陆的玩家
		"""
		self._logons.append( playerbase )
		self.onProcessEnterTimer()
	
	def onProcessEnterTimer( self ):
		"""
		检查进入
		"""
		if not self.isCellCreate():
			return

		if len( self._logons ) > 0:
			self.createLoginRoleCell( self._logons.pop( 0 ) )
		elif len( self._enters ) > 0:
			playerbase, position, direction, packArgs = self._enters.pop( 0 )
			self._teleportEntity( playerbase, position, direction, packArgs )
			
		if len( self._logons ) > 0 or len( self._enters ) > 0:#防止一下子过多人进入导致服务器出问题，这个进行了一个排除机制
			self.addTimerCallBack( 0.1, "onProcessEnterTimer", () )
	
	def teleportEntity( self, roleBase, position, direction, packArgs ):
		"""
		<define method>
		送到玩家
		"""
		self.pushPlayerToEnterList( roleBase, position, direction, packArgs )

	def _teleportEntity( self, roleBase, position, direction, packArgs ):
		"""
		传送玩家
		"""
		self.getScript().teleportEntity( self, roleBase, position, direction, packArgs )

#-----------------引擎回调------------------------------------------
	
	def onLoseCell( self ):
		"""
		CELL丢失
		"""
		if self.cellData:
			del self.cellData
			
		HasCellOjbect.onLoseCell( self )
		self.spaceMgrMB.onSpaceLoseCell( self.scriptID, self.spaceNumber )

	def onGetCell( self ):
		"""
		CELL创建完成
		"""
		HasCellOjbect.onGetCell( self )
		self.spaceMgrMB.onSpaceCreateCell( self.scriptID, self.spaceNumber, self )
		self.onProcessEnterTimer()
		
	def globalWorld( self, messageType, messageArg ):
		"""
		cell过来的消息广播
		"""
		KST.g_baseAppEntity.globalWold(messageType, messageArg)
		