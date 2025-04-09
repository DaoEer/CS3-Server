#include "ObjectTask.h"
#include "Util/ConvertUtil.h"

UObjectTask::UObjectTask()
	:Super()
{
	CustomTimeDilation = 1.0f;
}

void UObjectTask::InitParam()
{
	LifeTime = FSTRING_TO_FLOAT(Param1);
	CustomTimeDilation = FSTRING_TO_FLOAT(Param2);
}

void UObjectTask::TickObject()
{
	Super::TickObject();
	FOBJRECORD Item;
	Item.Time = FDateTime::Now();
	Item.ObjCounts = GUObjectArray.GetObjectArrayNum();
	Item.GCObjCounts = GUObjectArray.GetObjectArrayNumMinusPermanent();
	ObjRecords.Add(Item);
}

bool UObjectTask::Condition()
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

int32 UObjectTask::GetAvgObjCount()
{
	int32 Avg = 0;
	if (ObjRecords.Num() > 0)
	{
		int32 SumObjCount = 0;
		for (FOBJRECORD Item : ObjRecords)
		{
			SumObjCount += Item.GCObjCounts;
		}
		Avg = int(SumObjCount / ObjRecords.Num());
	}
	return Avg;
}

int32 UObjectTask::GetMinObjCount()
{
	int32 Min = 0;
	if (ObjRecords.Num() > 0)
	{
		Min = ObjRecords[0].GCObjCounts;
		for (FOBJRECORD Item : ObjRecords)
		{
			if (Item.GCObjCounts < Min)
			{
				Min = Item.GCObjCounts;
			}
		}
	}
	return Min;
}

int32 UObjectTask::GetMaxObjCount()
{
	int32 Max = 0;
	if (ObjRecords.Num() > 0)
	{
		Max = ObjRecords[0].GCObjCounts;
		for (FOBJRECORD Item : ObjRecords)
		{
			if (Item.GCObjCounts > Max)
			{
				Max = Item.GCObjCounts;
			}
		}
	}
	return Max;
}
