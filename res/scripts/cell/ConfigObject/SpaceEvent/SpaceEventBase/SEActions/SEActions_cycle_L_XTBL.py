# -*- coding: utf-8 -*-

# 副本事件行为

import KBEDebug
import KBEngine
import csdefine
import math
from ConfigObject.SpaceEvent.SpaceEventBase.SEActions.SEActionBase import SEActionBase
import Functions
import csconst


class SEAction267( SEActionBase ):
	"""
	玄天宝录:随机若干个石像开始颤动并爆发出妖气
	"""
	def init ( self, section ):
		SEActionBase.init( self, section )
		self._stoneNum = int(section["param1"])			# 暴动石像个数
		self._intervalTime = int(section["param2"])		# 距离下一次暴动的时间
		
	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return

		spaceEntity.initStochasticStoneCritical( self._stoneNum, self._intervalTime )

class SEAction268( SEActionBase ):
	"""
	玄天宝录:火棍停止旋转
	"""
	def init ( self, section ):
		SEActionBase.init( self, section )
		self._scriptID = section["param1"]				# 火棍的scriptID
		
	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return

		entitylist = spaceEntity.getEntityRecord( self._scriptID )
		if len(entitylist) == 0: return
		for entityID in entitylist:
			entity = KBEngine.entities.get( entityID )
			if entity:
				entity.stopMoving( csdefine.MOVE_TYPE_LOOP_ROTATOR )

class SEAction269( SEActionBase ):
	"""
	玄天宝录:石像恢复平静
	"""
	def init ( self, section ):
		SEActionBase.init( self, section )
		
	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		spaceEntity.onStopStochasticStoneCritical()
		for role in spaceEntity._spaceRoles:
			if role.getClient():
				role.client.CLIENT_NotifyXTBLStopShow()

class SEAction272( SEActionBase ):
	"""
	玄天宝录:开始日光发射
	"""
	def init ( self, section ):
		SEActionBase.init( self, section )
		self.scriptIDs  = section["param1"].split("|")  # 反射镜ID（左上角|右上角|右下角|左下角)
		self._scriptID = section["param2"]				# 大日宝镜ID
		
	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return

		mirrorScriptIDList = []
		for _scriptID in self.scriptIDs:
			entitylist = spaceEntity.getEntityRecord( _scriptID )
			if len(entitylist) == 0: return
			mirrorScriptIDList.append( entitylist[0] )

		entitylist1 = spaceEntity.getEntityRecord( self._scriptID )
		if len(entitylist1) == 0: return

		for player in spaceEntity._spaceRoles:
			if player.getClient():
				player.client.CLIENT_NotifyMirrorObject( entitylist1[0], mirrorScriptIDList )

class SEAction285( SEActionBase ):
	"""
	玄天宝录:显示结界血条界面
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.scriptID = section["param1"]			# 结界的scriptID

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return

		entityIDList = spaceEntity.getEntityRecord(self.scriptID)
		if not len(entityIDList):
			return
		entityID = entityIDList[0]
		entity = KBEngine.entities.get(entityID,None)

		if not entity:
			return
		percent = int(math.floor(entity.HP/entity.HP_Max*100))
		for e in spaceEntity._spaceRoles:
			e.client.CLIENT_ShowBloodPercentBar( percent )

class SEAction289( SEActionBase ):
	"""
	玄天宝录:显示下一次爆发时间提示界面
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.nextExplosionTime = int( section["param1"] )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return

		for e in spaceEntity._spaceRoles:
			if e.getClient():
				e.client.CLIENT_NotifyNextExplosionTime( str(self.nextExplosionTime * csconst.TIME_ENLARGE_MULTIPLE + Functions.getTime()) )

class SEAction293( SEActionBase ):
	"""
	玄天宝录:新增怪物加入随机暴动列表
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.scriptIDList = []
		if section["param1"]:
			self.scriptIDList = section["param1"].split("|")			# 怪物的scriptID

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return

		for scriptID in self.scriptIDList:
			entityIDList = spaceEntity.getEntityRecord(scriptID)
			if not len(entityIDList):
				return
			
			for entityID in entityIDList:
				spaceEntity.checkSolidify( entityID )

SEActionBase.setActionClass("SEAction267", SEAction267)
SEActionBase.setActionClass("SEAction268", SEAction268)
SEActionBase.setActionClass("SEAction269", SEAction269)
SEActionBase.setActionClass("SEAction272", SEAction272)
SEActionBase.setActionClass("SEAction285", SEAction285)
SEActionBase.setActionClass("SEAction289", SEAction289)
SEActionBase.setActionClass("SEAction293", SEAction293)