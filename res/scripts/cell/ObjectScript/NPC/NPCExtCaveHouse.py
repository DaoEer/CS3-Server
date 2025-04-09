# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
from ObjectScript.NPC import NPC
import csstatus


class NPCExtCaveHouse( NPC.NPC ):
	def __init__( self ):
		NPC.NPC.__init__( self )
		self.spaceScriptID = ""
		self.modelNumberList = []
		self.dongFuType = csdefine.SPACE_TYPE_PRIVATE
		self.effectList = []

	def initData( self, configData ):
		NPC.NPC.initData( self, configData )
		if configData["Param1"]:
			self.spaceScriptID = configData["Param1"]
		if configData["Param2"]:
			self.modelNumberList = configData["Param2"].split("|")
		if configData["Param3"]:
			self.dongFuType = int(configData["Param3"])
		if configData["Param4"]:
			self.effectList = configData["Param4"].split("|")

	def getModelByLevel( self, level ):
		"""获取对应等级的模型"""
		minLevel = min(level, len(self.modelNumberList))
		return self.modelNumberList[minLevel-1]
		
	def getDongFuType(self):
		"""返回洞符/高级洞府"""
		return self.dongFuType

	def gossipWith( self, selfEntity, srcEntityID ):
		"""
		处理玩家请求与NPC对话的信息
		"""
		playerCell = KBEngine.entities.get( srcEntityID, None )
		space = selfEntity.getCurrentSpace()
		# 洞府已经建好
		if selfEntity.buildState == csdefine.LHMJ_BUILD_STATE_READY:
			if playerCell.playerDBID == selfEntity.belongDBID:
				playerCell.client.OnEnterCaveHouse( selfEntity.id )		#进入洞府
				return
			elif playerCell.challengeDBID and playerCell.challengeDBID == selfEntity.belongDBID:
				if KBEngine.globalData.get( "LHMJ_ChallengeActive") or KBEngine.globalData.get( "LHMJ_PlunderActive" ):		# 掠夺战、争夺战开启
					playerCell.client.OnEnterOtherCaveHouse( selfEntity.id )	# 进入挑战洞府
					return
				else:
					playerCell.statusMessage( csstatus.LHMJ_CHANGELLENGE_NOT_OPEN, "" )
					return
			else:
				playerCell.statusMessage( csstatus.DONG_FU_NOT_BELONG_TO_PLAYER, "" )
		# 正在创建的洞府
		elif selfEntity.buildState == csdefine.LHMJ_BUILD_STATE_IS_BUILD:
			if playerCell.getBuildIndex() == selfEntity.group and int(space.spaceKey) == playerCell.caveHouseLine:
				playerCell.statusMessage( csstatus.DONG_FU_IS_IN_PROGRESS, "" )
		# 洞府占领状态
		elif selfEntity.buildState == csdefine.LHMJ_BUILD_STATE_OCUPPY:
			if playerCell.getBuildIndex() == selfEntity.group and int(space.spaceKey) == playerCell.caveHouseLine:
				playerCell.client.StartBuildCaveHouse( selfEntity.id, str( selfEntity.occupyProtectTime ))
		
