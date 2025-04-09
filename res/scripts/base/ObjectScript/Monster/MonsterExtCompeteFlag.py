# -*- coding: utf-8 -*-

import ObjectScript.Monster.Monster as Monster
import csconst

class MonsterExtCompeteFlag( Monster.Monster ):
	"""
	切磋 旗子
	"""
	def __init__( self ):
		Monster.Monster.__init__( self )



	def onClientEntity(self, selfEntity):
		"""
		"""
		#生成光圈
		competeTargetID1 = selfEntity.queryTemp("competeTargetID1")
		competeTargetID2 = selfEntity.queryTemp("competeTargetID2")
		competeTarget1 =  KBEngine.entities.get(competeTargetID1, None)
		if competeTarget1:
			competeTarget1.clientEntity(selfEntity.id).CLIENT_OnPlayParticles(selfEntity.id, csconst.COMPETE_EFFECTID,"",-1.0,(0.0,0.0,0.0))

		competeTarget2 =  KBEngine.entities.get(competeTargetID2, None)
		if competeTarget2:
			competeTarget2.clientEntity(selfEntity.id).CLIENT_OnPlayParticles(selfEntity.id, csconst.COMPETE_EFFECTID,"",-1.0,(0.0,0.0,0.0))