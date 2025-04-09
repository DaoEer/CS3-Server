// Fill out your copyright notice in the Description page of Project Settings.

#include "LocalMessageData.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Manager/LocalDataSaveManager.h"
#include "Manager/CfgManager.h"

ULocalMessageData::ULocalMessageData()
{
	if (!IsValid(UUECS3GameInstance::Instance)) return;
	int32 PlayerId = UGolbalBPFunctionLibrary::GetPlayerID();
	FString PlayerName = UGolbalBPFunctionLibrary::GetFStringPropertyValue(PlayerId, TEXT("playerName"));
	FileName = "LocalMessageRetipsData_" + PlayerName;
}

const FString & ULocalMessageData::GetFileName()
{
	return FileName;
}

void ULocalMessageData::SaveDataToFile(TArray<FUnRepeatData> data)
{
	MessageSettingData = data;
	UGolbalBPFunctionLibrary::GameInstance()->LocalDataSaveManager->SaveLocalMessageDataFile();
}

TArray<FUnRepeatData> ULocalMessageData::GetMessageData()
{
	return MessageSettingData;
}

void ULocalMessageData::InitLocalMessageData()
{
	MessageSettingData.Empty();
}
