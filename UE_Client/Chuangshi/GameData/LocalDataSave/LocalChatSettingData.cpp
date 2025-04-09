// Fill out your copyright notice in the Description page of Project Settings.

#include "LocalChatSettingData.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Manager/LocalDataSaveManager.h"
#include "Manager/CfgManager.h"

ULocalChatSettingData::ULocalChatSettingData()
{
	if (!IsValid(UUECS3GameInstance::Instance)) return;
	int32 PlayerId = UGolbalBPFunctionLibrary::GetPlayerID();
	FString PlayerName = UGolbalBPFunctionLibrary::GetFStringPropertyValue(PlayerId, TEXT("playerName"));
	FileName = "LocalChatSettingData_" + PlayerName;
}

const FString & ULocalChatSettingData::GetFileName()
{
	return FileName;
}

void ULocalChatSettingData::DefaultDataToFile()
{
	InitLocalChatSettingData();
	SaveDataToFile(ChatSettingData);
}

void ULocalChatSettingData::SaveDataToFile(FChatSettingData data)
{
	ChatSettingData = data;
	UGolbalBPFunctionLibrary::GameInstance()->LocalDataSaveManager->SaveLocalChatSettingDataFile();
}

FChatSettingData ULocalChatSettingData::GetDefaultChatSettingData()
{
	FChatSettingData TempChatSettingData;
	if (UGolbalBPFunctionLibrary::CfgManager())
	{
		const UConfigTable* ConfigTable = UGolbalBPFunctionLibrary::CfgManager()->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_CHAT_CHANNEL_DATA);
		if (ConfigTable)
		{
			TArray<FName> Rows = ConfigTable->GetRowNames();
			
			for (FName& Row : Rows)
			{
				const FChatChannelCfg* Data = ConfigTable->GetRow<FChatChannelCfg>(Row);
				if (Data)
				{
					FChatChannelCfg* TempData = const_cast<FChatChannelCfg*>(Data);
					TempChatSettingData.ChannelSettingData.Add(*TempData);
				}
			}
		}
	}

	TempChatSettingData.BaseSettingData.BGColor.R = 255;
	TempChatSettingData.BaseSettingData.BGColor.G = 255;
	TempChatSettingData.BaseSettingData.BGColor.B = 255;
	TempChatSettingData.BaseSettingData.BGColor.A = 204;
	TempChatSettingData.BaseSettingData.IsShowTime = false;
	TempChatSettingData.BaseSettingData.isHideAuto = true;
	TempChatSettingData.BaseSettingData.Transparency = 0.8f;
	TempChatSettingData.BaseSettingData.WinPosX = 100.0f;
	TempChatSettingData.BaseSettingData.WinPosY = 100.0f;
	return TempChatSettingData;
}

void ULocalChatSettingData::InitLocalChatSettingData()
{
	ChatSettingData = GetDefaultChatSettingData();
}
