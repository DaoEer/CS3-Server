#include "SkillClientSing.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Util/ConvertUtil.h"
#include "Util/CS3Debug.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Interface/GameObjectInterface.h"
#include "Interface/Monster/CSkillInterface.h"
#include "Manager/MessageManager.h"
#include "Skill//SkillLoader.h"

USkillClientSing::USkillClientSing()
{

}

USkillClientSing::~USkillClientSing()
{

}

void USkillClientSing::init(FString SkillId, const FSKILL_TABLE_DATA * dictDat)
{
	UCombatSkillClient::init(SkillId, dictDat);
	if (dictDat->Param1 != "")
	{
		_endHitSkill = FSTRING_TO_INT(dictDat->Param1);
	}
}

int32 USkillClientSing::useSkill(CS3Entity * caster, USkillTargetObjImpl * target)
{
	//将吟唱技能的目标传递给触发子技能
	setSkillSingTarget(caster, target);
	//当配置里的技能目标类型和传过来的技能目标类型不符时
	target = adaptiveTarget(caster, target);
	if (target == nullptr)
	{
		return (int32)SKILL_MESSAGE::SKILL_CAST_FAILED;
	}
	int32 state = useableCheck(caster, target);
	if (state != (int32)SKILL_MESSAGE::SKILL_GO_ON)
	{
		return state;
	}
	use(caster, target);
	return (int32)SKILL_MESSAGE::SKILL_GO_ON;
}

void USkillClientSing::onSkillEnd(CS3Entity * caster, USkillTargetObjImpl * target, bool castResult)
{
	UCombatSkillClient::onSkillEnd(caster, target, castResult);
	if (!castResult)
	{
		return;
	}
	target = getSkillSingTarget(caster);
	removeSkillSingTarget(caster);
	int32 state = continueCastSkill(caster, target);

	UGameObjectInterface * Interface = Cast<UGameObjectInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("GameObjectInterface"), caster->ID()));
	if (state != (int32)SKILL_MESSAGE::SKILL_GO_ON && IsValid(Interface) && Interface->isEntityFlag(ENTITY_TYPE::ENTITY_FLAG_ROLE))
	{
		UMessageManager* MessageManager = UUECS3GameInstance::Instance->MessageManager;
		MessageManager->ShowMessage(state);
	}
}

int32 USkillClientSing::continueCastSkill(CS3Entity * caster, USkillTargetObjImpl * target)
{
	if (target == nullptr)
	{
		return (int32)SKILL_MESSAGE::SKILL_CAST_FAILED;
	}
	USkill* skill = NULL;
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->SkillLoader))
	{
		skill = UUECS3GameInstance::Instance->SkillLoader->getSkillByID(_endHitSkill);
	}
	if (skill == nullptr)
	{
		return (int32)SKILL_MESSAGE::SKILL_NOT_EXIST;
	}
	return skill->useSkill(caster, target);
}

void USkillClientSing::setSkillSingTarget(CS3Entity * caster, USkillTargetObjImpl * target)
{
	UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), caster->ID()));
	if (IsValid(CSkillInterface))
	{
		CSkillInterface->SetSkillSingTarget(_endHitSkill, target);
	}
}

USkillTargetObjImpl * USkillClientSing::getSkillSingTarget(CS3Entity * caster)
{
	UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), caster->ID()));
	if (IsValid(CSkillInterface))
	{
		return CSkillInterface->GetSkillSingTarget(_endHitSkill);
	}
	return nullptr;
}

void USkillClientSing::removeSkillSingTarget(CS3Entity * caster)
{
	UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), caster->ID()));
	if (IsValid(CSkillInterface))
	{
		CSkillInterface->RemoveSkillSingTarget(_endHitSkill);
	}
}
