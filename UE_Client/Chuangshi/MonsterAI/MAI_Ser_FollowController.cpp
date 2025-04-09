// Fill out your copyright notice in the Description page of Project Settings.


#include "MAI_Ser_FollowController.h"
#include "Actor/Monster/MonsterCharacter.h"
#include "MAI_Public_func.h"
#include "MonsterAI/MonsterAIController.h"


void UMAI_Ser_FollowController::TickNode(UBehaviorTreeComponent& OwnerComp, uint8* NodeMemory, float DeltaSeconds)
{
	AMonsterCharacter* mCharacter = Cast<AMonsterCharacter>(OwnerComp.GetAIOwner()->GetPawn());
	if (!IsValid(mCharacter))
	{
		return;
	}
	
	APlayerCharacter* pActor = GetPlayerActor();
	if (IsValid(pActor))
	{
		AMonsterAIController* controller = Cast< AMonsterAIController >(  mCharacter->GetController() );
		controller->MoveToActor(pActor);
	}
}