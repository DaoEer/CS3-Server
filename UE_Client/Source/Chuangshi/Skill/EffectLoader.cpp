#include "EffectLoader.h"
#include "Chuangshi.h"
#include "Skill/Effect/EffectDamage.h"
#include "Skill/Effect/EffectAction.h"
#include "Skill/Effect/EffectAddBuff.h"
#include "Skill/Effect/EffectAddHP.h"
#include "Skill/Effect/EffectCreateEntity.h"
#include "Skill/Effect/EffectNormalDamage.h"
#include "Skill/Effect/EffectClientNormalDamage1.h"
#include "Skill/Effect/EffectRemoveBuff.h"
#include "Skill/Effect/HoldEffect/HoldEffectBindDisplayObject.h"
#include "Skill/Effect/HoldEffect/HoldEffectAddActCounter.h"
#include "Skill/Effect/HoldEffect/HoldEffectAddAttr.h"
#include "Skill/Effect/HoldEffect/HoldEffectConfusion.h"
#include "Skill/Effect/HoldEffect/HoldEffectDizzy.h"
#include "Skill/Effect/HoldEffect/HoldEffectFix.h"
#include "Skill/Effect/HoldEffect/HoldEffectInvincible.h"
#include "Skill/Effect/HoldEffect/HoldEffectPlayEffect.h"
#include "Skill/Effect/HoldEffect/HoldEffectUncontrollable.h"


UEffectLoader::UEffectLoader()
{
}

UEffectLoader::~UEffectLoader()
{
}

UEffectLoader * UEffectLoader::GetInstance()
{
	cs3_checkNoReentry();
	return NewObject<UEffectLoader>();
}

UEffectSkillBase * UEffectLoader::createEffect(FHIT_EFFECT effectData, USkill * skill)
{
	UEffectSkillBase * effectInstance = nullptr;
	if (effectData.HitEffectType == ENUM_HIT_EFFECT_TYPE::EffectAction)
	{
		UEffectAction* Temp = NewObject<UEffectAction>();
		Temp->init(effectData, skill);
		effectInstance = (UEffectSkillBase*)Temp;
	}
	else if (effectData.HitEffectType == ENUM_HIT_EFFECT_TYPE::EffectNormalDamage)
	{
		UEffectNormalDamage* Temp = NewObject<UEffectNormalDamage>();
		Temp->init(effectData, skill);
		effectInstance = (UEffectSkillBase*)Temp;
	}
	else if (effectData.HitEffectType == ENUM_HIT_EFFECT_TYPE::EffectClientNormalDamage1)
	{
		UEffectClientNormalDamage1* Temp = NewObject<UEffectClientNormalDamage1>();
		Temp->init(effectData, skill);
		effectInstance = (UEffectSkillBase*)Temp;
	}
	else if (effectData.HitEffectType == ENUM_HIT_EFFECT_TYPE::EffectDamage)
	{
		UEffectDamage* Temp = NewObject<UEffectDamage>();
		Temp->init(effectData, skill);
		effectInstance = (UEffectSkillBase*)Temp;
	}
	else if(effectData.HitEffectType == ENUM_HIT_EFFECT_TYPE::EffectAddBuff)
	{
		UEffectAddBuff* Temp = NewObject<UEffectAddBuff>();
		Temp->init(effectData, skill);
		effectInstance = (UEffectSkillBase*)Temp;
	}
	else if (effectData.HitEffectType == ENUM_HIT_EFFECT_TYPE::EffectAddHP)
	{
		UEffectAddHP* Temp = NewObject<UEffectAddHP>();
		Temp->init(effectData, skill);
		effectInstance = (UEffectSkillBase*)Temp;
	}
	else if (effectData.HitEffectType == ENUM_HIT_EFFECT_TYPE::EffectCreateEntity)
	{
		UEffectCreateEntity* Temp = NewObject<UEffectCreateEntity>();
		Temp->init(effectData, skill);
		effectInstance = (UEffectSkillBase*)Temp;
	}
	else if (effectData.HitEffectType == ENUM_HIT_EFFECT_TYPE::EffectRemoveBuff)
	{
		UEffectRemoveBuff* Temp = NewObject<UEffectRemoveBuff>();
		Temp->init(effectData, skill);
		effectInstance = (UEffectSkillBase*)Temp;
	}
	return effectInstance;
}

UHoldEffect * UEffectLoader::createHoldEffect(FHOLD_EFFECT effectData, USkill * skill)
{
	UHoldEffect * HoldEffectInstance = nullptr;
	if (effectData.HitEffectType == ENUM_HOLD_EFFECT_TYPE::HoldEffectBindDisplayObject)
	{
		UHoldEffectBindDisplayObject* Temp = NewObject<UHoldEffectBindDisplayObject>();
		Temp->init(effectData, skill);
		HoldEffectInstance = (UHoldEffect*)Temp;
	}
	else if (effectData.HitEffectType == ENUM_HOLD_EFFECT_TYPE::HoldEffectAddActCounter)
	{
		UHoldEffectAddActCounter* Temp = NewObject<UHoldEffectAddActCounter>();
		Temp->init(effectData, skill);
		HoldEffectInstance = (UHoldEffect*)Temp;
	}
	else if (effectData.HitEffectType == ENUM_HOLD_EFFECT_TYPE::HoldEffectAddAttr)
	{
		UHoldEffectAddAttr* Temp = NewObject<UHoldEffectAddAttr>();
		Temp->init(effectData, skill);
		HoldEffectInstance = (UHoldEffect*)Temp;
	}
	else if (effectData.HitEffectType == ENUM_HOLD_EFFECT_TYPE::HoldEffectConfusion)
	{
		UHoldEffectConfusion* Temp = NewObject<UHoldEffectConfusion>();
		Temp->init(effectData, skill);
		HoldEffectInstance = (UHoldEffect*)Temp;
	}
	else if (effectData.HitEffectType == ENUM_HOLD_EFFECT_TYPE::HoldEffectDizzy)
	{
		UHoldEffectDizzy* Temp = NewObject<UHoldEffectDizzy>();
		Temp->init(effectData, skill);
		HoldEffectInstance = (UHoldEffect*)Temp;
	}
	else if (effectData.HitEffectType == ENUM_HOLD_EFFECT_TYPE::HoldEffectFix)
	{
		UHoldEffectFix* Temp = NewObject<UHoldEffectFix>();
		Temp->init(effectData, skill);
		HoldEffectInstance = (UHoldEffect*)Temp;
	}
	else if (effectData.HitEffectType == ENUM_HOLD_EFFECT_TYPE::HoldEffectInvincible)
	{
		UHoldEffectInvincible* Temp = NewObject<UHoldEffectInvincible>();
		Temp->init(effectData, skill);
		HoldEffectInstance = (UHoldEffect*)Temp;
	}
	else if (effectData.HitEffectType == ENUM_HOLD_EFFECT_TYPE::HoldEffectPlayEffect)
	{
		UHoldEffectPlayEffect* Temp = NewObject<UHoldEffectPlayEffect>();
		Temp->init(effectData, skill);
		HoldEffectInstance = (UHoldEffect*)Temp;
	}
	else if (effectData.HitEffectType == ENUM_HOLD_EFFECT_TYPE::HoldEffectUncontrollable)
	{
		UHoldEffectUncontrollable* Temp = NewObject<UHoldEffectUncontrollable>();
		Temp->init(effectData, skill);
		HoldEffectInstance = (UHoldEffect*)Temp;
	}
	return HoldEffectInstance;
}
