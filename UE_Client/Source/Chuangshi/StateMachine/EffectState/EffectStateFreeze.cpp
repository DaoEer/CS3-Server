
#include "EffectStateFreeze.h"
#include "Actor/ServerCharacter.h"
#include "GameData/GameDeFine.h"



EffectStateFreeze::EffectStateFreeze()
{
}


EffectStateFreeze::~EffectStateFreeze()
{
}

void EffectStateFreeze::Add(AActor * _Actor)
{
	EffectStateBase::Add(_Actor);

	AServerCharacter* ServerCharacter = (AServerCharacter*)_Actor;
	if (ServerCharacter)
	{
		ServerCharacter->OnEnterEffectState(EFFECT_STATE::EFFECT_STATE_FREEZE);
	}
}

void EffectStateFreeze::Del(AActor * _Actor)
{
	EffectStateBase::Del(_Actor);

	AServerCharacter* ServerCharacter = (AServerCharacter*)_Actor;
	if (ServerCharacter)
	{
		ServerCharacter->OnExitEffectState(EFFECT_STATE::EFFECT_STATE_FREEZE);
	}
}
