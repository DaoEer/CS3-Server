#pragma once
#include "Entity.h" 

/*
* 文件名称：JumpBaseState.h
* 功能说明：人物跳跃状态基类
* 文件作者：ranyuan
* 目前维护：ranyuan
* 创建时间：2018-12-28
*/
class URoleStateMachine;


class JumpBaseState
{
public:
	JumpBaseState();
	virtual ~JumpBaseState();

	virtual void Enter();///< 刚进入时调用
	virtual void Exit();///< 离开时调用
	virtual void PlayJumpAction(const int32& ContinuousId,
		const TArray<FString>& JumpActionID, const TArray<FString>& BeginTime);

	/**
	*创建状态
	*
	*@param TableData ，表格数据（FSTATE_DATA*）
	*@param StateMachine ，角色状态机（URoleStateMachine*）
	*@param RoleEntity，（Entity*）
	*
	*@return 无
	*/
	void CreateState(URoleStateMachine* StateMachine, KBEngine::Entity* RoleEntity);
protected:
	URoleStateMachine* CurrentStateMachine;///< 当前状态机
	KBEngine::Entity* CurrentEntity;///<当前Entity
};
