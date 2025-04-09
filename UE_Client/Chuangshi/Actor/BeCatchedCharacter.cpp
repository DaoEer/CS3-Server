// Fill out your copyright notice in the Description page of Project Settings.

#include "BeCatchedCharacter.h"
#include "Components/CapsuleComponent.h"
#include "Component/AppearanceComponent.h"

ABeCatchedCharacter::ABeCatchedCharacter()
{
	CharacterClassName = TEXT("BeCatchedCharacter");
	m_AnimId = TEXT("");
	CreateRoleMesh();
	AppearanceComponent = CreateDefaultSubobject<UAppearanceComponent>(TEXT("AppearanceComponent"));
	GetCapsuleComponent()->SetCollisionEnabled(ECollisionEnabled::NoCollision);
}

void ABeCatchedCharacter::BeginPlay()
{
	Super::BeginPlay();
}


void ABeCatchedCharacter::SetInitAction()
{
	InitActionId = m_AnimId;
}

void ABeCatchedCharacter::OnCreateApperanceOver()
{
	Super::OnCreateApperanceOver();

	PlayAction(m_AnimId);
}



