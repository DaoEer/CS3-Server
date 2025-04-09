// Fill out your copyright notice in the Description page of Project Settings.


#include "CS3CameraComponent.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Actor/ServerCharacter.h"

UCS3CameraComponent::UCS3CameraComponent()
{

}

void UCS3CameraComponent::BeginPlay()
{
	Super::BeginPlay();
}

void UCS3CameraComponent::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
	Super::EndPlay(EndPlayReason);
}

