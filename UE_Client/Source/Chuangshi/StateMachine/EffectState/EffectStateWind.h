#pragma once

#include "EffectStateBase.h"

/*
* 文件名称：EffectStateWind.h
* 功能说明：缠绕效果
* 文件作者：Shenbing
* 目前维护：wuxiaoou
* 创建时间：2017-07-04
*/


class EffectStateWind : public EffectStateBase
{
public:
	EffectStateWind();
	virtual ~EffectStateWind();

	virtual void Add(AActor* _Actor)override;///< 刚进入时调用
	virtual void Del(AActor* _Actor)override;///< 离开时调用
};

