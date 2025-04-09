#pragma once

#include "EffectStateBase.h"

/*
* 文件名称：EffectStateInvincible.h
* 功能说明：无敌效果
* 文件作者：Chendongyong
* 目前维护：chengdongyong
* 创建时间：2017-06-16
*/

class EffectStateInvincible : public EffectStateBase
{
public:
	EffectStateInvincible();
	virtual ~EffectStateInvincible();

	virtual void Add(AActor* _Actor)override;///< 刚进入时调用
	virtual void Del(AActor* _Actor)override;///< 离开时调用
};

