# -*- coding: utf-8 -*-

import KBEngine
import KBEDebug
from Trap import Trap
import csdefine
import ECBProximityDefine

class TrapBattleFlag( Trap ):
	"""
	攻城梯 战旗
	"""
	def __init__( self ):
		self.setBarracksBelongType( csdefine.TRAP_BARRACKS_BELONG_NEUTRALLY )
		Trap.__init__( self )
		self.highOffRangeRoleIDs = []
		self.checkHighRangeTimerID = 0

	def setSelfEntityFlagExt(self):
		"""
		virtual method
		"""
		self.setEntityFlagExt(csdefine.ENTITY_FLAG_EXT_TRAP_BATTLEFLAG)

	def addOccurProgress( self, value ):
		"""
		增加占领进度
		"""
		if self.occurProgress + value > self.maxProgress:
			self.occurProgress = self.maxProgress
		else:
			self.occurProgress += value

		for enterID in self.enterIDs:
			entity = KBEngine.entities.get( enterID,None )
			if not entity or entity.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
				continue
			if entity.getClient():
				entity.client.CLIENT_UpdateBattleFlagProgressBar( self.occurProgress,self.maxProgress )

	def getOccurProgress( self ):
		"""
		获得占领进度
		"""
		return self.occurProgress

	def getMaxProgress( self ):
		"""
		获得最大进度
		"""
		return self.maxProgress

	def getBarracksBelongType( self ):
		"""
		获得归属
		"""
		return self.barracksBelongType

	def setBarracksBelongType( self, barracksBelongType ):
		"""
		"""
		self.barracksBelongType = barracksBelongType
		for enterID in self.enterIDs:
			entity = KBEngine.entities.get( enterID,None )
			if not entity or entity.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
				continue
			if entity.getClient():
				entity.client.CLIENT_OnOccupyBelongTypeChanged( self.barracksBelongType )

	def onEnterTrap( self, entity, rangeXZ, rangeY, controllerID, userArg = 0 ):
		"""
		进入触发陷阱内
		"""
		if entity.inDestroying():
			return
		if controllerID not in self.proximityInfo:	#是刚创建陷阱就触发的情况
			if controllerID in self.entersOnAddProximity:
				if entity.id not in self.entersOnAddProximity[ controllerID ]:
					self.entersOnAddProximity[ controllerID ].append( entity.id )
			else:
				self.entersOnAddProximity[ controllerID ] = [ entity.id ]
			return
		
		isSquare = self.proximityInfo[ controllerID ][3]
		if isSquare:	#方形
			if rangeY > 0 and abs( self.position.y - entity.position.y ) > rangeY:	#引擎的陷阱是一个高度无限延伸的“井”，因此加个高度验证避免在高空也能触发地面的陷阱
				return
			userArg = self.proximityInfo[ controllerID ][0]
			self.callEnterTrapCB( entity, rangeXZ, rangeY, controllerID, userArg )
		
		else:	#是“其他形状”陷阱：只添加到记录，不执行进陷阱回调
			if controllerID not in self.shapeProximityEnters:
				self.shapeProximityEnters[controllerID] = [ entity.id ]
			else:
				self.shapeProximityEnters[controllerID].append( entity.id )

	def onEnterCommonTrap( self, entity, rangeXZ, rangeY, controllerID ):
		"""
		callback method.
		进入陷阱
		"""
		if entity.getEntityFlag() == csdefine.ENTITY_FLAG_GHOST_RECEIVER:
			return
		if abs(entity.position.y - self.position.y) > 3.0: #限制3米检测
			if entity.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
				self.addHighOffRangeRoleIDs(entity.id, 3.0)
			return
		if entity.inDestroying():
			return
		if self.isState(csdefine.ENTITY_STATE_DEAD):
			return
		self.addTrapEnterEntity( entity )

	def addTrapEnterEntity( self, entity ):
		"""
		"""
		if entity.id  not in self.enterIDs:
			self.enterIDs.append( entity.id )
		self.getScript().onEnterTrap( self, entity.id )
		if entity and entity.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE and entity.getClient():
			if entity.getBelongSide() != self.getBarracksBelongType():
				entity.client.CLIENT_ShowBattleFlagProgressBar( self.id, self.barracksBelongType, self.occurProgress, self.maxProgress )
			elif self.occurProgress > 0:
				entity.client.CLIENT_ShowBattleFlagProgressBar( self.id, self.barracksBelongType, self.occurProgress, self.maxProgress )

	def onLeaveTrap( self, entity, rangeXZ, rangeY, controllerID, userArg = 0 ):
		"""
		离开触发陷阱内
		"""
		if entity.inDestroying():
			return
		if controllerID not in self.proximityInfo:
			return
		
		isSquare = self.proximityInfo[ controllerID ][3]
		if isSquare:	#方形
			userArg = self.proximityInfo[ controllerID ][0]
			self.callLeaveTrapCB( entity, controllerID, userArg )
		else:				#是“其他形状”陷阱：只移除记录，不执行离开陷阱回调
			if controllerID in self.shapeProximityEnters and entity.id in self.shapeProximityEnters[controllerID]:
				self.shapeProximityEnters[controllerID].remove( entity.id )

	def onLeaveCommonTrap( self, entity, controllerID ):
		"""
		callback method.
		离开陷阱
		"""
		if entity.inDestroying():
			return
		if self.isState(csdefine.ENTITY_STATE_DEAD):
			return
		
		if entity.id in self.enterIDs:
			self.enterIDs.remove( entity.id )
		self.getScript().onLeaveTrap( self, entity.id )
		
		if entity and entity.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
			if entity.id in self.highOffRangeRoleIDs:
				self.highOffRangeRoleIDs.remove( entity.id )
				if not len( self.highOffRangeRoleIDs ):
					self.popCheckHighOffRangeRoleTimer()
		if entity and entity.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE and entity.getClient():
			entity.client.CLIENT_HideBattleFlagProgressBar( self.id )

	def addHighOffRangeRoleIDs( self, roleEntitID, highRange ):
		"""
		增加高于陷阱高度检测的玩家
		"""
		if roleEntitID in self.enterIDs:
			return
		if roleEntitID not in self.highOffRangeRoleIDs:
			self.highOffRangeRoleIDs.append( roleEntitID )
		if len( self.highOffRangeRoleIDs ):
			if self.checkHighRangeTimerID <= 0:
				self.checkHighRangeTimerID = self.addTimerRepeat(1.0,"checkHighOffRangeRoleIDs",(highRange,))

	def checkHighOffRangeRoleIDs( self, highRange ):
		"""
		持续检测玩家高度
		"""
		if not len(self.highOffRangeRoleIDs):
			self.popCheckHighOffRangeRoleTimer()
			return
		tempEntityIDs = list( self.highOffRangeRoleIDs )
		needRemoveIDs = []
		for id in tempEntityIDs:
			roleEntity = KBEngine.entities.get( id,None )
			if roleEntity == None:
				needRemoveIDs.append(id)
				continue
			if abs(roleEntity.position.y - self.position.y) <= highRange:
				self.addTrapEnterEntity( roleEntity )
				needRemoveIDs.append(id)
		for needRemoveID in needRemoveIDs:
			if needRemoveID in self.highOffRangeRoleIDs:
				self.highOffRangeRoleIDs.remove( needRemoveID )

	def popCheckHighOffRangeRoleTimer( self ):
		"""
		"""
		if self.checkHighRangeTimerID > 0:
			self.popTimer( self.checkHighRangeTimerID )
			self.checkHighRangeTimerID = 0
			self.highOffRangeRoleIDs = []

	def occupyCheck( self, args ):
		"""
		占领
		"""
		if not len( self.enterIDs ):
			return
			
		spaceEntity = self.getCurrentSpace()
		if spaceEntity and (spaceEntity.getScript().getSpaceChildType() == csdefine.SPACE_CHILD_TYPE_GCZ or spaceEntity.getScript().getSpaceChildType() == csdefine.SPACE_TYPE_CHILD_TONG_PLUNDER):
			self.battleFlagGCZOccupyCheck( args )
		if spaceEntity and spaceEntity.getScript().getSpaceChildType() == csdefine.SPACE_CHILD_TYPE_LBC:
			self.battleFlagLBCOccupyCheck( args )

	def barracksReviveCheck( self, args ):
		"""
		回复检测
		"""
		pass

	def battleFlagGCZOccupyCheck( self, args ):
		"""
		攻城战战旗占领相关  只有进攻和防守的 PVE
		"""
		if self.getBarracksBelongType() == csdefine.TRAP_BARRACKS_BELONG_PROTECT:
			roleEntiys = []
			otherEntitys = [] 
			for enterID in self.enterIDs:
				entity = KBEngine.entities.get( enterID, None )
				if entity:
					if entity.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE and entity.getState() != csdefine.ENTITY_STATE_DEAD:
						if entity.getBelongSide() == csdefine.BELONG_SIDE_PROTECT:
							return
						
						roleEntiys.append( entity )
					else:
						otherEntitys.append( entity )

			if not len( roleEntiys ):
				return
			
			flag = True
			for entity in roleEntiys:
				if entity.getBelongSide() != csdefine.BELONG_SIDE_PROTECT:
					flag = False
					break
			
			if flag: return
			hasEnemyEntity = False
			for entity in otherEntitys:
				if roleEntiys[0].isEnemyRelation( entity ):
					hasEnemyEntity = True
					break
			if not hasEnemyEntity:
				self.addOccurProgress( int( args["param2"] ) )
				if self.getOccurProgress() >= self.getMaxProgress():
					self.addBuff( self, int( args["param3"].split("|")[0] ) )
					spaceEntity = self.getCurrentSpace()
					if spaceEntity:
						spaceEntity.getScript().onConditionChange( spaceEntity, "", self.scriptID, args["param3"].split("|")[1], str(self.id))
					self.setBarracksBelongType( csdefine.TRAP_BARRACKS_BELONG_ATTACK )
					self.addOccurProgress( -self.maxProgress )  

	def battleFlagLBCOccupyCheck( self, args ):
		"""
		练兵场战旗占领相关 PVP PVE
		"""
		if self.getBarracksBelongType() == csdefine.TRAP_BARRACKS_BELONG_PROTECT:
			role = None
			otherEntitys = [] 
			for enterID in self.enterIDs:
				entity = KBEngine.entities.get( enterID, None )
				if entity:
					if entity.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE and entity.isBelongSide(csdefine.BELONG_SIDE_ATTACK):
						role = entity
					else:
						otherEntitys.append( entity )

			if role == None:
				return
			for entity in otherEntitys:
				if role.canBuildEnemyRelation( entity ):
					return
					
			self.addOccurProgress( int( args["param2"] ) )
			if self.getOccurProgress() >= self.getMaxProgress():
				self.addBuff( self, int( args["param3"].split("|")[0] ) )
				spaceEntity = self.getCurrentSpace()
				if spaceEntity:
					spaceEntity.getScript().onConditionChange( spaceEntity, "", self.scriptID, args["param3"].split("|")[1], str(self.id))
				self.setBarracksBelongType( csdefine.TRAP_BARRACKS_BELONG_ATTACK )
				self.addOccurProgress( -self.maxProgress )  