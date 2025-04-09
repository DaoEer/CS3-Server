// Fill out your copyright notice in the Description page of Project Settings.


#include "WarnState.h"
#include "Actor/ServerCharacter.h"


void UWarnState::Enter()
{
	AServerCharacter* CurrentActor = Cast<AServerCharacter>(CurrentEntity->Actor());
	if (CurrentActor)
	{
		CurrentActor->OnEnterWarnState();
	}
}

void UWarnState::Execute()
{

}

void UWarnState::Exit()
{
	AServerCharacter* CurrentActor = Cast<AServerCharacter>(CurrentEntity->Actor());
	if (CurrentActor)
	{
		CurrentActor->OnExitWarnState();
	}
}

