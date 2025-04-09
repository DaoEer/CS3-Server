
#include "EffectStateConfusion.h"
#include "Actor/ServerCharacter.h"
#include "EffectStateBase.h"

EffectStateConfusion::EffectStateConfusion()
{
}

EffectStateConfusion::~EffectStateConfusion()
{
}

void EffectStateConfusion::Add(AActor * _Actor)
{
	EffectStateBase::Add(_Actor);
	AServerCharacter* PlayerActor = Cast<AServerCharacter>(_Actor);
	if (IsValid(PlayerActor) && PlayerActor->ActorIsPlayer())
	{

	}
}

void EffectStateConfusion::Del(AActor * _Actor)
{
	EffectStateBase::Del(_Actor);
}
