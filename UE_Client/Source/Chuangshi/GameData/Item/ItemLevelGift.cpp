// Fill out your copyright notice in the Description page of Project Settings.


#include "ItemLevelGift.h"
#include "GameDevelop/CS3GameInstance.h"
#include "GameData/MessageID.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Actor/ServerCharacter.h"

void UItemLevelGift::InitDynamicDataForJson(FString jsonStr)
{
	UJsonFieldData* temp = UJsonFieldData::Create(this);
	UJsonFieldData* returnvalue = temp->FromString(jsonStr);
	UJsonFieldData* root = returnvalue->GetObject(TEXT("ROOT"));
	Describe = root->GetString(TEXT("discribe"));
}


int32 UItemLevelGift::Use(AServerCharacter* player)
{
	int32 useresult = UseQuery(player);
	if (useresult == (UUECS3GameInstance::Instance->GMessageID->ITEM_USE_GO_ON_MSG))		//条件检测通过
	{
		if (!IsUseItemToPosition())
		{
			NotityUseItemToCell();
		}
		else
		{
			UseItemToPosition();
		}
	}
	else if(useresult == (UUECS3GameInstance::Instance->GMessageID->ITEM_USE_LV_LESS_MSG))
	{
		if (!IsUseItemToPosition())
		{
			NotityUseItemToCell();
		}
		else
		{
			UseItemToPosition();
		}
	}
	else
	{
		UGolbalBPFunctionLibrary::StatusMessage(useresult, TEXT(""));
	}
	return useresult;
}