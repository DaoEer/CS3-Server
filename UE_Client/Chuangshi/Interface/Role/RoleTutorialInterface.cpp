// Fill out your copyright notice in the Description page of Project Settings.

#include "RoleTutorialInterface.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Json.h"
#include "JsonFieldData.h"
#include "Util/ConvertUtil.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Manager/TutorialManager.h"
#include "KBEngine.h"

CONTROL_COMPILE_OPTIMIZE_START

CS3_BEGIN_INTERFACE_METHOD_MAP(URoleTutorialInterface, Supper)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(URoleTutorialInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()

void URoleTutorialInterface::OnRep_RecordTutorialIndexs()
{
	if (!RecordTutorialIndexs.IsEmpty())
	{
		RecordIndexList.Empty();
		if (RecordTutorialIndexs.Contains(TEXT("|")))
		{
			RecordIndexList = UGolbalBPFunctionLibrary::SplitString(RecordTutorialIndexs, false, TEXT("|"));
		}
		else
		{
			RecordIndexList.Add(RecordTutorialIndexs);
		}
		

		//删除配置中已经触的一次性触发记录
		ClearDoOnceEvents();
	}
}



void URoleTutorialInterface::ClearDoOnceEvents()
{
	UGolbalBPFunctionLibrary::TutorialManager()->ClearDoOnceEvents(RecordIndexList);
}

bool URoleTutorialInterface::IsDoneTriggerItem(const FString& Index)
{
	if (RecordIndexList.Contains(Index))
	{
		return true;
	}
	else
	{
		return false;
	}
}

void URoleTutorialInterface::FinishTriggerOnceTurtorial(const FName& KeyIndex)
{
	//通知服务器已经触发过那种仅能触发一个指引，让服务器记录数据
	FString Temp = FNAME_TO_FSTRING(KeyIndex);
	TArray<FString> args;
	args.Add(Temp);
	UGolbalBPFunctionLibrary::CellCall(EntityID, ("AddTrigger"), args);
}

void URoleTutorialInterface::onLeaveWorld()
{
	UGolbalBPFunctionLibrary::TutorialManager()->OnLeaveWorld();
	Supper::onLeaveWorld();
}

CONTROL_COMPILE_OPTIMIZE_END
