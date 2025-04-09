// Fill out your copyright notice in the Description page of Project Settings.

#include "TipsCharacter.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Component/AppearanceComponent.h"

void ATipsCharacter::BeginPlay()
{
	Super::BeginPlay();
}

void ATipsCharacter::OnCreateModelOver()
{
	Super::OnCreateModelOver();
}

void ATipsCharacter::CreateModel(FString ModelID)
{
	if (IsValid(this))
	{
		UGolbalBPFunctionLibrary::CS3SetModelPart(this, ModelID);
	}
}

void ATipsCharacter::InitBaseComponent()
{
		AppearanceComponent = CreateDefaultSubobject<UAppearanceComponent>(TEXT("AppearanceComponent"));
}
