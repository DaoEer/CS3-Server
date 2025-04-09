#pragma once

#include "JumpBaseState.h"
/*
* 文件名称：JumpTwoMoveUpState.h
* 功能说明：二段跑步起跳状态
* 文件作者：ranyuan
* 目前维护：ranyuan
* 创建时间：2019-03-29
*/

class JumpTwoMoveUpState : public JumpBaseState
{
public:
	JumpTwoMoveUpState();
	virtual ~JumpTwoMoveUpState();
	virtual void Enter()override;///< 刚进入时调用
	virtual void Exit()override;///< 离开时调用
};

