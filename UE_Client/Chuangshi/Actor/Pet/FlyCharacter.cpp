// Fill out your copyright notice in the Description page of Project Settings.

#include "FlyCharacter.h"
#include "../Player/PlayerCharacter.h"
#include "Component/AppearanceComponent.h"

AFlyCharacter::AFlyCharacter()
{
	CharacterClassName = TEXT("FlyCharacter");
	PrimaryActorTick.bCanEverTick = true;
	CreateRoleMesh();
	InitBaseComponent();
}

void AFlyCharacter::BeginPlay()
{
	Super::BeginPlay();

}


void AFlyCharacter::InitBaseComponent()
{
	AppearanceComponent = CreateDefaultSubobject<URoleAppearanceComponent>(TEXT("RoleAppearanceComponent"));
}

void AFlyCharacter::SetInitAction()
{
	InitActionId = "Idle_Free";
}

void AFlyCharacter::OnCreateModelOver()
{
	Super::OnCreateModelOver();
	if (FlyCharacterOnCreateModelOver.IsBound())
	{
		FlyCharacterOnCreateModelOver.Execute();
	}	
}
