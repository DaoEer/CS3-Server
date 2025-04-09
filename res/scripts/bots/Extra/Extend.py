# -*- coding: utf-8 -*-
import random, math
import csdefine
import csconst
import Math

def Unreal2KBEnginePosition(unrealPoint):
	"""
	"""
	return ( unrealPoint[1] * 0.01, unrealPoint[2] * 0.01, unrealPoint[0] * 0.01 )
	
def KBEngine2UnrealPosition(kbenginePoint):
	"""
	"""
	return ( kbenginePoint[2] * 100, kbenginePoint[0] * 100, kbenginePoint[1] * 100 )
	
def	StrToPosition(position):
	"""
	将字符串解析成坐标
	"""
	pos = position.split(" ")
	return Math.Vector3(float(pos[0]), float(pos[1]), float(pos[2]))

#------------------------------------------
# 挑选目标
#------------------------------------------
def checkCanAttack( entity, srcEntity = None ):
	"""
	ENTITY_STATE_PEAD						= 0				# 未决状态
	ENTITY_STATE_FREE						= 1				# 普通状态
	ENTITY_STATE_WARN						= 2				# 警戒状态
	ENTITY_STATE_FIGHT						= 3				# 战斗状态
	ENTITY_STATE_DEAD						= 4				# 死亡状态
	ENTITY_STATE_RESET						= 5				# 重置状态（怪物特有）
	ENTITY_STATE_SHOW						= 6				# 表演状态（怪物特有）
	ENTITY_STATE_STALL						= 7				# 摆摊状态
	ENTITY_STATE_MAX						= 8				# 状态最大值，高于此值的为无效状态
	"""
	if not entity:
		return False
		
	if entity.state not in [ csdefine.ENTITY_STATE_FREE, csdefine.ENTITY_STATE_WARN, csdefine.ENTITY_STATE_FIGHT]:
		return False
		
	#外面已经进行了一次过滤，所以如果是玩家的话，应该是PK
	if entity.hasFlag(csdefine.ENTITY_FLAG_ROLE):
		return True
		
	if entity.hasFlag( csdefine.FLAG_RELATION_NORMAL_TO_ROLE ):
		return False
		
	if entity.hasFlag( csdefine.FLAG_RELATION_NORMAL_TO_ROLE ):
		return False
	
	if srcEntity:
		campRelation = getCampRelation( srcEntity.getFinalCamp(), entity.getFinalCamp() )		#阵营关系
		if campRelation == csdefine.COMBAT_RELATION_ENEMY:
			return True
		else:
			return False
			
	return True
	
def getCampRelation( campA, campB ):
		"""
		获取阵营关系
		"""
		if campA == 0 or campB == 0:
			return csdefine.COMBAT_RELATION_DEFAULT
		
		if campA == campB:
			return csdefine.COMBAT_RELATION_NORMAL
		
		for key, relation in csconst.CAMP_RALETION.items():
			if set(key) == set( (campA, campB) ):
				return relation
		
		return csdefine.COMBAT_RELATION_DEFAULT
	
def checkInCenter( entity, center, radius ):
	"""
	判断是否在某个范围内
	"""
	if not entity:
		return False
		
	if (entity.position - center).length > radius:
		return False
		
	return True
	
def calRandomWalkPos(spawnPosition, randomWalkRadius):
	"""
	"""
	center = spawnPosition
	r = random.uniform( 1, randomWalkRadius ) #最少走1米
	b = 360.0 * random.random()
	x = r * math.cos(b)
	z = r * math.sin(b)
	return Math.Vector3(center.x + x, center.y, center.z + z)