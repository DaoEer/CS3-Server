// Fill out your copyright notice in the Description page of Project Settings.


#include "MagicCharacter.h"
#include "Component/AppearanceComponent.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "GameFramework/Actor.h"
#include "PlayerCharacter.h"
#include "Util/CS3Debug.h"
#include "Stats.h"
#include "Manager/CfgManager.h"

DECLARE_CYCLE_STAT(TEXT("Init"), STAT_Init, STATGROUP_AMagicCharacter);
DECLARE_CYCLE_STAT(TEXT("PlayActionAim"), STAT_PlayActionAim, STATGROUP_AMagicCharacter);
DECLARE_CYCLE_STAT(TEXT("SetFaBaoData"), STAT_SetFaBaoData, STATGROUP_AMagicCharacter);
DECLARE_CYCLE_STAT(TEXT("GetFaBaoData"), STAT_GetFaBaoData, STATGROUP_AMagicCharacter);

CONTROL_COMPILE_OPTIMIZE_START

AMagicCharacter::AMagicCharacter()
{
	CharacterClassName = TEXT("MagicCharacter");
	PrimaryActorTick.bCanEverTick = true;
	InitBaseComponent();
}

void AMagicCharacter::OnCreateApperanceOver()
{
	Super::OnCreateApperanceOver();
}

void AMagicCharacter::PlayActionAim(FName AimName)
{
	SCOPE_CYCLE_COUNTER(STAT_PlayActionAim);
	PlayAction(AimName);
}

void AMagicCharacter::Init(AServerCharacter* TargetActor, FString FaBaoRowName)
{
	SCOPE_CYCLE_COUNTER(STAT_Init);
	auto FaBaoTable = UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_FABAO_DATA);
	const FFABAO_DATA* fabaoData = FaBaoTable->GetRow<FFABAO_DATA>(FaBaoRowName);
	if (fabaoData != nullptr)
	{
		this->GetAppearanceComponent()->CreateAppearance(fabaoData->FabaoMeshData.FaBaoModelID);
		this->SetActorLocation(FVector::ZeroVector);
		this->AttachToComponent(TargetActor->GetMesh(), FAttachmentTransformRules::KeepRelativeTransform, fabaoData->SockeName);
		SetFaBaoData(fabaoData);
		InitOver();
	}
}

void AMagicCharacter::SetFaBaoData(const FFABAO_DATA* fabaodata)
{
	SCOPE_CYCLE_COUNTER(STAT_SetFaBaoData);
	FaBaoData = fabaodata;
}

void AMagicCharacter::GetFaBaoData(FFABAO_DATA& fabao)
{
	SCOPE_CYCLE_COUNTER(STAT_GetFaBaoData);
	if (FaBaoData!=nullptr)
	{
		fabao = *FaBaoData;
	}
}

void AMagicCharacter::InitBaseComponent()
{
	AppearanceComponent = CreateDefaultSubobject<UAppearanceComponent>(TEXT("AppearanceComponent"));
}

CONTROL_COMPILE_OPTIMIZE_END