#pragma once
#include "EffectStateBase.h"

class EffectStateStory :public EffectStateBase
{
public:
	EffectStateStory();
	virtual ~EffectStateStory();
	virtual void Add(AActor* _Actor)override;///< 刚进入时调用
	virtual void Del(AActor* _Actor)override;///< 离开时调用
};

