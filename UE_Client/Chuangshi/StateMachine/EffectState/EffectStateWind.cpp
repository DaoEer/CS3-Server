
#include "EffectStateWind.h"
#include "GameData/CharacterData.h"

#include "Actor/Player/PlayerCharacter.h"
#include "EffectStateBase.h"

EffectStateWind::EffectStateWind()
{

}

EffectStateWind::~EffectStateWind()
{

}

void EffectStateWind::Add(AActor* _Actor)
{
	EffectStateBase::Add(_Actor);
}

void EffectStateWind::Del(AActor* _Actor)
{
	EffectStateBase::Del(_Actor);
}
