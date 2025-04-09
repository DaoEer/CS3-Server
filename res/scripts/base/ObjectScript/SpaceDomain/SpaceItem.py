# -*- coding: utf-8 -*-
import KBEngine
import Functions
import ObjectScript

import KST

class SpaceItem:
	def __init__( self, domainObj, number, cid, params ):
		self.domainObj = domainObj			# 记录包含自己的SpaceDomain
		self.spaceNumber = number			# 空间ID
		self.cid = cid						# 创建在指定的cellapp（0：未指定）
		self.belongType = params.pop( "belongType" )	# 副本归属类型
		self.spaceKey = params.pop( "spaceKey" )		# 副本归属key
		self.createArgs = params			# dict, 记录了与此space相关的额外参数，如进入此space的同一条件(由SpaceItem创建时传递进来决定)
		self.spaceMailBox = None			# 空间的BASE mailbox
		self.hasBase = False
		self.baseCreateing = False			# 当前space base是否在创建中
		self.hasCell = False				# 是否存在cell标志
		self.cellCreateing = False			# 当前space是否在创建中
		self._enterPlayers = []				# 要进入空间的玩家数据: [(),...]
		self._loginPlayers = []				# 要上线进入空间的玩家数据: [Base,...]

	def createBase( self, callBack ):
		"""
		创建domain实体
		"""
		if self.baseCreateing or self.hasBase:
			return

		self.baseCreateing = True
		dict = { "spaceMgrMB" : KBEngine.globalData["SpaceManager"], "spaceNumber": self.spaceNumber, "cid": self.cid, "belongType": self.belongType, "spaceKey": self.spaceKey, "createArgs": self.createArgs }
		KST.g_objFactory.getSpaceObject( self.domainObj.scriptID ).createAnywhereEntity( dict, Functions.Functor( self.onCreateBaseCallback_, callBack ) )
		
	def onCreateBaseCallback_( self, callBack, base ):
		"""
		create domain call back
		@param 	base	:		domain entity base
		@type 	base	:		mailbox
		"""
		if not base:
			return
			
		self.spaceMailBox = base
		self.baseCreateing = False
		self.hasBase = True
		if callBack:
			callBack( self, base )

	def onLoseCell( self ):
		"""
		cell关闭
		"""
		self.hasCell = False

	def onGetCell( self ):
		"""
		space获得了cell部份，执行状态改变，并把需要进入space的玩家传到space中
		"""
		self.hasCell = True
		self.cellCreateing = False
		
		for playerBase, position, direction, pickData in self._enterPlayers:
			self.spaceMailBox.teleportEntity( playerBase, position, direction, pickData )

		for playerBase in self._loginPlayers:
			self.spaceMailBox.registerLogonPlayer( playerBase )
			
		self._enterPlayers = []
		self._loginPlayers = []

	def addToEnterList( self, playerBase, position, direction, pickData ):
		"""
		添加进入空间的玩家记录
		"""
		self._enterPlayers.append( ( playerBase, position, direction, pickData ) )
			
	def addToLogonList( self, playerBase ):
		"""
		添加在空间上线的玩家记录
		@param 	playerBase	:		玩家的base
		@type 	playerBase	:		mailbox
		"""
		self._loginPlayers.append( playerBase )
		
#-----------------------------------------------------------------------------
	def enter( self, playerBase, position, direction, pickData ):
		"""
		玩家进入空间
		@param 	playerBase	:		玩家的base
		@type 	playerBase	:		mailbox
		@param 	position	:		玩家的位置
		@type 	position	:		vector3
		@param 	direction	:		玩家的位置
		@type 	direction	:		vector3
		@return: None
		"""
		if self.hasCell:
			self.spaceMailBox.teleportEntity( playerBase, position, direction, pickData)
		else:
			self.addToEnterList( playerBase, position, direction, pickData )

	def login( self, playerBase, pickData ):
		"""
		玩家上线
		@param 	playerBase	:		玩家的base
		@type 	playerBase	:		mailbox
		"""
		if self.hasCell:
			self.spaceMailBox.registerLogonPlayer( playerBase )
		else:
			self.addToLogonList( playerBase )		# 加入等待列表中