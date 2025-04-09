# -*- coding- : utf-8 -*-

from ConfigObject.Drop.DropBase import Drop
import HotUpdate
import LoadModule

from Singleton import Singleton

class DropMgr( Singleton ):
	"""
	掉落数据管理器
	"""
	def __init__( self ):
		Singleton.__init__( self )
		self._dropDatas = {}

	def init( self ):
		jsFileObj = LoadModule. openJsonCfg( "GameObject/Monster.json" )
		for scriptID, sec in jsFileObj.items():
			self._dropDatas[ scriptID ] = Drop.Drop( sec )

	def reloadConfig( self ):
		"""
		配置支持热更新
		"""
		self._dropDatas.clear()
		jsFileObj = LoadModule. openJsonCfg( "GameObject/Monster.json" )
		for scriptID, sec in jsFileObj.items():
			self._dropDatas[ scriptID ] = Drop.Drop( sec )
	
	def getDrop( self, scriptID ):
		if scriptID in self._dropDatas:
			return self._dropDatas[scriptID]
		return None
	
	def drop( self, dieEntity, killer, args ):
		"""
		开始掉落处理
		"""
		if len(dieEntity.calculateBootyOwner()) > 0:	#非玩家杀死的怪物不执行掉落
			if dieEntity.getScriptID() in self._dropDatas:
				self._dropDatas[ dieEntity.getScriptID() ].doDrop( dieEntity, killer, args )

	def getMonsterDropItem( self, scriptID ):
		"""
		获取怪物掉落的物品,只能获取当前的怪物
		"""
		if scriptID in self._dropDatas:
			return self._dropDatas[scriptID].getDropItemDict()
		return {}
	
g_dropMgr = DropMgr()