# -*- coding: utf-8 -*-
import Vector
import Math
import math
import random

import csconst
import csdefine
from SearchScript.SearchBase import SearchBase
from SearchScript.FindEntityShape import FindEntityShape
import KBEDebug
import csarithmetic

class SearchDefult( SearchBase ):
		
	def entitiesInRangeExt(self, entity, range, entityType=None, position=None ):
		"""
		#默认方的
		"""
		curSpace = entity.getCurrentSpace()
		if position == None:
			position = entity.position

		rsList = []
		if curSpace.getScript().getSpaceType() in [csdefine.SPACE_TYPE_PLANE, csdefine.SPACE_TYPE_COPY,
										csdefine.SPACE_TYPE_POTENTIAL, csdefine.SPACE_TYPE_CHUAN_CHENG,
										csdefine.SPACE_TYPE_STORY_COPY, csdefine.SPACE_TYPE_JSSLC_CHANCE_COPY]:
			entitiesList = []
			if entityType == 'Role':
				entitiesList.extend(self.getSpaceRoles( curSpace ))
				for e in entitiesList:
					if FindEntityShape.rectangle(range, range, range, position, e.position):
						rsList.append(e)
			else:
				rsList = entity.entitiesInRange(range, entityType, position)
		else:
			rsList = entity.entitiesInRange( range, entityType, position )

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
		if curSpace.getScript().getSpaceType() in [csdefine.SPACE_TYPE_PLANE, csdefine.SPACE_TYPE_COPY,
										csdefine.SPACE_TYPE_POTENTIAL, csdefine.SPACE_TYPE_CHUAN_CHENG,
										csdefine.SPACE_TYPE_STORY_COPY, csdefine.SPACE_TYPE_JSSLC_CHANCE_COPY]:
			if entityType == 'Role':
				entitiesList.extend(self.getSpaceRoles( curSpace ))
			else:
				entitiesList = entity.entitiesInRange(range, entityType, position)

		else:
			entitiesList = entity.entitiesInRange(range, entityType, position)

		for e in entitiesList:
			if FindEntityShape.circle(range, csconst.AI_ENTITIES_IN_RANGE_HEIGHT, position, e.position):
				rsList.append(e)

		return rsList

	def entitiesInRangeExtForAI(self,entity, radius, height = csconst.AI_ENTITIES_IN_RANGE_HEIGHT, entityType=None, scriptID=[], exceptStates=[csdefine.ENTITY_STATE_PEAD, csdefine.ENTITY_STATE_DEAD], position=None ):
		"""
		"""
		if entityType == "":
			entityType = None

		if position == None:
			position = entity.position

		rsList = []
		curSpace = entity.getCurrentSpace()
		if curSpace.getScript().getSpaceType() in [csdefine.SPACE_TYPE_PLANE, csdefine.SPACE_TYPE_COPY,
									   csdefine.SPACE_TYPE_POTENTIAL, csdefine.SPACE_TYPE_CHUAN_CHENG,
									   csdefine.SPACE_TYPE_STORY_COPY, csdefine.SPACE_TYPE_JSSLC_CHANCE_COPY]:
			entitiesList = []
			if entityType == None:
				entitiesList.extend(self.getSpaceRoles( curSpace ))
				entitiesList.extend(self.getSpaceNPC( curSpace, scriptID ))
			elif entityType == 'Role':
				entitiesList.extend(self.getSpaceRoles( curSpace ))
			else:
				entitiesList.extend(self.getSpaceNPC( curSpace, scriptID ))

			for e in entitiesList:
				if FindEntityShape.circle( radius, height, position, e.position ) and self.aiFilter( e, exceptStates ):
					rsList.append(e)
		else:
			entitiesList = entity.entitiesInRange( radius, entityType, position)
			for e in entitiesList:
				if FindEntityShape.circle( radius, height, position, e.position ) and self.aiFilter( e, exceptStates ):
					rsList.append(e)
			if len(scriptID):
				rsList = [e for e in rsList if hasattr(e,"scriptID") and e.scriptID in scriptID]

		return rsList

	def entitiesInRangeExtForBehind(self, entity, length, height, entityType=None, scriptID=[], exceptStates=[csdefine.ENTITY_STATE_PEAD, csdefine.ENTITY_STATE_DEAD] ):
		"""
		怪物背后的矩形范围内是否有指定类型的entity
		"""
		if entityType == "":
			entityType = None
		position = Math.Vector3(entity.position)
		rsList = []
		curSpace = entity.getCurrentSpace()
		if curSpace.getScript().getSpaceType() in [csdefine.SPACE_TYPE_PLANE, csdefine.SPACE_TYPE_COPY,
									   csdefine.SPACE_TYPE_POTENTIAL, csdefine.SPACE_TYPE_CHUAN_CHENG,
									   csdefine.SPACE_TYPE_STORY_COPY, csdefine.SPACE_TYPE_JSSLC_CHANCE_COPY]:
			entitiesList = []
			if entityType == 'Role':
				entitiesList.extend(self.getSpaceRoles( curSpace ))
			else:
				entitiesList.extend(self.getSpaceNPC( curSpace, scriptID ))
			for e in entitiesList:
				if csarithmetic.isInRectangle( e.position, position, entity.direction.z + math.pi, length*2, height ):
					rsList.append(e)
		return rsList