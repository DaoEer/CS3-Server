# -*- coding: utf-8 -*-
import random
import csconst
import csdefine
from SrvDef import MoveTestType

#添加Entity的最大移动速度限制，防止不停循环移动，导致服务器崩溃
MAX_MOVE_SPEED = 25.0
MOVE_FUN_DICT = {}

def moveStop(entity):
	"""
	"""
	entity.cancelController( "Movement" )
	entity.moveControlID = 0
	return 0
	
#-----------------------  KBE原生移动接口 -------------------------------------------------
def kbeMove_moveNavigatePoint(entity, targetPosition, distance = 1.0, faceMovement = True, layer = 0):
	"""
	"""
	return entity.moveToPoint( targetPosition, min( entity.moveSpeed, MAX_MOVE_SPEED ), distance, entity.moveScriptID, faceMovement, True)

MOVE_FUN_DICT[MoveTestType.KBEMove] = {}
MOVE_FUN_DICT[MoveTestType.KBEMove][csdefine.MOVE_TYPE_STOP] = moveStop
MOVE_FUN_DICT[MoveTestType.KBEMove][csdefine.MOVE_TYPE_NAVIGATE_POINT] = kbeMove_moveNavigatePoint


#-----------------------  直接设置坐标移动  ------------------------------------------------
def setPosMove_moveNavigatePoint(entity, targetPosition, distance = 1.0, faceMovement = True, layer = 0):
	"""
	"""
	entity.position = targetPosition
	delayTime = random.randint(3, 5)
	entity.addTimerCallBack( delayTime, "onMoveOver",  (0, entity.moveScriptID) )
	return 0

def setPosMove_moveFightDisperse( entity, selectMovePos, selectStyle):
	"""
	"""
	entity.position = selectMovePos
	return 0

MOVE_FUN_DICT[MoveTestType.SetPos] = {}
MOVE_FUN_DICT[MoveTestType.SetPos][csdefine.MOVE_TYPE_STOP] = moveStop
MOVE_FUN_DICT[MoveTestType.SetPos][csdefine.MOVE_TYPE_NAVIGATE_POINT] = setPosMove_moveNavigatePoint
MOVE_FUN_DICT[MoveTestType.SetPos][csdefine.MOVE_TYPE_FIGHT_DISPERSE] = setPosMove_moveFightDisperse