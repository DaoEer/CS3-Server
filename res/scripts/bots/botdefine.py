# -*- coding: utf-8 -*-


#------默认值------

DEFAULT_SKILL_ID 			= 123456001
DEFAULT_SPACE 			= "L_KLZ"
DEFAULT_POSITON 		= (-2128.000000, 160.000000, -1803.000000)
DEFAULT_MONSTER 		= "200001"
USER_DATA_MOVETO		= 1002

#------entity状态------
ENTITY_STATE_PEAD						= 0				# 未决状态
ENTITY_STATE_FREE						= 1				# 普通状态
ENTITY_STATE_FIGHT						= 3				# 战斗状态
ENTITY_STATE_DEAD						= 4				# 死亡状态
ENTITY_STATE_RESET						= 5				# 重置状态（怪物特有）
ENTITY_STATE_SHOW						= 6				# 表演状态（怪物特有）
ENTITY_STATE_MAX						= 7				# 状态最大值，高于此值的为无效状态
