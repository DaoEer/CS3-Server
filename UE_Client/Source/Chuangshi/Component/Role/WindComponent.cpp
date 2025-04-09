// Fill out your copyright notice in the Description page of Project Settings.


#include "WindComponent.h"
#include "Engine/CollisionProfile.h"
#include "Components/CapsuleComponent.h"
#include "GameFramework/Character.h"

// Sets default values
AWindComponent::AWindComponent()
{
 	// Set this actor to call Tick() every frame.  You can turn this off to improve performance if you don't need it.
	PrimaryActorTick.bCanEverTick = true;
	IsWindCanMove = false;
	WindSpeed = 0.0f;
	WindDirection = FVector::ZeroVector;

	CapsuleComponent = CreateDefaultSubobject<UCapsuleComponent>(ACharacter::CapsuleComponentName);
	CapsuleComponent->InitCapsuleSize(34.0f, 88.0f);
	CapsuleComponent->SetCollisionProfileName(UCollisionProfile::Pawn_ProfileName);

	CapsuleComponent->CanCharacterStepUpOn = ECB_No;
	//CapsuleComponent->bShouldUpdatePhysicsVolume = true;
	CapsuleComponent->SetShouldUpdatePhysicsVolume(true);
	//CapsuleComponent->bCheckAsyncSceneOnMove = false;

	CapsuleComponent->SetCanEverAffectNavigation(false);
	CapsuleComponent->bDynamicObstacle = true;
	RootComponent = CapsuleComponent;

	CapsuleComponent->SetCollisionEnabled(ECollisionEnabled::NoCollision);
}

void AWindComponent::BeginWind(float _WindSpeed,FVector _WindDirection)
{
	if (_WindSpeed > 0)
	{
		WindSpeed = _WindSpeed;
	}
	if (_WindDirection != FVector::ZeroVector)
	{
		WindDirection = _WindDirection;
		WindDirection.Normalize();//方向单位化
	}

	if (WindSpeed <= 0.0f)
	{
		IsWindCanMove = false;
	}
	else
	{
		IsWindCanMove = true;
	}
}

void AWindComponent::StopWind()
{
	IsWindCanMove = false;
}

// Called every frame
void AWindComponent::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);

	if (!IsWindCanMove)
	{
		return;
	}

	FVector AddLocation = WindSpeed * DeltaTime * WindDirection;

	AddActorLocalOffset(AddLocation);
}

