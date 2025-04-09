# -*- coding: utf-8 -*-

import imp
import csdefine
import KST
import KBEDebug
import ConfigObject.MonsterAI.FSMExt as FSMExt
import ConfigObject.MonsterAI.AIActions as AIActions
import ConfigObject.MonsterAI.AIConditions as AIConditions



#加载配置
import MonsterAI

class AIMgr:
	def __init__( self ):
		self._monsterFSM = {}
	
	def getFSM( self, scriptID ):
		# 加载状态
		if scriptID not in self._monsterFSM:
			self.loadMonsterAI( scriptID )
		
		return self._monsterFSM[ scriptID ]
		
	def loadMonsterAI( self, scriptID ):
		"""
		加载AI配置
		"""		
		monsterObject = KST.g_objFactory.getMonsterObject( scriptID )
		AIConfig = MonsterAI.getConfig( scriptID )
		
		if AIConfig:
			FSMConfig = MonsterAI.FSMDatas.Datas[ AIConfig[ "FSM" ] ]
			FSMObj = FSMExt.AIFSM.AIFSM.getFSMClass( FSMConfig[ "script" ], scriptID )
			self._monsterFSM[ scriptID ] = FSMObj
			self._monsterFSM[ scriptID ].initData( FSMConfig, AIConfig )
		else:
			self._monsterFSM[ scriptID ] = None
	
	def reloadMonsterAI( self, scriptID ):
		"""
		重新加载AI配置
		"""
		self.reloadAIActions()
		self.reloadAIConditions()
		self.reloadAIFSMExt()
		
		monsterObject = KST.g_objFactory.getMonsterObject( scriptID )
		try:
			AIConfig = MonsterAI.reloadConfig( scriptID )
		except Exception as e:
			KBEDebug.ERROR_MSG("MonsterAI.reloadConfig( %s ) failed!  error:%s"%(scriptID,e))
			return False
		
		if AIConfig:
			FSMConfig = MonsterAI.FSMDatas.Datas[ AIConfig[ "FSM" ] ]
			FSMObj = FSMExt.AIFSM.AIFSM.getFSMClass( FSMConfig[ "script" ], scriptID )
			self._monsterFSM[ scriptID ] = FSMObj
			self._monsterFSM[ scriptID ].initData( FSMConfig, AIConfig )
			return True
		else:
			self._monsterFSM[ scriptID ] = None
		return False


	def reloadAIActions( self ):
		"""
		热更新AI行为脚本
		"""
		imp.reload(AIActions)

	def reloadAIConditions( self ):
		"""
		热更新AI条件脚本
		"""
		imp.reload(AIConditions)

	def reloadAIFSMExt( self ):
		"""
		热更新状态机拓展脚本
		"""
		imp.reload(FSMExt)

g_AIMgr = AIMgr()
