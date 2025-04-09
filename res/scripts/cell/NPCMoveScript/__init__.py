# -*- coding: utf-8 -*-

import csdefine

from NPCMoveScript import MoveStop
from NPCMoveScript import MoveNavigatePoint
from NPCMoveScript import MoveLinePoint
from NPCMoveScript import MoveChase
from NPCMoveScript import MovePatrol
from NPCMoveScript import MoveRandom
from NPCMoveScript import MoveWander
from NPCMoveScript import MoveAround
from NPCMoveScript import MoveCharge
from NPCMoveScript import MoveGoBack
from NPCMoveScript import MoveLoopRotator
from NPCMoveScript import MoveSkillChase
from NPCMoveScript import MoveHitBack
from NPCMoveScript import MoveRandomChoiceFormList
from NPCMoveScript import MoveFightDisperse
from NPCMoveScript import MoveChaseClient
from NPCMoveScript import MoveReversePatrol
from NPCMoveScript import MoveNavigatePointTest
from NPCMoveScript import MoveSoldierFollow
from NPCMoveScript import MoveSoldierRect
from NPCMoveScript import MoveSoldierCircle
from NPCMoveScript import MoveChaseOptimize
from NPCMoveScript import MoveRandomInSphere
from NPCMoveScript import MoveFlyToPoint
from NPCMoveScript import MoveSkillJump
from NPCMoveScript import MoveStopOptimize




# 普通怪物移动类型
g_moveDict = {}
g_moveDict[ csdefine.MOVE_TYPE_STOP ] = MoveStop.MoveStop(csdefine.MOVE_TYPE_STOP)
g_moveDict[ csdefine.MOVE_TYPE_NAVIGATE_POINT ] = MoveNavigatePoint.MoveNavigatePoint(csdefine.MOVE_TYPE_NAVIGATE_POINT)
g_moveDict[ csdefine.MOVE_TYPE_NAVIGATE_POINT_TEST ] = MoveNavigatePointTest.MoveNavigatePointTest(csdefine.MOVE_TYPE_NAVIGATE_POINT_TEST)
g_moveDict[ csdefine.MOVE_TYPE_MOVE_POINT ] = MoveLinePoint.MoveLinePoint(csdefine.MOVE_TYPE_MOVE_POINT)
g_moveDict[ csdefine.MOVE_TYPE_CHASE ] = MoveChase.MoveChase(csdefine.MOVE_TYPE_CHASE)
g_moveDict[ csdefine.MOVE_TYPE_PATROL ] = MovePatrol.MovePatrol(csdefine.MOVE_TYPE_PATROL)
g_moveDict[ csdefine.MOVE_TYPE_RANDOM ] = MoveRandom.MoveRandom(csdefine.MOVE_TYPE_RANDOM)
g_moveDict[ csdefine.MOVE_TYPE_WANDER ] = MoveWander.MoveWander(csdefine.MOVE_TYPE_WANDER)
g_moveDict[ csdefine.MOVE_TYPE_WALK_AROUND ] = MoveAround.MoveAround(csdefine.MOVE_TYPE_WALK_AROUND)
g_moveDict[ csdefine.MOVE_TYPE_CHARGE ] = MoveCharge.MoveCharge(csdefine.MOVE_TYPE_CHARGE)
g_moveDict[ csdefine.MOVE_TYPE_GOBACK ] = MoveGoBack.MoveGoBack( csdefine.MOVE_TYPE_GOBACK )
g_moveDict[ csdefine.MOVE_TYPE_LOOP_ROTATOR ] = MoveLoopRotator.MoveLoopRotator( csdefine.MOVE_TYPE_LOOP_ROTATOR )
g_moveDict[ csdefine.MOVE_TYPE_SKILL_CHASE ] = MoveSkillChase.MoveSkillChase(csdefine.MOVE_TYPE_SKILL_CHASE)
g_moveDict[ csdefine.MOVE_TYPE_HIT_BACK ] = MoveHitBack.MoveHitBack(csdefine.MOVE_TYPE_HIT_BACK)
g_moveDict[ csdefine.MOVE_TYPE_RANDOM_CHOICE_FORM_LIST ] = MoveRandomChoiceFormList.MoveRandomChoiceFormList(csdefine.MOVE_TYPE_RANDOM_CHOICE_FORM_LIST)
g_moveDict[ csdefine.MOVE_TYPE_FIGHT_DISPERSE ] = MoveFightDisperse.MoveFightDisperse(csdefine.MOVE_TYPE_FIGHT_DISPERSE)
g_moveDict[ csdefine.MOVE_TYPE_CHASE_CLIENT ] = MoveChaseClient.MoveChaseClient(csdefine.MOVE_TYPE_CHASE_CLIENT)
g_moveDict[ csdefine.MOVE_TYPE_REVERSE_PATROL ] = MoveReversePatrol.MoveReversePatrol(csdefine.MOVE_TYPE_REVERSE_PATROL)
g_moveDict[ csdefine.MOVE_TYPE_SOLDIER_FOLLOW ] = MoveSoldierFollow.MoveSoldierFollow(csdefine.MOVE_TYPE_SOLDIER_FOLLOW)
g_moveDict[ csdefine.MOVE_TYPE_SOLDIER_RECT ] = MoveSoldierRect.MoveSoldierRect(csdefine.MOVE_TYPE_SOLDIER_RECT)
g_moveDict[ csdefine.MOVE_TYPE_SOLDIER_CIRCLE ] = MoveSoldierCircle.MoveSoldierCircle(csdefine.MOVE_TYPE_SOLDIER_CIRCLE)
g_moveDict[ csdefine.MOVE_TYPE_RANDOM_IN_SPHERE ] = MoveRandomInSphere.MoveRandomInSphere(csdefine.MOVE_TYPE_RANDOM_IN_SPHERE)
g_moveDict[ csdefine.MOVE_TYPE_FLY_TO_POINT ] = MoveFlyToPoint.MoveFlyToPoint(csdefine.MOVE_TYPE_FLY_TO_POINT)
g_moveDict[ csdefine.MOVE_TYPE_SKILL_JUMP ] = MoveSkillJump.MoveSkillJump(csdefine.MOVE_TYPE_SKILL_JUMP)


#优化型怪物移动类型
g_moveDict_optimize = {}
g_moveDict_optimize[ csdefine.MOVE_TYPE_STOP ] = MoveStopOptimize.MoveStopOptimize(csdefine.MOVE_TYPE_STOP)
g_moveDict_optimize[ csdefine.MOVE_TYPE_NAVIGATE_POINT ] = MoveNavigatePoint.MoveNavigatePoint(csdefine.MOVE_TYPE_NAVIGATE_POINT)
g_moveDict_optimize[ csdefine.MOVE_TYPE_NAVIGATE_POINT_TEST ] = MoveNavigatePointTest.MoveNavigatePointTest(csdefine.MOVE_TYPE_NAVIGATE_POINT_TEST)
g_moveDict_optimize[ csdefine.MOVE_TYPE_MOVE_POINT ] = MoveLinePoint.MoveLinePoint(csdefine.MOVE_TYPE_MOVE_POINT)
g_moveDict_optimize[ csdefine.MOVE_TYPE_CHASE ] = MoveChaseOptimize.MoveChaseOptimize(csdefine.MOVE_TYPE_CHASE)
g_moveDict_optimize[ csdefine.MOVE_TYPE_PATROL ] = MovePatrol.MovePatrol(csdefine.MOVE_TYPE_PATROL)
g_moveDict_optimize[ csdefine.MOVE_TYPE_RANDOM ] = MoveRandom.MoveRandom(csdefine.MOVE_TYPE_RANDOM)
g_moveDict_optimize[ csdefine.MOVE_TYPE_WANDER ] = MoveWander.MoveWander(csdefine.MOVE_TYPE_WANDER)
g_moveDict_optimize[ csdefine.MOVE_TYPE_WALK_AROUND ] = MoveAround.MoveAround(csdefine.MOVE_TYPE_WALK_AROUND)
g_moveDict_optimize[ csdefine.MOVE_TYPE_CHARGE ] = MoveCharge.MoveCharge(csdefine.MOVE_TYPE_CHARGE)
g_moveDict_optimize[ csdefine.MOVE_TYPE_GOBACK ] = MoveGoBack.MoveGoBack( csdefine.MOVE_TYPE_GOBACK )
g_moveDict_optimize[ csdefine.MOVE_TYPE_LOOP_ROTATOR ] = MoveLoopRotator.MoveLoopRotator( csdefine.MOVE_TYPE_LOOP_ROTATOR )
g_moveDict_optimize[ csdefine.MOVE_TYPE_SKILL_CHASE ] = MoveSkillChase.MoveSkillChase(csdefine.MOVE_TYPE_SKILL_CHASE)
g_moveDict_optimize[ csdefine.MOVE_TYPE_HIT_BACK ] = MoveHitBack.MoveHitBack(csdefine.MOVE_TYPE_HIT_BACK)
g_moveDict_optimize[ csdefine.MOVE_TYPE_RANDOM_CHOICE_FORM_LIST ] = MoveRandomChoiceFormList.MoveRandomChoiceFormList(csdefine.MOVE_TYPE_RANDOM_CHOICE_FORM_LIST)
g_moveDict_optimize[ csdefine.MOVE_TYPE_FIGHT_DISPERSE ] = MoveFightDisperse.MoveFightDisperse(csdefine.MOVE_TYPE_FIGHT_DISPERSE)
g_moveDict_optimize[ csdefine.MOVE_TYPE_CHASE_CLIENT ] = MoveChaseClient.MoveChaseClient(csdefine.MOVE_TYPE_CHASE_CLIENT)
g_moveDict_optimize[ csdefine.MOVE_TYPE_REVERSE_PATROL ] = MoveReversePatrol.MoveReversePatrol(csdefine.MOVE_TYPE_REVERSE_PATROL)
g_moveDict_optimize[ csdefine.MOVE_TYPE_SOLDIER_FOLLOW ] = MoveSoldierFollow.MoveSoldierFollow(csdefine.MOVE_TYPE_SOLDIER_FOLLOW)
g_moveDict_optimize[ csdefine.MOVE_TYPE_SOLDIER_RECT ] = MoveSoldierRect.MoveSoldierRect(csdefine.MOVE_TYPE_SOLDIER_RECT)
g_moveDict_optimize[ csdefine.MOVE_TYPE_SOLDIER_CIRCLE ] = MoveSoldierCircle.MoveSoldierCircle(csdefine.MOVE_TYPE_SOLDIER_CIRCLE)
g_moveDict[ csdefine.MOVE_TYPE_RANDOM_IN_SPHERE ] = MoveRandomInSphere.MoveRandomInSphere(csdefine.MOVE_TYPE_RANDOM_IN_SPHERE)
g_moveDict[ csdefine.MOVE_TYPE_FLY_TO_POINT ] = MoveFlyToPoint.MoveFlyToPoint(csdefine.MOVE_TYPE_FLY_TO_POINT)
g_moveDict[ csdefine.MOVE_TYPE_SKILL_JUMP ] = MoveSkillJump.MoveSkillJump(csdefine.MOVE_TYPE_SKILL_JUMP)