// Fill out your copyright notice in the Description page of Project Settings.


#include "LocalTongSettingData.h"
#include "Manager/LocalDataSaveManager.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Util/GolbalBPFunctionLibrary.h"

ULocalTongSettingData::ULocalTongSettingData()
{
	if (!IsValid(UUECS3GameInstance::Instance)) return;
	int32 PlayerId = UGolbalBPFunctionLibrary::GetPlayerID();
	FString PlayerName = UGolbalBPFunctionLibrary::GetFStringPropertyValue(PlayerId, TEXT("playerName"));
	FileName = "LocalTongSettingData_" + PlayerName;
	InitLocalTongSettingData();
}

const FString& ULocalTongSettingData::GetFileName()
{
	return FileName;
}

void ULocalTongSettingData::InitLocalTongSettingData()
{
	TongEventSetDatas = GetTongEventSetDefaultData();
	SelectedOptionIndex = 0;
	IsShowOnlyMe = false;
	IsShowOffLineMembers = false;
}

TArray<FTONG_EVENT_SET_DATA> ULocalTongSettingData::GetTongEventSetDefaultData()
{
	TArray<FTONG_EVENT_SET_DATA> tempTongEventDatas;
	for (uint8 i=0;i<10;++i)
	{
		FTONG_EVENT_SET_DATA tempData;
		tempData.TongEventSetType= TONG_EVENT_SET_TYPE(i);
		tempData.IsChecked = true;
		tempTongEventDatas.Add(tempData);
	}	
	return tempTongEventDatas;
}

void ULocalTongSettingData::SaveTongEventSetData(TArray<FTONG_EVENT_SET_DATA> EventSetDatas, int32 SelectedIndex, bool IsOnlyMe)
{
	TongEventSetDatas = EventSetDatas;
	SelectedOptionIndex = SelectedIndex;
	IsShowOnlyMe = IsOnlyMe;
	UGolbalBPFunctionLibrary::GameInstance()->LocalDataSaveManager->SaveLocalTongSettingDataFile();
}

void ULocalTongSettingData::SaveTongMembersSetData(bool IsShowOffLine)
{
	IsShowOffLineMembers = IsShowOffLine;
	UGolbalBPFunctionLibrary::GameInstance()->LocalDataSaveManager->SaveLocalTongSettingDataFile();
}
