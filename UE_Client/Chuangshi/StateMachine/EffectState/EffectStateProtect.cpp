
#include "EffectStateProtect.h"
#include "EffectStateBase.h"



EffectStateProtect::EffectStateProtect()
{
}


EffectStateProtect::~EffectStateProtect()
{
}

void EffectStateProtect::Add(AActor* _Actor)
{
	EffectStateBase::Add(_Actor);
}

void EffectStateProtect::Del(AActor* _Actor)
{
	EffectStateBase::Del(_Actor);
}
