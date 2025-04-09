// Fill out your copyright notice in the Description page of Project Settings.


#include "QuestTaskGetTo.h"
#include "Manager/MapManager.h"
#include "GameDevelop/CS3GameInstance.h"

void UQuestTaskGetTo::InitDatas(const int32& FQuestID, const FCS3Task& _Task)
{
	UQuestTaskBase::InitDatas(FQuestID, _Task);
	UUECS3GameInstance::Instance->MapManager->AddAreaQuest(FQuestID, TaskID, _Task.TaskParam1, _Task.TaskParam2, _Task.TaskParam3);
}
