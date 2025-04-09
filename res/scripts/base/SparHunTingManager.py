# -*- coding: utf-8 -*-

import random
import KBEDebug
import Math
import KBEngine
import csdefine
from CoreObject import MgrPersistentObject
from ObjectScript.ObjectScriptFactory import g_objFactory
import csstatus
from ConfigObject.Crond.CrondDatas import CrondDatas
g_CrondDatas = CrondDatas.instance()
import KST

SPACE_SCRIPTID_LIST = ["fu_ben_JSSLC","fu_ben_JSSLC1"]
ONE_SPACE_MIN_PLAYERS_OPEN = 30

class ActiveItem( object ):
	"""
	"""
	def __init__( self, minLevel, maxLevel, maxCampEnter, spaceClassName ):
		self.minLevel = minLevel #最小等级
		self.maxLevel = maxLevel #最大等级
		self.spaceClassName = spaceClassName # 副本空间scriptID
		self.maxCampEnter = maxCampEnter #同阵营玩家进入最大数量
		self.signUpData = {}
		self.signUpData[csdefine.CAMP_TAOSIM] = []  #仙道容纳人列表
		self.signUpData[csdefine.CAMP_DEMON] = []	#魔道容纳人列表
		self.prepareSpaceKeys = []		#预创建空间Key值
		self.enters = []				#进入人数
		self.distributionSpaceInfo = {}

	def reset( self ):
		"""
		"""
		self.signUpData = {}
		self.signUpData[csdefine.CAMP_TAOSIM] = []  #仙道容纳人列表
		self.signUpData[csdefine.CAMP_DEMON] = []	#魔道容纳人列表
		self.enters = []
		self.distributionSpaceInfo = {}
		self.prepareSpaceKeys = []

	def checkLevel( self, level ):
		return level >= self.minLevel and level <= self.maxLevel

	def isAlreadySignUp( self, camp, dbid ):
		"""
		检查是否已报名
		"""
		return dbid in self.signUpData[camp]

	def signUp( self, dbid, level, camp ):
		"""
		报名
		"""
		if dbid not in self.signUpData[camp]:
			self.signUpData[camp].append(dbid)

		#空间的预创建处理
		spaceKey = self.getNewSpaceKey( camp )
		if spaceKey in self.prepareSpaceKeys:
			return

		countTaoSim = len(self.signUpData[csdefine.CAMP_TAOSIM])
		countDemon = len(self.signUpData[csdefine.CAMP_DEMON])
		maxSignUpCamp = 0
		if countTaoSim > countDemon:
			maxSignUpCamp = csdefine.CAMP_TAOSIM
		else:
			maxSignUpCamp = csdefine.CAMP_DEMON

		if len( self.prepareSpaceKeys ) == 0:
			self.prepareRequestSpace( spaceKey )

		if camp == maxSignUpCamp:
			if len(self.signUpData[camp]) - len(self.prepareSpaceKeys) * self.maxCampEnter > ONE_SPACE_MIN_PLAYERS_OPEN:	#如果单个阵营满了30，自动创建新的
				self.prepareRequestSpace( spaceKey )

	def onActiveStart( self ):
		"""
		活动开始
		"""
		self.distributionSpace()
		KBEngine.globalData["SpaceManager"].remoteCallDomain( self.spaceClassName,"activeStart",[] )

	def onActiveEnd( self ):
		"""
		活动结束
		"""
		KBEngine.globalData["SpaceManager"].remoteCallDomain( self.spaceClassName,"activeEnd",[] )
		self.prepareSpaceKeys = []

	def checkEnter( self, roleMB, params ):
		""" 
		检查进入
		"""
		camp = params.get("camp")
		level = params.get("level")
		dbID = params.get("playerDBID")
		if level >= self.minLevel and level <= self.maxLevel:
			if len(self.signUpData[camp]) < self.maxCampEnter:
				return True

			if dbID in self.signUpData[camp]:
				return True

		return False

	def teleportPlayer( self, position, direction, roleMB, params ):
		"""
		传送玩家
		"""
		camp = params.get("camp")
		dbID = params.get("playerDBID")
		if dbID not in self.signUpData[camp]:
			KBEDebug.ERROR_MSG("role %s not found" %(dbID))
			return
		
		if dbID not in self.enters:
			self.enters.append(dbID)

		params["spaceKey"] = self.selectEnterSpaceKey( camp,dbID )
		KBEngine.globalData["SpaceManager"].remoteCallDomain( self.spaceClassName,"teleportPlayerCallBack",(roleMB,position,direction,params) )

	def getNewSpaceKey( self, camp ):
		"""
		获得spaceKey
		"""
		return str(int(len(self.signUpData[camp])/self.maxCampEnter) + 1)

	def distributionSpace( self ):
		"""
		给玩家分配副本
		"""
		taoismList = self.signUpData[ csdefine.CAMP_TAOSIM ]
		demonList = self.signUpData[ csdefine.CAMP_DEMON ]

		#分配仙道玩家进入地图
		i = 0
		countTao = 0
		for taoismPlyaerDBID in taoismList:
			if len(self.prepareSpaceKeys) > i:
				self.distributionSpaceInfo[ taoismPlyaerDBID ] = self.prepareSpaceKeys[ i ]
				countTao += 1
				if countTao > self.maxCampEnter:
					i += 1
		
		#分配魔道玩家进入地图
		j = 0
		countDe = 0
		for demonPlyaerDBID in demonList:
			if len(self.prepareSpaceKeys) > i:
				self.distributionSpaceInfo[ demonPlyaerDBID ] = self.prepareSpaceKeys[ j ]
				countDe += 1
				if countDe > self.maxCampEnter:
					i += 1


	def prepareRequestSpace( self, spaceKey ):
		"""
		预创建副本
		"""
		spaceParams = {}
		spaceParams["spaceKey"] = spaceKey
		#spaceParams["minLevel"] = self.minLevel
		#spaceParams["maxLevel"] = self.maxLevel
		spaceParams["belongType"] = csdefine.SPACE_BELONG_NORMAL
		KBEngine.globalData["SpaceManager"].remoteCallDomain( self.spaceClassName, "requestNewSpace",(spaceParams,))
		self.prepareSpaceKeys.append(spaceKey)

	def selectEnterSpaceKey( self, camp, dbID ):
		"""
		选择要进入的地图Key
		"""
		if dbID in self.distributionSpaceInfo:
			return self.distributionSpaceInfo[dbID]
		else:
			if len( self.prepareSpaceKeys ) == 0:
				self.prepareRequestSpace(self.getNewSpaceKey(camp))

			spaceKey = random.choice( self.prepareSpaceKeys )
			self.distributionSpaceInfo[dbID] = spaceKey
			return spaceKey


class SparHunTingManager( MgrPersistentObject.MgrPersistentObject ):
	"""
	晶石狩猎场 管理类
	"""
	def __init__( self ) :
		MgrPersistentObject.MgrPersistentObject.__init__( self )
		self.activityItems = {}
		self.initActivityConfigData()
		self.register()
		self.activityState = csdefine.SHT_ACTIVITY_STATE_FREE
		self.timer1 = 0
		self.timer2 = 0
		self.onCompleteInit()

	def register( self ):
		"""
		注册
		"""
		taskEvents = { "SparHunTingMgr_Notice":"onActiveNotice",
						"SparHunTingMgr_SignUp":"onActiveSignUp",
						"SparHunTingMgr_SignUpEnd":"onActiveSignUpEnd",
						"SparHunTingMgr_Start":"onActiveStart",
						"SparHunTingMgr_End":"onActiveEnd"
		 }
		for taskName, callbackName in taskEvents.items():
			for scriptID, cmd in g_CrondDatas.getCrondTaskCmds(taskName):
		 		KBEngine.globalData["CrondManager"].addScheme( scriptID, cmd, self, callbackName, -1,() )

	def onActiveNotice( self, cmd, *callbackArgs ):
		"""
		活动公告
		"""
		self.sendWoldMsg( csstatus.SPARHUNTING_SIGN_UP,"" )

	def onActiveSignUp( self, cmd, *callbackArgs ):
		"""
		活动报名
		"""
		for item in self.activityItems.values():
			item.reset()

		self.setActiveState( csdefine.SHT_ACTIVITY_STATE_SIGNUP )

	def onActiveSignUpEnd( self, cmd, *callbackArgs ):
		"""
		结束活动报名
		"""
		#self.setActiveState( csdefine.SHT_ACTIVITY_STATE_FREE )#结束报名时间和活动开启时间目前策划是一致的，但可能存在计划任务先后执行的问题，这里就注释掉
		pass

	def onActiveStart( self, cmd, *callbackArgs ):
		"""
		活动开始
		"""
		self.sendWoldMsg(csstatus.SPARHUNTING_SIGN_UP_END,"")
		self.setActiveState( csdefine.SHT_ACTIVITY_STATE_START )
		for item in self.activityItems.values():
			item.onActiveStart()

	def onActiveEnd( self, cmd, *callbackArgs ):
		"""
		活动结束
		"""
		self.setActiveState( csdefine.SHT_ACTIVITY_STATE_FREE )
		for item in self.activityItems.values():
			item.onActiveEnd()

	def setActiveState( self, state ):
		"""
		设置活动状态
		"""
		self.activityState = state

	def getActiveState( self ):
		"""
		获得活动状态
		"""
		return self.activityState

	def sendWoldMsg( self, messageType, messageArg ):
		"""
		发送世界公告消息
		"""
		KST.g_baseAppEntity.globalWold( messageType, messageArg )

	def initActivityConfigData( self ):
		"""
		初始化数据
		"""
		for scriptID in SPACE_SCRIPTID_LIST:
			g_objFactory.getSpaceObject( scriptID ).mgrNotify()

	def registerToMgr( self, spaceClassName, minLevel, maxLevel, maxCampEnter ):
		"""
		"""
		self.activityItems[spaceClassName] = ActiveItem( minLevel, maxLevel, maxCampEnter, spaceClassName )

	def activeSignUp( self, playerMB, dbID, level, camp ):
		"""
		活动报名
		"""
		if self.getActiveState() != csdefine.SHT_ACTIVITY_STATE_SIGNUP:
			playerMB.client.statusMessage( csstatus.SPARHUNTING_ACTIVITY_SIGN_UP_TIME_ERROR, "" )
			return
		activeItem = None
		for item in self.activityItems.values():
			if item.checkLevel( level ):
				activeItem = item
				break
		if not activeItem:
			return
		if activeItem.isAlreadySignUp( camp, dbID ):
			playerMB.client.statusMessage( csstatus.SPARHUNTING_ACTIVITY_SIGN_UP_ALREADY,"" )
			return
		activeItem.signUp( dbID, level, camp )
		playerMB.client.statusMessage( csstatus.SPARHUNTING_ACTIVITY_SIGN_UP_SUCCESS,"" )

	def requestEnter( self, playerMB, position, direction,level ):
		"""
		请求进入
		"""
		if self.getActiveState() == csdefine.SHT_ACTIVITY_STATE_FREE: # 不在活动时间
			playerMB.client.statusMessage( csstatus.SPARHUNTING_ACTIVITY_NOT_START, "" )
			return
		elif self.getActiveState() == csdefine.SHT_ACTIVITY_STATE_SIGNUP: # 报名
			playerMB.client.statusMessage( csstatus.SPARHUNTING_ACTIVITY_SIGN_UP_TIME, "" )
			return

		activeItem = None
		for item in self.activityItems.values():
			if item.checkLevel( level ):
				activeItem = item
				break
		if not activeItem:
			return
		playerMB.gotoSpace(activeItem.spaceClassName,position,direction)

	def teleportPlayer( self, position, direction, roleMB, params ):
		"""
		传送玩家
		"""
		activeItem = None
		for item in self.activityItems.values():
			if item.checkEnter( roleMB,params ):
				activeItem = item
				break
		if not activeItem:
			roleMB.client.statusMessage(csstatus.SPARHUNTING_ACTIVITY_NOT_SIGN_UP,"")
			return

		activeItem.teleportPlayer( position, direction, roleMB, params )
