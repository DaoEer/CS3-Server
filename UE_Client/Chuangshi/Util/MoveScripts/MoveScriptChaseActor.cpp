// Fill out your copyright notice in the Description page of Project Settings.
#include "MoveScriptChaseActor.h"
#include "Blueprint/AIBlueprintHelperLibrary.h"


MoveScriptChaseActor::MoveScriptChaseActor(APawn* InPawn,  AActor* _GoalActor, float _AcceptanceRadius):MoveScriptBase(InPawn, _AcceptanceRadius) {
	GoalActor = _GoalActor;
}



void MoveScriptChaseActor::DoMove() {
	if (!IsValid(GetOwner()) || !IsValid(GetGoalActor())) {
		return;
	}
	UAIBlueprintHelperLibrary::SimpleMoveToLocation(GetOwner()->GetController(), GetGoalPos());
}

AActor* MoveScriptChaseActor::GetGoalActor() {
	return GoalActor;
}

FVector MoveScriptChaseActor::GetGoalPos() {
	if (IsValid(GetGoalActor())) {
		return GetGoalActor()->GetActorLocation();
	}
	else if(IsValid(GetOwner())){
		return GetOwner()->GetActorLocation();
	}
	else{
		return FVector::ZeroVector;
	}
}
void MoveScriptChaseActor::MoveReachCheck() {

	float distance = FVector::Dist(GetOwner()->GetActorLocation(),GetGoalPos() );
	if (distance <= AcceptanceRadius) {
		OnMoveOver();
	}
	else {
		DoMove();
	}
}

void MoveScriptChaseActor::OnMoveOver() {
	Super::OnMoveOver();
}