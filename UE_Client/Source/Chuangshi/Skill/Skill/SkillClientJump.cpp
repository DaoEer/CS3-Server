#include "SkillClientJump.h"
#include "Util/ConvertUtil.h"
#include "Util/CS3Debug.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Interface/GameObjectInterface.h"
#include "Interface/Monster/CSkillInterface.h"
#include "CS3Base/GameObject.h"

USkillClientJump::USkillClientJump()
{
}

USkillClientJump::~USkillClientJump()
{

}

void USkillClientJump::init(FString SkillId, const FSKILL_TABLE_DATA * dictDat)
{
	UCombatSkillClient::init(SkillId, dictDat);
	if (dictDat->Param1 != "")
	{
		delayTime = FSTRING_TO_FLOAT(dictDat->Param1);
	}
	if (dictDat->Param2 != "")
	{
		moveTime = FSTRING_TO_FLOAT(dictDat->Param2);
	}
}

int32 USkillClientJump::useableCheck(CS3Entity * caster, USkillTargetObjImpl * target)
{
	UGameObjectInterface * Interface = ((GameObject*)caster)->Interface_Cache.GameObjectInterface;
	if (IsValid(Interface) && Interface->isEntityFlag(ENTITY_TYPE::ENTITY_FLAG_ROLE))
	{
		return (int32)SKILL_MESSAGE::SKILL_CAST_FAILED;
	}
	return UCombatSkillClient::useableCheck(caster, target);
}

void USkillClientJump::cast(CS3Entity * caster, USkillTargetObjImpl * target)
{
	UCombatSkillClient::cast(caster, target);
	FVector targetPos = target->getObjectPosition();
	FVector dir = targetPos - caster->Position();
	dir.Normalize();
	float dist = FVector::Dist(caster->Position(), targetPos);
	float moveSpeed = 0.0;
	if (moveTime > 0.0)
	{
		//转化成米/s
		moveSpeed = dist / (moveTime * 100);
	}
	FVector dstPos = caster->Position() + dir * dist;
	UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), caster->ID()));
	if (IsValid(CSkillInterface))
	{
		CSkillInterface->CSkillClientJump(dstPos, moveSpeed, delayTime);
	}
}

void USkillClientJump::onSkillEnd(CS3Entity * caster, USkillTargetObjImpl * target, bool castResult)
{
	UCombatSkillClient::onSkillEnd(caster, target, castResult);
	UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), caster->ID()));
	if (IsValid(CSkillInterface))
	{
		CSkillInterface->CSkillStopMove(MOVETYPE::MOVE_TYPE_SKILL_JUMP);
	}
}
