// Fill out your copyright notice in the Description page of Project Settings.


#include "LocalData.h"
#include "Manager/LoginManager.h"
#include "Util/ConvertUtil.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Manager/LocalDataSaveManager.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Manager/QuestManager.h"

void ULocalData::UpdateLoginDataToFile(const FString & inServerIp, const FString & inAccount)
{
	LoginServerIp = inServerIp;
	FString defaultRoleDbid;
	if (LoginAccounts.Num() > 0 && EnterRoleDbids.Num() > 0)
	{
		// 查找保存首个账号与本次登陆账号相等，不保存处理
		if (!LoginAccounts[0].Compare(inAccount))
			return;
		int findNum = LoginAccounts.Find(inAccount);
		if (findNum != -1)
		{
			if (EnterRoleDbids.Num() > findNum)
			{
				defaultRoleDbid = EnterRoleDbids[findNum];
				EnterRoleDbids.RemoveAt(findNum);
			}
			LoginAccounts.RemoveAt(findNum);
		}
	}
	EnterRoleDbids.Insert(defaultRoleDbid, 0);
	LoginAccounts.Insert(inAccount, 0);
	UGolbalBPFunctionLibrary::GameInstance()->LocalDataSaveManager->SaveLocalDataFile();
}

void ULocalData::UpdateRolePosToRolePosMap(const FString & dbid, const int32 & pos)
{
	if (uint64(FSTRING_TO_INT64(dbid)) > 0)
	{
		for (auto posMap : AllRolePosMap)
		{
			if (posMap.Value == pos && !AllRolePosMap.Contains(dbid))
			{
				//Map中Key值不包含该dbid，但是value(位置)相同，所以将value值设置为-1
				AllRolePosMap.Add(dbid, -1);
				UGolbalBPFunctionLibrary::GameInstance()->LocalDataSaveManager->SaveLocalDataFile();
				return;
			}
		}
		if (AllRolePosMap.Contains(dbid))
		{
			AllRolePosMap.Remove(dbid);
		}
		AllRolePosMap.Add(dbid, pos);
	}
	UGolbalBPFunctionLibrary::GameInstance()->LocalDataSaveManager->SaveLocalDataFile();
}

int32 ULocalData::GetRolePosByDbid(const FString& dbid)
{
	if (uint64(FSTRING_TO_INT64(dbid))> 0 && AllRolePosMap.Contains(dbid))
	{
		return AllRolePosMap[dbid];
	}
	return -1;
}

bool ULocalData::GetPreLoadStoryLocalData(const FString & Key, const FString StoryID)
{
	if (PreLoadStoryData.Contains(Key))
	{
		for (auto data : (*PreLoadStoryData.Find(Key)).StoryIDs)
		{
			if (!data.Compare(StoryID))
			{
				return true;
			}
		}
		((*PreLoadStoryData.Find(Key)).StoryIDs).Add(StoryID);
	}
	else
	{
		FPRELOADSTORY_SAVEDATA temp;
		temp.StoryIDs = { StoryID };
		PreLoadStoryData.Add(Key, temp);
	}
	return false;
}

void ULocalData::OnPlayerEnterWorld()
{
	UQuestManager* QuestManager = UUECS3GameInstance::Instance->QuestManager;
	if (IsValid(QuestManager))
	{
		QuestManager->OnDelQuestDelegate.AddUObject(this, &ULocalData::UpdatePreLoadStoryLocalData);
	}
}

void ULocalData::UpdatePreLoadStoryLocalData(int32 QuestID)
{
	FString key = (UGolbalBPFunctionLibrary::GetFStringPropertyValue(UGolbalBPFunctionLibrary::GetPlayerID(), TEXT("playerName")).Append(TEXT("_"))).Append(INT_TO_FSTRING(QuestID));
	
	if (PreLoadStoryData.Contains(key))
	{
		PreLoadStoryData.Remove(key);
	}
}


const FString& ULocalData::GetFileName()
{
	return FileName;
}


