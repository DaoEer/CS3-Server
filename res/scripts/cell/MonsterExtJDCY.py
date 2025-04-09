# -*- coding: utf-8 -*-


#python
#engine
import KBEngine
#script
import Monster
import Math
import math
import csdefine
import KBEDebug
import random
import FightRuleMgr

#额外增加的搜索范围，加上次搜索范围是为了检测：光墙中心位置在玩家和妖卫的外侧，但两边却挡在玩家和妖卫之间的情况
SEARCH_RANGE_EXTRA = 10
TALK_OFF_WAR_BUFF = 14034502

class MonsterExtJDCY( Monster.Monster ):
	"""
	禁地采药怪物
	"""
	def __init__( self ):
		Monster.Monster.__init__( self )

	def monsterAITriggerEvent( self, eventType, args = [], triggerEntity = None ):
		"""
		triggerEntity: 当不是自身entity触发此事件时，传入该entity（比如陷阱触发）
		触发一个事件
		"""
		Monster.Monster.monsterAITriggerEvent( self, eventType, args, triggerEntity )
		if len(args)>2 and args[2].strip() == "tuozhan":
			FightRuleMgr.g_fightMgr.breakEnemyRelation( self, triggerEntity )

	def setSelfEntityFlagExt(self):
		"""
		virtual method
		"""
		self.setEntityFlagExt(csdefine.ENTITY_FLAG_EXT_MONSTER_EXT_JDCY)
		
	def CELL_onClientReady( self, srcEntityID ):
		"""
		<Expose method>
		客户端Character Actor已经准备好
		"""
		Monster.Monster.CELL_onClientReady( self, srcEntityID )
		self.getScript().setUpMonsterBaseDatas( self )
		self.moveSpeed = self.getScript().getWalkSpeed( self )

	def CELL_onAttackTarget( self, srcEntityID ):
		"""
		<Expose method>
		攻击玩家
		"""
		self.setTargetID( srcEntityID )
		spellList = []
		skillList = list( self.attcakSkills )
		random.shuffle(skillList)
		for skillID in skillList:
			tempList = [ skillID, self.getTargetID(),True ]
			spellList.append(tempList)
		self.behAdds(csdefine.BEHAVIOUR_TYPE_SPELL, spellList,csdefine.BEHAVIOUR_LOOP)

	def CELL_onSetControlledBy( self, srcEntityID ):
		"""
		在玩家视野范围内才设置controlledBy
		"""
		player = KBEngine.entities.get( srcEntityID, None )
		if player and player.isEntityInView( self ):
			self.controlledBy = player.base

	def hasBaffle(self, dstPos, srcPos):
		"""
		检查两个位置键是否有光墙阻挡
		"""
		#只考虑光墙的长度，不考虑高度和宽度
		dist = srcPos.distTo(dstPos)
		entities = self.entitiesInRangeExt(dist + SEARCH_RANGE_EXTRA, "MonsterExtCanPush")
		if entities:
			for entity in entities:
				# length = float(entity.param1)
				length = 8.0
				#怪物到玩家间的线段和光墙两端之间的线段相交，则有光墙阻挡
				(p1, p2) = self.getBothEndPos(length, entity.position, entity.direction.z)
				if self.isIntersect(srcPos, dstPos, p1, p2):
					return True
		return False
		
	def getBothEndPos(self, length, centerPos, yaw):
		"""
		根据线条长度和中心点坐标以及yaw获取两端坐标
		"""
		#计算线段A、B两点的坐标，先计算中心点O到A、B的单位向量
		OA = Math.Vector3(math.sin(yaw+math.pi/2),0,math.cos(yaw+math.pi/2))
		OB = Math.Vector3(math.sin(yaw-math.pi/2),0,math.cos(yaw-math.pi/2))
		#A点坐标
		posA = centerPos + OA*(length/2)
		#B点坐标
		posB= centerPos + OB*(length/2)
		return (posA, posB)
		
	def mult(self, p1, p2, p3):
		"""
		叉积
		"""
		return (p1.x - p3.x) * (p2.z - p3.z) - (p2.x - p3.x) * (p1.z - p3.z)
		
	def isIntersect(self, p1, p2, p3, p4):
		"""
		判断两条线段(p1p2和p3p4)是否相交
		"""
		#p1, p2为一条线段两端点 p3, p4为另一条线段的两端点 相交返回true, 不相交返回false
		if max(p1.x, p2.x) < min(p3.x, p4.x ):
			return False
		if max(p1.z, p2.z) < min(p3.z, p4.z):
			return False
		if max(p3.x, p4.x) < min(p1.x, p2.x):
			return False
		if max(p3.z, p4.z) < min(p1.z, p2.z):
			return False
		if self.mult(p3, p2, p1) * self.mult(p2, p4, p1) < 0:
			return False
		if self.mult(p1, p4, p3) * self.mult(p4, p2, p3) < 0:
			return False
		return True


	def monsterAICheckInViewRange( self, id ):
		"""
		是否在视野范围
		"""
		entity = KBEngine.entities.get( id, None )
		if entity:
			if entity.position.flatDistTo( self.position ) <= self.viewRange \
			and self.checkScoutHeight( entity ) and not entity.findBuffsByBuffID(TALK_OFF_WAR_BUFF) \
			and not self.hasBaffle(entity.position, self.position):
				return True
		return False
		