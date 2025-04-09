#pragma once

#include "JumpBaseState.h"

/*
* 文件名称：JumpMoveLandState.h
* 功能说明：跑步着陆
* 文件作者：ranyuan
* 目前维护：ranyuan
* 创建时间：2019-03-29
*/

class JumpMoveLandState : public JumpBaseState
{
public:
	JumpMoveLandState();
	virtual ~JumpMoveLandState();
	virtual void Enter()override;///< 刚进入时调用
	virtual void Exit()override;///< 离开时调用
};

