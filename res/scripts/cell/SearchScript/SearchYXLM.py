# -*- coding: utf-8 -*-
import Vector
import Math
import math
import random

import csconst
import csdefine
from SearchScript.SearchBase import SearchBase
from SearchScript.FindEntityShape import FindEntityShape
from ObjectScript.Monster.MonsterExtYXLMSoldier import MonsterExtYXLMSoldier

class SearchYXLM( SearchBase ):
		
	def entitiesInRangeExt(self,entity, range, entityType=None, position=None ):
		"""
		#默认方的
		"""
		curSpace = entity.getCurrentSpace()
		if position == None:
			position = entity.position
		entitiesList = []
		rsList = []
		if entityType == 'Role':
			entitiesList.extend(self.getSpaceRoles( curSpace ))
			for e in entitiesList:
				if FindEntityShape.rectangle(range, range, range, position, e.position):
					rsList.append(e)
		elif isinstance( entity, MonsterExtYXLMSoldier) and entityType == "MonsterExtYXLMSoldier":
			entitiesList = curSpace.getEntityMailBoxByPatrolList( entity.way )
			for e in entitiesList:
				if FindEntityShape.rectangle(range, range, range, position, e.position):
					rsList.append(e)
		else:
			rsList = entity.entitiesInRange(range, entityType, position)

		return rsList

	def entitiesInRangeExtCircle(self,entity, range, entityType=None, position=None ):
		"""
		# 圆的
		"""
		curSpace = entity.getCurrentSpace()
		if position == None:
			position = entity.position
		rsList = []
		entitiesList = []
		if entityType == 'Role':
			entitiesList.extend(self.getSpaceRoles( curSpace ))
		elif isinstance( entity, MonsterExtYXLMSoldier ) and entityType == "MonsterExtYXLMSoldier":
			entitiesList = curSpace.getEntityMailBoxByPatrolList( entity.way )
		else:
			entitiesList = entity.entitiesInRange(range, entityType, position)

		for e in entitiesList:
			if FindEntityShape.circle(range, csconst.AI_ENTITIES_IN_RANGE_HEIGHT, position, e.position):
				rsList.append(e)

		return rsList

	def entitiesInRangeExtForAI(self, entity,radius, height = csconst.AI_ENTITIES_IN_RANGE_HEIGHT, entityType=None, scriptID=[], exceptStates=[csdefine.ENTITY_STATE_PEAD, csdefine.ENTITY_STATE_DEAD], position=None ):
		"""
		"""
		if entityType == "":
			entityType = None

		if position == None:
			position = entity.position

		rsList = []
		curSpace = entity.getCurrentSpace()
		entitiesList = []
		if entityType == 'Role':
			entitiesList.extend(self.getSpaceRoles( curSpace ))
		elif isinstance( entity, MonsterExtYXLMSoldier ) and entityType == "MonsterExtYXLMSoldier":
			entitiesList = curSpace.getEntityMailBoxByPatrolList( entity.way )
		else:
			entitiesList.extend(self.getSpaceNPC( curSpace, scriptID ))
		for e in entitiesList:
			if FindEntityShape.circle( radius, height, position, e.position ) and self.aiFilter( e, exceptStates ):
				rsList.append(e)
			if len(scriptID):
				rsList = [e for e in rsList if hasattr(e,"scriptID") and e.scriptID in scriptID]
		return rsList

