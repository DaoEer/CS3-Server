#pragma once

#include "EffectStateBase.h"

/*
* 文件名称：EffectStateHide.h
* 功能说明：隐身效果
* 文件作者：Chendongyong
* 目前维护：chengdongyong
* 创建时间：2019-12-3
*/

class EffectStateHide : public EffectStateBase
{
public:
	EffectStateHide();
	virtual ~EffectStateHide();

	virtual void Add(AActor* _Actor)override;///< 刚进入时调用
	virtual void Del(AActor* _Actor)override;///< 离开时调用
};

