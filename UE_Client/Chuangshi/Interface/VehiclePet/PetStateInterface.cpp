// Fill out your copyright notice in the Description page of Project Settings.


#include "PetStateInterface.h"
#include "BehaviorTree/BlackboardComponent.h"
#include "Blueprint/AIBlueprintHelperLibrary.h"

void UPetStateInterface::OnStateChanged(const int32& NewState, const int32& OldState)
{
	Supper::OnStateChanged(NewState, OldState);

	if (UGolbalBPFunctionLibrary::GetIntPropertyValue(UGolbalBPFunctionLibrary::GetPlayerID(), TEXT("activePetID")) == EntityID)
	{
		UBlackboardComponent* myBlackBoard = UAIBlueprintHelperLibrary::GetBlackboard(GetActor());
		if (IsValid(myBlackBoard))
		{
			myBlackBoard->SetValueAsInt(FName(TEXT("State")), NewState);
		}
	}
}