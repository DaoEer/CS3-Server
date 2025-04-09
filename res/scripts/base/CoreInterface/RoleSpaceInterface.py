# -*- coding: utf-8 -*-
import KBEngine
import csconst
import csdefine
import KST
import KBEDebug
import SpaceContainer
from ObjectScript.ObjectScriptFactory import g_objFactory

class RoleSpaceInterface:
	def __init__( self ):
		self.birthSpace = ""
		self.birthSpaceBelong = 0
		self.birthPosistion = ( 0, 0, 0 )
		self.birthDirection = ( 0, 0, 0 )
		#标识当前cell是否正在创建
		self.creatingCell = False
	
	def logon( self ):
		"""
		登陆
		login表示当前玩家还没有cell，所以肯定有cellData
		"""
		self.birthSpace = self.cellData["spaceScriptID"]
		self.birthSpaceBelong = self.cellData["spaceBelongType"]
		self.birthPosistion = self.cellData["position"]
		self.birthDirection = self.cellData["direction"]
		
		self.loginToSpace( self.birthSpace, { "packBelongType":self.birthSpaceBelong } )
	
	def loginToSpace( self, spaceClassName, pickArgs ):
		"""
		玩家登陆到指定地方
		"""
		spaceObj = KST.g_objFactory.getSpaceObject( spaceClassName )
		if spaceObj:
			belongTypes = spaceObj.getSpaceBelongTypes()
			if len(belongTypes) == 1: 
				pickArgs["packBelongType"] = belongTypes[0] #如果space只有一个归属
			elif len(belongTypes) > 1: #如果space有多个归属(主要是针对 单人和组队)
				if self.teamID > 0 and csdefine.SPACE_BELONG_TEAM in belongTypes: #说明是组队
					pickArgs["packBelongType"] = csdefine.SPACE_BELONG_TEAM
				else:
					pickArgs["packBelongType"] = csdefine.SPACE_BELONG_PERSON

		params = SpaceContainer.getPickContainerLoginData( pickArgs.pop( "packBelongType" ), spaceClassName, self, pickArgs )
		KBEngine.globalData[ "SpaceManager" ].roleLogin( spaceClassName, self, params )
	
	def loginToReviveSpace( self ):
		"""
		<define method>
		登录到复活地图
		"""
		if self.cellData["camp"] == csdefine.CAMP_TAOSIM:
			self.cellData["spaceScriptID"] = csconst.SPAWN_SPACE_X
			self.cellData["position"] = csconst.SPAWN_POSITION_X
			self.cellData["direction"] = csconst.SPAWN_DIRECTION_X
		else:
			self.cellData["spaceScriptID"] = csconst.SPAWN_SPACE_M
			self.cellData["position"] = csconst.SPAWN_POSITION_M
			self.cellData["direction"] = csconst.SPAWN_DIRECTION_M
		
		self.cellData["spaceBelongType"] = csdefine.SPACE_BELONG_NORMAL
		self.logon()
		
	def loginToConfigSpace( self, spaceScriptID, position, direction ):
		"""
		<define method>
		登录到配置的地图（位面）
		"""
		self.cellData["spaceScriptID"] = spaceScriptID
		self.cellData["spaceBelongType"] = csdefine.SPACE_BELONG_NORMAL
		self.cellData["position"] = position
		self.cellData["direction"] = direction
		if self.cellData["HP"] == 0:  #玩家在位面死亡后，再次上线在主线地图自动复活（jira:CST-3363）
			self.cellData["HP"] = 1
		self.logon()

	def loginToBindReviveSpace( self ):
		"""
		登录到绑定复活点
		"""
		self.cellData["spaceScriptID"] = self.cellData["reviveSpaceScriptID"]
		self.cellData["position"] = self.cellData["revivePosition"]
		self.cellData["direction"] = self.cellData["reviveDirection"]
		self.logon()
	
	def onClientGetCell( self ):
		self.cell.onLoginSpace()
		
	def onGetCell( self ):
		"""
		cell创建成功
		"""
		self.creatingCell = False
		
	def onCreateCellFailure( self ):
		"""
		cell创建失败
		"""
		self.creatingCell = False
	
	def gotoSpace( self, spaceClassName, position, direction, pickArgs ):
		"""
		<Define method>
		传送到指定位置
		"""
		KBEngine.globalData[ "SpaceManager" ].gotoSpace( spaceClassName, self, position, direction, pickArgs )
	
	def createCellFromSpace( self, spaceCellMB ):
		"""
		<define method>
		在spaceCell上创建roleCell
		@param spaceCell:	空间cell
		@type spaceCell:	mailbox
		"""
		KBEDebug.DEBUG_MSG("Role[%d:%d] CreateCellFromSpace, space[%d]" %(self.databaseID, self.id, spaceCellMB.id))
		try:
			self.createCellEntity( spaceCellMB ) #引擎方法
			self.creatingCell = True
		except:
			self.addTimerCallBack( 1.0, "createCellFromSpace", ( spaceCellMB,) )
			
	def isCreatingCell(self):
		"""
		当前cell是否正在创建
		"""
		return self.creatingCell