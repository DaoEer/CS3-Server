# -*- coding: utf-8 -*-
import Const
import Math
import KBEMath
import KBEngine
import random
import csdefine
from ObjectScript import Space
from ObjectScript.Space.SpaceCopyMagicMazeChild import SpaceCopyMagicMazeChild


class SpaceCopyMagicMazeChildDestiny( SpaceCopyMagicMazeChild ):
	"""
	幻阵迷宫 天命玩法
	"""
	def __init__( self ):
		SpaceCopyMagicMazeChild.__init__( self )
		self.fubenList = []
		self.qiyuList = []
		self.baoxiangList = []
		self.wendaList = []
		self.delayTeleportTime = 0
		self.delayNotifyTime = 0
		self.needLevel = 0
		self.shangcibangList = []
		self.xiacibangList = []
		self.xuanwuList = []
		self.wenhao = []
		
	def initData( self, configData ):
		"""
		virtual method
		"""
		SpaceCopyMagicMazeChild.initData( self, configData )
		fuben = configData["SpaceData"].get("fuben", "")
		if fuben != "":
			self.fubenList = [i.strip() for i in fuben.split("|")]
		qiyu = configData["SpaceData"].get("qiyu", "")
		if qiyu != "":
			self.qiyuList = [i.strip() for i in qiyu.split("|")]
		baoxiang = configData["SpaceData"].get("baoxiang", "")
		if baoxiang != "":
			self.baoxiangList = [i.strip() for i in baoxiang.split("|")]
		wenda = configData["SpaceData"].get("wenda", "")
		if wenda != "":
			self.wendaList = [i.strip() for i in wenda.split("|")]
		self.delayTeleportTime = configData["SpaceData"].get("delayTeleportTime", 0)
		self.delayNotifyTime = configData["SpaceData"].get("delayNotifyTime", 0)
		self.needLevel = configData["SpaceData"].get("needLevel", 0)
		shangcibang = configData["SpaceData"].get("shangcibang", "")
		if shangcibang != "":
			self.shangcibangList = [i.strip() for i in shangcibang.split("|")]
		xiacibang = configData["SpaceData"].get("xiacibang", "")
		if xiacibang != "":
			self.xiacibangList = [i.strip() for i in xiacibang.split("|")]
		xuanwu = configData["SpaceData"].get("xuanwu", "")
		if xuanwu != "":
			self.xuanwuList = [i.strip() for i in xuanwu.split("|")]
		self.wenhao = configData["SpaceData"].get("wenhao", "")

	def getChildNeedLevel(self):
		"""
		"""
		return self.needLevel

	def randomZhuanPan( self, selfEntity):
		result = random.randint(1,4)
		isForward = True
		minDice = 1
		maxDice = 6
		maxStepCount = 1
		spaceName = ""
		belongType,spaceKey = self.getPlayerBelongTypeAndSpaceKey(selfEntity)
		if result == Const.MAGIC_MAZE_SHANG_CHI_BANG:
			minDice = random.randint(2,4)
			maxDice = minDice
		elif result == Const.MAGIC_MAZE_XIA_CI_BANG:
			isForward = False
			minDice = random.randint(2,4)
			maxDice = minDice
		elif result == Const.MAGIC_MAZE_XUAN_WU:
			maxDice = 1
			maxStepCount = random.randint(3,4)
		else:
			maxStepCount = 0
			#随机选择一种副本，然后进入
			type = random.randint(1,4)
			if type == Const.MGGIC_MAZE_WEN_HAO_FU_BEN:
				spaceName = random.choice(self.fubenList)
			elif type == Const.MGGIC_MAZE_WEN_HAO_QI_YU:
				spaceName = random.choice(self.qiyuList)
			elif type == Const.MGGIC_MAZE_WEN_HAO_BAO_XIANG:
				spaceName = random.choice(self.baoxiangList)
			else:
				spaceName = random.choice(self.wendaList)
		if spaceName == "":
			KBEngine.globalData["MagicMazeSpaceManager"].setSpaceExtraDice(belongType, spaceKey, minDice, maxDice, maxStepCount, isForward)
		else:
			#KBEngine.globalData["MagicMazeSpaceManager"].setExtraSpaceName(belongType, spaceKey, spaceName)
			selfEntity.addTimerCallBackForScript(self.delayTeleportTime, "onTeleportExtraSpace", (spaceName,))
		selfEntity.addTimerCallBackForScript( self.delayNotifyTime, "noticePlayerVoiceMsg", (result, minDice, maxDice, maxStepCount) )
		selfEntity.addTimerCallBack( 1 + self.delayTeleportTime, "closeSpace", () )
		
		#告知玩家效果
		for playerCell in selfEntity._spaceRoles:
			player = KBEngine.entities.get( playerCell.id, None )
			if player:
				player.client.CLIENT_MagicMazeDestinyResult(result)
		
				
	def noticePlayerVoiceMsg(self, selfEntity, result, minDice, maxDice, maxStepCount):
		"""
		给予玩家语音提示信息
		"""
		voiceID = ""
		if result == Const.MAGIC_MAZE_SHANG_CHI_BANG:
			if len(self.shangcibangList) >= 3:
				voiceID = self.shangcibangList[minDice - 2]
		elif result == Const.MAGIC_MAZE_XIA_CI_BANG:
			if len(self.xiacibangList) >= 3:
				voiceID = self.xiacibangList[minDice - 2]
		elif result == Const.MAGIC_MAZE_XUAN_WU:
			if len(self.xuanwuList) >= 2:
				voiceID = self.xuanwuList[maxStepCount - 3]
		else:
			voiceID = self.wenhao
		if voiceID != "":
			for playerCell in selfEntity._spaceRoles:
				player = KBEngine.entities.get( playerCell.id, None )
				if player:
					player.showMessagePlaySound( voiceID )
	
	def onTeleportExtraSpace( self, selfEntity, spaceName):
		teammates = []
		for playerCell in selfEntity._spaceRoles:
			teammates.append( playerCell.base )
		isPlayerInTeam = False
		for playerCell in selfEntity._spaceRoles:
			player = KBEngine.entities.get( playerCell.id, None )
			if player and player.isInTeam() and player.isTeamCaptain():
				belongType = csdefine.SPACE_BELONG_TEAM
				spaceKey = str( player.teamMailbox.id )
				spaceLevel = min( self.getChildNeedLevel() + 19, player.getLevel() )	#怪物等级上限为副本开放等级+19级（CST-2880）
				pickArg = { "packBelongType": belongType, "packSpaceLevel": spaceLevel, "spaceKey":spaceKey, "teammates": teammates, "isSpecialSpace": True,"mainScriptID":selfEntity.createArgs["mainScriptID"]}
				isPlayerInTeam = True
				player.gotoMagicMazeExtraSpace(belongType, selfEntity.scriptID, pickArg, spaceName)
		
		if not isPlayerInTeam:
			for playerCell in selfEntity._spaceRoles:
				player = KBEngine.entities.get( playerCell.id, None )
				if player:
					belongType = csdefine.SPACE_BELONG_PERSON
					spaceKey = str( player.playerDBID )
					spaceLevel = min( self.getChildNeedLevel() + 19, player.getLevel() )	#怪物等级上限为副本开放等级+19级（CST-2880）
					pickArg = { "packBelongType": belongType, "packSpaceLevel": spaceLevel, "spaceKey":spaceKey, "isSpecialSpace": True,"mainScriptID":selfEntity.createArgs["mainScriptID"]}
					player.gotoMagicMazeExtraSpace(belongType, selfEntity.scriptID, pickArg, spaceName)

	def onEnter( self, selfEntity, playerRole, packArgs ):
		SpaceCopyMagicMazeChild.onEnter( self, selfEntity, playerRole, packArgs )
		player = KBEngine.entities.get( playerRole.id, None )
		if player:
			player.client.CLIENT_CreateDestinyZhuanPan()