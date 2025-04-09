// Fill out your copyright notice in the Description page of Project Settings.


#include "FMOTask.h"
#include "Util/ConvertUtil.h"


UFMOTask::UFMOTask()
{

}

void UFMOTask::InitParam()
{
	LifeTime = FSTRING_TO_FLOAT(Param1);
	CustomTimeDilation = FSTRING_TO_FLOAT(Param2);
	MapName = Param3;
	AT_INFO(TEXT("UFMOTask InitParam ->Index[%d]"), Index);
}

void UFMOTask::TickObject()
{
	Super::TickObject();
	FFMORECORD Item;
	Item.Time = FDateTime::Now();
	extern ENGINE_API float GAverageFPS;
	Item.FPS = GAverageFPS;
	FPlatformMemoryStats MemoryStats = FPlatformMemory::GetStats();
	Item.UsePhysical = (float)MemoryStats.UsedPhysical / (1024.0f * 1024.0f);	//单位是MB
	Item.UseVirtual = (float)MemoryStats.UsedVirtual / (1024.0f * 1024.0f);	//单位是MB
	float UsedVirtual = (float)MemoryStats.UsedVirtual / (1024.0f * 1024.0f);	//单位是MB
	float UsedPhysical = (float)MemoryStats.UsedPhysical / (1024.0f * 1024.0f);	//单位是MB
	Item.GCObjCount = GUObjectArray.GetObjectArrayNumMinusPermanent();
	AT_INFO(TEXT("UFMOTask Map[%s] Record Current FPS[%f] and Memory, UsedVirtual[%f], UsedPhysical[%f]"), *MapName, Item.FPS, UsedVirtual, UsedPhysical);
	FMORecords.Add(Item);
}

bool UFMOTask::Condition()
{
	//AT_INFO(TEXT("UFMOTask StartCheck Condition ->Index[%d]"), Index);
	if (GetSumTickTime() >= LifeTime)
	{
		AT_INFO(TEXT("UFMOTask Complete Condition ->Index[%d]"), Index);
		return true;
	}
	else
	{
		return false;
	}
}

void UFMOTask::GetAvgData(float& AvgFrame, float& AvgMemUse, int32& AvgObjCount)
{
	AvgFrame = 0.0;
	AvgMemUse = 0.0;
	AvgObjCount = 0;
	int32 Length = FMORecords.Num();
	if (Length > 0)
	{
		double SumFrame = 0.0;
		double SumMemory = 0.0;
		int64 SumObj = 0;
		for (FFMORECORD Item : FMORecords)
		{
			SumFrame += Item.FPS;
			SumMemory += Item.UsePhysical;
			SumObj += Item.GCObjCount;
		}

		AvgFrame = float(SumFrame / Length);
		AvgMemUse = float(SumMemory / Length);
		AvgObjCount = int32(SumObj / Length);
	}
}

void UFMOTask::GetMinData(float& MinFrame, float& MinMemUse, int32& MinObjCount)
{
	MinFrame = 0.0;
	MinMemUse = 0.0;
	MinObjCount = 0;
	int32 Length = FMORecords.Num();
	if (Length > 0)
	{
		MinFrame = FMORecords[0].FPS;
		MinMemUse = FMORecords[0].UsePhysical;
		MinObjCount = FMORecords[0].GCObjCount;
		for (FFMORECORD Item : FMORecords)
		{
			if (Item.FPS < MinFrame)
			{
				MinFrame = Item.FPS;
			}
			if (Item.UsePhysical < MinMemUse)
			{
				MinMemUse = Item.UsePhysical;
			}
			if (Item.GCObjCount < MinObjCount)
			{
				MinObjCount = Item.GCObjCount;
			}
		}
	}
}

void UFMOTask::GetMaxData(float& MaxFrame, float& MaxMemUse, int32& MaxObjCount)
{
	MaxFrame = 0.0;
	MaxMemUse = 0.0;
	MaxObjCount = 0;
	int32 Length = FMORecords.Num();
	if (Length > 0)
	{
		MaxFrame = FMORecords[0].FPS;
		MaxMemUse = FMORecords[0].UsePhysical;
		MaxObjCount = FMORecords[0].GCObjCount;
		for (FFMORECORD Item : FMORecords)
		{
			if (Item.FPS > MaxFrame)
			{
				MaxFrame = Item.FPS;
			}
			if (Item.UsePhysical > MaxMemUse)
			{
				MaxMemUse = Item.UsePhysical;
			}
			if (Item.GCObjCount > MaxObjCount)
			{
				MaxObjCount = Item.GCObjCount;
			}
		}
	}
}

FString UFMOTask::GetLine()
{
	FString Line = TEXT("");
	Line += (MapName + TEXT(", "));
	float AvgFrame;
	float AvgMemUse;
	int32 AvgObjCount;
	GetAvgData(AvgFrame, AvgMemUse, AvgObjCount);
	float MinFrame;
	float MinMemUse;
	int32 MinObjCount;
	GetMinData(MinFrame, MinMemUse, MinObjCount);
	float MaxFrame;
	float MaxMemUse;
	int32 MaxObjCount;
	GetMaxData(MaxFrame, MaxMemUse, MaxObjCount);
	//Line += (FLOAT_TO_FSTRING(AvgFrame) + TEXT(", ") + FLOAT_TO_FSTRING(MinFrame) + TEXT(", ") + FLOAT_TO_FSTRING(MaxFrame) + TEXT(", "));
	//Line += (FLOAT_TO_FSTRING(AvgMemUse) + TEXT(", ") + FLOAT_TO_FSTRING(MinMemUse) + TEXT(", ") + FLOAT_TO_FSTRING(MaxMemUse) + TEXT(", "));
	//Line += (FLOAT_TO_FSTRING(AvgObjCount) + TEXT(", ") + FLOAT_TO_FSTRING(MinObjCount) + TEXT(", ") + FLOAT_TO_FSTRING(MaxObjCount) + TEXT(", "));
	Line += (FLOAT_TO_FSTRING(AvgFrame) + TEXT(", ") + FLOAT_TO_FSTRING(MinMemUse));
	return Line;
}

FString UFMOTask::GetTitle()
{
	//return TEXT("地图名, 平均帧率, 最低帧率, 最高帧率, 平均内存(MB), 最低内存(MB), 最高内存(MB), 平均Obj数量, 最低Obj数量, 最高Obj数量\n");
	return TEXT("地图名, 平均帧率, 最低物理内存(MB)\n");

}

FString UFMOTask::GetVirtualLine()
{
	FString Line = TEXT("");
	Line += (MapName + TEXT(", "));
	float AvgFrame;
	float AvgMemUse;
	int32 AvgObjCount;
	GetAvgData(AvgFrame, AvgMemUse, AvgObjCount);
	float MinFrame;
	float MinMemUse;
	int32 MinObjCount;
	GetMinData(MinFrame, MinMemUse, MinObjCount);
	float MaxFrame;
	float MaxMemUse;
	int32 MaxObjCount;
	GetMaxData(MaxFrame, MaxMemUse, MaxObjCount);
	float MaxVirtualMemUse = 0.0;
	float MinVirtualMemUse = 0.0;
	float AvgVirtualMemUse = 0.0;
	if (FMORecords.Num() > 0)
	{
		MaxVirtualMemUse = FMORecords[0].UseVirtual;
		MinVirtualMemUse = FMORecords[0].UseVirtual;
	}
	TArray<float> VirtualMemList;
	double SumVirtualMemUse = 0.0;
	for (FFMORECORD Item : FMORecords)
	{
		VirtualMemList.Add(Item.UseVirtual);
		if (MaxVirtualMemUse < Item.UseVirtual)
		{
			MaxVirtualMemUse = Item.UseVirtual;
		}
		if (MinVirtualMemUse > Item.UseVirtual)
		{
			MinVirtualMemUse = Item.UseVirtual;
		}
		SumVirtualMemUse += Item.UseVirtual;
	}
	if (FMORecords.Num() > 0)
	{
		AvgVirtualMemUse = float(SumVirtualMemUse / FMORecords.Num());
	}
	
	//Line += (FLOAT_TO_FSTRING(AvgFrame) + TEXT(", ") + FLOAT_TO_FSTRING(MinFrame) + TEXT(", ") + FLOAT_TO_FSTRING(MaxFrame) + TEXT(", "));
	//Line += (FLOAT_TO_FSTRING(AvgMemUse) + TEXT(", ") + FLOAT_TO_FSTRING(MinMemUse) + TEXT(", ") + FLOAT_TO_FSTRING(MaxMemUse) + TEXT(", "));
	//Line += (FLOAT_TO_FSTRING(AvgObjCount) + TEXT(", ") + FLOAT_TO_FSTRING(MinObjCount) + TEXT(", ") + FLOAT_TO_FSTRING(MaxObjCount) + TEXT(", "));
	Line += (FLOAT_TO_FSTRING(AvgFrame) + TEXT(", ") + FLOAT_TO_FSTRING(MinVirtualMemUse));
	return Line;
}

FString UFMOTask::GetVirtualTitle()
{
	return TEXT("地图名, 平均帧率, 最低虚拟内存(MB)\n");
}

FString UFMOTask::GetDetailLine()
{
	FString Line = TEXT("");
	Line += (MapName + TEXT(", "));
	float AvgFrame;
	float AvgMemUse;
	int32 AvgObjCount;
	GetAvgData(AvgFrame, AvgMemUse, AvgObjCount);
	float MinFrame;
	float MinMemUse;
	int32 MinObjCount;
	GetMinData(MinFrame, MinMemUse, MinObjCount);
	float MaxFrame;
	float MaxMemUse;
	int32 MaxObjCount;
	GetMaxData(MaxFrame, MaxMemUse, MaxObjCount);
	Line += (FLOAT_TO_FSTRING(AvgFrame) + TEXT(", ") + FLOAT_TO_FSTRING(MinFrame) + TEXT(", ") + FLOAT_TO_FSTRING(MaxFrame) + TEXT(", "));
	Line += (FLOAT_TO_FSTRING(AvgMemUse) + TEXT(", ") + FLOAT_TO_FSTRING(MinMemUse) + TEXT(", ") + FLOAT_TO_FSTRING(MaxMemUse) + TEXT(", "));
	Line += (FLOAT_TO_FSTRING(AvgObjCount) + TEXT(", ") + FLOAT_TO_FSTRING(MinObjCount) + TEXT(", ") + FLOAT_TO_FSTRING(MaxObjCount) + TEXT(", "));
	return Line;
}

FString UFMOTask::GetDetailTitle()
{
	return TEXT("地图名, 平均帧率, 最低帧率, 最高帧率, 平均内存(MB), 最低内存(MB), 最高内存(MB), 平均Obj数量, 最低Obj数量, 最高Obj数量\n");
}

