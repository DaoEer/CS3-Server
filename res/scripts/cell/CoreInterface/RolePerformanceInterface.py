
# -*- coding: utf-8 -*-
import KBEngine
import KBEDebug
import GMCommand
import KBEMath

import Math
import random
import Const
import csdefine
import QuestEventDefine
import KBEMath
import csstatus
import KBEDebug
class RolePerformanceInterface:
	"""
	玩家表现
	"""
	def __init__( self ):
		"""
		初始化
		"""
		self.playSoundRecords = {"AI":{}, "Space":{}}	#存放AI播放语音的信息 用于接收播放结束事件， {"AI":{"voiceID1":casterID1, "voiceID1":casterID1}, "Space":{"voiceID1":casterID1, "voiceID1":casterID1}}
		

	def showMessageUpPlayerHead(self, msgID):
		"""
		CST-4009
		玩家头顶冒字
		"""
		self.client.ShowMessageUpPlayerHead(msgID)

	def showMessagePlaySound(self, soundID):
		"""
		调用客户端显示界面内容并播放语音
		"""
		self.client.ShowMessagePlaySound(soundID)

	def stopPlaySound(self, srcEntityID, soundID):
		"""
		exposed method
		语音结束通知
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		self.onStopPlaySound(soundID)

	def onStopPlaySound(self, soundID):
		"""
		"""
		if soundID in self.playSoundRecords["AI"]:
			monsterID = self.playSoundRecords["AI"][soundID]
			monster = KBEngine.entities.get(monsterID, None)
			if monster:
				monster.monsterAITriggerEvent(csdefine.ENTITY_EVENT_STOP_PLAY_SOUND, [soundID])
			self.playSoundRecords["AI"].pop(soundID)
		elif soundID in self.playSoundRecords["Space"]:
			spaceID = self.playSoundRecords["Space"][soundID]
			spaceEntity = self.getCurrentSpace()
			if spaceEntity.id == spaceID:
				self.spaceEvent_stopPlaySound(soundID)
			self.playSoundRecords["Space"].pop(soundID)
		
	def showPrompetOper( self, prompetID, particleID, offectSize ):
		"""客户端使用物品提示"""
		self.client.ShowPrompetOper( prompetID, particleID, offectSize )
		
	def hidePrompetOper( self ):
		"""隐藏提示"""
		if self.getClient():
			self.client.HidePrompetOper()
		
	def startGuessGame( self, questID, initMsg, winMsg, lostMsg, finishMsg ):
		"""开始猜大小游戏"""
		self.GuessGameQuestID = int(questID.split("|")[0])
		self.GuessGameTaskID = int(questID.split("|")[1])
		self.winMsg = winMsg
		self.lostMsg = lostMsg
		self.finishMsg = finishMsg
		self.winNum = 0
		if not self.hasQuest( self.GuessGameQuestID ):
			KBEDebug.CRITICAL_MSG("player(%s,%d) has not quest(%d), can not startGuessGame!"%( self.getName(),self.id, questID ))
			return
		self.client.StartGuessGame( initMsg )
		
	def guessGameSize( self, srcEntityID, size ):
		"""
		exposed method
		猜大小
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		self.guessSize = int(size)
	
	def guessGameRoll( self, srcEntityID, roll ):
		"""
		exposed method
		设置点数
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		if int(roll) in Const.SIZE_DEFINE[self.guessSize]:
			self.winNum += 1
			if self.winNum >= 3:
				self.client.FinishGuess( self.finishMsg )
			else:
				self.client.RightGuess( self.winMsg )
		else:
			self.lostNum += 1
			self.client.WrongGuess( self.lostMsg )
			
			
	def endGuessGame( self, srcEntityID ):
		"""
		exposed method
		完成猜大小任务
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		if winNum >= 3:
			self.setLoopQuestTaskCompleteNum( 1 )
		else:
			self.setLoopQuestTaskCompleteNum( 0 )
		self.forceQuestTaskIncreaseState( self.GuessGameQuestID , self.GuessGameTaskID)
		self.guessGameQuestID = 0
		self.winMsg = ""
		self.lostMsg = ""
		self.finishMsg = ""
		
	def isChallengeChangeBody( self, isChallenge, planeScriptID ):
		"""是否比赛变身"""
		if isChallenge:
			self.gotoSpacePlane( planeScriptID )

	def ldwj_putDownJinDan( self, srcEntityID ):
		"""
		exposed method
		灵岛危机：玩家放下金丹
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		jinDanBuffID = self.queryTemp("JinDanBuffID")
		if not jinDanBuffID:
			return
		indexList = self.findBuffsByBuffID( jinDanBuffID )
		if len(indexList) == 0:
			return
		self.removeBuff( indexList[0], csdefine.BUFF_END_RESON_BY_INTERRUPT )
			
	def onSwordCollisionBegin( self, srcEntityID, swordType, collisionType, position ):
		"""
		exposed method
		CST-2149 灵箭开始碰撞
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		spaceEntity = self.getCurrentSpace()
		if spaceEntity and (self.isInSpaceCopy() or self.isInSpacePlane()):
			spaceEntity.getScript().onConditionChange( spaceEntity, "", spaceEntity.id, "CollisionBegin", swordType + "|" + str(collisionType) + "|" + str(position.x) + "|" + str(position.y) + "|" + str(position.z))

	def onObtainCountAddList( self, srcEntityID, sparkey, addValue ):
		"""
		exposed method
		晶石碰撞产生能量球计数
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		spaceEntity = self.getCurrentSpace()
		if spaceEntity and (self.isInSpaceCopy() or self.isInSpacePlane()):
			spaceEntity.getScript().spaceEvent_addCount( spaceEntity, sparkey, addValue )


	def onBaGuaJigsawCompleted( self, srcEntityID ):
		"""
		exposed method
		八卦阵拼图成功
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		spaceEntity = self.getCurrentSpace()
		if spaceEntity and (self.isInSpaceCopy() or self.isInSpacePlane()):
			spaceEntity.getScript().onConditionChange(  spaceEntity, "", spaceEntity.id, "notice", "" )


	def cameraMove(self, targetEntityID, effectIDs, moveTime, delayTime):
		"""
		摄像机移动
		"""
		self.client.RoleCameraMoveToEntity(targetEntityID, effectIDs, moveTime, delayTime)

	def onCameraMove(self):
		"""
		摄像机移动结束 设置设置玩家位置朝向，改变模型
		"""
		#获取附身buff数据
		buffIndexs = self.findBuffsByBuffScript("BuffUsurp")
		if not len(buffIndexs):
			return
		buffData = self.getAttrBuffs()[buffIndexs[0]]
		buff = self.getBuff(buffData.buffID)

		casterID =  buffData.casterID
		caster = KBEngine.entities.get(casterID, None)
		if not caster:
			return
		self.position = Math.Vector3(caster.position)
		direction = Math.Vector3(caster.direction)
		self.changeDirection(direction, csdefine.REASON_CHANGE_DIR_FORCE)
		
		spaceEntity = self.getCurrentSpace()
		if not spaceEntity:
			return

		caster.destroySelf()
		spaceEntity.usurpStart(self, caster.scriptID, buffData.getTempData("isValid"))	
		self.client.RoleCameraMoveToEntityCB(buff.destroyEffectID)
		self.showMessageUpPlayerHead(Const.SKILL_POSSESS_SUCC_TIPS_ID)


	def onRoleCameraMoveToEntity(self, srcEntityID ):
		"""
		exposed method
		摄像机移动至指定entity位置回调
		"""
		if not self.validateClientCall( srcEntityID ):
			return

		self.onCameraMove()
	
	def createMonsterExtLightWall(self, position, direction):
		"""
		exposed method
		创建光墙，CST-3248专用
		
		param position: 客户端位置
		param direction: 客户端朝向
		"""
		position = KBEMath.Unreal2KBEnginePosition(position.split(" "))
		direction = KBEMath.Unreal2KBEngineDirection(direction.split(" "))
		player.createEntityNear("MonsterExtLightWall", position, direction, {})
		
	def addItemByOpenSpellBox(self, itemID, amount, reason ):
		"""
		"""
		result, _ = self.addItemByID( itemID, amount, reason )
		if result == csstatus.ITEM_GO_ON:
			self.client.ShowSpellBoxResultMessage( csdefine.SPELL_BOX_RESULT_ADDITEM,itemID )
		else:
			self.statusMessage( result )
	
	def dialogWithNPCTaskScriptID( self, npcScriptID):
		"""
		设置当前客户端NPC对话任务目标的NPCScriptID
		"""
		self.client.OnDialogWithNPCTaskScriptID( npcScriptID )
	
	def triggerQuestDialogWithNPC( self, srcEntityID, npcScriptID ):
		"""
		exposed method
		语音结束后，触发对话任务行为
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		self.triggerQuestEvent(QuestEventDefine.EVENT_TALK_WITH_NPC, npcScriptID)
		self.dialogWithNPCTaskScriptID("")
		
	def selectMonsterMenu( self, srcEntityID, monsterID, index ):
		"""
		exposed method
		回收怪物
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		monster = KBEngine.entities.get( monsterID )
		if monster and not monster.isDestroySelf:
			monster.onPlayerSelectMenu( self, index )
			
