#include "EffectCreateEntity.h"
#include "Util/ConvertUtil.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Interface/Monster/CSkillInterface.h"
#include "Skill/SkillBase/Skill.h"

UEffectCreateEntity::UEffectCreateEntity()
{
}

UEffectCreateEntity::~UEffectCreateEntity()
{
}

void UEffectCreateEntity::init(FHIT_EFFECT dictDat, USkill * skill)
{
	UEffectSkillBase::init(dictDat, skill);
	_scriptID = dictDat.Param1;
	if (dictDat.Param2 != "")
	{
		TArray<FString> Param2 = UGolbalBPFunctionLibrary::SplitString(dictDat.Param1, false, TEXT("|"));
		_offsetFront = FSTRING_TO_FLOAT(Param2[0]);
		if (Param2.Num() >= 2)
		{
			_offsetLeft = FSTRING_TO_FLOAT(Param2[1]);
		}
	}
}

void UEffectCreateEntity::onReceive(USkill * skill, CS3Entity * caster, CS3Entity * receiver)
{
	float yaw = receiver->Direction().Z * PI / 180;
	FVector direction = receiver->Direction();
	FVector position = receiver->Position();

	if (_offsetFront != 0.0)
	{
		position.Y += _offsetFront * FMath::Sin(yaw);
		position.X += _offsetFront * FMath::Cos(yaw);
	}
	if (_offsetLeft != 0.0)
	{
		position.Y += _offsetLeft * FMath::Sin(yaw - PI / 2);
		position.X += _offsetLeft * FMath::Cos(yaw - PI / 2);
	}

	UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), receiver->ID()));
	if (IsValid(CSkillInterface))
	{
		CSkillInterface->CSkillCreateEntityByScriptID(_scriptID, position, direction);
	}
}
