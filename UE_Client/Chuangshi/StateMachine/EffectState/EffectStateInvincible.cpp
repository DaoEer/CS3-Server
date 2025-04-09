
#include "EffectStateInvincible.h"
#include "EffectStateBase.h"

EffectStateInvincible::EffectStateInvincible()
{
}

EffectStateInvincible::~EffectStateInvincible()
{
}

void EffectStateInvincible::Add(AActor * _Actor)
{
	EffectStateBase::Add(_Actor);
}

void EffectStateInvincible::Del(AActor * _Actor)
{
	EffectStateBase::Del(_Actor);
}
