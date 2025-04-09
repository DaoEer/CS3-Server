// Fill out your copyright notice in the Description page of Project Settings.


#include "BaseProfile.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"
#include "Util/ConvertUtil.h"

CONTROL_COMPILE_OPTIMIZE_START

UBaseProfile::UBaseProfile()
{
	//bCanEverTick = true;
	CustomTimeDilation = 5.0f;
}



void UBaseProfile::StartRecord()
{
	LoadCfg();
	StartTickTask();
	bCanEverTick = true;
}


void UBaseProfile::StartTickTask()
{
	AT_INFO(TEXT("Read To Start New Task CurrTaskIndex[%d]"), CurrTaskIndex);
	if (!IsComplete())
	{
		UBaseTask* CurrTask = Tasks[CurrTaskIndex];
		if (CurrTask)
		{
			CurrTask->StartTick();
			UGolbalBPFunctionLibrary::StatusMessage(2551,INT_TO_FSTRING(CurrTask->Index));
		}
	}
}

void UBaseProfile::LoadCfg()
{

}

void UBaseProfile::TickObject()
{
	if (IsComplete())
	{
		bCanEverTick = false;
		EndRecord();
	}
	else
	{
		if (Tasks.Num() > 0)
		{
			UBaseTask* CurrTask = Tasks[CurrTaskIndex];
			if (CurrTask->IsComplete)
			{
				CurrTaskIndex += 1;
				StartTickTask();
			}
		}
	}
}

bool UBaseProfile::IsComplete()
{
	if (Tasks.Num() == (CurrTaskIndex + 1) && Tasks[CurrTaskIndex]->IsComplete)
	{
		return true;
	}
	else
	{
		return false;
	}
}

UBaseTask* UBaseProfile::GetCurrTask()
{
	if (Tasks.Num() > 0)
	{
		if (!IsComplete())
		{
			return Tasks[CurrTaskIndex];
		}
	}

	return nullptr;
	
}

CONTROL_COMPILE_OPTIMIZE_END
