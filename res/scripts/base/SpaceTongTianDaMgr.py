# -*- coding: utf-8 -*-
import csdefine
import KBEDebug
import KBEngine
import Const
import KST
import csstatus
import LoadModule
import time
from CoreObject import MgrPersistentObject

from ConfigObject.Crond.CrondDatas import CrondDatas
g_CrondDatas = CrondDatas.instance()


class SpaceTongTianDaMgr( MgrPersistentObject.MgrPersistentObject ):
	"""
	通天塔管理器
	"""
	def __init__( self ):
		MgrPersistentObject.MgrPersistentObject.__init__( self )
		self.challengeFailurePlayerList = []  # 突破挑战失败（playDBID，playDBID）
		self.tongTianDaData = {}
		self.register()
		self.initData()

	def initData( self ):
		"""
		解析数据
		"""
		dataCfg = LoadModule.openJsonCfg("LunHuiMiJin/TongTianDaCfg.json")
		self.tongTianDaData = dataCfg
		self.onCompleteInit()
		
	def register( self ):
		"""
		注册
		"""
		taskEvents = { "SpaceTongTianDaMgr_Clear":"onClearData"
		 }
		for taskName, callbackName in taskEvents.items():
			for scriptID, cmd in g_CrondDatas.getCrondTaskCmds(taskName):
		 		KBEngine.globalData["CrondManager"].addScheme( scriptID, cmd, self, callbackName, -1, () )

	def onClearData( self, cmd, *callbackArgs ):
		"""
		每日的0点更新，更新后玩家当日在通天塔中的数据会被全部清除
		"""
		KST.g_baseAppEntity.globalResetTongTianDaData()

	def onEnterTongTianDa( self, roleMB, layerNumber ):
		"""
		进入通天塔试炼
		"""
		roleMB.cell.gotoSpaceEnterPos( self.tongTianDaData[ str( layerNumber ) ], { "time": time.time() } )