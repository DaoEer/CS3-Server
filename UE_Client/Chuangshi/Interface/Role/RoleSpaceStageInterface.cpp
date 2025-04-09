// Fill out your copyright notice in the Description page of Project Settings.


#include "RoleSpaceStageInterface.h"
#include "Json.h"
#include "JsonFieldData.h"
#include "Util/ConvertUtil.h"
#include "Util/CS3Debug.h"
#include "Manager/MapManager.h"

CS3_BEGIN_INTERFACE_METHOD_MAP(URoleSpaceStageInterface, Supper)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(URoleSpaceStageInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()
	
URoleSpaceStageInterface::URoleSpaceStageInterface()
{
}

URoleSpaceStageInterface::~URoleSpaceStageInterface()
{
}

void URoleSpaceStageInterface::CLIENT_showSpaceStageWin_Implementation(const FString& stageFileName, const TArray<FString>& completeStages, const FString& spaceStageJson)
{
	UJsonFieldData* tempJson = UJsonFieldData::Create(this);
	auto returnvalue = tempJson->FromString(spaceStageJson);
	auto tempArray = returnvalue->GetObjectArray(this,TEXT("ROOT"));
	for (auto temp: tempArray)
	{
		int32 stageIndex = FSTRING_TO_INT(temp->GetString(TEXT("stageIndex")));
		FString title = temp->GetString(TEXT("title"));
		FString comment = temp->GetString(TEXT("comment"));
		auto taskArray = temp->GetObjectArray(this,TEXT("tasks"));
		for (int i = 0; i < taskArray.Num(); i++)
		{
			int32 	taskIndex = FSTRING_TO_INT(taskArray[i]->GetString(TEXT("taskIndex")));
			FString	implType = taskArray[i]->GetString(TEXT("implType"));
			FString	taskTitle = taskArray[i]->GetString(TEXT("title"));
			FString	val = taskArray[i]->GetString(TEXT("val"));
			FString	reqVal = taskArray[i]->GetString(TEXT("reqVal"));
			FString	param1 = taskArray[i]->GetString(TEXT("param1"));
			FString	param2 = taskArray[i]->GetString(TEXT("param2"));
			FString	param3 = taskArray[i]->GetString(TEXT("param3"));
			FString	navigateData = taskArray[i]->GetString(TEXT("navigateData"));
			bool isShowByProgressbar = FSTRING_TO_INT(taskArray[i]->GetString(TEXT("isShowByProgressbar"))) ? true : false;
			bool isEnd = false;
			if (i == (taskArray.Num() - 1))
			{
				isEnd = true;
			}
			ShowSpaceStageWin(stageFileName, completeStages,stageIndex, title, comment, taskIndex, implType, taskTitle, val, reqVal, param1, param2, param3, navigateData, isShowByProgressbar, isEnd);
		}
	}	
}

void URoleSpaceStageInterface::CLIENT_updateSpaceStageWin_Implementation(const int32& stageIndex, const FString& taskData)
{
	UJsonFieldData* tempJson = UJsonFieldData::Create(this);
	auto returnvalue = tempJson->FromString(taskData);
	auto tempArray = returnvalue->GetObjectArray(this,TEXT("ROOT"));
	for (auto item :tempArray)
	{
		int32 taskIndex = FSTRING_TO_INT(item->GetString(TEXT("taskIndex")));
		FString val = item->GetString(TEXT("val"));
		UpdateSpaceStageWin(stageIndex, taskIndex, val);
	}
}

void URoleSpaceStageInterface::CLIENT_updateCompleteSpaceStage_Implementation(const TArray<FString>& completeStages)
{

}

void URoleSpaceStageInterface::CLIENT_hideSpaceStageWin_Implementation()
{

}

/**
添加阶段目标区域，用于触发“进入某范围”阶段目标，阶段开始或进入副本时由服务器调用
*/
void URoleSpaceStageInterface::CLIENT_AddSpaceStageTaskArea_Implementation(const FString& SpaceScriptID, const int32 & StageIndex, const FString & AreaInfoStr)
{
	//AreaInfoStr 格式 {"ROOT": [{"areaZRange": "1", "taskIndex": 1, "areaParam": "", "shapeType": ""}, {"areaZRange": "1", "taskIndex": 2, "areaParam": "", "shapeType": ""}]}
	
	CLIENT_ClearSpaceStageTaskArea();///先清空一下，因为小退下线的情况下可能会清空失败。
	TArray<FString> InfoArray;
	FString sLeft;
	FString sRight(AreaInfoStr);
	sRight.Split("[{", &sLeft, &sRight);
	sRight.Split("}]}", &sLeft, &sRight);
	sLeft.ParseIntoArray(InfoArray, TEXT("}, {"), true);

	for (auto InfoStr : InfoArray)	// InfoStr格式 "areaZRange": "1", "taskIndex": 1, "areaParam": "1", "shapeType": ""
	{
		INT32 TaskIndex = 0;
		INT8 ShapeType = 0;
		float CeilHeight = 0.0;
		float FloorHeight = 0.0;
		FString AreaParam = "";

		TArray<FString> ParamArray;
		InfoStr.ParseIntoArray(ParamArray, TEXT(", "), true);
		for (auto ParamStr : ParamArray)
		{
			FString sKey;
			FString sValue(ParamStr);
			sValue.Split(": ", &sKey, &sValue);
			sKey.RemoveFromStart("\"");
			sKey.RemoveFromEnd("\"");
			sValue.RemoveFromStart("\"");
			sValue.RemoveFromEnd("\"");

			if (sKey == "taskIndex") { TaskIndex = FSTRING_TO_INT(sValue); }
			else if (sKey == "shapeType") { ShapeType = FSTRING_TO_INT(sValue); }
			else if (sKey == "areaZRange")
			{
				FString SplitStr = FString(TEXT("|"));
				TArray<FString> FSplitArray = UGolbalBPFunctionLibrary::SplitString(sValue, true, SplitStr);
				if (FSplitArray.Num() > 0)
				{
					CeilHeight = FSTRING_TO_FLOAT(FSplitArray[0]);
				}
				if (FSplitArray.Num() > 1)
				{
					FloorHeight = FSTRING_TO_FLOAT(FSplitArray[1]);
				}
			}
			else if (sKey == "areaParam") { AreaParam = sValue; }
		}
		
		UUECS3GameInstance::Instance->MapManager->AddSpaceStageArea(SpaceScriptID, StageIndex, TaskIndex, ShapeType, CeilHeight, FloorHeight, AreaParam);
	}
}

/**
清除阶段目标区域，阶段完成或离开副本时由服务器调用
*/
void URoleSpaceStageInterface::CLIENT_ClearSpaceStageTaskArea_Implementation()
{
	UUECS3GameInstance::Instance->MapManager->ClearSpaceStageArea();
}

void URoleSpaceStageInterface::CLIENT_showSpaceStageNextTask_Implementation(const int32& stageIndex, const FString& tasksJson)
{
	UJsonFieldData* tempJson = UJsonFieldData::Create(this);
	auto returnvalue = tempJson->FromString(tasksJson);
	auto tempArray = returnvalue->GetObjectArray(this,TEXT("ROOT"));
	for (int i = 0; i < tempArray.Num(); i++)
	{
		int32 	taskIndex = FSTRING_TO_INT(tempArray[i]->GetString(TEXT("taskIndex")));
		FString	implType = tempArray[i]->GetString(TEXT("implType"));
		FString	taskTitle = tempArray[i]->GetString(TEXT("title"));
		FString	val = tempArray[i]->GetString(TEXT("val"));
		FString	reqVal = tempArray[i]->GetString(TEXT("reqVal"));
		FString	param1 = tempArray[i]->GetString(TEXT("param1"));
		FString	param2 = tempArray[i]->GetString(TEXT("param2"));
		FString	param3 = tempArray[i]->GetString(TEXT("param3"));
		FString	navigateData = tempArray[i]->GetString(TEXT("navigateData"));
		bool isShowByProgressbar = FSTRING_TO_INT(tempArray[i]->GetString(TEXT("isShowByProgressbar"))) ? true : false;
		bool isEnd = false;
		if (i == (tempArray.Num() - 1))
		{
			isEnd = true;
		}
		ShowSpaceStageNextTask(stageIndex, taskIndex, implType, taskTitle, val, reqVal, param1, param2, param3, navigateData, isShowByProgressbar, isEnd);
	}
}

void URoleSpaceStageInterface::CLIENT_showSpaceStatistics_Implementation(const FString& statisticsFileName, const FString& statisticsJson)
{
	UJsonFieldData* tempJson = UJsonFieldData::Create(this);
	auto returnvalue = tempJson->FromString(statisticsJson);
	auto tempArray = returnvalue->GetObjectArray(this, TEXT("ROOT"));
	if (tempArray.Num())
	{	// 只有一个元素
		auto statisticsList = tempArray[0]->GetObjectArray(this, TEXT("statisticsList"));
		int32 questID = FSTRING_TO_INT(tempArray[0]->GetString(TEXT("questID")));
		FString title = tempArray[0]->GetString(TEXT("title"));
		FString comment = tempArray[0]->GetString(TEXT("comment"));
		for (int i = 0; i < statisticsList.Num(); i++)
		{
			int32 entryIndex = FSTRING_TO_INT(statisticsList[i]->GetString(TEXT("entryIndex")));
			FString statisticsTitle = statisticsList[i]->GetString(TEXT("title"));
			FString value = statisticsList[i]->GetString(TEXT("value"));
			FString postfix = statisticsList[i]->GetString(TEXT("postfix"));
			FString param1 = statisticsList[i]->GetString(TEXT("param1"));
			FString param2 = statisticsList[i]->GetString(TEXT("param2"));
			FString param3 = statisticsList[i]->GetString(TEXT("param3"));
			FString param4 = statisticsList[i]->GetString(TEXT("param4")); 
			FString progress = statisticsList[i]->GetString(TEXT("progress"));
			bool isEnd = false;
			if (i == (statisticsList.Num() - 1))
			{
				isEnd = true;
			}
			ShowSpaceStatistics(statisticsFileName, questID, title, comment, entryIndex, statisticsTitle, value, postfix, param1, param2, param3, param4, progress, isEnd);
		}
	}
}

void URoleSpaceStageInterface::CLIENT_updateSpaceStatistics_Implementation(const FString& statisticsJson)
{
	UJsonFieldData* tempJson = UJsonFieldData::Create(this);
	auto returnvalue = tempJson->FromString(statisticsJson);
	auto tempArray = returnvalue->GetObjectArray(this, TEXT("ROOT"));
	for (auto temp:tempArray)
	{
		int32 entryIndex = FSTRING_TO_INT(temp->GetString(TEXT("entryIndex")));
		FString value = temp->GetString(TEXT("value"));
		UpdateSpaceStatistics(entryIndex, value);
	}
}

void URoleSpaceStageInterface::CLIENT_hideSpaceStatistics_Implementation()
{

}

/**
玩家进入阶段目标区域
*/
void URoleSpaceStageInterface::CELL_OnEnterSpaceStageArea(INT32 StageIndex, INT32 TaskIndex)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceStageInterface::CELL_OnEnterSpaceStageArea : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray Args;
	Args.Add(StageIndex);
	Args.Add(TaskIndex);

	GetEntity()->CellCall(TEXT("CELL_OnEnterSpaceStageArea"), Args);
}

void URoleSpaceStageInterface::InitBlueCB()
{
	ArrBlueFunc.Add("CLIENT_showSpaceStageWin");
	ArrBlueFunc.Add("CLIENT_updateSpaceStageWin");
	ArrBlueFunc.Add("CLIENT_updateCompleteSpaceStage");
	ArrBlueFunc.Add("CLIENT_hideSpaceStageWin");
	ArrBlueFunc.Add("CLIENT_AddSpaceStageTaskArea");
	ArrBlueFunc.Add("CLIENT_ClearSpaceStageTaskArea");
	ArrBlueFunc.Add("CLIENT_showSpaceStageNextTask");

	//----------副本统计-------------------------
	ArrBlueFunc.Add("CLIENT_showSpaceStatistics");
	ArrBlueFunc.Add("CLIENT_updateSpaceStatistics");
	ArrBlueFunc.Add("CLIENT_hideSpaceStatistics");
	Supper::InitBlueCB();
}

