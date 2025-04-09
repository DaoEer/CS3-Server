// Fill out your copyright notice in the Description page of Project Settings.


#include "LocalRelationData.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Manager/TimeManager.h"
#include "Timespan.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "../ConstDataBP.h"
#include "Manager/LocalDataSaveManager.h"


ULocalRelationData::ULocalRelationData()
{
	if (!IsValid(UUECS3GameInstance::Instance)) return;
	int32 PlayerId = UGolbalBPFunctionLibrary::GetPlayerID();
	FString PlayerName = UGolbalBPFunctionLibrary::GetFStringPropertyValue(PlayerId, TEXT("playerName"));
	FileName = "LocalRelationData_" + PlayerName;
	InitLocalRelationData();
}

const FString& ULocalRelationData::GetFileName()
{
	return FileName;
}

void ULocalRelationData::InitLocalRelationData()
{
	IsShowOnlyOnline = false;
	RelationChatDatas.Empty();
}

TArray<FRelationChatData> ULocalRelationData::GetRelationChatDatas(const FString& RelationUId)
{
	///获得数据之前先做下数据清理
	RemoveRelationChatData(RelationUId);
	TArray<FRelationChatData> TempChatDatas;
	for (auto It = RelationChatDatas.CreateConstIterator(); It; ++It)
	{
		if (It.Key() == RelationUId)
		{
			TempChatDatas = It.Value();
			return TempChatDatas;
		}
	}
	return TempChatDatas;
}

void ULocalRelationData::SaveRelationChatData(const FString& RelationUId, FRelationChatData RelationChatData)
{
	if (RelationChatDatas.Contains(RelationUId))
	{
		RelationChatDatas[RelationUId].Add(RelationChatData);
	}
	else
	{
		TArray<FRelationChatData> tempChatDatas;
		tempChatDatas.Add(RelationChatData);
		RelationChatDatas.Add(RelationUId, tempChatDatas);
	}
	UGolbalBPFunctionLibrary::GameInstance()->LocalDataSaveManager->SaveLocalRelationDataFile();
}

void ULocalRelationData::SaveRelationSetShowOnline(bool IsShowOnline)
{
	IsShowOnlyOnline = IsShowOnline;
	UGolbalBPFunctionLibrary::GameInstance()->LocalDataSaveManager->SaveLocalRelationDataFile();
}

void ULocalRelationData::RemoveRelationChatData(const FString& RelationUId)
{
	int32 longestTime = UUECS3GameInstance::Instance->ConstDataBP->RELATION_CHAT_LOG_LONGEST_TIME;
	int32 maxNum = UUECS3GameInstance::Instance->ConstDataBP->RELATION_CHAT_LOG_MAX_NUM;
	if (RelationChatDatas.Contains(RelationUId))
	{
		TArray<FRelationChatData> tempChatDatas;
		for (auto It : RelationChatDatas[RelationUId])
		{
			FTimespan intervalTime = UUECS3GameInstance::Instance->TimeManager->GetClientTime() - It.time;
			if (longestTime >= intervalTime.GetDays())
			{
				tempChatDatas.Add(It);
			}
		}
		while (tempChatDatas.Num() > maxNum)
		{
			tempChatDatas.RemoveAt(0);
		}
		RelationChatDatas[RelationUId] = tempChatDatas;
	}
	UGolbalBPFunctionLibrary::GameInstance()->LocalDataSaveManager->SaveLocalRelationDataFile();
}

