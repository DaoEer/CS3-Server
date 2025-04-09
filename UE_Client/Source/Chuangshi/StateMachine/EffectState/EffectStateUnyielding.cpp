
#include "EffectStateUnyielding.h"

#include "EffectStateBase.h"



EffectStateUnyielding::EffectStateUnyielding()
{
}


EffectStateUnyielding::~EffectStateUnyielding()
{
}
void EffectStateUnyielding::Add(AActor * _Actor)
{
	EffectStateBase::Add(_Actor);
}

void EffectStateUnyielding::Del(AActor * _Actor)
{
	EffectStateBase::Del(_Actor);
}