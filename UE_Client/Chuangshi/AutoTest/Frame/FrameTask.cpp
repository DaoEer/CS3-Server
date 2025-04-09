// Fill out your copyright notice in the Description page of Project Settings.


#include "FrameTask.h"
#include"Chuangshi.h"




UFrameTask::UFrameTask()
	:Super()
{
	CustomTimeDilation = 1.0;
}

void UFrameTask::InitParam()
{
	LifeTime = FSTRING_TO_FLOAT(Param1);
	CustomTimeDilation = FSTRING_TO_FLOAT(Param2);
}

void UFrameTask::TickObject()
{
	Super::TickObject();
	FFRAMERECORD Item;
	Item.Time = FDateTime::Now();
	extern ENGINE_API float GAverageFPS;
	Item.FPS = GAverageFPS;
	FrameRecords.Add(Item);
}

bool UFrameTask::Condition()
{
	if (GetSumTickTime() >= LifeTime)
	{
		return true;
	}
	else
	{
		return false;
	}
}

int32 UFrameTask::GetAvgFrame()
{
	int32 Avg = 0;
	if (FrameRecords.Num() > 0)
	{
		int32 Sum = 0;
		for (FFRAMERECORD Item : FrameRecords)
		{
			Sum += Item.FPS;
		}
		Avg = int(Sum / FrameRecords.Num());
	}
	return Avg;
}

int32 UFrameTask::GetMinFrame()
{
	int32 Min = 0;
	if (FrameRecords.Num() > 0)
	{
		Min = FrameRecords[0].FPS;
		for (FFRAMERECORD Item : FrameRecords)
		{
			if (Item.FPS < Min)
			{
				Min = Item.FPS;
			}
		}
	}
	return Min;
}

int32 UFrameTask::GetMaxFrame()
{
	int32 Max = 0;
	if (FrameRecords.Num() > 0)
	{
		Max = FrameRecords[0].FPS;
		for (FFRAMERECORD Item : FrameRecords)
		{
			if (Item.FPS > Max)
			{
				Max = Item.FPS;
			}
		}
	}
	return Max;
}
