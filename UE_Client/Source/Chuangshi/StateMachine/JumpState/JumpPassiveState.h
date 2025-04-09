#pragma once

#include "JumpBaseState.h"

/*
* 文件名称：JumpPassiveState.h
* 功能说明：被动跳跃状态
* 文件作者：ranyuan
* 目前维护：ranyuan
* 创建时间：2019-07-30
*/

class JumpPassiveState : public JumpBaseState
{
public:
	JumpPassiveState();
	virtual ~JumpPassiveState();
	virtual void Enter()override;///< 刚进入时调用
	virtual void Exit()override;///< 离开时调用
};

