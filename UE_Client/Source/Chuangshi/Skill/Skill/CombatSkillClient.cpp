#include "CombatSkillClient.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Interface/GameObjectInterface.h"
#include "Interface/SkillInterface.h"
#include "Interface/Monster/CSkillInterface.h"
#include "CS3Base/GameObject.h"

UCombatSkillClient::UCombatSkillClient()
{
}

UCombatSkillClient::~UCombatSkillClient()
{
}

void UCombatSkillClient::init(FString SkillId, const FSKILL_TABLE_DATA * dictDat)
{
	USkill::init(SkillId, dictDat);
	_isShowIntonateUI = dictDat->ShowIntonate;
	_intonateName = dictDat->IntonateName;

	TArray<FString> iconName = UGolbalBPFunctionLibrary::SplitString(dictDat->SkillName, false, TEXT("."));
	if (iconName.Num() > 1)
	{
		_iconName = iconName[iconName.Num() - 1];
	}
}

void UCombatSkillClient::onSkillBegin(CS3Entity * caster, USkillTargetObjImpl * target)
{
	UGameObjectInterface * Interface = ((GameObject*)caster)->Interface_Cache.GameObjectInterface;
	if (IsValid(Interface) && Interface->isEntityFlag(ENTITY_TYPE::ENTITY_FLAG_ROLE) && _isShowIntonateUI)
	{
		UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), caster->ID()));
		if (IsValid(CSkillInterface))
		{
			CSkillInterface->intonateSpell(getSkillTotalTime(), getID());
		}
	}

	if (IsValid(Interface) && Interface->isEntityFlag(ENTITY_TYPE::ENTITY_FLAG_MONSTER) && _isShowIntonateUI)
	{
		USkillInterface *SkillInterface = ((GameObject*)caster)->Interface_Cache.SkillInterface;
		if (IsValid(SkillInterface))
		{
			SkillInterface->OnShowIntonateBar(caster->ID(), getSkillTotalTime(), getID());
		}
	}
	USkill::onSkillBegin(caster, target);
}

void UCombatSkillClient::onSkillEnd(CS3Entity * caster, USkillTargetObjImpl * target, bool castResult)
{
	if (!caster)
	{
		return;
	}
	UGameObjectInterface * Interface = ((GameObject*)caster)->Interface_Cache.GameObjectInterface;
	if (IsValid(Interface) && Interface->isEntityFlag(ENTITY_TYPE::ENTITY_FLAG_ROLE) && _isShowIntonateUI)
	{
		UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), caster->ID()));
		if (IsValid(CSkillInterface))
		{
			CSkillInterface->intonateSpellOver();
		}
	}

	if (IsValid(Interface) && Interface->isEntityFlag(ENTITY_TYPE::ENTITY_FLAG_MONSTER) && _isShowIntonateUI)
	{
		USkillInterface *SkillInterface = ((GameObject*)caster)->Interface_Cache.SkillInterface;
		if (IsValid(SkillInterface))
		{
			SkillInterface->OnHideIntonateBar(caster->ID());
		}
	}
	USkill::onSkillEnd(caster, target, castResult);
}
