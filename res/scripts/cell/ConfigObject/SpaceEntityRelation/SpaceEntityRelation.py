# -*- coding: utf-8 -*-
import KBEDebug
import csdefine
import csconst
import KBEngine
from FactionRelationLoader import g_FactionRelationLoader

class RelationBase:
	"""
	基类
	"""
	@classmethod
	def getRelation( SELF, srcEntity, target ):
		"""
		virtual method
		"""
		return csdefine.COMBAT_RELATION_NORMAL

#---------------------------玩家关系判断实例----------------------------------------
class RelRole_Camp( RelationBase ):
	"""
	玩家关系判断类：阵营决定pvp关系
	"""
	@classmethod
	def getRelation( SELF, srcEntity, target ):
		"""
		virtual method
		"""
		#非战斗entity
		if target.getEntityFlag() not in csdefine.COMBAT_ENTITY_FLAG_LIST:
			return csdefine.COMBAT_RELATION_NORMAL
		
		#非战斗状态
		#if srcEntity.getState() in csconst.NOT_ATTACK_STATES:
		#	return csdefine.COMBAT_RELATION_NONE
		
		#是否准备好
		if not srcEntity.isReady() or ( target and not target.isReady() ):
			return csdefine.COMBAT_RELATION_NONE
		
		# 观察者标志位
		if srcEntity.hasFlag( csdefine.ROLE_FLAG_WATCHER ):
			return csdefine.COMBAT_RELATION_NORMAL
		
		#自己有潜入
		if srcEntity.isHasStateFlag(csdefine.STATE_FLAG_SLIPINTO):
			return csdefine.COMBAT_RELATION_NORMAL
		
		#对方有潜入
		if target.isHasStateFlag(csdefine.STATE_FLAG_SLIPINTO):
			return csdefine.COMBAT_RELATION_NORMAL

		#如果是幻兽，则把判断对象换成主人
		if target and target.getEntityFlag() == csdefine.ENTITY_FLAG_VEHICLEPET:
			target = target.getOwnerEntity()
		
		#如果是傀儡，则把判断对象换成傀儡施法者
		if target and target.getEntityFlag() == csdefine.ENTITY_FLAG_GHOST_RECEIVER:
			target = target.getOwnerEntity()
			
		if target and target.getEntityFlagExt() == csdefine.ENTITY_FLAG_EXT_MONSTER_EXT_TISHEN:
			target = target.getOwnerEntity()
			
		if target and target.getEntityFlagExt() == csdefine.ENTITY_FLAG_EXT_FENSHEN:
			target = target.getOwnerEntity()
		
		#CMonster
		if target and target.getEntityFlagExt() == csdefine.ENTITY_FLAG_MONSTER_CTRL_BY_CLIENT:
			target = target.getControlEntity()
			
		if target == None:
			return csdefine.COMBAT_RELATION_NORMAL

		# 对方是玩家，默认为友好
		if target.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:

			if srcEntity.isHasStateFlag(csdefine.STATE_FLAG_XIN_MO) or target.isHasStateFlag(csdefine.STATE_FLAG_XIN_MO):
				return csdefine.COMBAT_RELATION_ENEMY

			if srcEntity.isTeammate( target.id ):
				return csdefine.COMBAT_RELATION_NORMAL
			
			campRelation = srcEntity.getCampRelation( srcEntity.getFinalCamp(), target.getFinalCamp() )		#阵营关系
			if campRelation != csdefine.COMBAT_RELATION_DEFAULT:
				return campRelation
			
			return csdefine.COMBAT_RELATION_NORMAL
		
		# 对方是怪物，默认为敌对
		elif target.getEntityFlag() == csdefine.ENTITY_FLAG_MONSTER:

			if target.isState( csdefine.ENTITY_STATE_RESET ):
				return csdefine.COMBAT_RELATION_NONE
			
			if target.hasFlag( csdefine.FLAG_RELATION_NORMAL_TO_ROLE ):
				return csdefine.COMBAT_RELATION_NORMAL

			if target.hasFlag( csdefine.FLAG_RELATION_ENEMY_TO_ROLE ):
				return csdefine.COMBAT_RELATION_ENEMY

			campRelation = srcEntity.getCampRelation( srcEntity.getFinalCamp(), target.getFinalCamp() )		#阵营关系
			if campRelation != csdefine.COMBAT_RELATION_DEFAULT:
				return campRelation
			
			return csdefine.COMBAT_RELATION_ENEMY
		# 对方是NPC，默认为友好
		elif target.getEntityFlag() == csdefine.ENTITY_FLAG_NPC:
			campRelation = srcEntity.getCampRelation( srcEntity.getFinalCamp(), target.getFinalCamp() )	#阵营关系
			if campRelation != csdefine.COMBAT_RELATION_DEFAULT:
				return campRelation

			return csdefine.COMBAT_RELATION_NORMAL
		# 其他物种，默认为友好
		else:
			return csdefine.COMBAT_RELATION_NORMAL

class RelRole_PKMode( RelationBase ):
	"""
	玩家关系判断类：pk模式决定pvp关系
	"""
	@classmethod
	def getRelation( SELF, srcEntity, target ):
		"""
		virtual method
		"""
		#非战斗entity
		if target.getEntityFlag() not in csdefine.COMBAT_ENTITY_FLAG_LIST:
			return csdefine.COMBAT_RELATION_NORMAL
		
		#非战斗状态
		#if srcEntity.getState() in csconst.NOT_ATTACK_STATES:
		#	return csdefine.COMBAT_RELATION_NONE
		
		#是否准备好
		if not srcEntity.isReady() or ( target and not target.isReady() ):
			return csdefine.COMBAT_RELATION_NONE
		
		# 观察者标志位
		if srcEntity.hasFlag( csdefine.ROLE_FLAG_WATCHER ):
			return csdefine.COMBAT_RELATION_NORMAL
		
		#自己有潜入
		if srcEntity.isHasStateFlag(csdefine.STATE_FLAG_SLIPINTO):
			return csdefine.COMBAT_RELATION_NORMAL
		
		#对方有潜入
		if target.isHasStateFlag(csdefine.STATE_FLAG_SLIPINTO):
			return csdefine.COMBAT_RELATION_NORMAL

		#如果是幻兽，则把判断对象换成主人
		if target and target.getEntityFlag() == csdefine.ENTITY_FLAG_VEHICLEPET:
			target = target.getOwnerEntity()

		#如果是傀儡，则把判断对象换成傀儡施法者
		if target and target.getEntityFlag() == csdefine.ENTITY_FLAG_GHOST_RECEIVER:
			target = target.getOwnerEntity()

		if target and target.getEntityFlagExt() == csdefine.ENTITY_FLAG_EXT_MONSTER_EXT_TISHEN:
			target = target.getOwnerEntity()
			
		if target and target.getEntityFlagExt() == csdefine.ENTITY_FLAG_EXT_FENSHEN:
			target = target.getOwnerEntity()
		
		#CMonster
		if target and target.getEntityFlagExt() == csdefine.ENTITY_FLAG_MONSTER_CTRL_BY_CLIENT:
			target = target.getControlEntity()
			

		if target == None:
			return csdefine.COMBAT_RELATION_NORMAL

		# 对方是玩家，默认为友好
		if target.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:

			if srcEntity.isHasStateFlag(csdefine.STATE_FLAG_XIN_MO) or target.isHasStateFlag(csdefine.STATE_FLAG_XIN_MO):
				return csdefine.COMBAT_RELATION_ENEMY

			if srcEntity.isTeammate( target.id ):
				return csdefine.COMBAT_RELATION_NORMAL
			
			relation = srcEntity.getPkModeRelation( target )		#pk模式决定关系
			if relation != csdefine.COMBAT_RELATION_DEFAULT:
				return relation
			
			return csdefine.COMBAT_RELATION_NORMAL
		
		# 对方是怪物，默认为敌对
		elif target.getEntityFlag() == csdefine.ENTITY_FLAG_MONSTER:

			if target.isState( csdefine.ENTITY_STATE_RESET ):
				return csdefine.COMBAT_RELATION_NONE
			
			if target.hasFlag( csdefine.FLAG_RELATION_NORMAL_TO_ROLE ):
				return csdefine.COMBAT_RELATION_NORMAL

			if target.hasFlag( csdefine.FLAG_RELATION_ENEMY_TO_ROLE ):
				return csdefine.COMBAT_RELATION_ENEMY

			campRelation = srcEntity.getCampRelation( srcEntity.getFinalCamp(), target.getFinalCamp() )		#阵营关系
			if campRelation != csdefine.COMBAT_RELATION_DEFAULT:
				return campRelation
			return csdefine.COMBAT_RELATION_ENEMY
		# 对方是NPC，默认为友好
		elif target.getEntityFlag() == csdefine.ENTITY_FLAG_NPC:
			campRelation = srcEntity.getCampRelation( srcEntity.getFinalCamp(), target.getFinalCamp() )	#阵营关系
			if campRelation != csdefine.COMBAT_RELATION_DEFAULT:
				return campRelation

			return csdefine.COMBAT_RELATION_NORMAL
		# 其他物种，默认为友好
		else:
			return csdefine.COMBAT_RELATION_NORMAL

class RelRole_Peace( RelationBase ):
	"""
	玩家关系判断类：与其他玩家完全友好
	"""
	@classmethod
	def getRelation( SELF, srcEntity, target ):
		"""
		virtual method
		"""
		#非战斗entity
		if target.getEntityFlag() not in csdefine.COMBAT_ENTITY_FLAG_LIST:
			return csdefine.COMBAT_RELATION_NORMAL
		
		#非战斗状态
		#if srcEntity.getState() in csconst.NOT_ATTACK_STATES:
		#	return csdefine.COMBAT_RELATION_NONE
		
		#是否准备好
		if not srcEntity.isReady() or ( target and not target.isReady() ):
			return csdefine.COMBAT_RELATION_NONE
		
		# 观察者标志位
		if srcEntity.hasFlag( csdefine.ROLE_FLAG_WATCHER ):
			return csdefine.COMBAT_RELATION_NORMAL
		
		#自己有潜入
		if srcEntity.isHasStateFlag(csdefine.STATE_FLAG_SLIPINTO):
			return csdefine.COMBAT_RELATION_NORMAL
		
		#对方有潜入
		if target.isHasStateFlag(csdefine.STATE_FLAG_SLIPINTO):
			return csdefine.COMBAT_RELATION_NORMAL

		#如果是幻兽，则把判断对象换成主人
		if target and target.getEntityFlag() == csdefine.ENTITY_FLAG_VEHICLEPET:
			target = target.getOwnerEntity()

		#如果是傀儡，则把判断对象换成傀儡施法者
		if target and target.getEntityFlag() == csdefine.ENTITY_FLAG_GHOST_RECEIVER:
			target = target.getOwnerEntity()

		if target and target.getEntityFlagExt() == csdefine.ENTITY_FLAG_EXT_MONSTER_EXT_TISHEN:
			target = target.getOwnerEntity()

		if target and target.getEntityFlagExt() == csdefine.ENTITY_FLAG_EXT_FENSHEN:
			target = target.getOwnerEntity()
		
		#CMonster
		if target and target.getEntityFlagExt() == csdefine.ENTITY_FLAG_MONSTER_CTRL_BY_CLIENT:
			target = target.getControlEntity()
			

		if target == None:
			return csdefine.COMBAT_RELATION_NORMAL

		# 对方是玩家，默认为友好
		if target.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
			
			return csdefine.COMBAT_RELATION_NORMAL
		
		# 对方是怪物，默认为敌对
		elif target.getEntityFlag() == csdefine.ENTITY_FLAG_MONSTER:

			if target.isState( csdefine.ENTITY_STATE_RESET ):
				return csdefine.COMBAT_RELATION_NONE
			
			if target.hasFlag( csdefine.FLAG_RELATION_NORMAL_TO_ROLE ):
				return csdefine.COMBAT_RELATION_NORMAL

			if target.hasFlag( csdefine.FLAG_RELATION_ENEMY_TO_ROLE ):
				return csdefine.COMBAT_RELATION_ENEMY

			campRelation = srcEntity.getCampRelation( srcEntity.getFinalCamp(), target.getFinalCamp() )		#阵营关系
			if campRelation != csdefine.COMBAT_RELATION_DEFAULT:
				return campRelation
			
			return csdefine.COMBAT_RELATION_ENEMY
		# 对方是NPC，默认为友好
		elif target.getEntityFlag() == csdefine.ENTITY_FLAG_NPC:
			campRelation = srcEntity.getCampRelation( srcEntity.getFinalCamp(), target.getFinalCamp() )	#阵营关系
			if campRelation != csdefine.COMBAT_RELATION_DEFAULT:
				return campRelation

			return csdefine.COMBAT_RELATION_NORMAL
		# 其他物种，默认为友好
		else:
			return csdefine.COMBAT_RELATION_NORMAL

class RelRole_Enemy( RelationBase ):
	"""
	玩家关系判断类：与其他玩家完全敌对
	"""
	@classmethod
	def getRelation( SELF, srcEntity, target ):
		"""
		virtual method
		"""
		#非战斗entity
		if target.getEntityFlag() not in csdefine.COMBAT_ENTITY_FLAG_LIST:
			return csdefine.COMBAT_RELATION_NORMAL

		#非战斗状态
		#if srcEntity.getState() in csconst.NOT_ATTACK_STATES:
		#	return csdefine.COMBAT_RELATION_NONE

		#是否准备好
		if not srcEntity.isReady() or ( target and not target.isReady() ):
			return csdefine.COMBAT_RELATION_NONE

		#观察者标志位
		if srcEntity.hasFlag( csdefine.ROLE_FLAG_WATCHER ):
			return csdefine.COMBAT_RELATION_NORMAL

		#自己有潜入
		if srcEntity.isHasStateFlag(csdefine.STATE_FLAG_SLIPINTO):
			return csdefine.COMBAT_RELATION_NORMAL

		#对方有潜入
		if target.isHasStateFlag(csdefine.STATE_FLAG_SLIPINTO):
			return csdefine.COMBAT_RELATION_NORMAL

		#如果是幻兽，则把判断对象换成主人
		if target and target.getEntityFlag() == csdefine.ENTITY_FLAG_VEHICLEPET:
			target = target.getOwnerEntity()

		#如果是傀儡，则把判断对象换成傀儡施法者
		if target and target.getEntityFlag() == csdefine.ENTITY_FLAG_GHOST_RECEIVER:
			target = target.getOwnerEntity()

		if target and target.getEntityFlagExt() == csdefine.ENTITY_FLAG_EXT_MONSTER_EXT_TISHEN:
			target = target.getOwnerEntity()
			
		if target and target.getEntityFlagExt() == csdefine.ENTITY_FLAG_EXT_FENSHEN:
			target = target.getOwnerEntity()
		
		#CMonster
		if target and target.getEntityFlagExt() == csdefine.ENTITY_FLAG_MONSTER_CTRL_BY_CLIENT:
			target = target.getControlEntity()
			

		if target == None:
			return csdefine.COMBAT_RELATION_NORMAL

		# 对方是玩家，默认为友好
		if target.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE and target.id != srcEntity.id:
			
			return csdefine.COMBAT_RELATION_ENEMY

		# 对方是怪物，默认为敌对
		elif target.getEntityFlag() == csdefine.ENTITY_FLAG_MONSTER:

			if target.isState( csdefine.ENTITY_STATE_RESET ):
				return csdefine.COMBAT_RELATION_NONE
			
			if target.hasFlag( csdefine.FLAG_RELATION_NORMAL_TO_ROLE ):
				return csdefine.COMBAT_RELATION_NORMAL

			if target.hasFlag( csdefine.FLAG_RELATION_ENEMY_TO_ROLE ):
				return csdefine.COMBAT_RELATION_ENEMY

			campRelation = srcEntity.getCampRelation( srcEntity.getFinalCamp(), target.getFinalCamp() )		#阵营关系
			if campRelation != csdefine.COMBAT_RELATION_DEFAULT:
				return campRelation
			
			return csdefine.COMBAT_RELATION_ENEMY
		# 对方是NPC，默认为友好
		elif target.getEntityFlag() == csdefine.ENTITY_FLAG_NPC:
			campRelation = srcEntity.getCampRelation( srcEntity.getFinalCamp(), target.getFinalCamp() )	#阵营关系
			if campRelation != csdefine.COMBAT_RELATION_DEFAULT:
				return campRelation

			return csdefine.COMBAT_RELATION_NORMAL
		# 其他物种，默认为友好
		else:
			return csdefine.COMBAT_RELATION_NORMAL

class RelRole_TongStarcraft( RelationBase ):
	"""
	玩家关系判断类:与其他帮会玩家敌对
	"""
	@classmethod
	def getRelation( SELF, srcEntity, target ):
		"""
		virtual method
		"""
		#非战斗entity
		if target.getEntityFlag() not in csdefine.COMBAT_ENTITY_FLAG_LIST:
			return csdefine.COMBAT_RELATION_NORMAL

		#非战斗状态
		#if srcEntity.getState() in csconst.NOT_ATTACK_STATES:
		#	return csdefine.COMBAT_RELATION_NONE

		#是否准备好
		if not srcEntity.isReady() or ( target and not target.isReady() ):
			return csdefine.COMBAT_RELATION_NONE

		#观察者标志位
		if srcEntity.hasFlag( csdefine.ROLE_FLAG_WATCHER ):
			return csdefine.COMBAT_RELATION_NORMAL

		#自己有潜入
		if srcEntity.isHasStateFlag(csdefine.STATE_FLAG_SLIPINTO):
			return csdefine.COMBAT_RELATION_NORMAL

		#对方有潜入
		if target.isHasStateFlag(csdefine.STATE_FLAG_SLIPINTO):
			return csdefine.COMBAT_RELATION_NORMAL

		#如果是幻兽，则把判断对象换成主人
		if target and target.getEntityFlag() == csdefine.ENTITY_FLAG_VEHICLEPET:
			target = target.getOwnerEntity()

		#如果是傀儡，则把判断对象换成傀儡施法者
		if target and target.getEntityFlag() == csdefine.ENTITY_FLAG_GHOST_RECEIVER:
			target = target.getOwnerEntity()

		if target and target.getEntityFlagExt() == csdefine.ENTITY_FLAG_EXT_MONSTER_EXT_TISHEN:
			target = target.getOwnerEntity()
			
		if target and target.getEntityFlagExt() == csdefine.ENTITY_FLAG_EXT_FENSHEN:
			target = target.getOwnerEntity()
		
		#CMonster
		if target and target.getEntityFlagExt() == csdefine.ENTITY_FLAG_MONSTER_CTRL_BY_CLIENT:
			target = target.getControlEntity()
			

		if target == None:
			return csdefine.COMBAT_RELATION_NORMAL
		# 对方是玩家
		if target.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE and srcEntity.tongMB and target.tongMB and srcEntity.tongDBID != target.tongDBID:
			return csdefine.COMBAT_RELATION_ENEMY

		# 对方是怪物，默认为敌对
		elif target.getEntityFlag() == csdefine.ENTITY_FLAG_MONSTER:

			if target.isState( csdefine.ENTITY_STATE_RESET ):
				return csdefine.COMBAT_RELATION_NONE
			
			if target.hasFlag( csdefine.FLAG_RELATION_NORMAL_TO_ROLE ):
				return csdefine.COMBAT_RELATION_NORMAL

			if target.hasFlag( csdefine.FLAG_RELATION_ENEMY_TO_ROLE ):
				return csdefine.COMBAT_RELATION_ENEMY

			campRelation = srcEntity.getCampRelation( srcEntity.getFinalCamp(), target.getFinalCamp() )		#阵营关系
			if campRelation != csdefine.COMBAT_RELATION_DEFAULT:
				return campRelation
			
			return csdefine.COMBAT_RELATION_ENEMY
		# 对方是NPC，默认为友好
		elif target.getEntityFlag() == csdefine.ENTITY_FLAG_NPC:
			campRelation = srcEntity.getCampRelation( srcEntity.getFinalCamp(), target.getFinalCamp() )	#阵营关系
			if campRelation != csdefine.COMBAT_RELATION_DEFAULT:
				return campRelation

			return csdefine.COMBAT_RELATION_NORMAL
		# 其他物种，默认为友好
		else:
			return csdefine.COMBAT_RELATION_NORMAL

class RelRole_TeamStarcraft( RelationBase ):
	"""
	玩家关系判断类:与其他队伍玩家敌对
	"""
	@classmethod
	def getRelation( SELF, srcEntity, target ):
		"""
		virtual method
		"""
		#非战斗entity
		if target.getEntityFlag() not in csdefine.COMBAT_ENTITY_FLAG_LIST:
			return csdefine.COMBAT_RELATION_NORMAL

		#非战斗状态
		#if srcEntity.getState() in csconst.NOT_ATTACK_STATES:
		#	return csdefine.COMBAT_RELATION_NONE

		#是否准备好
		if not srcEntity.isReady() or ( target and not target.isReady() ):
			return csdefine.COMBAT_RELATION_NONE

		#观察者标志位
		if srcEntity.hasFlag( csdefine.ROLE_FLAG_WATCHER ):
			return csdefine.COMBAT_RELATION_NORMAL

		#自己有潜入
		if srcEntity.isHasStateFlag(csdefine.STATE_FLAG_SLIPINTO):
			return csdefine.COMBAT_RELATION_NORMAL

		#对方有潜入
		if target.isHasStateFlag(csdefine.STATE_FLAG_SLIPINTO):
			return csdefine.COMBAT_RELATION_NORMAL

		#如果是幻兽，则把判断对象换成主人
		if target and target.getEntityFlag() == csdefine.ENTITY_FLAG_VEHICLEPET:
			target = target.getOwnerEntity()

		#如果是傀儡，则把判断对象换成傀儡施法者
		if target and target.getEntityFlag() == csdefine.ENTITY_FLAG_GHOST_RECEIVER:
			target = target.getOwnerEntity()

		if target and target.getEntityFlagExt() == csdefine.ENTITY_FLAG_EXT_MONSTER_EXT_TISHEN:
			target = target.getOwnerEntity()
			
		if target and target.getEntityFlagExt() == csdefine.ENTITY_FLAG_EXT_FENSHEN:
			target = target.getOwnerEntity()
		
		#CMonster
		if target and target.getEntityFlagExt() == csdefine.ENTITY_FLAG_MONSTER_CTRL_BY_CLIENT:
			target = target.getControlEntity()

		if target == None:
			return csdefine.COMBAT_RELATION_NORMAL
		# 对方是玩家
		if target.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE and srcEntity.teamMailbox and target.teamMailbox and srcEntity.teamMailbox.id != target.teamMailbox.id:
			return csdefine.COMBAT_RELATION_ENEMY

		# 对方是怪物，默认为敌对
		elif target.getEntityFlag() == csdefine.ENTITY_FLAG_MONSTER:

			if target.isState( csdefine.ENTITY_STATE_RESET ):
				return csdefine.COMBAT_RELATION_NONE
			
			if target.hasFlag( csdefine.FLAG_RELATION_NORMAL_TO_ROLE ):
				return csdefine.COMBAT_RELATION_NORMAL

			if target.hasFlag( csdefine.FLAG_RELATION_ENEMY_TO_ROLE ):
				return csdefine.COMBAT_RELATION_ENEMY

			campRelation = srcEntity.getCampRelation( srcEntity.getFinalCamp(), target.getFinalCamp() )		#阵营关系
			if campRelation != csdefine.COMBAT_RELATION_DEFAULT:
				return campRelation
			
			return csdefine.COMBAT_RELATION_ENEMY
		# 对方是NPC，默认为友好
		elif target.getEntityFlag() == csdefine.ENTITY_FLAG_NPC:
			campRelation = srcEntity.getCampRelation( srcEntity.getFinalCamp(), target.getFinalCamp() )	#阵营关系
			if campRelation != csdefine.COMBAT_RELATION_DEFAULT:
				return campRelation

			return csdefine.COMBAT_RELATION_NORMAL
		# 其他物种，默认为友好
		else:
			return csdefine.COMBAT_RELATION_NORMAL

#---------------------------其他entity关系判断实例----------------------------------------
class RelMonster_Default( RelationBase ):
	"""
	通用Monster关系判断实例
	"""
	@classmethod
	def getRelation( SELF, srcEntity, target ):
		"""
		virtual method
		"""
		#非战斗entity
		if target.getEntityFlag() not in csdefine.COMBAT_ENTITY_FLAG_LIST:
			return csdefine.COMBAT_RELATION_NORMAL
		
		#非战斗状态
		#if srcEntity.getState() in csconst.NOT_ATTACK_STATES:
		#	return csdefine.COMBAT_RELATION_NONE
		
		#是否准备好
		if not srcEntity.isReady() or ( target and not target.isReady() ):
			return csdefine.COMBAT_RELATION_NONE
		
		#自己有潜入
		if srcEntity.isHasStateFlag(csdefine.STATE_FLAG_SLIPINTO):
			return csdefine.COMBAT_RELATION_NORMAL
		
		#对方有潜入
		if target.isHasStateFlag(csdefine.STATE_FLAG_SLIPINTO):
			return csdefine.COMBAT_RELATION_NORMAL
			
		#如果是幻兽，则把判断对象换成主人
		if target and target.getEntityFlag() == csdefine.ENTITY_FLAG_VEHICLEPET:
			target = target.getOwnerEntity()

		#如果是傀儡，则把判断对象换成傀儡施法者
		if target and target.getEntityFlag() == csdefine.ENTITY_FLAG_GHOST_RECEIVER:
			target = target.getOwnerEntity()

		if target and target.getEntityFlagExt() == csdefine.ENTITY_FLAG_EXT_MONSTER_EXT_TISHEN:
			target = target.getOwnerEntity()
			
		if target and target.getEntityFlagExt() == csdefine.ENTITY_FLAG_EXT_FENSHEN:
			target = target.getOwnerEntity()
		
		#如果是callMonster，则把判断对象换成主人
		if target and target.getEntityFlagExt() == csdefine.ENTITY_FLAG_EXT_MONSTER_EXT_CALL:
			target = target.getOwnerEntity()

		#CMonster
		if target and target.getEntityFlagExt() == csdefine.ENTITY_FLAG_MONSTER_CTRL_BY_CLIENT:
			target = target.getControlEntity()

		if target == None:
			return csdefine.COMBAT_RELATION_NORMAL
			
		# 对方是玩家，默认为敌对
		if target.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:

			if target.hasFlag( csdefine.ROLE_FLAG_WATCHER ):
				return csdefine.COMBAT_RELATION_NORMAL
			
			if srcEntity.hasFlag( csdefine.FLAG_RELATION_NORMAL_TO_ROLE ):
				return csdefine.COMBAT_RELATION_NORMAL
			
			if srcEntity.hasFlag( csdefine.FLAG_RELATION_ENEMY_TO_ROLE):
				return csdefine.COMBAT_RELATION_ENEMY
				
			campRelation = srcEntity.getCampRelation( srcEntity.getFinalCamp(), target.getFinalCamp() )		#阵营关系
			if campRelation != csdefine.COMBAT_RELATION_DEFAULT:
				return campRelation
			
			return csdefine.COMBAT_RELATION_ENEMY
		
		# 对方是怪物，默认为友好
		elif target.getEntityFlag() == csdefine.ENTITY_FLAG_MONSTER:
			if srcEntity.hasFlag( csdefine.FLAG_RELATION_ENEMY_TO_MONSTER ) and target.hasFlag( csdefine.FLAG_RELATION_NORMAL_TO_MONSTER ):		# 有相矛盾的标记位则抵消
				pass
			elif srcEntity.hasFlag( csdefine.FLAG_RELATION_NORMAL_TO_MONSTER ) and target.hasFlag( csdefine.FLAG_RELATION_ENEMY_TO_MONSTER ):	# 有相矛盾的标记位则抵消
				pass
			elif srcEntity.hasFlag( csdefine.FLAG_RELATION_NORMAL_TO_MONSTER ) or target.hasFlag( csdefine.FLAG_RELATION_NORMAL_TO_MONSTER ):	# 一方有友好标记位，返回友好
				return csdefine.COMBAT_RELATION_NORMAL
			elif srcEntity.hasFlag( csdefine.FLAG_RELATION_ENEMY_TO_MONSTER ) or target.hasFlag( csdefine.FLAG_RELATION_ENEMY_TO_MONSTER ):		# 一方有敌对标记位，返回敌对
				return csdefine.COMBAT_RELATION_ENEMY
			
			factionRelation = g_FactionRelationLoader.getRelation( srcEntity.getFinalfaction(), target.getFinalfaction() )	#势力关系
			if factionRelation != csdefine.COMBAT_RELATION_DEFAULT:
				return factionRelation
			
			campRelation = srcEntity.getCampRelation( srcEntity.getFinalCamp(), target.getFinalCamp() )				#阵营关系
			if campRelation != csdefine.COMBAT_RELATION_DEFAULT:
				return campRelation
			
			return csdefine.COMBAT_RELATION_NORMAL
		
		# 其他物种，默认为友好
		else:
			return csdefine.COMBAT_RELATION_NORMAL


#---------------------------其他entity关系判断实例----------------------------------------
class RelCMonster_Default( RelationBase ):
	"""
	通用Monster关系判断实例
	"""
	@classmethod
	def getRelation( SELF, srcEntity, target ):
		"""
		virtual method
		"""
		owner = srcEntity.getControlEntity()
		if owner:
			return owner.queryRelation(  target )
		return csdefine.COMBAT_RELATION_NORMAL
		
class RelTrapObject_Default( RelationBase ):
	"""
	通用TrapObject关系判断实例
	"""
	@classmethod
	def getRelation( SELF, srcEntity, target ):
		"""
		virtual method
		"""
		#如果目标是处于未准备好的状态下，则返回友好关系
		if not srcEntity.isReady() or not target.isReady():
			return csdefine.COMBAT_RELATION_NONE
		# 对方是玩家，默认为敌对
		if target.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
			
			if srcEntity.hasFlag( csdefine.FLAG_RELATION_EMENY_TO_ROLE ):
				return csdefine.COMBAT_RELATION_ENEMY
				
			if srcEntity.hasFlag( csdefine.FLAG_RELATION_FRIEND_TO_ROLE ):
				return csdefine.COMBAT_RELATION_NORMAL
				
		return csdefine.COMBAT_RELATION_NORMAL

class RelNPC_Default( RelationBase ):
	"""
	通用NPC关系判断实例
	"""
	@classmethod
	def getRelation( SELF, srcEntity, target ):
		"""
		virtual method
		"""
		return csdefine.COMBAT_RELATION_NORMAL

class RelSpellBox_Default( RelationBase ):
	"""
	通用SpellBox关系判断实例
	"""
	@classmethod
	def getRelation( SELF, srcEntity, target ):
		"""
		virtual method
		"""
		return csdefine.COMBAT_RELATION_NORMAL

class RelMovingPlatform_Default( RelationBase ):
	"""
	通用MovingPlatform关系判断实例
	"""
	@classmethod
	def getRelation( SELF, srcEntity, target ):
		"""
		virtual method
		"""
		return csdefine.COMBAT_RELATION_NORMAL

class RelVehiclePet_Default( RelationBase ):
	"""
	宠物关系判断实例
	"""
	@classmethod
	def getRelation( SELF, srcEntity, target ):
		"""
		virtual method
		"""
		#非战斗entity
		if target.getEntityFlag() not in csdefine.COMBAT_ENTITY_FLAG_LIST:
			return csdefine.COMBAT_RELATION_NORMAL
		
		#非战斗状态
		#if srcEntity.getState() in csconst.NOT_ATTACK_STATES:
		#	return csdefine.COMBAT_RELATION_NONE
		
		#是否准备好
		if not srcEntity.isReady() or ( target and not target.isReady() ):
			return csdefine.COMBAT_RELATION_NONE
		
		#如果是幻兽，则把对象改成主人
		if target and target.getEntityFlag() == csdefine.ENTITY_FLAG_VEHICLEPET:
			target = target.getOwnerEntity()

		#如果是傀儡，则把判断对象换成傀儡施法者
		if target and target.getEntityFlag() == csdefine.ENTITY_FLAG_GHOST_RECEIVER:
			target = target.getOwnerEntity()

		if target and target.getEntityFlagExt() == csdefine.ENTITY_FLAG_EXT_MONSTER_EXT_TISHEN:
			target = target.getOwnerEntity()
			
		if target and target.getEntityFlagExt() == csdefine.ENTITY_FLAG_EXT_FENSHEN:
			target = target.getOwnerEntity()
		
		#CMonster
		if target and target.getEntityFlagExt() == csdefine.ENTITY_FLAG_MONSTER_CTRL_BY_CLIENT:
			target = target.getControlEntity()

		if target == None:
			return csdefine.COMBAT_RELATION_NORMAL
			
		if srcEntity.getOwnerEntity():
			return srcEntity.getOwnerEntity().queryRelation( target )
		else:
			return csdefine.COMBAT_RELATION_NORMAL
	
class RelMonsterExtTiShen( RelationBase ):
	"""
	替身关系判断实例
	"""
	@classmethod
	def getRelation( SELF, srcEntity, target ):
		"""
		virtual method
		"""
		return srcEntity.getRelation(target)
		
class RelMonsterExtFenShen( RelationBase ):
	"""
	分身关系判断实例
	"""
	@classmethod
	def getRelation( SELF, srcEntity, target ):
		"""
		virtual method
		"""
		return srcEntity.getRelation(target)

class RelGhostReceiver_Default( RelationBase ):
	"""
	傀儡关系判断
	"""
	@classmethod
	def getRelation( SELF, srcEntity, target ):
		"""
		virtual method
		"""
		#非战斗entity
		if target.getEntityFlag() not in csdefine.COMBAT_ENTITY_FLAG_LIST:
			return csdefine.COMBAT_RELATION_NORMAL

		# #非战斗状态
		# if srcEntity.getState() in csconst.NOT_ATTACK_STATES:
		# 	return csdefine.COMBAT_RELATION_NONE
		
		#是否准备好
		if not srcEntity.isReady() or ( target and not target.isReady() ):
			return csdefine.COMBAT_RELATION_NONE

		#如果是幻兽，则把判断对象换成主人
		if target and target.getEntityFlag() == csdefine.ENTITY_FLAG_VEHICLEPET:
			target = target.getOwnerEntity()

		#如果是傀儡，则把判断对象换成傀儡施法者
		if target and target.getEntityFlag() == csdefine.ENTITY_FLAG_GHOST_RECEIVER:
			target = target.getOwnerEntity()

		if target and target.getEntityFlagExt() == csdefine.ENTITY_FLAG_EXT_MONSTER_EXT_TISHEN:
			target = target.getOwnerEntity()
			
		if target and target.getEntityFlagExt() == csdefine.ENTITY_FLAG_EXT_FENSHEN:
			target = target.getOwnerEntity()
		
		#CMonster
		if target and target.getEntityFlagExt() == csdefine.ENTITY_FLAG_MONSTER_CTRL_BY_CLIENT:
			target = target.getControlEntity()

		if target == None:
			return csdefine.COMBAT_RELATION_DEFAULT

		if srcEntity.getOwnerEntity():
			return srcEntity.getOwnerEntity().queryRelation( target )
		else:
			return csdefine.COMBAT_RELATION_DEFAULT

class RelRoleEntityRelationGCZ( RelationBase ):
	"""
	攻城战 玩家关系判断实例
	"""
	@classmethod
	def getRelation( SELF, srcEntity, target ):
		"""
		virtual method
		"""
		#非战斗entity
		if target.getEntityFlag() not in csdefine.COMBAT_ENTITY_FLAG_LIST:
			return csdefine.COMBAT_RELATION_NORMAL
		
		#非战斗状态
		#if srcEntity.getState() in csconst.NOT_ATTACK_STATES:
		#	return csdefine.COMBAT_RELATION_NONE
		
		#是否准备好
		if not srcEntity.isReady() or ( target and not target.isReady() ):
			return csdefine.COMBAT_RELATION_NONE
		
		# 观察者标志位
		if srcEntity.hasFlag( csdefine.ROLE_FLAG_WATCHER ):
			return csdefine.COMBAT_RELATION_NORMAL
		
		#自己有潜入
		if srcEntity.isHasStateFlag(csdefine.STATE_FLAG_SLIPINTO):
			return csdefine.COMBAT_RELATION_NORMAL
		
		#对方有潜入
		if target.isHasStateFlag(csdefine.STATE_FLAG_SLIPINTO):
			return csdefine.COMBAT_RELATION_NORMAL

		#如果是幻兽，则把判断对象换成主人
		if target and target.getEntityFlag() == csdefine.ENTITY_FLAG_VEHICLEPET:
			target = target.getOwnerEntity()

		#如果是傀儡，则把判断对象换成傀儡施法者
		if target and target.getEntityFlag() == csdefine.ENTITY_FLAG_GHOST_RECEIVER:
			target = target.getOwnerEntity()

		if target and target.getEntityFlagExt() == csdefine.ENTITY_FLAG_EXT_MONSTER_EXT_TISHEN:
			target = target.getOwnerEntity()

		if target and target.getEntityFlagExt() == csdefine.ENTITY_FLAG_EXT_FENSHEN:
			target = target.getOwnerEntity()
		
		#CMonster
		if target and target.getEntityFlagExt() == csdefine.ENTITY_FLAG_MONSTER_CTRL_BY_CLIENT:
			target = target.getControlEntity()
			

		if target == None:
			return csdefine.COMBAT_RELATION_NORMAL

		# 对方是玩家，默认为友好
		if target.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
			if srcEntity.getBelongSide() != target.getBelongSide():
				return csdefine.COMBAT_RELATION_ENEMY
			return csdefine.COMBAT_RELATION_NORMAL

		# 对方是怪物，默认为敌对
		elif target.getEntityFlag() == csdefine.ENTITY_FLAG_MONSTER:

			if target.isState( csdefine.ENTITY_STATE_RESET ):
				return csdefine.COMBAT_RELATION_NONE

			if target.hasFlag( csdefine.FLAG_RELATION_NORMAL_TO_ROLE ):
				return csdefine.COMBAT_RELATION_NORMAL

			if target.hasFlag( csdefine.FLAG_RELATION_ENEMY_TO_ROLE ):
				return csdefine.COMBAT_RELATION_ENEMY

			if srcEntity.getBelongSide() == target.getBelongSide():
				return csdefine.COMBAT_RELATION_NORMAL
			return csdefine.COMBAT_RELATION_ENEMY

		# 其他物种，默认为友好
		else:
			return csdefine.COMBAT_RELATION_NORMAL

class RelEntityRelationGCZ( RelationBase ):
	"""
	攻城战 Entity关系判断实例
	"""
	@classmethod
	def getRelation( SELF, srcEntity, target ):
		"""
		virtual method
		"""
		#非战斗entity
		if srcEntity.getEntityFlag() not in csdefine.COMBAT_ENTITY_FLAG_LIST:
			return csdefine.COMBAT_RELATION_NORMAL
		#非战斗entity
		if target.getEntityFlag() not in csdefine.COMBAT_ENTITY_FLAG_LIST:
			return csdefine.COMBAT_RELATION_NORMAL

		#是否准备好
		if not srcEntity.isReady() or ( target and not target.isReady() ):
			return csdefine.COMBAT_RELATION_NONE
		
		#自己有潜入
		if srcEntity.isHasStateFlag(csdefine.STATE_FLAG_SLIPINTO):
			return csdefine.COMBAT_RELATION_NORMAL
		
		#对方有潜入
		if target.isHasStateFlag(csdefine.STATE_FLAG_SLIPINTO):
			return csdefine.COMBAT_RELATION_NORMAL
			
		#如果是幻兽，则把判断对象换成主人
		if target and target.getEntityFlag() == csdefine.ENTITY_FLAG_VEHICLEPET:
			target = target.getOwnerEntity()

		#如果是傀儡，则把判断对象换成傀儡施法者
		if target and target.getEntityFlag() == csdefine.ENTITY_FLAG_GHOST_RECEIVER:
			target = target.getOwnerEntity()

		if target and target.getEntityFlagExt() == csdefine.ENTITY_FLAG_EXT_MONSTER_EXT_TISHEN:
			target = target.getOwnerEntity()
			
		if target and target.getEntityFlagExt() == csdefine.ENTITY_FLAG_EXT_FENSHEN:
			target = target.getOwnerEntity()
		
		#CMonster
		if target and target.getEntityFlagExt() == csdefine.ENTITY_FLAG_MONSTER_CTRL_BY_CLIENT:
			target = target.getControlEntity()

		if target == None:
			return csdefine.COMBAT_RELATION_NORMAL
			
		# 对方是玩家，默认为敌对
		if target.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
			if target.hasFlag( csdefine.ROLE_FLAG_WATCHER ):
				return csdefine.COMBAT_RELATION_NORMAL
			
			if srcEntity.hasFlag( csdefine.FLAG_RELATION_NORMAL_TO_ROLE ):
				return csdefine.COMBAT_RELATION_NORMAL
			
			if srcEntity.hasFlag( csdefine.FLAG_RELATION_ENEMY_TO_ROLE):
				return csdefine.COMBAT_RELATION_ENEMY

			if srcEntity.getBelongSide() == target.getBelongSide():
				return csdefine.COMBAT_RELATION_NORMAL
			return csdefine.COMBAT_RELATION_ENEMY

		# 对方是怪物，默认为友好
		elif target.getEntityFlag() == csdefine.ENTITY_FLAG_MONSTER:
			if srcEntity.hasFlag( csdefine.FLAG_RELATION_NORMAL_TO_MONSTER ) or target.hasFlag( csdefine.FLAG_RELATION_NORMAL_TO_MONSTER ):	# 一方有友好标记位，返回友好
				return csdefine.COMBAT_RELATION_NORMAL
			elif srcEntity.hasFlag( csdefine.FLAG_RELATION_ENEMY_TO_MONSTER ) or target.hasFlag( csdefine.FLAG_RELATION_ENEMY_TO_MONSTER ):		# 一方有敌对标记位，返回敌对
				return csdefine.COMBAT_RELATION_ENEMY
			if srcEntity.getBelongSide() != target.getBelongSide():
				return csdefine.COMBAT_RELATION_ENEMY
			return csdefine.COMBAT_RELATION_NORMAL

		# 其他物种，默认为友好
		else:
			return csdefine.COMBAT_RELATION_NORMAL
			
class RelEntityRelationLHMJ( RelationBase ):
	"""
	轮回秘境 entity关系判断实例
	"""
	@classmethod
	def getRelation( SELF, srcEntity, target ):
		"""
		virtual method
		"""
		if target.isEntityFlag( csdefine.ENTITY_FLAG_MONSTER ) and not target.isEntityFlagExt(csdefine.ENTITY_FLAG_EXT_MONSTER_EXT_COVER):
			return csdefine.COMBAT_RELATION_ENEMY
		# 活动开启才能开打
		if KBEngine.globalData.get( "LHMJ_ChallengeActive") or KBEngine.globalData.get( "LHMJ_PlunderActive"):
			if srcEntity.isEntityFlag( csdefine.ENTITY_FLAG_VEHICLEPET ):	# 幻兽 转化为 玩家
				srcEntity = srcEntity.getOwnerEntity()
				
			if srcEntity.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ):
				if target.isEntityFlag( csdefine.ENTITY_FLAG_VEHICLEPET ):
					target = target.getOwnerEntity()
				if target and target.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ):
					if srcEntity.playerDBID == target.challengeDBID:
						return csdefine.COMBAT_RELATION_ENEMY
					elif srcEntity.challengeDBID == target.playerDBID:
						return csdefine.COMBAT_RELATION_ENEMY
				elif target.isEntityFlagExt(csdefine.ENTITY_FLAG_EXT_MONSTER_EXT_COVER):
					if target.belongDBID == srcEntity.challengeDBID:
						return csdefine.COMBAT_RELATION_ENEMY
						
			elif srcEntity.isEntityFlagExt(csdefine.ENTITY_FLAG_EXT_MONSTER_EXT_COVER):
				if srcEntity.belongDBID == target.challengeDBID:
					return csdefine.COMBAT_RELATION_ENEMY
		return csdefine.COMBAT_RELATION_NORMAL