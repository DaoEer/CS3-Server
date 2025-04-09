#pragma once

#include "ClimbLadderBaseState.h"
#include "GameData/CharacterData.h"

/*
* 文件名称：ClimbLadderExitTopState.h
* 功能说明：从顶部离开状态
* 文件作者：ranyuan
* 目前维护：ranyuan
* 创建时间：2020-03-24
*/
class ACharacter;
class ClimbLadderExitTopState : public ClimbLadderBaseState
{
public:
	ClimbLadderExitTopState();
	virtual ~ClimbLadderExitTopState();
	virtual void Enter()override;///< 刚进入时调用
	virtual void Exit()override;///< 离开时调用
};

