// Fill out your copyright notice in the Description page of Project Settings.


#include "MonsterCommonController.h"
#include "Actor/Monster/MonsterCharacter.h"
#include "Interface/Monster/BehaviourInterface.h"
#include "GameFramework/Pawn.h"


FPathFollowingRequestResult AMonsterCommonController::MoveTo(const FAIMoveRequest& MoveRequest, FNavPathSharedPtr* OutPath /*= nullptr*/)
{
	FPathFollowingRequestResult ResultData;
	ResultData.Code = EPathFollowingRequestResult::Failed;

	APawn* const MyPawn = GetPawn();
	if (IsValid(MyPawn))
	{
		AMonsterCharacter* MonsterCharacter = Cast<AMonsterCharacter>(MyPawn);
		if (IsValid(MonsterCharacter))
		{
			UBehaviourInterface* BehaviourInterface = Cast<UBehaviourInterface>(MonsterCharacter->GetInterfaceByName(TEXT("BehaviourInterface")));
			if (IsValid(BehaviourInterface) && BehaviourInterface->GetIsUsingSkill())
			{
				return ResultData;
			}
		}
	}
	
	return Super::MoveTo(MoveRequest, OutPath);
}

void AMonsterCommonController::OnMoveCompleted(FAIRequestID RequestID, const FPathFollowingResult& Result)
{
	AAIController::OnMoveCompleted( RequestID, Result );
	AMonsterCharacter* MCharacter = Cast<AMonsterCharacter>(GetPawn());
	if (IsValid(MCharacter))
	{
		MCharacter->OnMoveOver( RequestID.GetID(), Result.IsSuccess() );
	}
}