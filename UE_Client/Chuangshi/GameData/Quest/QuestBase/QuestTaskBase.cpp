// Fill out your copyright notice in the Description page of Project Settings.

#include "QuestTaskBase.h"


void UQuestTaskBase::InitDatas(const int32& FQuestID, const FCS3Task& _Task)
{
	QuestID = FQuestID;
	TaskName = _Task.TaskName;
	TaskID = _Task.TaskID;
	Progress = _Task.Progress;
	Goal = _Task.Goal;
	Priority = _Task.Priority;
	TaskClass = _Task.TaskClass;
	TaskParam1 = _Task.TaskParam1;
	TaskParam2 = _Task.TaskParam2;
	TaskParam3 = _Task.TaskParam3;
	NavigateData = _Task.NavigateData;
}

bool UQuestTaskBase::IsTaskStatus(int32 Status)
{
	if (Progress>=Goal)
	{
		return Status == int32(QUEST_TASK_STATE::TASK_IS_DONE);
	}
	return Status == int32(QUEST_TASK_STATE::TASK_NOT_DONE);
}

void UQuestTaskBase::Update(const int32& Progress_)
{
	Progress = Progress_;
}

void UQuestTaskBase::SetDone()
{
	
}


void UQuestTaskTalkWithWhisper::SetDone()
{
	IsComplete = true;
}

bool UQuestTaskTalkWithWhisper::IsTaskStatus(int32 Status)
{
	if (IsComplete)
	{
		return Status == int32(QUEST_TASK_STATE::TASK_IS_DONE);
	}
	if (Progress >= Goal)
	{
		return Status == int32(QUEST_TASK_STATE::TASK_IS_DONE);
	}
	return Status == int32(QUEST_TASK_STATE::TASK_NOT_DONE);
}
