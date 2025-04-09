#pragma once

#include "JumpBaseState.h"
/*
* 文件名称：JumpStandState.h
* 功能说明：跳跃站立状态（未跳跃时）
* 文件作者：ranyuan
* 目前维护：ranyuan
* 创建时间：2019-03-29
*/

class JumpStandState : public JumpBaseState
{
public:
	JumpStandState();
	virtual ~JumpStandState();
	virtual void Enter()override;///< 刚进入时调用
	virtual void Exit()override;///< 离开时调用
};

