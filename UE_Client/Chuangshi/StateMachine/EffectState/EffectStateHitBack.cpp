
#include "EffectStateHitBack.h"
#include "GameData/CharacterData.h"

#include "Actor/Player/PlayerCharacter.h"
#include "EffectStateBase.h"
#include "GameData/GameDeFine.h"

EffectStateHitBack::EffectStateHitBack()
{
}

EffectStateHitBack::~EffectStateHitBack()
{

}

void EffectStateHitBack::Add(AActor * _Actor)
{
	EffectStateBase::Add(_Actor);
	AServerCharacter* ServerCharacter = (AServerCharacter*)_Actor;
	if (ServerCharacter)
	{
		ServerCharacter->OnEnterEffectState	(EFFECT_STATE::EFFECT_STATE_HIT_BACK);
	}
}

void EffectStateHitBack::Del(AActor * _Actor)
{
	EffectStateBase::Del(_Actor);
	AServerCharacter* ServerCharacter = (AServerCharacter*)_Actor;
	if (ServerCharacter)
	{
		ServerCharacter->OnExitEffectState(EFFECT_STATE::EFFECT_STATE_HIT_BACK);
	}
}
