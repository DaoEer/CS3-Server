#include "SkillClientCharge.h"
#include "Util/ConvertUtil.h"
#include "Util/CS3Debug.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Interface/GameObjectInterface.h"
#include "Interface/Monster/CSkillInterface.h"
#include "CS3Base/GameObject.h"
#include "Entity/Monster/CMonster.h"
#include "Actor/Monster/MonsterCharacter.h"
#include "MonsterAI/MonsterAIController.h"

USkillClientCharge::USkillClientCharge()
{
}

USkillClientCharge::~USkillClientCharge()
{
}

void USkillClientCharge::init(FString SkillId, const FSKILL_TABLE_DATA * dictDat)
{
	UCombatSkillClient::init(SkillId, dictDat);
	if (dictDat->Param1 != "")
	{
		casterMoveSpeed = FSTRING_TO_FLOAT(dictDat->Param1) > 0.0 ? FSTRING_TO_FLOAT(dictDat->Param1) : 0.0;
	}
	if (dictDat->Param2 != "")
	{
		casterMoveDistance = FSTRING_TO_FLOAT(dictDat->Param2) > 0.0 ? FSTRING_TO_FLOAT(dictDat->Param2) * 100 : 0.0;
	}
}

void USkillClientCharge::cast(CS3Entity * caster, USkillTargetObjImpl * target)
{
	UCombatSkillClient::cast(caster, target);
	FVector direction = FVector(0.0, 0.0, 0.0);
	bool ischangeDirection = false;
	float yaw = caster->Direction().Z * PI / 180;
	FVector targetPos = target->getObjectPosition();
	FVector dir = targetPos - caster->Position();
	float z = FMath::Atan2(dir.Y, dir.X);
	if (casterMoveSpeed > 0.0)
	{

		if (getTargetType() != ENUM_CAST_TARGET_TYPE::TargetNothing)
		{
			if (FVector::Dist2D(caster->Position(), targetPos) > 10.0)
			{
				direction = FVector(0.0, 0.0, z);
				yaw = z;
				ischangeDirection = true;
			}
		}
		FVector dstPos = FVector(caster->Position().X + casterMoveDistance * FMath::Cos(yaw), caster->Position().Y + casterMoveDistance * FMath::Sin(yaw), caster->Position().Z + dir.Z *(casterMoveDistance/100));
		
		
		//临时修改一下CMonster冲锋处理
		UGameObjectInterface * Interface = ((GameObject*)caster)->Interface_Cache.GameObjectInterface;
		if (IsValid(Interface) && Interface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_MONSTER_CTRL_BY_CLIENT))
		{
			AMonsterCharacter* MCharacter = Cast<AMonsterCharacter>(caster->Actor());
			if (IsValid(MCharacter))
			{
				AMonsterAIController* MAIController = Cast<AMonsterAIController>(MCharacter->GetController());
				if (IsValid(MAIController))
				{
					MAIController->MoveCharge(dstPos, casterMoveSpeed * 100);
				}
			}			
		}
		else 
		{
			//原逻辑
			UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), caster->ID()));
			if (IsValid(CSkillInterface))
			{
				CSkillInterface->CSkillClientCharge(dstPos, direction, casterMoveSpeed, ischangeDirection);
			}
		}
	}
}

void USkillClientCharge::onSkillEnd(CS3Entity * caster, USkillTargetObjImpl * target, bool castResult)
{
	UCombatSkillClient::onSkillEnd(caster, target, castResult);
	UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), caster->ID()));
	if (IsValid(CSkillInterface))
	{
		CSkillInterface->CSkillStopMove(MOVETYPE::MOVETYPE_CHARGE);
	}
}
