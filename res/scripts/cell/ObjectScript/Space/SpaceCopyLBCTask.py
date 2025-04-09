#-*-coding:utf-8 -*-


from ObjectScript.Space.SpaceCopy import SpaceCopy
import Functions
import KBEMath
import Math


class SpaceCopyLBCTask(SpaceCopy):
	"""
	"""
	def __init__(self):
		SpaceCopy.__init__(self)
		self.pointDatas = []
		self.monsterDatas = []
		self.moveSpeed = 0.0
		self.armLength = 0.0
		self.cameraRotation = Math.Vector3(0,0,0)
		self.actionTimes = 1
		self.battleBuffID = 0
		self.vectoryEffectID = ""
		self.sceneDatas = []
		self.cmderID = ""
		self.routes = []
		self.nearDist = 5.0
		self.leaveVoiceIDs = {}

	
	def initData( self, configData ):
		"""
		"""
		SpaceCopy.initData(self, configData)
		pointDatas = configData["SpaceData"].get("pointDatas", [])
		for data in pointDatas:
			spawnPos = data["spawnPos"]
			spawnPos = Functions.vector3TypeConvert(spawnPos)
			spawnPos = KBEMath.Unreal2KBEnginePosition(spawnPos)

			spawnDir = data["spawnDir"]
			spawnDir = Functions.vector3TypeConvert(spawnDir)
			spawnDir = KBEMath.Unreal2KBEngineDirection(spawnDir)
			self.pointDatas.append({"spawnPos":spawnPos, "spawnDir":spawnDir})

		self.monsterDatas = configData["SpaceData"].get("monsterDatas", [])
		#玩家移动速度
		self.moveSpeed = configData["SpaceData"].get("moveSpeed", 600.0)

		#离开副本前的语音
		self.leaveVoiceIDs = configData["SpaceData"].get("leaveVoiceIDs", {})
		self.armLength = configData["SpaceData"].get("armLength",0.0)
		cameraRotationStr = configData["SpaceData"].get( "cameraRotation","" )
		self.cameraRotation = Functions.vector3TypeConvert( cameraRotationStr )

		self.actionTimes = configData["SpaceData"].get("actionTimes", 1)
		self.vectoryEffectID = configData["SpaceData"].get("vectoryEffectID", "")
		self.battleBuffID = configData["SpaceData"].get("battleBuffID", 0)
		self.sceneDatas = configData["SpaceData"].get("sceneDatas", [])
		self.taskExp = configData["SpaceData"].get("taskExp", [])
		self.cmderID = configData["SpaceData"].get("cmderID","")
		self.bodyAmount = int(configData["SpaceData"].get("bodyAmount", 5))
		self.bodyRadius = float(configData["SpaceData"].get("bodyRadius", 600.0))
		self.nearDist = float(configData["SpaceData"].get("nearDist", 5.0))
		
		routes = configData["SpaceData"].get("routes",[])
		for posList in routes:
			tempList = []
			for pos in posList:
				pos = Functions.vector3TypeConvert(pos)
				tempList.append(pos)
			self.routes.append(tempList)

		self.voiceIDs = configData["SpaceData"].get("voiceIDs", [])
		self.createMonsterDelay = configData["SpaceData"].get("createMonsterDelay", [])
		self.createMonsterDelayReverse = configData["SpaceData"].get("createMonsterDelayReverse", [])


	def onTeleportCompleted( self, selfEntity, playerRole ):
		SpaceCopy.onTeleportCompleted( self, selfEntity, playerRole )
		modelNumList = playerRole.getRoleBarracksSoldierModelNumbers()
		playerRole.setArmyModelList( modelNumList )
		if playerRole.getClient():
			playerRole.getClient().StartRoleLbcTaskOperation( self.armLength, self.cameraRotation )
			playerRole.getClient().ShowLbcStartTrainWnd()


	def onLeave( self, selfEntity, playerRole, packArgs ):
		"""
		"""
		SpaceCopy.onLeave( self, selfEntity, playerRole, packArgs )
		playerRole.resetArmyModelList()
		if playerRole.getClient():
			playerRole.getClient().EndRoleLbcTaskOperation()

