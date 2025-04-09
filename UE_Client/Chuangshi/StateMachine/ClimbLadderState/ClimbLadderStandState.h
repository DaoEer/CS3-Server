#pragma once

#include "ClimbLadderBaseState.h"

/*
* 文件名称：ClimbLadderStandState.h
* 功能说明：非攀爬状态，待机中
* 文件作者：ranyuan
* 目前维护：ranyuan
* 创建时间：2020-03-24
*/

class ClimbLadderStandState : public ClimbLadderBaseState
{
public:
	ClimbLadderStandState();
	virtual ~ClimbLadderStandState();
	virtual void Enter()override;///< 刚进入时调用
	virtual void Exit()override;///< 离开时调用
};

