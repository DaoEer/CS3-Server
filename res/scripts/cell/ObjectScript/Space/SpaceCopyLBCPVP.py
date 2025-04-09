# -*- coding: utf-8 -*-


from ObjectScript.Space.SpaceCopyLBCBase import SpaceCopyLBCBase
import KBEMath
import Functions
import csdefine

class SpaceCopyLBCPVP( SpaceCopyLBCBase ):
	"""
	高级练兵场-英雄王座玩法
	"""
	def __init__( self ):
		SpaceCopyLBCBase.__init__( self )
		self.allowTeamNumber = 0	#允许组队的人数
		self.enterProtectInfo = ()	# 进入防守方的位置
		self.enterAttackInfo = ()	# 进入进攻方位置数据
		self.offensiveScriptIDList = []		#进攻方防御塔scriptID列表
		self.defensiveScriptIDList = [] 	#防守方防御塔scriptID列表
		

	def initData( self, configData ):
		"""
		virtual method
		"""
		SpaceCopyLBCBase.initData( self, configData )
		self.allowTeamNumber = configData["SpaceData"].get("allowTeamNumber",0)

		enterPosInfos = configData["SpaceData"].get("enterPos","").split("|")
		enterDirInfos = configData["SpaceData"].get("enterDir","").split("|")
		enterPosList = []
		enterDirList = []
		for enterPosInfo in enterPosInfos:
			pos = Functions.vector3TypeConvert(enterPosInfo)
			pos = KBEMath.Unreal2KBEnginePosition( pos )
			enterPosList.append(pos)

		for enterDirInfo in enterDirInfos:
			dir = Functions.vector3TypeConvert(enterDirInfo)
			dir = KBEMath.Unreal2KBEngineDirection( dir )
			enterDirList.append(dir)
		self.enterAttackInfo = (enterPosList[0],enterDirList[0] )
		self.enterProtectInfo = (enterPosList[1],enterDirList[1] )

		self.offensiveScriptIDList = configData["SpaceData"].get("offensiveScriptIDList", "").split("|")
		self.defensiveScriptIDList = configData["SpaceData"].get("defensiveScriptIDList", "").split("|")

	def getOffensiveScripts(self):
		"""
		"""
		return self.offensiveScriptIDList

	def getDefensiveScripts(self):
		"""
		"""
		return self.defensiveScriptIDList


	def getAllowTeamNumber( self ):
		"""
		允许几人组队
		"""
		return self.allowTeamNumber

	def getProtectEnterInfo( self ):
		"""
		获得防守方的进入信息
		"""
		return self.enterProtectInfo

	def getAttackEnterInfo( self ):
		"""
		获得进攻方的进入信息
		"""
		return self.enterAttackInfo

	def getPackDomainData( self, playerEntity, args ):
		gotoArgs = SpaceCopyLBCBase.getPackDomainData( self,playerEntity, args )
		gotoArgs["spaceKey"] = str(gotoArgs.get("belongDBID",0))
		return gotoArgs

	def onEnter( self, selfEntity, playerRole, packArgs ):
		SpaceCopyLBCBase.onEnter( self, selfEntity, playerRole, packArgs )








