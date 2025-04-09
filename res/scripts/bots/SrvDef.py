# -*- coding: utf-8 -*-

#日志输出
class LogLevel:
	"""
	日志等级
	"""
	DEBUG_LOG = 1
	WARNING_LOG = 2
	ERROR_LOG = 3
	
#施法禁止标志位
ActForbidDct = {
	"ACTION_FORBID_MOVE"			: 0,
	"ACTION_FORBID_SPELL"			: 1,
	"ACTION_FORBID_USE_ITEM"		: 2,
	"ACTION_FORBID_BE_ATTACK"		: 3,
	"ACTION_FORBID_ATTACK"			: 4,
	"ACTION_FORBID_JUMP"			: 5,
	"ACTION_FORBID_WIELD"			: 6,
	"ACTION_FORBID_CHAT"			: 7,
	"ACTION_FORBID_TALK"			: 8,
	"ACTION_FORBID_TRIGGER_PASSIVE"	: 9,
	"ACTION_FORBID_BE_HIT_BACK"		: 10,
	"ACTION_FORBID_CHANGE_BODY"		: 11,
	"ACTION_FORBID_CHANGE_POSTURE"	: 12,
	"ACTION_FORBID_CONJURE_PET"		: 13,
	"ACTION_FORBID_TRANSLATE_DIRECTION"	: 14,
	"ACTION_FORBID_EMERGENCY_EXIT"	: 15,
	"ACTION_FORBID_MOUNT_PET"		: 16,
	"ACTION_FORBID_BE_CONTROL"		: 17,
	"ACTION_FORBID_NONE"			: 255,
}

EntityTypeDct = {
	0 	: "无",
	1	: "role",
	2	: "space",
	3	: "Monster",
	4	: "NPC",
	5	: "传送门",
	6	: "SpellBox",
	7	: "Trap",
	8	: "移动平台",
	9	: "Pet",
	10	: "掉落箱子",
	11	: "技能ghost受术者",
	12	: "传送石",
	13	: "管理器",
	14	: "帐号"
}