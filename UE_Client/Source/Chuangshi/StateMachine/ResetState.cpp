// Fill out your copyright notice in the Description page of Project Settings.


#include "ResetState.h"
#include "Actor/ServerCharacter.h"

void UResetState::Enter()
{
	AServerCharacter* CurrentActor = Cast<AServerCharacter>(CurrentEntity->Actor());
	if (CurrentActor)
	{
		CurrentActor->OnEnterResetState();
	}
}

void UResetState::Execute()
{

}

void UResetState::Exit()
{
	AServerCharacter* CurrentActor = Cast<AServerCharacter>(CurrentEntity->Actor());
	if (CurrentActor)
	{
		CurrentActor->OnExitResetState();
	}
}


