
#include "EffectStateDizzy.h"

#include "GameData/GameDeFine.h"
#include "GameData/CharacterData.h"

#include "Actor/ServerCharacter.h"
#include "Actor/Player/PlayerCharacter.h"

EffectStateDizzy::EffectStateDizzy()
{
}

EffectStateDizzy::~EffectStateDizzy()
{
}

void EffectStateDizzy::Add(AActor * _Actor)
{
	EffectStateBase::Add(_Actor);
	AServerCharacter* ServerCharacter = (AServerCharacter*)_Actor;
	if (ServerCharacter)
	{
		ServerCharacter->OnEnterEffectState(EFFECT_STATE::EFFECT_STATE_DIZZY);
	}
}

void EffectStateDizzy::Del(AActor * _Actor)
{
	EffectStateBase::Del(_Actor);
	AServerCharacter* ServerCharacter = (AServerCharacter*)_Actor;
	if (ServerCharacter)
	{
		ServerCharacter->OnExitEffectState(EFFECT_STATE::EFFECT_STATE_DIZZY);
	}
}
