// Fill out your copyright notice in the Description page of Project Settings.


#include "MovingPlatformCharacter.h"
#include "Component/AvatarFilterActorComponent.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "GameDevelop/CS3PlayerController.h"
#include "Component/AppearanceComponent.h"

void AMovingPlatformCharacter::InitFilterActorComponent()
{
	SetFilterComponent(NewObject<UAvatarFilterActorComponent>(this, "root", RF_NoFlags, nullptr, false, nullptr));

	GetFilterComponent()->RegisterComponent();
	GetFilterComponent()->InitFilter(true);
}

AMovingPlatformCharacter::AMovingPlatformCharacter()
{
	PrimaryActorTick.bCanEverTick = true;
	CharacterClassName = TEXT("MovingPlatformCharacter");
	bActorCanSetpOn = true;
	InitBaseComponent();
}

void AMovingPlatformCharacter::BeginPlay()
{
	Super::BeginPlay();
}


void AMovingPlatformCharacter::InitBaseComponent()
{
	AppearanceComponent = CreateDefaultSubobject<UAppearanceComponent>(TEXT("AppearanceComponent"));
}

void AMovingPlatformCharacter::GossipWith()
{
	
}

void AMovingPlatformCharacter::SetInitAction()
{
	InitActionId = "None";
}

void AMovingPlatformCharacter::PlayDeadEffect()
{

}

FString AMovingPlatformCharacter::GetEntityUName()
{
	return UGolbalBPFunctionLibrary::GetFStringPropertyValue(EntityId, TEXT("uname"));
}

bool AMovingPlatformCharacter::IsEntityBoss()
{
	return false;
}
