// Fill out your copyright notice in the Description page of Project Settings.

#include "ClientGameCharacter.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "Component/AppearanceComponent.h"
#include "Util/CS3Debug.h"


CONTROL_COMPILE_OPTIMIZE_START
AClientGameCharacter::AClientGameCharacter()
{
	CharacterClassName = TEXT("ClientGameCharacter");
	PrimaryActorTick.bCanEverTick = true;
	InitBaseComponent();
	SetBaseGravityScale(0.0f);
}

void AClientGameCharacter::BeginPlay()
{
	Super::BeginPlay();
}

void AClientGameCharacter::InitBaseComponent()
{
	AppearanceComponent = CreateDefaultSubobject<UAppearanceComponent>(TEXT("AppearanceComponent"));
}

void AClientGameCharacter::PlayClientAction(FName InActionId)
{
	FActionOverDelegate ActionOverDelegate;

	ActionOverDelegate.AddUObject(this, &AClientGameCharacter::OnPlayClientActionFinished);

	PlayAction(InActionId, 0, ActionOverDelegate);
}

void AClientGameCharacter::OnCreateApperanceOver()
{
	Super::OnCreateApperanceOver();

	OnCreateApperanceOverBP();
}
CONTROL_COMPILE_OPTIMIZE_END
