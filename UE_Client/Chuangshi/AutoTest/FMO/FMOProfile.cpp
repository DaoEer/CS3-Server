// Fill out your copyright notice in the Description page of Project Settings.


#include "FMOProfile.h"
#include "AutoTest/BaseTest/BaseTask.h"
#include "FMOTask.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"
#include "Util/ConvertUtil.h"

CONTROL_COMPILE_OPTIMIZE_START

UFMOProfile::UFMOProfile()
	: Super()
{
	bCanEverTick = true;
}

void UFMOProfile::LoadCfg()
{
	Tasks.Empty();
	FString GameSaveDir = FPaths::ProjectSavedDir();
	FString FilePath = FPaths::Combine(GameSaveDir, TEXT("FMOCfg.csv"));
	FString Lines;
	FFileHelper::LoadFileToString(Lines, *FilePath);
	AT_INFO(TEXT("FMOCFG Content: %s"), *Lines);
	TArray<FString> AllLines = UGolbalBPFunctionLibrary::SplitString(Lines, false, TEXT("\r\n"));
	for (FString Line : AllLines)
	{
		Line = Line.Replace(TEXT("\t"), TEXT(""));
		TArray<FString> Items = UGolbalBPFunctionLibrary::SplitString(Line, false, TEXT(","));
		UClass* BP_Class = UGolbalBPFunctionLibrary::GetUClassByStr(Items[1]);
		UBaseTask* Task = NewObject<UBaseTask>(this, BP_Class);
		Task->Index = FSTRING_TO_INT(Items[0]);
		if (Items.Num() > 2)
		{
			Task->Param1 = Items[2];
		}
		if (Items.Num() > 3)
		{
			Task->Param2 = Items[3];
		}
		if (Items.Num() > 4)
		{
			Task->Param3 = Items[4];
		}
		if (Items.Num() > 5)
		{
			Task->Param4 = Items[5];
		}
		if (Items.Num() > 6)
		{
			Task->Param5 = Items[6];
		}
		if (Items.Num() > 7)
		{
			Task->Comment = Items[7];
		}
		Tasks.Add(Task);
	}
}

void UFMOProfile::EndRecord()
{
	if (Tasks.Num() > 0)
	{
		//写物理内存报告
		FString FileContent = TEXT("");
		FString Line = UFMOTask::GetTitle();
		Line = UGolbalBPFunctionLibrary::HandleLineFeeds(Line);
		FileContent += Line;
		for (UBaseTask* Item : Tasks)
		{
			UFMOTask* Temp = Cast<UFMOTask>(Item);
			if (IsValid(Temp))
			{
				Line = Temp->GetLine();
				Line = UGolbalBPFunctionLibrary::HandleLineFeeds(Line);
				FileContent += Line;

			}
		}
		FString GameSaveDir = FPaths::ProjectSavedDir();
		FDateTime Time = FDateTime::Now();
		FString TimeStr = Time.ToString(TEXT("%Y%m%d"));
		FString FilePath = FPaths::Combine(GameSaveDir, TimeStr + TEXT("RecordFPSAndPhysicalMem.csv"));
		FFileHelper::SaveStringToFile(FileContent, *FilePath, FFileHelper::EEncodingOptions::ForceUTF8);


		//写虚拟内存报告
		FString VirtualFileContent = TEXT("");
		FString VirtualLine = UFMOTask::GetVirtualTitle();
		VirtualLine = UGolbalBPFunctionLibrary::HandleLineFeeds(VirtualLine);
		VirtualFileContent += VirtualLine;
		for (UBaseTask* Item : Tasks)
		{
			UFMOTask* Temp = Cast<UFMOTask>(Item);
			if (IsValid(Temp))
			{
				VirtualLine = Temp->GetVirtualLine();
				VirtualLine = UGolbalBPFunctionLibrary::HandleLineFeeds(VirtualLine);
				VirtualFileContent += VirtualLine;

			}
		}
		//FString GameSaveDir = FPaths::ProjectSavedDir();
		//FDateTime Time = FDateTime::Now();
		//FString TimeStr = Time.ToString(TEXT("%Y%m%d"));
		FString VirtualFilePath = FPaths::Combine(GameSaveDir, TimeStr + TEXT("RecordFPSAndVirtualMem.csv"));
		FFileHelper::SaveStringToFile(VirtualFileContent, *VirtualFilePath, FFileHelper::EEncodingOptions::ForceUTF8);

		//写详细报告
		FString FileDetailContent = TEXT("");
		FString DetailLine = UFMOTask::GetDetailTitle();
		DetailLine = UGolbalBPFunctionLibrary::HandleLineFeeds(DetailLine);
		FileDetailContent += DetailLine;
		for (UBaseTask* Item : Tasks)
		{
			UFMOTask* Temp = Cast<UFMOTask>(Item);
			if (IsValid(Temp))
			{
				DetailLine = Temp->GetDetailLine();
				DetailLine = UGolbalBPFunctionLibrary::HandleLineFeeds(DetailLine);
				FileDetailContent += DetailLine;

			}
		}
		//FString GameSaveDir = FPaths::ProjectSavedDir();
		//FDateTime Time = FDateTime::Now();
		//FString TimeStr = Time.ToString(TEXT("%Y%m%d"));
		FString DetailFilePath = FPaths::Combine(GameSaveDir, TimeStr + TEXT("DetailRecordFPSAndMem.csv"));
		FFileHelper::SaveStringToFile(FileDetailContent, *DetailFilePath, FFileHelper::EEncodingOptions::ForceUTF8);
	}
	if (IsComplete())
	{
		UGolbalBPFunctionLibrary::StatusMessage(2550, TEXT(""));
	}
}

void UFMOProfile::StartTickTask()
{
	Super::StartTickTask();
	EndRecord();	//每次执行完一个就写入数据，避免客户端崩溃导致执行的任务无数据输出

}

CONTROL_COMPILE_OPTIMIZE_END
