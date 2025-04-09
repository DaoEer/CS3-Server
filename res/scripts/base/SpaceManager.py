# -*- coding: utf-8 -*-
import KBEDebug
import KBEngine
import KBEMath
import Math
import KST
import csdefine
from ObjectScript.Space import g_spaceConsumeObjectDict
from CoreObject.MgrPersistentObject import MgrPersistentObject
from KBEDebug import *
import Settings
from ConfigObject.Crond.CrondDatas import CrondDatas
g_CrondDatas = CrondDatas.instance()

class SpaceManager( MgrPersistentObject ):
	"""
	空间管理器
	"""
	def __init__( self ):
		MgrPersistentObject.__init__( self )
		self._lastSpaceNumber = 0 								# 用于分配space的ID
		self._spaceNumbers = []									# 用于记录所有已经分配的 space的number 的集合
		self._canDistributionSpaceNumbers = []					#可分配spaceNumber
		self.spaceDomains = KST.g_objFactory.getAllSpaceDomian()
		self.spaceGlobalRecord = {}								# 副本记录，用于cell进副本时预先查找某spaceKey的副本是否存在
		
		self.initFlag = False
		self.initSpaces = set()
		self.cid2consume = {}
		self.initDelayTimerID = 0
		self.waitInitDomain = []
		self.pid2cellInfo = {}		#调试用
		self.noBalanceSpace = {}
		self.registerCrond()
		self.initDomains()
		

	def registerCrond( self ):
		"""
		将活动key 注册到Crond中
		"""
		taskEvents = {
			"SpaceManager_onControlSpace": "onControlSpace",
		}
		for taskName, callbackName in taskEvents.items():
			for scriptID, cmd in g_CrondDatas.getCrondTaskCmds(taskName):
				KBEngine.globalData["CrondManager"].addScheme( scriptID, cmd, self, callbackName, -1, (scriptID,) )
		
	def initDomains( self ):
		"""
		"""
		if self.initFlag:
			return
		
		#起来多少个cell之后才开始进行初始化
		if len(KST.temp_cellApps) < Settings.space_wait_init_cell_amount:
			return
		
		self.initFlag = True
		self.waitInitDomain = list(self.spaceDomains.keys())
		#为解决（KBEN-202 KBE引擎BUG -- space创建在指定cellapp上未达预期）这里强制延时
		self.initDelayTimerID = self.addTimerCallBack(Settings.space_wait_init_time, "onInitDomains", ())
		
	def onInitDomains( self ):
		"""
		"""
		if self.initDelayTimerID:
			self.popTimer(self.initDelayTimerID)
			self.initDelayTimerID = 0
			
		flag = False
		if len(self.waitInitDomain) >= len(self.spaceDomains):
			#自己配置的space消耗的话，一次性初始化好了（加快开服速度）
			if len(g_spaceConsumeObjectDict) > 0:
				for key in list(g_spaceConsumeObjectDict.keys()):
					if key in self.spaceDomains:
						self.spaceDomains[key].initDomain()
						self.waitInitDomain.remove(key)
						flag = True	#放这里是防止两个配置地图不一致
			
		if not flag and len(self.waitInitDomain) > 0:
			initPer = Settings.space_init_domain_per if Settings.space_init_domain_per > 0 else 5
			for i in range(min(initPer, len(self.waitInitDomain))):
				key = self.waitInitDomain.pop(0)
				self.spaceDomains[key].initDomain()
		
		if len(self.waitInitDomain) > 0:
			self.initDelayTimerID = self.addTimerCallBack(Settings.space_wait_init_tick, "onInitDomains", ())
		else:
			self.serverStartProcessCheck()
	
	def getNewSpaceNumber( self, nums = 0 ):
		"""
		获取一个唯一的space编号
		nums : 获取次数
		@return: INT32
		"""
		if nums == 5: #取5次还是取不到，说明逻辑错误了
			KBEDebug.ERROR_MSG( "can't new space number!!!" )
			return
			
		result = 0
		if self._lastSpaceNumber < csdefine.INT_16_MAX: #如果这个值上限了，那么就从回收池里面取
			self._lastSpaceNumber+=1
			result = self._lastSpaceNumber
		elif len( self._canDistributionSpaceNumbers ):
			result = self._canDistributionSpaceNumbers.pop( 0 )
		else:
			KBEDebug.ERROR_MSG( "can't new space number!!!" )
			return
			
		if result in self._spaceNumbers:
			return self.getNewSpaceNumber( nums + 1 )
			
		self._spaceNumbers.append( result )
		return result
	
	def remoteCallDomain( self, spaceClassName, methodName, args ):
		"""
		<define method>
		转发调用Domain的一个方式
		"""
		_domain = self.spaceDomains[ spaceClassName ]
		try:
			method = getattr( _domain, methodName )
		except AttributeError as errstr:
			ERROR_MSG( "Domain class(%s) has not method %s." % ( spaceClassName, methodName ) )
			return
		method( *args )
	
	def onSpaceCopyItemCreate( self, spaceClassName, belongType, spaceKey ):
		"""
		<define method>
		一个副本spaceItem创建
		"""
		if spaceClassName not in self.spaceGlobalRecord:
			self.spaceGlobalRecord[ spaceClassName ] = {}
		if belongType not in self.spaceGlobalRecord[ spaceClassName ]:
			self.spaceGlobalRecord[ spaceClassName ][ belongType ] = []
		self.spaceGlobalRecord[ spaceClassName ][ belongType ].append( spaceKey )
	
	def onSpaceCopyItemDelete( self, spaceClassName, belongType, spaceKey ):
		"""
		<define method>
		一个副本spaceItem删除
		"""
		self.spaceGlobalRecord[ spaceClassName ][ belongType ].remove( spaceKey )
		if len( self.spaceGlobalRecord[ spaceClassName ][ belongType ] ) == 0:
			self.spaceGlobalRecord[ spaceClassName ].pop( belongType )
		if len( self.spaceGlobalRecord[ spaceClassName ] ) == 0:
			self.spaceGlobalRecord.pop( spaceClassName )

#-----------------remote call------------------------------------------
	def roleLogin( self, spaceClassName, roleMB, pickArgs ):
		"""
		<define method>
		"""
		if spaceClassName in self.spaceDomains:
			self.spaceDomains[ spaceClassName ].roleLogin( roleMB, pickArgs )
		else:
			roleMB.loginToConfigSpace( "L_FMC", KBEMath.Unreal2KBEnginePosition( Math.Vector3(23614.0, 21573.0, 12230.0)), KBEMath.Unreal2KBEngineDirection( Math.Vector3(0, 0, -86.5)) )
			KBEDebug.ERROR_MSG( "space scriptID( %s ) is not exit! login failure!!!! "%spaceClassName )
	
	def gotoSpace( self, spaceClassName, roleMB, position, direction, pickArgs ):
		"""
		<define method>
		"""
		self.spaceDomains[ spaceClassName ].gotoSpace( roleMB, position, direction, pickArgs )
		KST.calculateTeleportTimes()
	
	def onSpaceCreateCell( self, spaceClassName, spaceNumber, spaceMB ):
		"""
		<define method>
		"""
		self.spaceDomains[ spaceClassName ].onSpaceCreateCell( spaceNumber, spaceMB )
	
	def onSpaceLoseCell( self, spaceClassName, spaceNumber ):
		"""
		<define method>
		"""
		self._canDistributionSpaceNumbers.append( spaceNumber ) #把已经销毁的地图number加入可分配的列表里面
		
		if spaceNumber in self._spaceNumbers:
			self._spaceNumbers.remove( spaceNumber )
			
		self.spaceDomains[ spaceClassName ].onSpaceLoseCell( spaceNumber )
	
#------------------------------------------------------------------------------
	def onLoadOver( self, spaceScriptID ):
		"""
		define method
		Space加载完
		"""	
		if spaceScriptID not in Settings.space_init_completed_space_scriptID:
			return
		
		if spaceScriptID in self.initSpaces:
			return
		
		self.initSpaces.add( spaceScriptID )
		self.serverStartProcessCheck()
	
	def serverStartProcessCheck( self ):
		"""
		服务器启动检查
		"""
		if len( list( self.initSpaces ^ set( Settings.space_init_completed_space_scriptID ) ) ) == 0:
			self.onCompleteInit()
		
	def incCellAppSpace( self, spaceScriptID, cid ):
		"""
		不参与负载均衡的cellapp中有新创的space
		"""
		if cid <= 0:	#未指定cellapp，那就不用管了
			return
			
		spaceList = KST.g_objFactory.getAllNoBalanceSpace()
		cellappList = KST.g_objFactory.getAllNoBalanceCellAPPList()
		if cid in cellappList:
			if spaceScriptID not in spaceList:
				KBEDebug.ERROR_MSG("space[%s] not balance space, cid:%s" %(spaceScriptID, cid))
				return
			
			self.noBalanceSpace.setdefault(spaceScriptID, {})
			self.noBalanceSpace[spaceScriptID].setdefault(cid, 0 )
			self.noBalanceSpace[spaceScriptID][cid] += 1
			return
		
		consume = KST.g_objFactory.getSpaceConsume(spaceScriptID)
		self.cid2consume.setdefault(cid, 0)
		self.cid2consume[cid] += consume
		
		pid = (KST.temp_cellApps.get(cid, {})).get("pid", 0)
		if pid == 0: return
		
		self.pid2cellInfo.setdefault(pid, [cid, 0, {}])
		self.pid2cellInfo[pid][1] = self.cid2consume[cid]
		self.pid2cellInfo[pid][2].setdefault(spaceScriptID, 0)
		self.pid2cellInfo[pid][2][spaceScriptID] += consume
		
	def decCellAppSpace( self, spaceScriptID, cid ):
		"""
		不参与负载均衡的cellapp中有space销毁
		"""
		if cid <= 0:	#未指定cellapp，那就不用管了
			return
			
		cellappList = KST.g_objFactory.getAllNoBalanceCellAPPList()
		if cid in cellappList:
			if spaceScriptID not in self.noBalanceSpace:
				KBEDebug.ERROR_MSG("not found space[%s], noBalanceSpace %s" %(spaceScriptID, self.noBalanceSpace))
				return
			
			amount = self.noBalanceSpace[spaceScriptID].get(cid, 0)
			if amount <= 0:
				self.noBalanceSpace[spaceScriptID].pop(cid, None)
				return
			
			self.noBalanceSpace[spaceScriptID][cid] -= 1
			if self.noBalanceSpace[spaceScriptID][cid] <= 0:
				self.noBalanceSpace[spaceScriptID].pop(cid)
			return
		
		if cid not in self.cid2consume:
			KBEDebug.ERROR_MSG("not found cid[%d]" %(cid))
			return
		
		consume = KST.g_objFactory.getSpaceConsume(spaceScriptID)
		self.cid2consume[cid] -= consume
		if self.cid2consume[cid] <= 0:
			self.cid2consume[cid] = 0
			
		pid = (KST.temp_cellApps.get(cid, {})).get("pid", 0)
		if pid not in self.pid2cellInfo: 
			return
		
		if spaceScriptID not in self.pid2cellInfo[pid][2]: 
			return
		
		self.pid2cellInfo[pid][2][spaceScriptID] -= consume
		if self.pid2cellInfo[pid][2][spaceScriptID] <= 0:
			self.pid2cellInfo[pid][2].pop(spaceScriptID, None)
		self.pid2cellInfo[pid][1] = self.cid2consume[cid]
		
	def getFreeCellAppCid( self, spaceScriptID ):
		"""
		寻找一个负载较轻的cellapp
		"""
		#指定的space创建在不参与负载均衡的指定cellapp中
		spaceList = KST.g_objFactory.getAllNoBalanceSpace()
		cellappList = KST.g_objFactory.getAllNoBalanceCellAPPList()
		if spaceScriptID in spaceList:
			if len(cellappList) <= 0:
				return -1
			
			if len(self.noBalanceSpace.get(spaceScriptID, {})) < len(cellappList):
				temp = list(set(cellappList) - set(self.noBalanceSpace.get(spaceScriptID, {}).keys()))
				return temp[0]
				
			cid = 0
			amount = 9999999999
			for k,v in self.noBalanceSpace[spaceScriptID].items():
				if amount > v:
					cid = k
					amount = v
			return cid
		
		#手动指定space创建在参与负载均衡的cellapp中
		if spaceScriptID not in g_spaceConsumeObjectDict:
			return 0
		
		cids = list(set(KST.temp_cellApps.keys()) - set(cellappList) - set(self.cid2consume.keys()))
		if len(cids) > 0:
			return cids[0]
		
		cid = 0
		consume = 999999999999
		for key in self.cid2consume.keys():
			if consume > self.cid2consume[key]:
				cid = key
				consume = self.cid2consume[key]
		return cid
		
	def OutputProcessInfos(self):
		"""
		"""
		from ObjectScript.SpaceDomain.SpaceDomainMultiLine import SpaceDomainMultiLine
		for pid, lst in self.pid2cellInfo.items():
			KBEDebug.OUTPUT_PROCESS_INFOS("pid:{}, cid:{}, consume:{}".format(pid, lst[0], lst[1]))
			for k, v in lst[2].items():
				KBEDebug.OUTPUT_PROCESS_INFOS("{}:{}".format(k, v))
		for _ , v in self.spaceDomains.items():
			if isinstance(v, SpaceDomainMultiLine):
				v.OutputProcessInfos()
		KBEDebug.OUTPUT_PROCESS_INFOS("---- SpaceManager ---\n")
		
	def onControlSpace(self, cmd, scriptID):
		"""
		开启/关闭space(CST-11490)
		"""
		crond = g_CrondDatas.getCrondByCrondID(scriptID)
		if crond is None: return	
		spaceScriptIDList = crond["param1"].split("|")
		openStatus = int(crond["param2"])
		for spaceScriptID in spaceScriptIDList:
			key = csdefine.CONTROL_SPACE_KEY + spaceScriptID
			KBEngine.globalData[key] = openStatus
			
			#if spaceScriptID in self.spaceDomains and not openStatus:
			#	self.spaceDomains[ spaceScriptID ].onControlCloseSpace()
		