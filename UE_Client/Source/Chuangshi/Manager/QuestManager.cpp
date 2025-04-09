// Fill out your copyright notice in the Description page of Project Settings.

#include "QuestManager.h"
#include "Manager/CfgManager.h"
#include "GameData/StrToClass.h"
#include"Chuangshi.h"
#include "CfgManager.h"
#include "GameData/Quest/ClientQuestInfo.h"
UQuestManager* UQuestManager::GetInstance()
{
	cs3_checkNoReentry();

	return NewObject<UQuestManager>();
}

void UQuestManager::onEnterWorld()
{

}

void UQuestManager::onLeaveWorld()
{
	QuestTable.Empty();
	QuestLogger.Empty();
}

void UQuestManager::ClearQuestLog()
{
	QuestLogger.Empty();
}

void UQuestManager::ClearQuestLogByType(const FString& type)
{
	for (auto questid : QuestLogger)
	{
		auto quest = GetQuestConfig(questid);
		
		if (quest->QuestClass == type)
		{
			QuestLogger.Remove(questid);
		}
	}
}

void UQuestManager::AddQuest(const FString & JsonStr, const QUEST_TYPE type,int32 ID)
{
	FString QuestStr;
	const UConfigTable* Table = UGolbalBPFunctionLibrary::CfgManager()->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_STRTOCLASS);
	if (type ==QUEST_TYPE::QUEST_TYPE_MAILLINE)
	{
		QuestStr = TEXT("MailLine");
	}
	else if (type == QUEST_TYPE::QUEST_TYPE_BRANCH)
	{
		QuestStr = TEXT("Branch");
	}
	else if (type == QUEST_TYPE::QUEST_TYPE_DAILY)
	{
		QuestStr = TEXT("Daily");
	}
	else if (type == QUEST_TYPE::QUEST_TYPE_LOOP)
	{
		QuestStr = TEXT("Loop");
	}
	else if (type == QUEST_TYPE::QUEST_TYPE_QIYUAN)
	{
		QuestStr = TEXT("QiYuan");
	}
	else
	{
		QuestStr = TEXT("QuestBase");
	}
	FStrToClass* Data = const_cast<FStrToClass*>(Table->GetRow<FStrToClass>(QuestStr));
	UQuestBase* Quest = NewObject<UQuestBase>(this, Data->GetTargetClass());
	Quest->InitDatas( JsonStr );
	Quest->SetListViewTasksAndLastPriorityIndex();
	QuestTable.Add(ID, Quest);
}

void UQuestManager::DelQuest(const int32 & QuestID)
{
	if (QuestTable.Contains(QuestID))
	{
		QuestTable.Remove(QuestID);

		if (OnDelQuestDelegate.IsBound())
		{
			OnDelQuestDelegate.Broadcast(QuestID);
		}
	}
}

bool UQuestManager::HasQuest(const int32 & QuestID)
{
	if (QuestTable.Contains(QuestID))
	{
		return true;
	}
	return false;
}

void UQuestManager::UpdateQuest(const int32 & QuestID, const int32 & TaskID, const int32 & Progress)
{
	if (QuestTable.Contains(QuestID))
	{
		QuestTable[QuestID]->UpdateTask(TaskID, Progress);
	}

	
}

void UQuestManager::SetQuestTaskDone(const int32 & QuestID, const int32 & TaskID)
{
	if (QuestTable.Contains(QuestID))
	{
		QuestTable[QuestID]->SetTaskDone(TaskID);
	}
}

void UQuestManager::CommitQuest(const int32 & QuestID)
{
	DelQuest(QuestID);
	QuestLogger.Add(QuestID);
}

void UQuestManager::CompleteQuest(const int32 & QuestID)
{
	if (QuestTable.Contains(QuestID))
	{
		QuestTable[QuestID]->Complete();
	}

	
}

void UQuestManager::OnRecvQuestLog(const FString & LogStr)
{
	for (auto str : UGolbalBPFunctionLibrary::SplitString(LogStr))
	{
		QuestLogger.Add(FSTRING_TO_INT(str));
	}
}

void UQuestManager::onRemoveQuestLog(const int32 & QuestID)
{
	if (QuestLogger.Contains(QuestID))
	{
		QuestLogger.Remove(QuestID);
	}
}
bool UQuestManager::IsQuestType(const int32 & QuestID, int32 Type)
{
	if (!QuestTable.Contains(QuestID))
	{
		CS3_Warning(TEXT("Can not find player questID(%d)!!"), QuestID);
		return false;
	}
	UQuestBase* QuestInst = QuestTable.FindRef(QuestID);
	if (int32(QuestInst->GetType())==Type)
	{
		return true;
	}
	return false;
}

bool UQuestManager::IsQuestStatus(const int32 & QuestID, int32 Status)
{
	if (QuestLogger.Contains(QuestID))
	{
		return Status==int32(QUEST_STATE::QUEST_HAD_FINISH);
	}
	if (QuestTable.Contains(QuestID))
	{
		return (int32(QuestTable[QuestID]->GetState()) == Status);
	}
	return int32(QUEST_STATE::QUEST_NOT_ACCEPT)==Status;
}

bool UQuestManager::IsTaskStatus(const int32& QuestID, const int32& TaskID, int32 Status)
{
	if (QuestLogger.Contains(QuestID))
	{
		return Status == int32(QUEST_TASK_STATE::TASK_IS_DONE);
	}
	if (QuestTable.Contains(QuestID))
	{
		if (QuestTable[QuestID]->GetTask(TaskID))
		{
			return QuestTable[QuestID]->GetTask(TaskID)->IsTaskStatus( Status );
		}
	}
	return Status == int32(QUEST_TASK_STATE::TASK_NOT_DONE);
}

int32 UQuestManager::GetTaskPriority(const int32& QuestID, const int32& TaskID)
{
	if (QuestTable.Contains(QuestID))
	{
		if (QuestTable[QuestID]->GetTask(TaskID))
		{
			return QuestTable[QuestID]->GetTask(TaskID)->GetPriority();
		}
	}
	CS3_Warning(TEXT("Can not find player questID(%d)!!"), QuestID);
	return -1;
}

UQuestBase* UQuestManager::GetQuestByID(const int32& QuestID)
{
	if (!QuestTable.Contains(QuestID))
	{
		CS3_Warning(TEXT("Can not find player questID(%d)!!"), QuestID);
		return nullptr;
	}
	UQuestBase* QuestInst = QuestTable.FindRef(QuestID);
	return QuestInst;
}

TArray<int32> UQuestManager::GetQuestIDsByType(QUEST_TYPE Type)
{
	TArray<int32> QuestIDs;
	for (auto item: QuestTable)
	{
		if ((item.Value)->GetType() == Type)
		{
			QuestIDs.Add(item.Key);
		}
	}
	return QuestIDs;
}

void UQuestManager::GetPlayerQuestIDs(TArray<int32>& AllQuests)
{
	QuestTable.GetKeys(AllQuests);
}

const FCS3ClientQuestInfo * UQuestManager::GetQuestConfig(const int32 & QuestID)
{
	auto QusetTable1 = UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_QUEST_DATA);
	return QusetTable1->GetRow<FCS3ClientQuestInfo>(INT_TO_FSTRING(QuestID));
}
