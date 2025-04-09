#pragma once
#include "EffectStateBase.h"

/*
* 文件名称：EffectStateUnyielding.h
* 功能说明：不屈效果
* 文件作者：xuyongqi
* 目前维护：xuyongqi
* 创建时间：2018-08-06
*/

class EffectStateUnyielding : public EffectStateBase
{
public:
	EffectStateUnyielding();
	virtual ~EffectStateUnyielding();

	virtual void Add(AActor* _Actor)override;///< 刚进入时调用
	virtual void Del(AActor* _Actor)override;///< 离开时调用
};

