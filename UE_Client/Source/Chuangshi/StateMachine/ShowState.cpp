// Fill out your copyright notice in the Description page of Project Settings.


#include "ShowState.h"
#include "Actor/ServerCharacter.h"

void UShowState::Enter()
{
	AServerCharacter* CurrentActor = Cast<AServerCharacter>(CurrentEntity->Actor());
	if (CurrentActor)
	{
		CurrentActor->OnEnterShowState();
	}
}

void UShowState::Execute()
{

}

void UShowState::Exit()
{
	AServerCharacter* CurrentActor = Cast<AServerCharacter>(CurrentEntity->Actor());
	if (CurrentActor)
	{
		CurrentActor->OnExitShowState();
	}
}