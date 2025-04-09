#pragma once
#include "EffectStateBase.h"

/*
* 文件名称：EffectStateFreeze.h
* 功能说明：冻结效果
* 文件作者：xuyongqi
* 目前维护：xuyongqi
* 创建时间：2018-08-06
*/

class EffectStateFreeze : public EffectStateBase
{
public:
	EffectStateFreeze();
	virtual ~EffectStateFreeze();

	virtual void Add(AActor* _Actor)override;///< 刚进入时调用
	virtual void Del(AActor* _Actor)override;///< 离开时调用
};

