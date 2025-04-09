# -*- coding: utf-8 -*-
#
#
# 陷阱周期性行为

import csdefine
import csstatus


class TrapCycleActionBase:
	"""
	陷阱周期性触发效果基础类
	"""
	type = csdefine.TRAP_CYCLE_ACTION_NONE

	@staticmethod
	def cycleBegin( selfEntity, index, args ):
		"""
		"""
		timerID = selfEntity.queryTemp( "TRAP_CYCLE_ACTION_TIMERID_%d"%index, 0 )
		if timerID:return
		
		timerID = selfEntity.addTimerRepeatForScript( float( args["param1"] ), "cycleDo", ( args["scriptKey"],args ))
		selfEntity.setTemp( "TRAP_CYCLE_ACTION_TIMERID_%d"%index, timerID )
		
	@staticmethod
	def cycleEnd( selfEntity, index, args ):
		"""
		"""
		timerID = selfEntity.queryTemp( "TRAP_CYCLE_ACTION_TIMERID_%d"%index, 0 )
		if timerID:
			selfEntity.popTimer( timerID )
			selfEntity.removeTemp( "TRAP_CYCLE_ACTION_TIMERID_%d"%index )
		
	@staticmethod
	def cycleDo( selfEntity, args ):
		"""
		"""
		pass
		
		
class TrapCycleActionUseSkill( TrapCycleActionBase ):
	"""
	陷阱周期性对自己使用技能
	"""
	type = csdefine.TRAP_CYCLE_ACTION_USE_SKILL
		
	@staticmethod
	def cycleDo( selfEntity, args ):
		"""
		"""
		selfEntity.useSkillToEntity( int(args["param2"]), selfEntity.id )

class TrapCycleActionCreateEntity( TrapCycleActionBase ):
	"""
	陷阱周期性将自己销毁
	"""
	type = csdefine.TRAP_CYCLE_ACTION_CREATE_ENTITY
	
	@staticmethod
	def cycleDo( selfEntity, args ):
		"""
		"""
		selfEntity.createEntityByScriptID( args["param2"],selfEntity.position,selfEntity.direction,{"spawnPos":selfEntity.position} )

class TrapCycleActionSparHunTingCheck( TrapCycleActionBase ):
	"""
	晶石狩猎场 周期给阵营的玩家增加金钱
	"""
	type = csdefine.TRAP_CYCLE_ACTION_CHECKAROUND

	@staticmethod
	def cycleDo( selfEntity, args ):
		"""
		"""
		data = selfEntity.queryTemp("rewardCamp") #data[0] 表示获得奖励的阵营 data[1]表示每次获得奖励的金钱
		money = selfEntity.queryTemp("rewardMoney")
		selfEntity.setTemp("rewardMoney",money + data[1]) 
		spaceEntity = selfEntity.getCurrentSpace()
		if spaceEntity:
			spaceEntity.addCampMoney(data[0],data[1])

class TrapCycleActionCheckHasPlayer( TrapCycleActionBase ):
	"""
	CST-3740 检查一定范围内是否有玩家
	"""
	type = csdefine.TRAP_CYCLE_ACTION_CHECKHASPLAYER

	@staticmethod
	def cycleDo( selfEntity, args ):
		"""
		"""
		#param3 格式：buffID|type   如需新增类型需修改蓝图
		buffID, msgType = args["param3"].split("|")
		time = selfEntity.queryTemp("HasPlayerTime")
		roleList = selfEntity.entitiesInRangeExt( float(args["param2"]), "Role" )
		if time == None:
			time = 0.0
			selfEntity.setTemp("HasPlayerTime",time)
		if len(roleList) > 0:
			if time >= 1.0:
				spaceEntity = selfEntity.getCurrentSpace()
				if spaceEntity:
					spaceEntity.getScript().onConditionChange(spaceEntity,"",spaceEntity.scriptID,"add","")
				msgStr = selfEntity.scriptID + '|' + msgType
				roleList[0].showFaBaoCollectSuccMsg(msgStr)
				selfEntity.changeState( csdefine.ENTITY_STATE_DEAD )
				return
			buffList = roleList[0].findBuffsByBuffID(int(buffID))
			if len(buffList) <= 0:
				roleList[0].addBuff(selfEntity,int(buffID))
			#curEnergyValue = roleList[0].queryTemp("CurEnergyValue")
			#maxEnergyValue = roleList[0].queryTemp("MaxEnergyValue")
			#if not (curEnergyValue and maxEnergyValue):
			#	return
			#if curEnergyValue > 3:
			#	curEnergyValue -= 3.14
			#else:
			#	curEnergyValue = 0
			#roleList[0].setTemp("CurEnergyValue",curEnergyValue)
			#roleList[0].updateEnergyBar(curEnergyValue,maxEnergyValue)
			time += 0.07
			selfEntity.setTemp("HasPlayerTime",time)
			selfEntity.allClients.CLIENT_ChangeProgressBar(time)
		else:
			if time > 0.15:
				time -= 0.15
			else:
				time = 0.0
			selfEntity.setTemp("HasPlayerTime",time)
			selfEntity.allClients.CLIENT_ChangeProgressBar(time)
			

class TrapCycleActionBattleFlagCheck( TrapCycleActionBase ):
	"""
	攻城战  战旗占领
	"""
	type = csdefine.TRAP_CYCLE_ACTION_BATTLEFLAG_CHECK

	@staticmethod
	def cycleDo( selfEntity, args ):
		"""
		"""
		selfEntity.occupyCheck( args )

class TrapCycleActionBarracksReviveCheck( TrapCycleActionBase ):
	"""
	攻城战 兵营的回复检测
	"""
	type = csdefine.TRAP_CYCLE_ACTION_BARRACKS_REVIVE_CHECK

	@staticmethod
	def cycleDo( selfEntity, args ):
		"""
		"""
		selfEntity.barracksReviveCheck( args )