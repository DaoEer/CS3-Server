# -*- coding: utf-8 -*-
import botdefine
import csdefine
import Define
import Functions
import KBEngine
import random
from BotTasks.BehaviourMgr import BehaviourMgr
from configObject.taskConfig import monsterPosition
mp = monsterPosition.Datas

ATTACK_TIMES_LIMIT = 20


skill1 = 100000001 #神罗天征
skill2 = 100096001 #瞬发版
skill3 = 999001005 #有目标的技能


class BotBehaviourInterface( object ):
	def __init__( self ):
		self.behaviours = None
		self.stopFlag = 0
		self._attackTargetID = -1
		self._attackTargetScriptID = ""
		self._killMonsterCounter = {}
		self._attackTimes = 0		
		self.initBehaviour()
		self.behaviourType = ""
		self.startKey=""
		self.timerID=0

	#--------------------------------------		
	def reset(self):
		"""
		重置各种初始数据
		"""
		self.teleportTo( botdefine.DEFAULT_SPACE ,botdefine.DEFAULT_POSITON,)
		#清空任务和任务完成标记
		self.resetQuest()
		
		for uid in self.petCages.keys():
			self.cell.freePet(uid)
		
	#------自动战斗------
	def startAutoFight(self):
		self.autoFightFlag = True				#开启战斗
		self.autoFight()
		
	def stopAutoFight(self):
		self.autoFightFlag = False				#结束战斗
		self.fightTargetID = 0
	
	#------------------------------------------
	# 机器人行为
	#------------------------------------------
	def initBehaviour( self ):
		self.behaviours = BehaviourMgr()

	def startTask( self, behaviourType,startKey="" ):
		"""
		开始新任务（指的是机器人做的事，并非一定指游戏任务）
		"""
		self.stopFlag = 0
		self.behaviourType = behaviourType
		self.startKey = startKey
		self.behaviours.startTask( self, behaviourType, startKey )
	
	def behControlReset( self, behaviourType ):
		"""
		重置行为管理器
		"""
		if behaviourType == 0: #重置所有
			for behObj in self.behaviours.values():
				behObj.reset( self )
		else:
			self.behaviours[ behaviourType ].reset( self )
		
	def behOver( self, time=6 ):
		"""
		"""
		if self.stopFlag:
			return
		KBEngine.callback( time, self.onBehOver )
		
	def onBehOver( self ):
		self.behaviours.doOver( self )

	def behDoNext( self ):
		KBEngine.cancelCallback( self.timerID )
		self.timerID = KBEngine.callback(600,self.restart)
		self.resetMonsterCounter()
		self.behaviours.doNext( self )
	#停止执行	
	def stopTask(self):
		self.stopFlag=1
	#继续执行	
	def continueTask(self):
		self.stopFlag=0
		KBEngine.callback( 1, self.onBehOver )

	def restart( self ):
		self.reset()
		self.resetMonsterCounter()
		self.startTask(self.behaviourType,self.startKey)

	#------------------------------------------
	# 击杀怪物统计
	#------------------------------------------
	def addKillMonsterCounter( self, scriptID ):
		"""
		添加击杀记录
		"""
		if not scriptID:
			return
		self.outputMsg("addKillMonsterCounter: %s"%scriptID )
		if scriptID in self._killMonsterCounter:
			self._killMonsterCounter[ scriptID ] += 1
		else:
			self._killMonsterCounter[ scriptID ] = 1

	def getKillMonstersCounter( self, scriptIDs ):
		"""
		获取击杀怪物的类量
		"""
		result = 0
		for scriptID, count in self._killMonsterCounter.items():
			if scriptID in scriptIDs:
				result += count

		return result
		
	def getKillMonsters(self):
		"""
		获取击杀怪物的类量
		"""
		return self._killMonsterCounter

	def resetMonsterCounter( self ):
		"""
		清空打怪记录
		"""
		self._killMonsterCounter.clear()
		self._attackTimes = 0
		self._attackTargetID = -1
		self._attackTargetScriptID = ""
		self.outputMsg( "attackTimes %s"%self._attackTimes)
	

	#------------------------------------------
	# 攻击 
	#------------------------------------------

	def killMonster( self, scriptIDs, amount ):
		"""
		杀指定的怪物
		"""
		if self._attackTimes >=  ATTACK_TIMES_LIMIT*amount:
			self.outputMsg("killMonster too much times %s"%scriptIDs)
			return
		selectMonster = self.selectAttackMonster( scriptIDs )
		if selectMonster:
			self._attackTargetID = selectMonster.id
			self._attackTargetScriptID = selectMonster.scriptID
			self.loopAttack()
		else:
			self.outputMsg("selectMonster is None")
			self.attackOver()

	def selectAttackSkill( self ):
		"""
		选择攻击技能
		"""
		return skill1
	
	def loopAttack( self ):
		"""
		循环使用技能攻击指定entity直到杀死目标为止
		"""
		skillID = self.selectAttackSkill()
		target = self.getAttackTarget()
		
		if target:
			self.moveTo(target.position)
			self.useSkillToTarget( skillID, target.id )
			KBEngine.callback( 6, self.loopAttack )
		else:
			self.attackOver()

	def attackOver( self ):
		self._attackTimes += 1
		self.outputMsg( "attackTimes %s"%self._attackTimes)
		#self.addKillMonsterCounter( self._attackTargetScriptID )
		self._attackTargetID = -1
		self._attackTargetScriptID = ""
		self.behOver()

	def getAttackTarget( self ):
		target = self.clientapp.entities.get( self._attackTargetID, None )
		if self.checkCanAttack( target ):
			return target
		else:
			return None

	
	#------------------------------------------
	# 移动/传送 KBE坐标单位是米，UE4坐标单位是厘米
	#------------------------------------------
	def goto( self, spaceLabel, position ):
		""" 传送或跑到目标位置 UE4坐标"""
		if spaceLabel is None and position is None:
			return 3
		self.outputMsg("goto %s %s"%(spaceLabel,position))
		if spaceLabel == self.spaceScriptID:
			lenth = self.position.distTo(position)
			needtime = lenth/self.moveSpeed
			if needtime > 60:								#有的地图太大，跑太远了。所以如果太远就直接传送吧
				self.teleportTo( spaceLabel, position )		#UE4坐标
				return 6
			serPosition = ( position[1] * 0.01, position[2] * 0.01, position[0] * 0.01 )
			self.moveTo( position )							#KBE坐标
			return needtime+3
		else:
			self.teleportTo( spaceLabel, position )		#UE4坐标
			return 6
		
	def moveTo( self, dstPosition ):
		""" 参数dstPosition 要用 KBE坐标 """
		self.moveToPoint( dstPosition, self.moveSpeed, 0.0, 0, True, True )

	def teleportTo( self, spaceLabel, dstPosition ):
		"""
		传送到指定地方 UE4坐标
		"""
		if not spaceLabel:
			self.position = dstPosition
		else:
			x, y, z = dstPosition
			strArgs = "%s %s %s %s"%( spaceLabel, x, y, z )
			self.GMCommand( self, "GOTO", strArgs )

	def findNPC( self, killMonsterScriptIDs, spaceScriptID="" ): 
		if spaceScriptID == "":
			spaceScriptID = self.spaceScriptID						#获取所在地图
		for monsterSID in killMonsterScriptIDs:
			if (spaceScriptID in mp) and (monsterSID in mp[spaceScriptID]):		#取得所在地图中目标怪物的位置
				position = mp[spaceScriptID][monsterSID]
				return spaceScriptID,position
			else:
				for sp in mp:
					if monsterSID in mp[sp]:
						return sp, mp[sp][monsterSID]
		return None,None		
		
	def onMoveFailure( self, controllerID, userData ):
		"""
		"""
		pass
		
	#------------------------------------------
	# 挑选目标
	#------------------------------------------
	def checkCanAttack( self, entity ):
		"""
		ENTITY_STATE_PEAD						= 0				# 未决状态
		ENTITY_STATE_FREE						= 1				# 普通状态
		ENTITY_STATE_WARN						= 2				# 警戒状态
		ENTITY_STATE_FIGHT						= 3				# 战斗状态
		ENTITY_STATE_DEAD						= 4				# 死亡状态
		ENTITY_STATE_RESET						= 5				# 重置状态（怪物特有）
		ENTITY_STATE_SHOW						= 6				# 表演状态（怪物特有）
		ENTITY_STATE_STALL						= 7				# 摆摊状态
		ENTITY_STATE_MAX						= 8				# 状态最大值，高于此值的为无效状态
		"""
		if not entity:
			return False
			
		if entity.state not in [ csdefine.ENTITY_STATE_FREE, csdefine.ENTITY_STATE_WARN, csdefine.ENTITY_STATE_FIGHT]:
			#self.outputMsg("checkCanAttack False entity %s %s state is %s"%(entity.scriptID,entity.id,entity.state))
			if entity.state==csdefine.ENTITY_STATE_SHOW:
				self.GMCommand(entity, "set_attr","state csdefine.ENTITY_STATE_FREE")
				#self.outputMsg("change entity %s state to %s"%(entity.id,csdefine.ENTITY_STATE_FREE))
			return False

		if entity.entityFlag == csdefine.ENTITY_FLAG_ROLE:
			if entity.camp == self.camp:
				self.outputMsg("checkCanAttack False entity %s Camp is %s"%(entity.playerName,entity.camp))			
				return False
		"""
		if self.position.distTo( entity.position ) > 20 :
			result = False
		"""

		return True

	def selectAttackMonster( self, scriptIDs ): 
		"""
		选择攻击目标
		"""
		return self.__getMinDistanceMonster( scriptIDs )

	def selectAttackRole( self, scriptIDs ): 
		"""
		选择攻击目标
		"""
		return self.__getEnemyMinDistanceRole()

	def __getMinDistanceMonster( self, scriptIDs ):
		"""
		获取范围内离自己最近的一个指定类型怪物
		"""
		result = None
		minDist = -1
		for e in self.entitiesInRange( 50 ):
			if e .entityFlag !=3 :
				#self.outputMsg("entity %s entityFlag is %i"%(e.id,e.entityFlag))
				continue
			self.outputMsg("entity %s entityFlag is %i "%(e.scriptID,e.entityFlag))
			
			cnd = lambda entity : True if entity.entityFlag==csdefine.ENTITY_FLAG_MONSTER and entity.scriptID in scriptIDs and self.checkCanAttack( entity ) else False
			if not cnd(e):continue
			dstToEntity = self.position.distTo( e.position )
			if minDist == -1:
				minDist = dstToEntity
				result = e
				if minDist == 0:
					break

			if dstToEntity < minDist:
				dstToEntity = minDist
				result = e
		
		self.outputMsg("entitys can attack is %s"%result)
		return result
	
	def __getEnemyMinDistanceRole( self ):
		"""
		获取范围内离自己最近的一个玩家
		"""
		result = None
		minDist = -1

		for e in self.entitiesInRange( 50, cnd = lambda entity : True if entity.entityFlag==csdefine.ENTITY_FLAG_ROLE and self.checkCanAttack( entity ) else False ):
			dstToEntity = self.position.distTo( e.position )
			if minDist == -1:
				minDist = dstToEntity
				result = e
				if minDist == 0:
					break

			if dstToEntity < minDist:
				dstToEntity = minDist
				result = e

		return result
		
	
	#------------------------------------------
	# 通用
	#------------------------------------------
	def clearStates(self):
		#清除未决Buff 等
		self.cell.CELL_onClientReady()
