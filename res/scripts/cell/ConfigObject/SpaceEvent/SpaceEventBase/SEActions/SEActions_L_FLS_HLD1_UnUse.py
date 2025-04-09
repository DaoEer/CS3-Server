# -*- coding: utf-8 -*-

# 副本事件行为
import KBEDebug
import KBEngine
import Math
import Functions
import KBEMath
import random
import csarithmetic
from ConfigObject.SpaceEvent.SpaceEventBase.SEActions.SEActionBase import SEActionBase

class SEAction58( SEActionBase ):
	"""
	在圆形区域内刷欢乐鼎
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		posO = Functions.vector3TypeConvert( section["param1"] )
		self._posO = KBEMath.Unreal2KBEnginePosition( posO )
		self.radius = float(section["param2"])
		self._scriptID = section["param3"]
		self._amount = int(section["param4"] )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		tempAmount = self._amount
		endPosList = []
		for i in range(0,tempAmount):
			endPos = None
			def getEndPos( srcPosX, srcPosY, srcPosZ):
				for pos in endPosList:
					if pos.flatDistTo(Math.Vector3(srcPosX,srcPosY,srcPosZ)) < 1.0:
						return None
				return Math.Vector3(srcPosX,srcPosY,srcPosZ)
			while endPos == None:
				srcPos = csarithmetic.getPositionByCircular( self._posO , self.radius )
				endPos = getEndPos(srcPos.x,srcPos.y,srcPos.z)
				if endPos != None:
					endPosList.append(endPos)
		while tempAmount > 0:
			dir = Math.Vector3(0,0,0)
			entity = spaceEntity.createEntityByScriptID( self._scriptID , endPosList[tempAmount - 1], dir,{"spawnPos":endPosList[tempAmount - 1], "spawnDir": dir } )
			if entity:
				tempAmount -= 1
			else:
				KBEDebug.ERROR_MSG("----scriptID = %s is error "%self._scriptID)

class SEAction59( SEActionBase ):
	"""
	随机选择一个真欢乐鼎发出亮光
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.effectID = section["param1"]
		self._scriptID = section["param2"]

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		entitylist = spaceEntity.getEntityRecord(self._scriptID)
		if len(entitylist) == 0: return
		theTrue = KBEngine.entities.get(random.choice( entitylist ))
		theTrue.setIsTrue( True )
		theTrue.allClients.CLIENT_OnPlayParticles( theTrue.id,self.effectID,"", 1.0,Math.Vector3(0,0,0) )

class SEAction60( SEActionBase ):
	"""
	通知欢乐鼎变换位置
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		posO = Functions.vector3TypeConvert( section["param1"] )
		self._posO = KBEMath.Unreal2KBEnginePosition( posO )
		self.radius = float(section["param2"])
		self._scriptID = section["param3"]
		self._effectID = section["param4"]
		
	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		entitylist = spaceEntity.getEntityRecord( self._scriptID )
		if len( entitylist ) > 0:
			HLDEntity = KBEngine.entities.get(entitylist[0])
			if not HLDEntity: return
			HLDEntity.HLDStartMove( self._posO, self.radius )
			for id in entitylist:
				HLDEntity = KBEngine.entities.get(id)
				if not HLDEntity: return
				for player in spaceEntity._spaceRoles:
					player.client.PlayBindEffect(HLDEntity.id,self._effectID)

class SEAction61( SEActionBase ):
	"""
	通知客户端欢乐鼎可以开始了
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return		
		for player in spaceEntity._spaceRoles:
			player.client.HLDCanStart()

class SEAction70( SEActionBase ):
	"""
	欢乐鼎结束
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		spaceEntity.getScript().onConditionChange( spaceEntity, "HLD", spaceEntity.id, "END", "" )
		for e in spaceEntity._spaceRoles:
			e.client.HLDEnd()

SEActionBase.setActionClass("SEAction58", SEAction58)
SEActionBase.setActionClass("SEAction59", SEAction59)
SEActionBase.setActionClass("SEAction60", SEAction60)
SEActionBase.setActionClass("SEAction61", SEAction61)
SEActionBase.setActionClass("SEAction70", SEAction70)
