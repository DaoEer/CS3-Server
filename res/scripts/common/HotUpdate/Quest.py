# -*- coding: utf-8 -*-

#-----------------------------------------------------------------------------------
# 任务脚本热更新
#-----------------------------------------------------------------------------------
import HotUpdate
import sys
import ConfigObject.Quest.QuestRequirements
import ConfigObject.Quest.QuestFunctions
import ConfigObject.Quest.QuestRewards
import ConfigObject.Quest.QuestTasks
from imp import reload
def HotUpdateQuest( restr = "" ):
	"""
	quest热更新
	@type        restr		：STRING
	模块名称    具体格式为"mod1.mod2.modN:className"
	"""
	compons = restr.split( ":" )							# 拆分路径和模块
	assert len( compons ) > 0, "wrong module name!"			# 排除空路径
	mod = compons[0]										#热更新模块名
	str = compons[-1]										#热更新的类名
	module = sys.modules[mod]
	new = reload( module )
	if str:
		new = getattr( new, str )
	return new

def HotUpdateQuestRequire( RequireStr = "" ):
	"""
	任务条件热更新
	@param RequireStr :		热更新的任务条件类名
	@type RequireStr  :		String 
	@return  : RequireStr不为空字符串，则返回RequireStr的实例
	"""
	return HotUpdate.reloadByModule( ConfigObject.Quest.QuestRequirements, RequireStr )
	
def HotUpdateQuestFunc( FuncStr = "" ):
	"""
	任务行为热更新
	@param FuncStr :	热更新的任务行为类名
	@type FuncStr  :	String
	@return  : FuncStr不为空字符串，则返回FuncStr的实例
	"""
	return HotUpdate.reloadByModule( ConfigObject.Quest.QuestFunctions, FuncStr )
	
def HotUpdateQuestReWards( RewardStr = "" ):
	"""
	任务奖励热更新
	@param RewardStr :	热更新的任务奖励类名
	@type RewardStr  :	String
	@return  : RewardStr不为空字符串，则返回RewardStr的实例
	"""
	return HotUpdate.reloadByModule( ConfigObject.Quest.QuestRewards, RewardStr )
	
def HotUpdateQuestTasks( TaskStr = "" ):
	"""
	任务目标热更新
	@param TaskStr :	热更新的任务目标类名
	@type TaskStr  :	String
	@return  : TaskStr不为空字符串，则返回TaskStr的实例
	"""
	return HotUpdate.reloadByModule( ConfigObject.Quest.QuestTasks, TaskStr )
