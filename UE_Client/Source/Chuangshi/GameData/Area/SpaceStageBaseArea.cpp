// Fill out your copyright notice in the Description page of Project Settings.

#include "SpaceStageBaseArea.h"
#include "Interface/Role/RoleSpaceStageInterface.h"
#include "Actor/ServerCharacter.h"
#include "Util/GolbalBPFunctionLibrary.h"

USpaceStageBaseArea::USpaceStageBaseArea()
{
}

USpaceStageBaseArea::~USpaceStageBaseArea()
{
}

void USpaceStageBaseArea::InitParams(FString _ScriptID, INT32 _StageIndex, INT32 _TaskIndex, float _CeilHeight, float _FloorHeight, FString AreaParam)
{
	StageIndex = _StageIndex;
	TaskIndex = _TaskIndex;
	CeilHeight = _CeilHeight;
	FloorHeight = _FloorHeight;
	ScriptID = _ScriptID;
	MapScriptID = _ScriptID;
}

void USpaceStageBaseArea::OnEnter(const FString SpaceScriptID)
{
	URoleSpaceStageInterface* RoleSpaceStageInterface = Cast<URoleSpaceStageInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleSpaceStageInterface"), 0));
	if (RoleSpaceStageInterface)
	{
		RoleSpaceStageInterface->CELL_OnEnterSpaceStageArea(StageIndex, TaskIndex);
	}
}
