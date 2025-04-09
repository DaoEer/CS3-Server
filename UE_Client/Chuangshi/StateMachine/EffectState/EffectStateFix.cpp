
#include "EffectStateFix.h"

EffectStateFix::EffectStateFix()
{
}

EffectStateFix::~EffectStateFix()
{
}

void EffectStateFix::Add(AActor * _Actor)
{
	EffectStateBase::Add(_Actor);
}

void EffectStateFix::Del(AActor * _Actor)
{
	EffectStateBase::Del(_Actor);
}
