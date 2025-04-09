# -*- coding: utf-8 -*-

import time
import KBEMath
import KBEDebug
import csdefine
import Const
import csconst
import Functions
import csstatus
from ObjectScript.Space.SpaceCopy import SpaceCopy

class SpaceCopyLingMaiZhanChang( SpaceCopy ):
	"""
	灵脉战场
	"""
	def __init__( self ):
		SpaceCopy.__init__( self )
		self._xianEnterPos = (0,0,0)
		self._xianEnterDir = (0,0,0)
		self._xianRevivePos_1 = (0,0,0)
		self._xianReviveDir_1 = (0,0,0)
		self._xianRevivePos_2 = (0,0,0)
		self._xianReviveDir_2 = (0,0,0)
		
		self._moEnterPos = (0,0,0)
		self._moEnterDir = (0,0,0)
		self._moRevivePos_1 = (0,0,0)
		self._moReviveDir_1 = (0,0,0)
		self._moRevivePos_2 = (0,0,0)
		self._moReviveDir_2 = (0,0,0)
		self._pagodaScript = {}
		self._pagodaScript[csdefine.CAMP_TAOSIM] = []	# 极阳灵塔 （[ scriptID,... ]）
		self._pagodaScript[csdefine.CAMP_DEMON] = []	# 极阴灵塔 （[ scriptID,... ]）
		self._huluDistance = 0.0						# 葫芦检测距离
		self._distance = 0.0							# 灵塔检测距离
		self._crystalBuffID = 0							# 拖葫芦的buffID
		self._shadeDectPos = (0,0,0)					# 极阴灵塔的监测中心位置
		self._sunDectPos = (0,0,0)						# 极阳灵塔的监测中心位置

		self.loserRewardMailID = 0 #失败方奖励邮件ID
		self.winnerRewardMailID = 0 #胜利方奖励邮件ID
		self.killExpRate = 0 #玩家击杀经验奖励系数
		self.killExploits = 0#玩家击杀军功奖励
		self.finalExpDict = {} #结算经验奖励 按等级和胜负区分
		self.finalLostExploits = 0 #结算军功奖励 失败方
		self.finalWinExploits = 0 #结算军功奖励 胜利方
		self.outRewardMailDict = {} #把数值结算奖励通过邮件发给出局的玩家
	
	def initData( self, configData ):
		"""
		"""
		SpaceCopy.initData( self, configData )
		
		posStr = configData["SpaceData"].get( "xianEnterPos", "" )
		pos = Functions.vector3TypeConvert( posStr )
		if pos:
			self._xianEnterPos = KBEMath.Unreal2KBEnginePosition( pos )
		dirStr = configData["SpaceData"].get( "xianEnterDir", "" )
		dir = Functions.vector3TypeConvert( dirStr )
		if dir:
			self._xianEnterDir = KBEMath.Unreal2KBEngineDirection( dir )
		
		posStr = configData["SpaceData"].get( "xianRevivePos_1", "" )
		pos = Functions.vector3TypeConvert( posStr )
		if pos:
			self._xianRevivePos_1 = KBEMath.Unreal2KBEnginePosition( pos )
		dirStr = configData["SpaceData"].get( "xianReviveDir_1", "" )
		dir = Functions.vector3TypeConvert( dirStr )
		if dir:
			self._xianReviveDir_1 = KBEMath.Unreal2KBEngineDirection( dir )
			
		posStr = configData["SpaceData"].get( "xianRevivePos_2", "" )
		pos = Functions.vector3TypeConvert( posStr )
		if pos:
			self._xianRevivePos_2 = KBEMath.Unreal2KBEnginePosition( pos )
		dirStr = configData["SpaceData"].get( "xianReviveDir_2", "" )
		dir = Functions.vector3TypeConvert( dirStr )
		if dir:
			self._xianReviveDir_2 = KBEMath.Unreal2KBEngineDirection( dir )
			
		posStr = configData["SpaceData"].get( "moEnterPos", "" )
		pos = Functions.vector3TypeConvert( posStr )
		if pos:
			self._moEnterPos = KBEMath.Unreal2KBEnginePosition( pos )
		dirStr = configData["SpaceData"].get( "moEnterDir", "" )
		dir = Functions.vector3TypeConvert( dirStr )
		if dir:
			self._moEnterDir = KBEMath.Unreal2KBEngineDirection( dir )
			
		posStr = configData["SpaceData"].get( "moRevivePos_1", "" )
		pos = Functions.vector3TypeConvert( posStr )
		if pos:
			self._moRevivePos_1 = KBEMath.Unreal2KBEnginePosition( pos )
		dirStr = configData["SpaceData"].get( "moReviveDir_1", "" )
		dir = Functions.vector3TypeConvert( dirStr )
		if dir:
			self._moReviveDir_1 = KBEMath.Unreal2KBEngineDirection( dir )
			
		posStr = configData["SpaceData"].get( "moRevivePos_2", "" )
		pos = Functions.vector3TypeConvert( posStr )
		if pos:
			self._moRevivePos_2 = KBEMath.Unreal2KBEnginePosition( pos )
		dirStr = configData["SpaceData"].get( "moReviveDir_2", "" )
		dir = Functions.vector3TypeConvert( dirStr )
		if dir:
			self._moReviveDir_2 = KBEMath.Unreal2KBEngineDirection( dir )
		
		scriptIDs = configData["SpaceData"].get( "sunPagoda", "" )
		if scriptIDs:
			for scriptID in scriptIDs.split(","):
				self._pagodaScript[csdefine.CAMP_TAOSIM].append( scriptID )
		scriptIDs = configData["SpaceData"].get( "shadePagoda", "" )
		if scriptIDs:
			for scriptID in scriptIDs.split(","):
				self._pagodaScript[csdefine.CAMP_DEMON].append( scriptID )
		
		distance = configData["SpaceData"].get("huluDistance", 0 )
		if distance:
			self._huluDistance = float( distance )
		
		distance = configData["SpaceData"].get("pagodaDistance", 0 )
		if distance:
			self._distance = float( distance )
		buffID = configData["SpaceData"].get("crystalBuffID", 0 )
		if distance:
			self._crystalBuffID = int( buffID )
		
		posStr = configData["SpaceData"].get( "shadeDectPos", "" )
		pos = Functions.vector3TypeConvert( posStr )
		if pos:
			self._shadeDectPos = KBEMath.Unreal2KBEnginePosition( pos )
		posStr = configData["SpaceData"].get( "sunDectPos", "" )
		pos = Functions.vector3TypeConvert( posStr )
		if pos:
			self._sunDectPos = KBEMath.Unreal2KBEnginePosition( pos )

		self.tempCampBuffs = configData['SpaceData'].get('tempCampBuffs', {})

		self.loserRewardMailID = configData["SpaceData"].get("loserRewardMailID", 0)
		self.winnerRewardMailID = configData["SpaceData"].get("winnerRewardMailID", 0)
		self.killExpRate = configData["SpaceData"].get("killExpRate", 0)
		self.killExploits = configData["SpaceData"].get("killExploits", 0)
		finalExpDict = configData["SpaceData"].get("finalExpDict", {})
		for level, expList in finalExpDict.items():
			self.finalExpDict[int(level)] = expList
		self.finalLostExploits = configData["SpaceData"].get("finalLostExploits", 0)
		self.finalWinExploits = configData["SpaceData"].get("finalWinExploits", 0)
		outRewardMailDict = configData["SpaceData"].get("outRewardMailDict", {})
		for level, mailIDList in outRewardMailDict.items():
			self.outRewardMailDict[int(level)] = mailIDList

	def getReviveInfo( self, player ):
		"""获取玩家复活信息"""
		if player.getFinalCamp() == csdefine.CAMP_TAOSIM:
			pos1 = player.position.distTo( self._xianRevivePos_1 )
			pos2 = player.position.distTo( self._xianRevivePos_2 )
			if pos1 <= pos2:
				return self._xianRevivePos_1, self._xianReviveDir_1
			else:
				return self._xianRevivePos_2, self._xianReviveDir_2
		else:
			pos1 = player.position.distTo( self._moRevivePos_1 )
			pos2 = player.position.distTo( self._moRevivePos_2 )
			if pos1 <= pos2:
				return self._moRevivePos_1, self._moReviveDir_1
			else:
				return self._moRevivePos_2, self._moReviveDir_2
	
	def setReviveType( self ):
		"""
		设置复活类型  CST-2208
		"""
		pass
		
	def getPackDomainData( self, playerEntity, args ):
		"""
		"""
		param = SpaceCopy.getPackDomainData( self, playerEntity, {} )
		param.update(args)
		param["playerDBID"] = playerEntity.playerDBID
		return param
	
	def startSpaceLife( self, selfEntity ):
		"""
		开始计时
		"""
		spaceLifeSecond = self.spaceLife + selfEntity.dynamicTime
		selfEntity.lifeTime = self.spaceLife		# 副本时长
		selfEntity.lifeStartTime = time.time()		# 副本计时开始时间
		selfEntity.lifeTimer = selfEntity.addTimerCallBack( spaceLifeSecond, "onLifeTimeArrive", () )
#		selfEntity.lifeNotifyTimer = selfEntity.addTimerCallBackForScript( spaceLifeSecond - Const.SPACE_LIFE_NOTIFY_TIME, "showTimeCountDown", ( csstatus.SPACE_CLOSE_NOTIFY, Const.SPACE_LIFE_NOTIFY_TIME ) )
		for e in selfEntity._spaceRoles:
			e.client.CLIENT_ShowLingMaiLife( str(spaceLifeSecond * csconst.TIME_ENLARGE_MULTIPLE + Functions.getTime()))
			
	def getPagodaScriptIDs( self, type ):
		"""获取灵塔scriptID"""
		if type in self._pagodaScript:
			return self._pagodaScript[type]
		return []
		
	def getCrystalBuff( self ):
		"""获取玩家的骑葫芦buffID"""
		return self._crystalBuffID
		
	def getHuLuDistance( self ):
		"""获取葫芦可监测范围"""
		return self._huluDistance
		
	def getPagodaDistance( self ):
		"""获取灵塔可监测范围"""
		return self._distance
		
	def getShadeDectPos( self ):
		""""""
		return self._shadeDectPos
		
	def getSunDectPos( self ):
		""""""
		return self._sunDectPos
		
	def getEnterInfoByCamp( self, camp ):
		"""根据阵营获得进入副本的位置朝向"""
		if camp == csdefine.CAMP_TAOSIM:
			return self._xianEnterPos, self._xianEnterDir
		else:
			return self._moEnterPos, self._moEnterDir

	def getTempCampBuff(self, tempCamp):
		return self.tempCampBuffs.get(str(tempCamp), 0)


	def getLoserRewardMailID(self):
		return self.loserRewardMailID

	def getWinnerRewardMailID(self):
		return self.winnerRewardMailID

	def getKillExpRate(self):
		return self.killExpRate

	def getKillExploits(self):
		return self.killExploits

	def getFinalExpDict(self, level, index):
		level = level//10*10
		if level in self.finalExpDict:
			return self.finalExpDict[level][index]
		return 0

	def getFinalWinExploits(self):
		return self.finalWinExploits

	def getFinalLostExploits(self):
		return self.finalLostExploits

	def getOutRewardMailID(self, level, index):
		"""
		获取失败出局的奖励邮件ID
		"""
		level = level//10*10
		if level in self.outRewardMailDict:
			return self.outRewardMailDict[level][index]
		return 0