// Fill out your copyright notice in the Description page of Project Settings.
#include "MoveScriptRandomWalk.h"
#include "AIController.h"
#include "Blueprint/AIBlueprintHelperLibrary.h"


MoveScriptRandomWalk::MoveScriptRandomWalk(APawn* InPawn, FVector _OriginalPos, float _RandomRange, float _AcceptianRadius):MoveScriptBase(InPawn, _AcceptianRadius) {
	OriginalPos = _OriginalPos;
	RandomRange = _RandomRange;
}


void MoveScriptRandomWalk::DoMove() {
	GoalPos = GetGoalPos();
	UAIBlueprintHelperLibrary::SimpleMoveToLocation(GetOwner()->GetController(), GoalPos);

	//AAIController* AIController = Cast<AAIController>(GetOwner()->GetController());
	//AIController->MoveToLocation(GoalPos);
}


FVector MoveScriptRandomWalk::GetGoalPos() {
	float Raius = FMath::FRandRange(0.0, RandomRange);
	float Theta = FMath::FRandRange(0.0, 360.0);
	FVector _GoalPos = OriginalPos + FVector(FMath::Sin(PI / 180.0 * Theta)*Raius, FMath::Cos(PI / 180.0*Theta)*Raius, 0);
	return _GoalPos;
}

void MoveScriptRandomWalk::MoveReachCheck() {
	float distance = FVector::Dist(GetOwner()->GetActorLocation(), GoalPos);
	if (distance <= AcceptanceRadius) {
		OnMoveOver();
	}
}

void MoveScriptRandomWalk::OnMoveOver() {
	Super::OnMoveOver();
}