# -*- coding: utf-8 -*-
#用于定义一些调试相关的内容

#日志输出
class LogLevel:
	"""
	日志等级
	"""
	DEBUG_LOG = 1
	INFO_LOG = 2
	WARNING_LOG = 3
	ERROR_LOG = 4

LogDct = {
	"DEBUG"		: LogLevel.DEBUG_LOG,	
	"INFO"		: LogLevel.INFO_LOG,	
	"WARNING"	: LogLevel.WARNING_LOG,	
	"ERROR"		: LogLevel.ERROR_LOG,		
}

#移动测试
class MoveTestType:
	"""
	移动测试类型
	"""
	Default = 0	#默认(目前移动方式)
	KBEMove = 1	#kbe原生移动接口	
	SetPos = 2	#直接设置坐标
	StopMove = 3#停止移动

#怪物移动测试定义
MoveTestTypeDct = {
	"Default"		: MoveTestType.Default,
	"KBEMove"		: MoveTestType.KBEMove,	
	"SetPos"		: MoveTestType.SetPos,	
	"StopMove"		: MoveTestType.StopMove,
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