#pragma once

#include "JumpBaseState.h"
/*
* 文件名称：JumpStandLandState.h
* 功能说明：原地着陆
* 文件作者：ranyuan
* 目前维护：ranyuan
* 创建时间：2019-03-29
*/

class JumpStandLandState : public JumpBaseState
{
public:
	JumpStandLandState();
	virtual ~JumpStandLandState();
	virtual void Enter()override;///< 刚进入时调用
	virtual void Exit()override;///< 离开时调用
};

