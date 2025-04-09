# -*- coding: utf-8 -*-
#
#
# 陷阱进入（离开）一般行为
import random
import Functions
import KBEngine
import KBEMath
import csdefine
from ConfigObject.Reward.RewardBase import RewardMgr

class TrapNormalActionBase:
	"""
	陷阱触发效果基础类
	"""
	def __init__( self ):
		"""
		"""
		pass

	@staticmethod
	def do( selfEntity, avatar, args ):
		"""
		"""
		pass

class TrapNormalActionEnterPlane( TrapNormalActionBase ):
	"""
	进入位面
	"""
	def __init__( self ):
		"""
		"""
		pass

	@staticmethod
	def do( selfEntity, avatar, args ):
		"""
		"""
		avatar.gotoSpacePlane( args[0] )
		
class TrapNormalActionLeavePlane( TrapNormalActionBase ):
	"""
	离开位面
	"""
	def __init__( self ):
		"""
		"""
		pass

	@staticmethod
	def do( selfEntity, avatar, args ):
		"""
		"""
		avatar.leaveSpacePlane( args[0] )
		
class TrapNormalActionSpell( TrapNormalActionBase ):
	"""
	陷阱对目标施法
	"""
	def __init__( self ):
		"""
		"""
		pass

	@staticmethod
	def do( selfEntity, avatar, args ):
		"""
		"""
		selfEntity.useSkillToEntity( int(args[0]), avatar.id )

class TrapNormalActionHitBack( TrapNormalActionBase ):
	"""
	击退行为
	"""
	def __init__( self ):
		"""
		"""
		pass

	@staticmethod
	def do( selfEntity, avatar, args ):
		"""
		"""
		avatar.addBuff(selfEntity,int(args[0]))

class TrapNormalActionDeadSelf( TrapNormalActionBase ):
	"""
	陷阱进入死亡状态
	"""
	def __init__( self ):
		"""
		"""
		pass

	@staticmethod
	def do( selfEntity, avatar, args ):
		"""
		"""
		if args:
			selfEntity.addTimerCallBack( float(args[0]), "changeState", (csdefine.ENTITY_STATE_DEAD,))
		else:
			selfEntity.changeState(csdefine.ENTITY_STATE_DEAD)

class TrapNormalActionAddTeleportPoint( TrapNormalActionBase ):
	"""
	进入陷阱添加开启的传送点
	"""
	def __init__( self ):
		"""
		"""
		pass

	@staticmethod
	def do( selfEntity, avatar, args ):
		"""
		"""
		index = args[0]
		if avatar.__class__.__name__ == "Role":
			avatar.addTeleportPoint( index )
			
class TrapNormalActionStartWalk( TrapNormalActionBase ):
	"""
	进入陷阱开始巡逻
	"""
	def __init__( self ):
		"""
		"""
		pass

	@staticmethod
	def do( selfEntity, avatar, args ):
		"""
		"""
		selfEntity.startWalk()

class TrapNormalActionCreateEntity( TrapNormalActionBase ):
	"""
	进入陷阱随机创建Entitiy param1:scriptID用“|”分隔
	"""
	def __init__( self ):
		"""
		"""
		pass

	@staticmethod
	def do( selfEntity, avatar, args ):
		"""
		"""
		scriptIDList = args[0].split("|")
		index = random.randint(0,len(scriptIDList) -1 )
		selfEntity.createEntityByScriptID(scriptIDList[index],selfEntity.position,selfEntity.direction,{"spawnPos":selfEntity.position})

class TrapNormalSpaceDoorTeleport( TrapNormalActionBase ):
	"""
	大地图传送门的传送行为
	"""
	def __init__( self ):
		"""
		"""
		pass

	@staticmethod
	def do( selfEntity, avatar, args ):
		"""
		"""
		pos = Functions.vector3TypeConvert( args[1] )
		dir = Functions.vector3TypeConvert( args[2] )
		avatar.doorTeamFollowTransport( selfEntity, args[0], pos, dir )	#组队跟随传送
		avatar.gotoSpaceUE4( args[0], pos, dir )

class TrapNormalChangeSpaceLife( TrapNormalActionBase ):
	"""
	副本计时 增加\减少
	"""
	def __init__( self ):
		"""
		"""
		pass

	@staticmethod
	def do( selfEntity, avatar, args ):
		"""
		"""
		_time = int(args[0])
		spaceEntity = selfEntity.getCurrentSpace()
		if spaceEntity:
			spaceEntity.getScript().changeSpaceLife( spaceEntity, _time )

class TrapNormalPlayAction( TrapNormalActionBase ):
	"""
	陷阱播个一组动作
	"""
	def __init__( self ):
		"""
		"""
		pass

	@staticmethod
	def do( selfEntity, avatar, args ):
		"""
		"""
		actionIDs = args[0].strip().split('|')
		delayTimes = [ float(t) for t in args[1].strip().split('|')]
		
		delayTime = 0
		for index in list( range(0, len(actionIDs)) ):
			selfEntity.addTimerCallBack( delayTime, 'playAction', (actionIDs[index],) )
			delayTime += delayTimes[index]


class TrapNormalGetReward( TrapNormalActionBase ):
	"""
	获得奖励
	"""
	def __init__( self ):
		"""
		"""
		pass

	@staticmethod
	def do( selfEntity, avatar, args ):
		"""
		"""
		rewardID = args[0].strip()
		datas = RewardMgr.g_rewardMgr.getReward(rewardID, {"player":avatar})
		RewardMgr.g_rewardMgr.doRewards(datas, avatar.id, csdefine.ADD_REWARD_REASON_COMMON_TYPE_TRAP_ACTION)

class TrapNormalSetDirection( TrapNormalActionBase ):
	"""
	改变进入者朝向（不配取陷阱朝向）
	"""
	def __init__( self ):
		"""
		"""
		pass

	@staticmethod
	def do( selfEntity, avatar, args ):
		"""
		"""
		if args[0] == "":
			direction = selfEntity.direction
			avatar.changeDirection(direction, csdefine.REASON_CHANGE_DIR_FORCE)
		else:
			direction = Functions.vector3TypeConvert( args[0] )
			direction = KBEMath.Unreal2KBEngineDirection( direction )
			avatar.changeDirection(direction, csdefine.REASON_CHANGE_DIR_FORCE)
		RotationTime = 0.0
		if len(args) >= 2:
			RotationTime = float(args[1]) if float(args[1]) > 0 else 0.0
		avatar.allClients.OnPlayerCameraRotation(RotationTime)
			
class TrapNormalSetTemp( TrapNormalActionBase ):
	"""
	添加temp值
	"""
	def __init__( self ):
		"""
		"""
		pass

	@staticmethod
	def do( selfEntity, avatar, args ):
		"""
		"""
		if args[0]:
			value = avatar.queryTemp( args[0], 0 )
		avatar.setTemp( args[0], value + 1 )

class TrapNormalConditionChange( TrapNormalActionBase ):
	"""
	给副本发送通知
	"""
	def __init__( self ):
		"""
		"""
		pass

	@staticmethod
	def do( selfEntity, avatar, args ):
		"""
		"""
		spaceEntity = avatar.getCurrentSpace()
		if spaceEntity:
			spaceEntity.getScript().onConditionChange( spaceEntity,"Trap",selfEntity.scriptID,args[0],"" )

class TrapNormalCreateHeHua( TrapNormalActionBase ):
	"""
	CST-3660 创建荷花
	"""
	def __init__( self ):
		"""
		"""
		pass

	@staticmethod
	def do( selfEntity, avatar, args ):
		"""
		"""
		spaceEntity = avatar.getCurrentSpace()
		if not spaceEntity:
			return
		point = spaceEntity.getPointInCoord( selfEntity.id )
		if spaceEntity.whiteHeHuaID == args[0]:
			spaceEntity.addTimerCallBack(float(args[1]),"createWhiteHeHuaCB",(tuple(point),))
		elif spaceEntity.redHeHuaID == args[0]:
			spaceEntity.addTimerCallBack( float(args[1]),"createRedHeHuaCB", (tuple(point),))
			
		selfEntity.delayDestroy(2.5)


class TrapNormalGetItem( TrapNormalActionBase ):
	"""
	玩家获得物品(怪物则使用技能)
	"""
	def __init__( self ):
		"""
		"""
		pass

	@staticmethod
	def do( selfEntity, avatar, args ):
		"""
		"""
		if avatar.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ):
			avatar.addItemByID(int(args[0]))
		else:
			if len(args) >= 2:
				selfEntity.useSkillToEntity(int(args[1]), avatar.id)

class TrapNormalHQLZCreateEntity( TrapNormalActionBase ):
	"""
	环任务:获取龙珠 随机创建Entity 并记录
	"""
	def __init__( self ):
		"""
		"""
		pass

	@staticmethod
	def do( selfEntity, avatar, args ):
		"""
		"""
		point = selfEntity.queryTemp("PointPos",())
		spaceEntity = selfEntity.getCurrentSpace()
		if spaceEntity:
			if spaceEntity.isPointHasEntity(point):
				return

			scriptIDList = args[0].split("|")
			index = random.randint(0,len(scriptIDList) -1 )
			selfEntity.createEntityByScriptID(scriptIDList[index],selfEntity.position,selfEntity.direction,{"spawnPos":selfEntity.position})
			spaceEntity.addPointHasEntity( point )


class TrapNormalTeleportNearestEntity( TrapNormalActionBase ):
	"""
	传送距离最近的同scriptID的entity
	"""
	def __init__( self ):
		"""
		"""
		pass

	@staticmethod
	def do( selfEntity, avatar, args ):
		"""
		"""
		IDList = selfEntity.getCurrentSpace().getEntityRecord(selfEntity.scriptID)
		nextTrap = None
		distance = 0
		for id in IDList:
			e = KBEngine.entities.get( id, None )
			if id == selfEntity.id or not e:
				continue
			if not distance:	
				distance = selfEntity.position.distTo(e.position)
				nextTrap = e
				continue
			_dis = selfEntity.position.distTo(e.position)
			if distance > _dis:
				distance = _dis
				nextTrap = e
		_time = 2.0
		if args:
			_time = float(args[0])
		if nextTrap:
			avatar.addTimerCallBack( _time,  "gotoSpace", (avatar.getCurrentSpaceScriptID(), nextTrap.position, nextTrap.direction) )

class TrapNormalTeleportRandomPosition( TrapNormalActionBase ):
	"""
	传送到随机位置
	"""
	def __init__( self ):
		"""
		"""
		pass

	@staticmethod
	def do( selfEntity, avatar, args ):
		"""
		"""
		teleportList = args[0].split("|")
		random.shuffle( teleportList )
		strList  = teleportList[0].split(":")
		Position = KBEMath.Unreal2KBEnginePosition(Functions.vector3TypeConvert( strList[0]))
		Direction = KBEMath.Unreal2KBEngineDirection(Functions.vector3TypeConvert( strList[1]))
		avatar.gotoSpace(avatar.getCurrentSpaceScriptID(), Position, Direction)

class TrapNormalActionSpellSelf( TrapNormalActionBase ):
	"""
	对自身施法
	"""
	def __init__(self):
		pass

	@staticmethod
	def do(selfEntity, avatar, args):
		"""
		"""
		selfEntity.useSkillToEntity( int(args[0]), selfEntity.id )

class TrapNormalSendAI( TrapNormalActionBase ):
	"""
	给某些scriptID的怪物发送AI指令
	"""
	def __init__(self):
		pass

	@staticmethod
	def do(selfEntity, avatar, args):
		"""
		"""
		scriptIDs = args[0].split("|")
		commandID = args[1]
		spaceEntity = selfEntity.getCurrentSpace()
		for scriptID in scriptIDs:
			for id in spaceEntity.getEntityRecord( scriptID ):
				entity = KBEngine.entities.get( id )
				if not entity:
					continue
				entity.monsterAIOnCommand( selfEntity.id, spaceEntity.scriptID, commandID )

class TrapNormalRemoveBuff( TrapNormalActionBase ):
	"""
	移除Buff
	"""
	def __init__(self):
		pass

	@staticmethod
	def do(selfEntity, avatar, args):
		"""
		"""
		avatar.removeBuffByID( int( args[0] ) )

class TrapNormalActionTriggerSpellSelf( TrapNormalActionBase ):
	"""
	触发者对自身施法
	"""
	def __init__(self):
		pass

	@staticmethod
	def do(selfEntity, avatar, args):
		"""
		"""
		avatar.useSkillToEntity( int(args[0]), avatar.id )