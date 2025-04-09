# -*- coding: utf-8 -*-

#########################################################
# 模块: ECBProximityConst
# 功能: 为陷阱封装类ECBProximityInterface提供常量定义
#########################################################


# addProximityExt 添加的陷阱回调id，此处 id 从 0xf000 开始
PROXIMITY_COMMON							= 0xf000	# 通用陷阱
PROXIMITY_AI_ATTACK							= 0xf001	# ai主动攻击陷阱
PROXIMITY_AI_INITIATIVE						= 0xf002	# ai主动反应陷阱
PROXIMITY_AI_ATTACK_1						= 0xf003	# ai主动攻击陷阱
PROXIMITY_AI_INITIATIVE_1					= 0xf004	# ai主动反应陷阱



# 全局Callback字典，用来从指定的ID查询回调函数
#
gcbs = {
	PROXIMITY_COMMON					: "onEnterCommonTrap|onLeaveCommonTrap",
	PROXIMITY_AI_ATTACK					: "onEnterAIAttackTrap|onLeaveAIAttackTrap",
	PROXIMITY_AI_INITIATIVE				: "onEnterAIInitiativeTrap|onLeaveAIInitiativeTrap",
	PROXIMITY_AI_ATTACK_1				: "monsterAIOnEnterAIAttackTrap|monsterAIOnLeaveAttackTrap",
	PROXIMITY_AI_INITIATIVE_1			: "monsterAIOnEnterInitiativeTrap|monsterAIOnLeaveInitiativeTrap",
}