// Fill out your copyright notice in the Description page of Project Settings.

#include "BaseQuestArea.h"
#include "Vector.h"
#include "Interface/Role/RoleQuestInterface.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Actor/ServerCharacter.h"
#include "Manager/QuestManager.h"
#include "Util/ConvertUtil.h"


UBaseQuestArea::UBaseQuestArea()
{
}

UBaseQuestArea::~UBaseQuestArea()
{

}

bool UBaseQuestArea::IsPlayerIn()
{
	AServerCharacter* PlayerActor = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
	if (!PlayerActor)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UBaseQuestArea::IsPlayerIn : PlayerActor!"));
		return false;
	}

	if (UUECS3GameInstance::pKBEApp == nullptr)
	{
		return false;
	}
	const FString level = UUECS3GameInstance::pKBEApp->pBaseApp()->GetSpaceData(FString(TEXT("SPACE_SCRIPT_ID")));
	if (!level.Equals(ScriptID))return false;

	FVector PlayerPosition = PlayerActor->GetActorLocation();
	// 两个坐标点之间的距离
	int Distance = FVector::Dist(Point, PlayerPosition);
	if (Distance > Range)return false;

	return true;
}

void UBaseQuestArea::InitDatas(int _QuestID, int _TaskID, const FString & Param1, const FString & Param2, const FString & Param3)
{
	ScriptID = Param1;
	QuestID = _QuestID;
	TaskID = _TaskID;
	Range = FSTRING_TO_INT(Param3) * 100;

	FString SplitStr = FString(TEXT(" "));
	TArray<FString> FSplitArray = UGolbalBPFunctionLibrary::SplitString(Param2, true, SplitStr);
	if (FSplitArray.Num() < 3) return;
	Point = FVector(FSTRING_TO_FLOAT(FSplitArray[0]), FSTRING_TO_FLOAT(FSplitArray[1]), FSTRING_TO_FLOAT(FSplitArray[2]));
}

bool UBaseQuestArea::CheckCondition()
{
	URoleQuestInterface* RoleQuestInterface = Cast<URoleQuestInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleQuestInterface"), 0));
	if (RoleQuestInterface)
	{
		if (RoleQuestInterface->IsQuestStatus(QuestID, int32(QUEST_STATE::QUEST_IS_DONE)))return false;
		//判断任务目标状态
		if (RoleQuestInterface->IsTaskStatus(QuestID, TaskID, int32(QUEST_TASK_STATE::TASK_IS_DONE)))return false;
		//判断任务目标优先级
		UQuestBase* quest = UUECS3GameInstance::Instance->QuestManager->GetQuestByID(QuestID);
		if (IsValid(quest))
		{
			UQuestTaskBase* task = quest->GetTask(TaskID);
			if (IsValid(task))
			{
				if (!quest->IsPriorityTasksInViewTasks(task->GetPriority()))return false;
			}
		}
	}
	else
	{
		return false;
	}
	return true;
}

void UBaseQuestArea::OnEnter(const FString SpaceScriptID)
{
	//CS3_Display(CS3DebugType::CL_Undefined, TEXT("UAreaQuest::trriger--------------->>>"));
	//UUECS3GameInstance* GameInstance = UUECS3GameInstance::Instance;
	//const FString Method = FString(TEXT("broadcastQuestEvent"));
	//TArray<FString> Arg;
	//Arg.Add(INT_TO_FSTRING(QuestID));
	//Arg.Add(INT_TO_FSTRING(TaskID));
	//UGolbalBPFunctionLibrary::CellCall(UGolbalBPFunctionLibrary::GetPlayerID(), Method, Arg);
	URoleQuestInterface * RoleQuestInterface = Cast<URoleQuestInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleQuestInterface")));
	if (RoleQuestInterface)
	{
		RoleQuestInterface->RPC_broadcastQuestEvent( INT_TO_FSTRING(QuestID), INT_TO_FSTRING(TaskID));
	}
}