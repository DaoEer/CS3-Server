// Fill out your copyright notice in the Description page of Project Settings.

#include "LocalKitbagData.h"
#include "LocalTongSettingData.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Manager/LocalDataSaveManager.h"
#include "Util/CS3Debug.h"
CONTROL_COMPILE_OPTIMIZE_START

ULocalKitbagData::ULocalKitbagData()
{
	if (!IsValid(UUECS3GameInstance::Instance)) return;
	int32 PlayerId = UGolbalBPFunctionLibrary::GetPlayerID();
	FString PlayerName = UGolbalBPFunctionLibrary::GetFStringPropertyValue(PlayerId, TEXT("playerName"));
	FileName = "LocalKitbagData_" + PlayerName;
}

void ULocalKitbagData::AddLocalItem(UItemBase* Item)
{
	if (KitbagData.Contains(Item->UID)) return;

	FLOCAL_ITEM_DATA localItem;
	localItem.ItemUID = Item->UID;
	localItem.ItemID = Item->ItemID;
	/// 白色品质，不显示show样式
	localItem.isShowNew = Item->Quality > int(QUALITY::QUALITY_WHITE);
	localItem.CreateTime = FDateTime::Now();
	KitbagData.Add(Item->UID, localItem);
	UGolbalBPFunctionLibrary::GameInstance()->LocalDataSaveManager->SaveLocalItemDataFile();
}

void ULocalKitbagData::RemoveLocalItem(const FString& ItemUID)
{
	if (KitbagData.Contains(ItemUID))
	{
		KitbagData.Remove(ItemUID);
		UGolbalBPFunctionLibrary::GameInstance()->LocalDataSaveManager->SaveLocalItemDataFile();
	}
}

bool ULocalKitbagData::IsShowNewTip(const FString& ItemUID)
{
	if (KitbagData.Contains(ItemUID))
	{
		if (KitbagData[ItemUID].isShowNew)
		{
			/// 超过3天，则不在显示new样式
			if ((FDateTime::Now() - KitbagData[ItemUID].CreateTime).GetDays() >= 3)
			{
				KitbagData[ItemUID].isShowNew = false;
			}
			return KitbagData[ItemUID].isShowNew;
		}
	}
	return false;
}

void ULocalKitbagData::SaveNewTip(const FString& ItemUID, const bool& IsShowNew)
{
	if (KitbagData.Contains(ItemUID))
	{
		KitbagData[ItemUID].isShowNew = IsShowNew;
		UGolbalBPFunctionLibrary::GameInstance()->LocalDataSaveManager->SaveLocalItemDataFile();
	}
}

const FString& ULocalKitbagData::GetFileName()
{
	return FileName;
}

CONTROL_COMPILE_OPTIMIZE_END