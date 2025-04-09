# -*- coding: utf-8 -*-

import Const
from ObjectScript.SpellBox import SpellBox

class SpellBoxJinDan( SpellBox.SpellBox ):
	"""
	灵岛危机副本金丹脚本
	"""
	def __init__( self ):
		SpellBox.SpellBox.__init__( self )

	def onClientActorReady( self, selfEntity ):
		"""
		客户端Character Actor已经准备好
		"""
		if selfEntity.lifeTime > 0:
			selfEntity.allClients.CLIENT_ShowTopCountDown( selfEntity.getRemainLifeTime(), 1.0 )	#头顶显示倒计时，时长等于lifeTime时间		
	
	def onLifeTimeCB( self, selfEntity ):
		"""
		virtual method
		生存时间到达
		"""
		selfEntity.lifeTimerID = 0
		selfEntity.allClients.CLIENT_HideTopCountDown()				#隐藏头顶倒计时
		if selfEntity.onlifeTimeUseSkill:
			selfEntity.useSkillToEntity( selfEntity.onlifeTimeUseSkill , selfEntity.id )	#使用爆炸技能
		selfEntity.delayDestroy( 0.1 ) #目前由于spellbox自己对于自己释放技能，对于施法者自己增加的效果是无用的，对于其他entity的作用效果有用，所以做了自己手动销毁
		