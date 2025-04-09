#include "HoldEffect.h"
#include "Skill/SkillBase/Skill.h"

UHoldEffect::UHoldEffect()
{
}

UHoldEffect::~UHoldEffect()
{
}

void UHoldEffect::init(FHOLD_EFFECT dictDat, USkill * skill)
{
}

UHoldEffectDataType * UHoldEffect::getNewEffectData(CS3Entity * caster, CS3Entity * receiver)
{
	UHoldEffectDataType * effectData = NewObject <UHoldEffectDataType>();
	return effectData;
}

bool UHoldEffect::canEffect(CS3Entity * caster, CS3Entity * receiver)
{
	return true;
}

void UHoldEffect::onBegin(UHoldEffectDataType * effectData, CS3Entity * receiver)
{
}

void UHoldEffect::onEnd(UHoldEffectDataType * effectData, CS3Entity * receiver)
{
}

void UHoldEffect::onClientActorCreate(UHoldEffectDataType * effectData, CS3Entity * receiver)
{

}
