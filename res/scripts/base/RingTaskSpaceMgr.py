# -*- coding: utf-8 -*-

import KST
import KBEngine
from CoreObject import MgrPersistentObject
from KBEDebug import *
import LoadModule
import Functions
import random
import Math
import KBEMath
import Const

RING_TASK_MAIN_SCENE_ONE	= "cycle_L_HRWMJ01"
RING_TASK_MAIN_SCENE_TWO	= "cycle_L_HRWMJ02"
RING_TASK_MAIN_SCENE_THREE	= "cycle_L_HRWMJ03"
RING_TASK_RANGE_ONE 		= range( 0, 6 )
RING_TASK_RANGE_TWO 		= range( 6, 12 )
RING_TASK_RANGE_THREE 		= range( 12, 18 )

class RingTaskItem( object ):
	"""
	环任务秘境数据管理
	"""
	def __init__(self, spaceKey, progress, isInMainScene ):
		self.spaceKey = spaceKey
		self.progress = progress
		self.isInMainScene = isInMainScene

	def setCurrentProgress( self, progress ):
		"""
		设置当前进度
		"""
		self.progress = progress

	def setIsInMainScene( self, isInMainScene ):
		"""
		设置是否在主场景中
		"""
		self.isInMainScene = isInMainScene


class RingTaskSpaceMgr( MgrPersistentObject.MgrPersistentObject ):
	"""
	环任务秘境管理器
	"""
	def __init__( self ):
		MgrPersistentObject.MgrPersistentObject.__init__( self )
		self.ringTaskInfo = {}		# 记录所有的对应信息(包括当前进度等信息)
		self.ringTaskData = {}
		self.initData()

	def initData( self ):
		"""
		解析数据
		"""
		dataCfg = LoadModule.openJsonCfg("Quest/QuestConfigs/LoopQuestConfig.json")
		self.ringTaskData = dataCfg
		self.onCompleteInit()

	def getRingTaskItem( self, spaceKey ):
		"""
		获取对应信息
		"""
		if spaceKey in self.ringTaskInfo:
			return self.ringTaskInfo[spaceKey]
		else:
			return None

	def setRingTaskItem( self, spaceKey ):
		"""
		设置数据
		"""
		ringTaskItem = self.getRingTaskItem( spaceKey )
		if ringTaskItem == None:
			newRingTaskInfo = RingTaskItem( spaceKey, 0, True )
			self.ringTaskInfo[spaceKey] = newRingTaskInfo

	def gotoRingTaskSpace( self, roleMB, questID, pickArg, isSignOut ):
		"""
		传送到对应位置
		"""
		ringTaskItem = self.getRingTaskItem( pickArg["spaceKey"] )
		if ringTaskItem == None:
			newRingTaskInfo = RingTaskItem( pickArg["spaceKey"], 0, True )
			self.ringTaskInfo[pickArg["spaceKey"]] = newRingTaskInfo
			roleMB.cell.gotoSpaceEnterPos( RING_TASK_MAIN_SCENE_ONE, pickArg )
		else:
			progress = ringTaskItem.progress
			if not ringTaskItem.isInMainScene:
				roleMB.cell.gotoSpaceEnterPos( self.ringTaskData[questID]["subSpace"], pickArg )
			else:
				if not isSignOut:
					exitPos = Functions.vector3TypeConvert( self.ringTaskData[str(progress)]["exitPos"] )
					exitDir = Functions.vector3TypeConvert( self.ringTaskData[str(progress)]["exitDir"] )
					self.deliveryAppointPosition( exitPos, exitDir, progress, roleMB, pickArg )
				else:
					leavePos = Functions.vector3TypeConvert( self.ringTaskData[str(progress)]["leavePos"] )
					leaveDir = Functions.vector3TypeConvert( self.ringTaskData[str(progress)]["leaveDir"] )
					self.deliveryAppointPosition( leavePos, leaveDir, progress, roleMB, pickArg )
	
	def deliveryAppointPosition( self, position, direction, curProgress, roleMB, pickArg ):
		"""
		传送到指定位置
		"""
		if curProgress in RING_TASK_RANGE_ONE:
			roleMB.cell.gotoSpaceUseArg( RING_TASK_MAIN_SCENE_ONE, KBEMath.Unreal2KBEnginePosition( position ), KBEMath.Unreal2KBEngineDirection( direction ), pickArg )
		elif curProgress in RING_TASK_RANGE_TWO:
			roleMB.cell.gotoSpaceUseArg( RING_TASK_MAIN_SCENE_TWO, KBEMath.Unreal2KBEnginePosition( position ), KBEMath.Unreal2KBEngineDirection( direction ), pickArg )
		elif curProgress in RING_TASK_RANGE_THREE:
			roleMB.cell.gotoSpaceUseArg( RING_TASK_MAIN_SCENE_THREE, KBEMath.Unreal2KBEnginePosition( position ), KBEMath.Unreal2KBEngineDirection( direction ), pickArg )

	def onChildSceneSuccess( self, spaceKey ):
		"""
		子场景副本成功
		"""
		ringTaskItem = self.getRingTaskItem( spaceKey )
		if ringTaskItem != None:
			ringTaskItem.setIsInMainScene( True )
		
	def onChildSceneFailure( self, spaceKey ):
		"""
		子场景副本失败
		"""
		ringTaskItem = self.getRingTaskItem( spaceKey )
		if ringTaskItem != None:
			ringTaskItem.setIsInMainScene( True )

	def setIsInMainScene( self, spaceKey, isInMainScene ):
		"""
		设置是否在主场景
		"""
		ringTaskItem = self.getRingTaskItem( spaceKey )
		if ringTaskItem != None:
			ringTaskItem.setIsInMainScene( isInMainScene )

	def setCurrentProgress( self, spaceKey, progress ):
		"""
		设置当前进度
		"""
		ringTaskItem = self.getRingTaskItem( spaceKey )
		if ringTaskItem != None:
			ringTaskItem.setCurrentProgress( progress )

	def setPreloadSpace( self, roleMB, spaceKey, questID, isPreload ):
		"""
		通知预加载的地图
		"""
		ringTaskItem = self.getRingTaskItem( spaceKey )
		DEBUG_MSG("+++++++++++++++++++++++++++",ringTaskItem)
		DEBUG_MSG("+++++++++++++questID++++++++++++++",questID)
		DEBUG_MSG("+++++++++++++isPreload++++++++++++++",isPreload)
		if ringTaskItem == None:
			if questID in self.ringTaskData:
				roleMB.cell.onNotifyPreloadSpace( self.ringTaskData[questID]["subSpace"], isPreload)
		else:
			DEBUG_MSG("**************isInMainScene************",ringTaskItem.isInMainScene)
			if not ringTaskItem.isInMainScene:
				if ringTaskItem.progress in RING_TASK_RANGE_ONE:
					roleMB.cell.onNotifyPreloadSpace( RING_TASK_MAIN_SCENE_ONE, isPreload )
				elif ringTaskItem.progress in RING_TASK_RANGE_TWO:
					roleMB.cell.onNotifyPreloadSpace( RING_TASK_MAIN_SCENE_TWO, isPreload )
				elif ringTaskItem.progress in RING_TASK_RANGE_THREE:
					roleMB.cell.onNotifyPreloadSpace( RING_TASK_MAIN_SCENE_THREE, isPreload )
			else:
				if questID in self.ringTaskData:
					DEBUG_MSG("**************subSpace************",self.ringTaskData[questID]["subSpace"])
					roleMB.cell.onNotifyPreloadSpace( self.ringTaskData[questID]["subSpace"], isPreload )

	def setLoadingSpace( self, roleMB, spaceKey ):
		"""
		正常切换地图
		"""
		ringTaskItem = self.getRingTaskItem( spaceKey )
		if ringTaskItem.progress in RING_TASK_RANGE_ONE:
			roleMB.cell.onNotifyLoadingSpace( RING_TASK_MAIN_SCENE_ONE )
		elif ringTaskItem.progress in RING_TASK_RANGE_TWO:
			roleMB.cell.onNotifyLoadingSpace( RING_TASK_MAIN_SCENE_TWO )
		elif ringTaskItem.progress in RING_TASK_RANGE_THREE:
			roleMB.cell.onNotifyLoadingSpace( RING_TASK_MAIN_SCENE_THREE )

	def notifyToCloseRingTaskParentSpace( self, loopQuestNum, playerDBID ):
		"""
		通知关闭玩家环任务主副本场景
		"""
		spaceScriptID = ""
		if loopQuestNum in RING_TASK_RANGE_TWO:
			spaceScriptID = RING_TASK_MAIN_SCENE_ONE
		if loopQuestNum in RING_TASK_RANGE_THREE:
			spaceScriptID = RING_TASK_MAIN_SCENE_TWO

		if loopQuestNum in RING_TASK_RANGE_THREE:
			spaceScriptID = RING_TASK_MAIN_SCENE_THREE

		KBEngine.globalData["SpaceManager"].remoteCallDomain(spaceScriptID,"notifyToCloseRingTaskParentSpace",(str(playerDBID),))

	def notifyCloseAllRingTaskSpace( self, playerDBID ):
		"""
		"""
		for spaceScriptID in [RING_TASK_MAIN_SCENE_ONE,RING_TASK_MAIN_SCENE_TWO,RING_TASK_MAIN_SCENE_THREE]:
			KBEngine.globalData["SpaceManager"].remoteCallDomain(spaceScriptID,"notifyToCloseRingTaskParentSpace",(str(playerDBID),))
		
