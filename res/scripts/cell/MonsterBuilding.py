# -*- coding: utf-8 -*-


#python
#engine
import KBEngine
#script
import Monster
import csdefine

class MonsterBuilding( Monster.Monster ):
	"""
	防御塔类Monster
	"""
	def __init__( self ):
		Monster.Monster.__init__( self )

	def onWitnessed( self, isWitnessed ):
		"""
		玩家视野范围内才开始执行
		"""
		Monster.Monster.onWitnessed( self, isWitnessed )
		if isWitnessed:
			# 碰撞标志位
			self.addFlag( csdefine.FLAG_OPEN_COLLISION )
			#开启mesh和staticmesh的碰撞
			self.addFlag( csdefine.FLAG_MESH_COLLISION )
			# 霸体状态
			self.effectStateInc( csdefine.EFFECT_STATE_UNCONTROLLABLE )