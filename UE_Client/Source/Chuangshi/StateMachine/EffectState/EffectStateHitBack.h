#pragma once

#include "EffectStateBase.h"

/*
* 文件名称：EffectStateHitBack.h
* 功能说明：击退效果（击退的动作表现，不在此处实现！因为击退有距离等参数）
* 文件作者：Chendongyong
* 目前维护：chengdongyong
* 创建时间：2017-06-16
*/

class EffectStateHitBack : public EffectStateBase
{
public:
	EffectStateHitBack();
	virtual ~EffectStateHitBack();

	virtual void Add(AActor* _Actor)override;///< 刚进入时调用
	virtual void Del(AActor* _Actor)override;///< 离开时调用
};

