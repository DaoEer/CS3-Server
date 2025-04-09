// Fill out your copyright notice in the Description page of Project Settings.


#include "ItemUseAssist.h"
#include "Util/ConvertUtil.h"

FString UItemUseAssist::GetModelAssist()
{
	return Param1;
}

float UItemUseAssist::GetModelAssistOffsetH()
{
	return FSTRING_TO_FLOAT(Param3);
}

int32 UItemUseAssist::UseQuery(AServerCharacter* player)
{
	if (!Param2.IsEmpty())
	{
		const FString SpaceScriptID = UGolbalBPFunctionLibrary::GetSpaceData(FString(TEXT("SPACE_SCRIPT_ID")));
		if (Param2.Contains("|"))
		{
			TArray<FString> tempArr = UGolbalBPFunctionLibrary::SplitString(Param2);
			if (!tempArr.Contains(SpaceScriptID))
			{
				return 5311;
			}
		}
		else if (!Param2.Equals(SpaceScriptID))
		{
			return 5311;
		}
		
		
	}
	
	return UItemUse::UseQuery(player);
}

FRotator UItemUseAssist::GetModelRotationAssist(const AServerCharacter * Owner)
{
	if (IsValid(Owner))
	{
		return Owner->GetActorRotation();
	}
	return FRotator::ZeroRotator;
}

bool UItemUseAssist::CheckModelAssistValid(const FVector & Pos)
{
	return true;
}

void UItemUseAssist::UseItemToPosition()
{
	USkillInterface* skillInterface = UGolbalBPFunctionLibrary::GetCS3PlayerEntity() ? UGolbalBPFunctionLibrary::GetCS3PlayerEntity()->Interface_Cache.SkillInterface : nullptr;

	if (skillInterface)
	{
		skillInterface->UsePositionItemExt(UID, SkillID);
	}
}
