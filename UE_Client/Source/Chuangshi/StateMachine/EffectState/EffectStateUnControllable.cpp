
#include "EffectStateUnControllable.h"

#include "Actor/ServerCharacter.h"
#include "EffectStateBase.h"
#include "GameData/GameDeFine.h"

EffectStateUnControllable::EffectStateUnControllable()
{
}

EffectStateUnControllable::~EffectStateUnControllable()
{
}

void EffectStateUnControllable::Add(AActor * _Actor)
{
	EffectStateBase::Add(_Actor);

	AServerCharacter* ServerCharacter = (AServerCharacter*)_Actor;
	if (ServerCharacter)
	{
		ServerCharacter->OnEnterEffectState(EFFECT_STATE::EFFECT_STATE_UNCONTROLLABLE);
	}
}

void EffectStateUnControllable::Del(AActor * _Actor)
{
	EffectStateBase::Del(_Actor);

	AServerCharacter* ServerCharacter = (AServerCharacter*)_Actor;
	if (ServerCharacter)
	{
		//ServerCharacter->OnExitEffectState(EFFECT_STATE::EFFECT_STATE_UNCONTROLLABLE);
	}
}
