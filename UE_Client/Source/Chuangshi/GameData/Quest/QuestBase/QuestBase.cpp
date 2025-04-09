// Fill out your copyright notice in the Description page of Project Settings.

#include "QuestBase.h"
#include "GameData/StrToClass.h"
#include "GameDevelop/CS3GameInstance.h"
#include "../../EnumCsvDefine.h"
#include "Manager/CfgManager.h"
#include "GameData/Quest/ClientQuestInfo.h"
#include "Util/ConvertUtil.h"
#include "JsonFieldData.h"
#include "Util/ConvertUtil.h"
#include "Util/CS3Debug.h"


void UQuestBase::InitDatas(const FString JsonStr)
{
	//动态数据从服务器传来的JsonStr里面获取
	auto JsonData = UJsonFieldData::Create(this)->FromString(JsonStr)->GetObject(TEXT("ROOT"));
	ID = FSTRING_TO_INT(JsonData->GetString(TEXT("id")));
	Type = QUEST_TYPE(FSTRING_TO_INT(JsonData->GetString(TEXT("type"))));
	State = QUEST_STATE(FSTRING_TO_INT(JsonData->GetString(TEXT("status"))));
	//静态数据
	auto QusetTable1 = UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_QUEST_DATA);
	const FCS3ClientQuestInfo* questInfo = QusetTable1->GetRow<FCS3ClientQuestInfo>(INT_TO_FSTRING(ID));
	if (!questInfo)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleQuestInterface::GetTalkInfoByJson : Data!"));
		return;
	}
	nextQuestID = FSTRING_TO_INT(questInfo->NextQuest);
	QuestName = questInfo->Title;
	LogDesc = questInfo->TaskLogDes;
	Description = questInfo->Description;
	bIsAutoAccept = (bool)questInfo->IsAutoAccept;
	bIsAutoCommit = (bool)questInfo->IsAutoCommit;
	Finish_by = questInfo->Finish_by;
	//奖励
	TArray<FCS3RewardInfo> RewardInfos;
	UJsonFieldData* RewardData = JsonData->GetObject(TEXT("rewards"));
	for (FString RewardStr : RewardData->GetObjectKeys(UUECS3GameInstance::Instance->GetWorld()))
	{
		FCS3RewardInfo TemporaryRewardInfo;
		TemporaryRewardInfo.Type = REWARED_TYPE(FSTRING_TO_INT(RewardStr));
		if (TemporaryRewardInfo.Type == REWARED_TYPE::REWARD_TYPE_ITEM_CHOOSE)///<可选任务奖励数据
		{
			TArray<UJsonFieldData*> DataArray = RewardData->GetObjectArray(UUECS3GameInstance::Instance->GetWorld(), RewardStr);
			FString InfoStr = TEXT("");
			for (UJsonFieldData* Data : DataArray)
			{
				FString IndexStr = Data->GetString(TEXT("index"));
				FString DataString = Data->GetString(TEXT("Datas"));
				InfoStr += IndexStr + TEXT("|") + DataString + TEXT("||");
			}
			TemporaryRewardInfo.Value = InfoStr;
		}
		else
		{
			TemporaryRewardInfo.Value = RewardData->GetString(RewardStr);
		}
		RewardInfo.Add(TemporaryRewardInfo);
	}
	//Task
	TArray<FCS3Task> TemporaryTasks;

	int taskNum = JsonData->GetStringArray(TEXT("taskID")).Num();
	
	for (int i = 0; i < taskNum; ++i)
	{
		FCS3Task task;
		task.TaskID = FSTRING_TO_INT(JsonData->GetStringArray(TEXT("taskID"))[i]);
		task.Progress = FSTRING_TO_INT(JsonData->GetStringArray(TEXT("progress"))[i]);
		for (int j = 0; j < taskNum; ++j)
		{
			if (task.TaskID != questInfo->Tasks[i].ID)
			{
				continue;
			}
			task.TaskClass = questInfo->Tasks[i].TaskClass;
			task.TaskName = questInfo->Tasks[i].Name;
			task.Goal = questInfo->Tasks[i].Goal;

			if (Type == QUEST_TYPE::QUEST_TYPE_JSZZ)
			{
				task.TaskParam1 = JsonData->GetStringArray(TEXT("taskParam1"))[i];
				task.TaskParam2 = JsonData->GetStringArray(TEXT("taskParam2"))[i];
				task.TaskParam3 = JsonData->GetStringArray(TEXT("taskParam3"))[i];
				task.NavigateData = JsonData->GetStringArray(TEXT("navigateData"))[i];
			}
			else if (Type == QUEST_TYPE::QUEST_TYPE_QIYUAN)
			{
				task.TaskParam1 = JsonData->GetStringArray(TEXT("taskParam1"))[i];
				task.TaskParam2 = JsonData->GetStringArray(TEXT("taskParam2"))[i];
				task.TaskParam3 = JsonData->GetStringArray(TEXT("taskParam3"))[i];
				task.NavigateData = JsonData->GetStringArray(TEXT("navigateData"))[i];
			}
			else {
				task.TaskParam1 = questInfo->Tasks[i].Param1;
				task.TaskParam2 = questInfo->Tasks[i].Param2;
				task.TaskParam3 = questInfo->Tasks[i].Param3;
				task.NavigateData = questInfo->Tasks[i].NavigateData;
			}
			task.Priority = questInfo->Tasks[i].Priority;
			TemporaryTasks.Add(task);
			break;
		}
	}

	const UConfigTable* Table = UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_STRTOCLASS);
	
	for (auto It = TemporaryTasks.CreateConstIterator(); It; ++It)
	{
		UQuestTaskBase* Task;
		int32 Index = It.GetIndex();
		FStrToClass* TaskClass = const_cast<FStrToClass*>(Table->GetRow<FStrToClass>(TemporaryTasks[Index].TaskClass));
		if (TemporaryTasks[Index].TaskClass == "QuestTaskTalkWithWhisper")
		{
			UQuestTaskTalkWithWhisper* Temp = NewObject<UQuestTaskTalkWithWhisper>();
			Task = (UQuestTaskBase*) Temp;
		}
		else if (TaskClass!= nullptr)
		{
			Task = NewObject<UQuestTaskBase>(this, TaskClass->GetTargetClass());
		}
		else
		{
			Task = NewObject<UQuestTaskBase>();
		}
		
		Task->InitDatas(ID, TemporaryTasks[Index]);
		Tasks.Add(TemporaryTasks[Index].TaskID, Task);
	}
	LastTaskPriorityIndex = 0;
	SetTasksSortByPriority();
}

QUEST_STATE UQuestBase::GetState()
{
	for (auto It = Tasks.CreateConstIterator(); It; ++It)
	{
		if (It.Value()->IsTaskStatus(int32(QUEST_TASK_STATE::TASK_NOT_DONE)))
		{
			return QUEST_STATE::QUEST_NOT_DONE;
		}
	}
	return QUEST_STATE::QUEST_IS_DONE;
}

UQuestTaskBase* UQuestBase::GetTask(const int32 TaskID)
{
	if (Tasks.Contains(TaskID))
	{
		return Tasks[TaskID];
	}
	return nullptr;
}

TArray<UQuestTaskBase*> UQuestBase::GetTasks()
{
	TArray<UQuestTaskBase*> TempTasks;
	Tasks.ValueSort([](UQuestTaskBase& TaskA, UQuestTaskBase& TaskB) {return TaskA.GetPriority() < TaskB.GetPriority(); });
	for (auto& Task : Tasks)
	{
		if (Task.Value)
		{
			TempTasks.Add(Task.Value);
		}
	}
	return TempTasks;
}

void UQuestBase::UpdateTask(const int32 & TaskID, const int32 & Progress)
{
	for (auto& TaskPiar : TaskMap)
	{
		TArray<UQuestTaskBase*> TaskList = TaskPiar.Value;
		for (auto Task : TaskList)
		{
			if (Task->GetTaskID() == TaskID)
			{
				Task->Update(Progress);
			}
		}
	}
	if (Tasks.Contains(TaskID))
	{
		UQuestTaskBase* Task = Tasks[TaskID];
		Task->Update(Progress);
		SetListViewTasksAndLastPriorityIndex();
		OnQuestTaskChange.Broadcast(ID, TaskID, Progress);
	}
}

void UQuestBase::SetTaskDone(const int32 & TaskID)
{
	if (Tasks.Contains(TaskID))
	{
		UQuestTaskBase* Task = Tasks[TaskID];
		Task->SetDone();
	}
}

void UQuestBase::Complete()
{
	State = QUEST_STATE::QUEST_IS_DONE;
}

void UQuestBase::SetState(const QUEST_STATE& NewState)
{
	State = NewState;
}

void UQuestBase::SetTasksSortByPriority()
{
	for (auto& Task : Tasks)
		{
		if (Task.Value)
			{
			int32 Priority = Task.Value->GetPriority();
			if (!TaskMap.Contains(Priority) )
				{
					TArray<UQuestTaskBase*> TaskList;
					TaskMap.Add(Priority, TaskList);
				}
			TaskMap[Priority].Add(Task.Value);
			}
		}
	TaskMap.KeySort([](const int32 KeyA, const int32 KeyB) {return KeyA < KeyB; });
	for (auto& TaskPiar : TaskMap)
	{
		TArray<UQuestTaskBase*> TasksList = TaskPiar.Value;
		TasksList.Sort([](UQuestTaskBase& TaskA, UQuestTaskBase& TaskB) { return TaskA.GetTaskID() < TaskB.GetTaskID(); });
		TaskMap[TaskPiar.Key] = TasksList;
	}
}

void UQuestBase::SetListViewTasksAndLastPriorityIndex()
{
	ViewTasks.Empty();
	for (auto& TaskPiar : TaskMap)
	{
		if (TaskPiar.Value.Num() > 0)
		{
			int32 Priority = TaskPiar.Key;
			if (Priority == 0)
			{
				if (TaskMap.Contains(Priority))
				{
					ViewTasks.Append(TaskMap[Priority]);
				}
			}
			else if (IsHasAnyTaskDone(Priority))
			{				
				bool isPreTaskHasDone = true;
				for (int32 index = Priority -1; index > 0; index--)
				{
					if (!IsHasAnyTaskDone(index))
					{
						if (!IsPriorityTasksInViewTasks(index))
						{
							if (TaskMap.Contains(index))
							{
								ViewTasks.Append(TaskMap[index]);
							}
						}						
						isPreTaskHasDone = false;
					}
				}
				if (isPreTaskHasDone)
				{
					if (TaskMap.Contains(Priority))
					{
						ViewTasks.Append(TaskMap[Priority]);
					}
				}
			}
		}
	}
	TArray<int32> Priorities;
	if ((TaskMap.Num() > 1))
	{
		TaskMap.GetKeys(Priorities);
		Priorities.Sort();
		if (ViewTasks.Num() < 1)
		{
			int32 FirstPriority = Priorities[0];
			if (TaskMap.Contains(FirstPriority))
			{
				ViewTasks = TaskMap[FirstPriority];
			}
		}	
	}
	int32 TasksNum = ViewTasks.Num();
	if (TasksNum < 1)
	{
		return;
	}
	UQuestTaskBase* LastTask = ViewTasks[TasksNum - 1];
	int32 LastTaskPriority = LastTask->GetPriority();
	if (IsSamePriorityTasksHasDone(LastTaskPriority))
	{
		for (auto& TaskPiar : TaskMap)
		{
			if (TaskPiar.Key > LastTaskPriority)
			{
				LastTaskPriority = TaskPiar.Key;
				ViewTasks.Append(TaskPiar.Value);
				break;
			}
		}
	}
	if (Priorities.Contains(LastTaskPriority))
	{
		LastTaskPriorityIndex = Priorities.Find(LastTaskPriority);
	}
}

bool UQuestBase::IsSamePriorityTasksHasDone(const int32 Priority)
{
	if (TaskMap.Contains(Priority))
	{
		TArray<UQuestTaskBase*> TempTasks = TaskMap[Priority];
		for (auto& Task : TempTasks)
		{
			if (!Task->IsTaskStatus(2))
			{
				return false;
			}
		}
	}
	return true;
}

bool UQuestBase::IsPriorityTasksQuest()
{
	for (auto& Task : Tasks)
	{
		if (Task.Value)
		{
			int32 Priority = Task.Value->GetPriority();
			if (Priority > 0)
			{
				return true;
			}
		}
	}
	return false;
}

bool UQuestBase::IsHasAnyTaskDone(const int32 Priority)
{
	if (TaskMap.Contains(Priority))
	{
		TArray<UQuestTaskBase*> TempTasks = TaskMap[Priority];
		for (auto& Task : TempTasks)
		{
			if (Task->IsTaskStatus(2))
			{
				return true;
			}
		}
	}
	return false;
}

bool UQuestBase::IsPriorityTasksInViewTasks(const int32 Priority)
{
	if (TaskMap.Contains(Priority))
	{
		TArray<UQuestTaskBase*> TempTasks = TaskMap[Priority];
		for (auto& Task : TempTasks)
		{
			if (ViewTasks.Contains(Task))
			{
				return true;
			}
		}
		return false;
	}
	return false;
}