# -*- coding: utf-8 -*-
#
events = set()

def DEFINE(event, g = globals()):
	global events
	index = len(events) + 1
	exec("%s = %i" % (event, index), g)
	events.add(index)

# ----------------------------------------------------------
# 下列事件定义之后，可以使用 QuestEventDefine.事件名称 的方式
# 获取到；例如定义事件 DEFINE( "EVENT_MONSTER_DIE" )之后，可以
# 这样：QuestEventDefine.EVENT_MONSTER_DIE 获取
#
# 这些定义的值是没有意义的，不能在代码里使用这些值，只要使用
# 这个定义变量就可以。这样做的目的是，任何任务事件都必须在此
# 模块进行定义，才能正确触发，而不允许在其他地方随意定义任务
# 事件。
# ----------------------------------------------------------

# 怪物击杀事件
DEFINE( "EVENT_MONSTER_DIE" )

# 获取物品事件
DEFINE( "EVENT_GET_ITEM" )

# 清空物品事件
DEFINE( "EVENT_REMOVE_ITEM" )

# 物品提交事件
DEFINE( "EVENT_COMMIT_ITEM" )

#使用物品
DEFINE( "EVENT_USE_ITEM" )

# 学习技能事件
DEFINE( "EVENT_LEARN_SKILL" )

# 到达某地事件
DEFINE( "EVENT_GET_TO" )

# 达到修为层次事件
DEFINE( "EVENT_XIUWEI_LEVEL" )

# 通用事件
DEFINE( "EVENT_EVENT_TRIGGER" )

# 进入潜能副本事件
DEFINE( "EVENT_ENTER_POTENTIAL_COPY" )

# 进入传承副本事件
DEFINE( "EVENT_ENTER_CHUAN_CHENG_COPY" )

# 使用技能事件
DEFINE( "EVENT_USE_SKILL" )

# 猜大小事件
DEFINE( "EVENT_GUESS_GAME" )

# 召唤幻兽事件
DEFINE( "EVENT_CONJURE_PET" )

# 骑乘事件
DEFINE( "EVENT_MOUNT_PET" )

# 与NPC对话事件
DEFINE( "EVENT_TALK_WITH_NPC" )

# 环任务与NPC交互通用事件
DEFINE( "EVENT_HUAN_COMMON_TASK" )

#达到某等级事件
DEFINE( "EVENT_PLAYER_LEVEL" )

#答题事件
DEFINE( "EVENT_ANSWER_QUESTION" )

#建造洞府事件
DEFINE( "EVENT_BUILD_DONGFU" )

# 因使用物品而清空物品事件
DEFINE( "EVENT_REMOVE_ITEM_ON_USE" )