# -*- coding: utf-8 -*-
import Vector
import Math
import math
import random

import csconst
import csdefine

class SearchBase( object ):
	def __init__( self ):
		object.__init__( self )
		
	def entitiesInRangeExt(self, entity,range, entityType=None, position=None ):
		"""
		#默认方的
		vitural  method
		"""
		pass

	def entitiesInRangeExtCircle(self,entity, range, entityType=None, position=None ):
		"""
		# 圆的
		vitural  method
		"""
		pass

	def entitiesInRangeExtForAI(self,entity, radius, height = csconst.AI_ENTITIES_IN_RANGE_HEIGHT, entityType=None, scriptID=[], exceptStates=[csdefine.ENTITY_STATE_PEAD, csdefine.ENTITY_STATE_DEAD], position=None ):
		"""
		vitural  method
		"""
		pass

	def aiFilter(self, entity, exceptStates = [ csdefine.ENTITY_STATE_PEAD, csdefine.ENTITY_STATE_DEAD ], exceptEffect = [ csdefine.EFFECT_STATE_PROTECT ] ):
		if entity.getEntityFlag() in [ csdefine.ENTITY_FLAG_MONSTER, csdefine.ENTITY_FLAG_ROLE, csdefine.ENTITY_FLAG_TRAP ]:
			if entity.state in exceptStates:
				return False

			for eff in exceptEffect:
				if entity.hasEffectState( eff ):
					return False

		return True

	# 取pc
	def getSpaceRoles(self, curSpace ):
		return curSpace.getSpaceRoles()

	# 取npc
	def getSpaceNPC(self, curSpace, scriptIDs ):
		rsList = []
		if not len(scriptIDs):
			for e in curSpace.entityMailBoxRecord.values():
				rsList.extend(e)
		else:
			for sid in scriptIDs:
				for e in curSpace.getEntityMailBoxRecord( sid ):
					rsList.append( e )
		return rsList
