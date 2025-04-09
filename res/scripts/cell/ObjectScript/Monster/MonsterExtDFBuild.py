# -*- coding: utf-8 -*-

import KBEngine
import csdefine
import ObjectScript.Monster.Monster as Monster


class MonsterExtDFBuild( Monster.Monster ):
	"""
	洞府建筑
	"""
	def __init__( self ):
		Monster.Monster.__init__( self )
	
	def initData( self, data ):
		"""
		初始化数据
		@param data: dict
		"""
		Monster.Monster.initData( self, data )
	
	def onRemoveEnemy( self, selfEntity, entityID ):
		"""
		重载掉此方法，敌人列表为空时不会进入重置状态
		"""
		pass
		
	def onHPChanged( self, selfEntity, oldValue ):
		"""
		virtual method
		血量改变
		"""
		if selfEntity.HP == selfEntity.HP_Max:return
		record = selfEntity.queryTemp("HPRecord", 0)
		percent = int(selfEntity.HP / selfEntity.HP_Max * 10)
		if record != percent:
			selfEntity.setTemp( "HPRecord", percent )
			space = selfEntity.getCurrentSpace()
			space.onDFBuildHPChange( self.param1 )




	


	


