#pragma once

#include "ClimbLadderBaseState.h"

/*
* 文件名称：ClimbLadderMoveState.h
* 功能说明：攀爬状态
* 文件作者：ranyuan
* 目前维护：ranyuan
* 创建时间：2020-03-24
*/

class ClimbLadderMoveState : public ClimbLadderBaseState
{
public:
	ClimbLadderMoveState();
	virtual ~ClimbLadderMoveState();
	virtual void Enter()override;///< 刚进入时调用
	virtual void Exit()override;///< 离开时调用
};

