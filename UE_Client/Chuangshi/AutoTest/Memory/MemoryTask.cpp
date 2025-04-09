#include "MemoryTask.h"
#include "Util/ConvertUtil.h"

UMemoryTask::UMemoryTask()
	:Super()
{
	CustomTimeDilation = 1.0f;
}

void UMemoryTask::InitParam()
{
	LifeTime = FSTRING_TO_FLOAT(Param1);
	CustomTimeDilation = FSTRING_TO_FLOAT(Param2);
}

void UMemoryTask::TickObject()
{
	Super::TickObject();
	FMEMRECORD Item;
	Item.Time = FDateTime::Now();
	FPlatformMemoryStats MemoryStats = FPlatformMemory::GetStats();
	Item.UsePhysical = (float)MemoryStats.UsedPhysical / (1024.0f * 1024.0f);	//µ¥Î»ÊÇMB
	MemRecords.Add(Item);
}

bool UMemoryTask::Condition()
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

int32 UMemoryTask::GetAvgUseMemory()
{
	int32 Avg = 0;
	if (MemRecords.Num() > 0)
	{
		int32 Sum = 0;
		for (FMEMRECORD Item : MemRecords)
		{
			Sum += Item.UsePhysical;
		}
		Avg = int(Sum / MemRecords.Num());
	}
	return Avg;
}

int32 UMemoryTask::GetMinUseMemory()
{
	int32 Min = 0;
	if (MemRecords.Num() > 0)
	{
		Min = MemRecords[0].UsePhysical;
		for (FMEMRECORD Item : MemRecords)
		{
			if (Item.UsePhysical < Min)
			{
				Min = Item.UsePhysical;
			}
		}
	}
	return Min;
}

int32 UMemoryTask::GetMaxUseMemory()
{
	int32 Max = 0;
	if (MemRecords.Num() > 0)
	{
		Max = MemRecords[0].UsePhysical;
		for (FMEMRECORD Item : MemRecords)
		{
			if (Item.UsePhysical > Max)
			{
				Max = Item.UsePhysical;
			}
		}
	}
	return Max;
}
