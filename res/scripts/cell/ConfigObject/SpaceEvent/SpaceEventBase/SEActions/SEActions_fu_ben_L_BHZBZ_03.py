# -*- coding: utf-8 -*-
# 副本事件行为
import KBEDebug
import KBEngine
from ConfigObject.SpaceEvent.SpaceEventBase.SEActions.SEActionBase import SEActionBase
import random
import csdefine

class SEAction292( SEActionBase ):
	"""
	CST-7257 程序功能需求——（40级）帮会争霸第三场比赛——新增需求
	玩家被击杀
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.radius = float( section["param1"] ) # 获得助攻的范围

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		dieEntity = KBEngine.entities.get(triggerID,None)
		killEntity = KBEngine.entities.get( eventParams["killerID"],None )
		if dieEntity == None or killEntity == None:
			return
		if killEntity.getEntityFlag() == csdefine.ENTITY_FLAG_VEHICLEPET:
			killEntity = killEntity.getOwnerEntity()
		if not killEntity or killEntity.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
			return
		spaceEntity.kill( killEntity.tongDBID, killEntity, dieEntity.tongDBID,dieEntity )
		roleList = dieEntity.entitiesInRangeExtCircle( self.radius, "Role" )
		petList = dieEntity.entitiesInRangeExtCircle( self.radius,"VehiclePet" )
		roleList.extend( petList )
		for entity in roleList:
			if entity.getEntityFlag() == csdefine.ENTITY_FLAG_VEHICLEPET:
				entity = entity.getOwnerEntity()
			if entity and entity.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE and entity.tongDBID == killEntity.tongDBID and entity.id != killEntity.id:
				spaceEntity.addTongMemberAssists( killEntity,entity.tongDBID, entity )

SEActionBase.setActionClass("SEAction292", SEAction292)

