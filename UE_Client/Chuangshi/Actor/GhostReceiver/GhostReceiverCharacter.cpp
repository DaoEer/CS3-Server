// Fill out your copyright notice in the Description page of Project Settings.

#include "GhostReceiverCharacter.h"
#include "Component/AppearanceComponent.h"


AGhostReceiverCharacter::AGhostReceiverCharacter()
{
	CharacterClassName = TEXT("GhostReceiverCharacter");
	PrimaryActorTick.bCanEverTick = false;
	InitBaseComponent();
}


void AGhostReceiverCharacter::InitBaseComponent()
{
	AppearanceComponent = CreateDefaultSubobject<UAppearanceComponent>(TEXT("AppearanceComponent"));
}